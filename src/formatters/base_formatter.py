from abc import ABC, abstractmethod

class BaseFormatter(ABC):
    """出力形式の抽象（O, L, D: 依存性逆転のための境界）"""
    @abstractmethod
    def export(self, questions, filename: str, **kwargs):
        raise NotImplementedError
