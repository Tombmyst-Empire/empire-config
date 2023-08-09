from typing import Type, TypeVar

from ecfg.library.configuration import BaseConfiguration, DataclassConfiguration, DictConfig
from ecfg.library.config_manager import ConfigManager


T = TypeVar('T')


__all__ = [
    'get_config',
    'BaseConfiguration',
    'DictConfig',
    'DataclassConfiguration',
    'ConfigManager'
]


def get_config(
        config_name: str,
        *,
        config_type: Type[T] = DictConfig,
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
    return ConfigManager.get_config(config_name, config_type, config_path, is_encoded, serializable)
