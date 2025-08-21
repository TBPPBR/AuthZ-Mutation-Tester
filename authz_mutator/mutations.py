from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict

from .types import RequestSpec


class Mutation(ABC):
    @abstractmethod
    def apply(self, request: RequestSpec) -> None:
        ...

    @abstractmethod
    def describe(self) -> str:
        ...


class RemoveHeaderMutation(Mutation):
    def __init__(self, name: str) -> None:
        self.name = name

    def apply(self, request: RequestSpec) -> None:
        request.headers.pop(self.name, None)

    def describe(self) -> str:
        return f"remove_header name={self.name}"


class ReplaceHeaderMutation(Mutation):
    def __init__(self, name: str, value: str) -> None:
        self.name = name
        self.value = value

    def apply(self, request: RequestSpec) -> None:
        request.headers[self.name] = self.value

    def describe(self) -> str:
        return f"replace_header name={self.name}"


class MethodMutation(Mutation):
    def __init__(self, method: str) -> None:
        self.method = method.upper()

    def apply(self, request: RequestSpec) -> None:
        request.method = self.method

    def describe(self) -> str:
        return f"method {self.method}"


class BodyReplaceMutation(Mutation):
    def __init__(self, path: str, value: Any) -> None:
        self.path = path
        self.value = value

    def apply(self, request: RequestSpec) -> None:
        if request.json is None or not isinstance(request.json, dict):
            return
        _set_nested(request.json, self.path, self.value)

    def describe(self) -> str:
        return f"body_replace {self.path}"


def _set_nested(obj: Dict[str, Any], path: str, value: Any) -> None:
    """Set a nested field by dot-separated path, creating dicts as needed."""
    parts = path.split(".")
    cursor: Dict[str, Any] = obj
    for key in parts[:-1]:
        if key not in cursor or not isinstance(cursor[key], dict):
            cursor[key] = {}
        cursor = cursor[key]
    cursor[parts[-1]] = value


def parse_mutation(spec: Dict[str, Any]) -> Mutation:
    type_ = str(spec.get("type", "")).lower()
    if type_ == "remove_header":
        return RemoveHeaderMutation(name=str(spec["name"]))
    elif type_ == "replace_header":
        return ReplaceHeaderMutation(name=str(spec["name"]), value=str(spec["value"]))
    elif type_ == "method":
        return MethodMutation(method=str(spec["method"]))
    elif type_ == "body_replace":
        return BodyReplaceMutation(path=str(spec["path"]), value=spec.get("value"))
    else:
        raise ValueError(f"Unknown mutation type: {type_}")
