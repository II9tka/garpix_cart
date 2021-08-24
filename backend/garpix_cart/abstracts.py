from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List


class AbstractCartSession(ABC):
    @abstractmethod
    def get(self) -> Optional[Dict[str, Any]]:
        ...

    @abstractmethod
    def modify_session(self, values) -> bool:
        ...


class AbstractCartHandler(ABC):
    @abstractmethod
    def validate(self, products) -> List[Dict[str, Any]]:
        ...

    @abstractmethod
    def is_valid(self, products) -> bool:
        ...

    @abstractmethod
    def make(self, products) -> bool:
        ...

    @abstractmethod
    def error_log(self, products) -> Optional[str]:
        ...
