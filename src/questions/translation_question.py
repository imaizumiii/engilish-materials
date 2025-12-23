from .base_question import BaseQuestion

class TranslationQuestion(BaseQuestion):
    """
    英文和訳問題クラス
    """
    def __init__(
        self,
        english_text: str,
        japanese_text: str
    ):
        """
        Args:
            english_text (str): 英文
            japanese_text (str): 和訳
        """
        self._en = english_text.strip()
        self._ja = japanese_text.strip()

    def text(self) -> str:
        # 問題文として英文を返す
        # ユーザー要望: スペースを広げる（半角スペース1つ -> 2つ）
        return self._en.replace(" ", "  ")

    def answer(self) -> str:
        # 解答として和訳を返す
        return self._ja

    def ja(self) -> str:
        # 和訳データ
        return self._ja

