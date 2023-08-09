from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import asdict
from typing import Any


class BaseConfiguration(ABC):
    @abstractmethod
    def to_json(self) -> dict[str, Any]:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def from_json(cls, data: dict[str, Any]) -> BaseConfiguration:
        raise NotImplementedError()


class DictConfig(BaseConfiguration, dict):
    def to_json(self) -> dict[str, Any]:
        return self

    @classmethod
    @abstractmethod
    def from_json(cls, data: dict[str, Any]) -> BaseConfiguration:
        return cls(data)


class DataclassConfiguration(BaseConfiguration):
    """
    Configuration based on a dataclass

    .. warning :: Current limitation of this functionality is that the dataclass must not have nested dataclasses.
    """
    def to_json(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> BaseConfiguration:
        return cls(**data)
