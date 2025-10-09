from .base_question import BaseQuestion
from ..utils.text_utils import tokenize_for_shuffle, extract_trailing_punct, strip_trailing_punct
import random
import hashlib

class RearrangeQuestion(BaseQuestion):
    """
    並べ替え問題。シャッフルは文ハッシュで安定化。
    text(): "( token / token / ... ) ?" のように全体を括り、句読点は外側。
    """
    def __init__(
        self,
        correct_sentence: str,
        ja: str | None = None,
        bracket_left: str = "(",
        bracket_right: str = ")",
        auto_punct: bool = True,
        default_punct: str = ".",
        space_before_punct: bool = True,
    ):
        self._answer = correct_sentence.strip()
        self._ja = (ja or "").strip()
        self._brl = bracket_left
        self._brr = bracket_right
        self._space_before_punct = space_before_punct

        # 句読点を自動検出 or 既定にフォールバック
        detected = extract_trailing_punct(self._answer) if auto_punct else ""
        self._trail = detected if detected else (default_punct or "")

        # トークン化（末尾句読点は外す）
        core = strip_trailing_punct(self._answer)
        tokens = core.split()

        # 再現性のあるシャッフル
        seed = int(hashlib.md5(self._answer.encode("utf-8")).hexdigest(), 16) % (10**8)
        rnd = random.Random(seed)
        self._shuffled = tokens[:]
        rnd.shuffle(self._shuffled)

    def text(self) -> str:
        # "( a / b / c )" の形で全体を括る
        inner = " / ".join(self._shuffled)
        s = f"{self._brl} {inner} {self._brr}"
        if self._trail:
            s += (" " if self._space_before_punct else "") + self._trail
        return s

    def answer(self) -> str:
        return self._answer

    def ja(self) -> str:
        return self._ja
