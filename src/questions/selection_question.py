from .base_question import BaseQuestion

class SelectionQuestion(BaseQuestion):
    """
    4択選択問題クラス
    """
    def __init__(
        self,
        question_text: str,
        japanese_text: str,
        options: list[str],
        correct_idx: int
    ):
        """
        Args:
            question_text (str): 穴埋めを含む英文
            japanese_text (str): 日本語訳
            options (list[str]): 選択肢リスト（長さ4）
            correct_idx (int): 正解のインデックス (0~3)
        """
        self._text = question_text
        self._ja = japanese_text
        self._options = options
        self._correct_idx = correct_idx

    def text(self) -> str:
        # 問題文そのもの
        return self._text

    def answer(self) -> str:
        # 解答ページ用: "(1) answer_word" の形式
        if 0 <= self._correct_idx < len(self._options):
            ans_num = self._correct_idx + 1
            ans_word = self._options[self._correct_idx]
            return f"({ans_num}) {ans_word}"
        return ""

    def ja(self) -> str:
        return self._ja

    def get_options(self) -> list[str]:
        return self._options

