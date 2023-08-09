from __future__ import annotations
import atexit
from dataclasses import dataclass
from os import path
from typing import Type, TypeVar, Generic
from base64 import b85decode, b85encode
from orjson import loads, dumps

from empire_commons.exceptions import ProgrammingException
from ecfg.library.configuration import BaseConfiguration, DictConfig


T = TypeVar('T')


@dataclass(frozen=True, slots=True)
class _Configuration(Generic[T]):
    config: T
    is_encoded: bool
    type_: Type[BaseConfiguration]
    path: str
    serializable: bool


class ConfigManager:
    """
    This class contains all loaded Configurations.
    """
    _instances: dict[str, _Configuration] = {}

    @staticmethod
    def save():
        for config in ConfigManager._instances.values():
            ConfigManager._save_config(config)

    @staticmethod
    def get_config(
            config_name: str,
            config_type: Type[BaseConfiguration] = DictConfig,
            config_path: str | None = None,
            is_encoded: bool = False,
            serializable: bool = True
    ) -> T:
        """
        Returns an instantiated and loaded *config_type* configuration instance.

        If the configuration *config_name* was already loaded, it returns the instance stored in memory, otherwise,
        it loads it from file ``{config_path|USER/.empire}/config_name.ecfg``.

        .. note :: The standard for *config_name* is to use the same as project name in-code (example: for this one, it would be ``ecfg``)

        :param config_name: The name of the config.
        :param config_type: The type in which the loaded configuration will be instantiated.
        :param config_path: When provided, enforces a path where to find the configuration file. Default is using ``USER/.empire/``
        :param is_encoded: When true, encodes the config to base85, otherwise, writes as plain JSON.
        :param serializable: When false, the config will stay in memory, and won't be persisted
        :return: The configuration instance
        """
        config_name = ConfigManager.get_effective_config_name(config_name)

        if config_name in ConfigManager._instances:
            return ConfigManager._instances[config_name].config

        return ConfigManager._load_config(config_name, config_type, config_path, is_encoded, serializable)

    @staticmethod
    def reload_config(config_name: str) -> T:
        """
        Reloads **the already loaded configuration *config_name*** from file.
        :param config_name: The config name
        :return: The reloaded configuration instance
        """
        config_name = ConfigManager.get_effective_config_name(config_name)

        if config_name not in ConfigManager._instances:
            raise ProgrammingException(f'Configuration {config_name} is not loaded, cannot reload it. Use "get_config()" instead.')

        current: _Configuration = ConfigManager._instances[config_name]
        return ConfigManager._load_config(config_name, current.type_, current.path, current.is_encoded, current.serializable)

    @staticmethod
    def close_config_without_save(config_name: str):
        """
        Frees from memory the loaded *config_name*, without saving it before.
        :param config_name: The config name
        """
        config_name = ConfigManager.get_effective_config_name(config_name)
        if config_name in ConfigManager._instances:
            del ConfigManager._instances[config_name]

    @staticmethod
    def _load_config(
            config_name: str,
            config_type: Type[BaseConfiguration],
            config_path: str,
            is_encoded: bool,
            serializable: bool
    ) -> BaseConfiguration:
        if not serializable:
            ConfigManager._instances[config_name] = _Configuration(
                config_type(),
                is_encoded=True,
                type_=config_type,
                path=config_path,
                serializable=False
            )
        else:
            config_path = ConfigManager.get_full_config_path(config_name, config_path)

            if path.isfile(config_path):
                if is_encoded:
                    with open(config_path, 'rb') as f:
                        ConfigManager._instances[config_name] = _Configuration(
                            config_type().from_json(loads(b85decode(f.read()).decode())),
                            is_encoded=True,
                            type_=config_type,
                            path=config_path,
                            serializable=True
                        )
                else:
                    with open(config_path, 'r', encoding='utf8') as f:
                        ConfigManager._instances[config_name] = _Configuration(
                            config_type().from_json(loads(f.read())),
                            is_encoded=False,
                            type_=config_type,
                            path=config_path,
                            serializable=True
                        )
            else:
                ConfigManager._instances[config_name] = _Configuration(
                    config_type(),
                    is_encoded=is_encoded,
                    type_=config_type,
                    path=config_path,
                    serializable=True
                )

        return ConfigManager._instances[config_name].config

    @staticmethod
    def _save_config(config: _Configuration):
        if not config.serializable:
            return

        if config.is_encoded:
            with open(config.path, 'wb') as f:
                f.write(b85encode(dumps(config.config.to_json())))
        else:
            with open(config.path, 'w') as f:
                f.write(dumps(config.config.to_json()).decode())

    @staticmethod
    def get_effective_config_name(config_name: str) -> str:
        return config_name.lower().strip()

    @staticmethod
    def get_full_config_path(config_name: str, config_path: str) -> str:
        if not config_path:
            return path.join(path.expanduser('~'), '.empire', f'{config_name}.ecfg')
        else:
            return path.join(config_path, f'{config_name}.ecfg')


atexit.register(ConfigManager.save)
