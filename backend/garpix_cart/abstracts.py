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
    def validate(self, products) -> List[Dict[str, Any]]:
        ...

    def is_valid(self, products) -> bool:
        ...

    def make(self, products) -> bool:
        ...

    def error_log(self, products) -> Optional[str]:
        ...
