from abc import ABC, abstractmethod

class BaseQuestion(ABC):
    """問題オブジェクトの最小インターフェース（S, L を満たす抽象）"""
    @abstractmethod
    def text(self) -> str:
        """学習者に提示する問題文（シャッフル済み語列など）"""
        raise NotImplementedError

    @abstractmethod
    def answer(self) -> str:
        """正答（完全英文）"""
        raise NotImplementedError
