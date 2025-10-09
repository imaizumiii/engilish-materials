import csv
from .rearrange_question import RearrangeQuestion
from .. import config

def _parse_meta_header(line: str) -> dict:
    """
    '# key=value; key2=value2' 形式のメタ行を辞書化。
    値の前後空白はトリムする。
    """
    meta = {}
    raw = line.lstrip("#").strip()
    if not raw:
        return meta
    parts = [p for p in raw.split(";") if p.strip()]
    for part in parts:
        if "=" in part:
            k, v = part.split("=", 1)
            meta[k.strip().lower()] = v.strip()
    return meta

class QuestionBank:
    """CSVを読み込み，問題の生成のみ担当（単一責任）"""
    def __init__(self, unit_name: str):
        self.unit_name = unit_name
        self._questions = []
        self._meta = {}

    def load_from_csv(self, path: str):
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            first_row = True
            for row in reader:
                if not row:
                    continue
                # 先頭行メタ（'# ...' のみ1回）
                if first_row and len(row) == 1 and row[0].strip().startswith("#"):
                    self._meta.update(_parse_meta_header(row[0]))
                    first_row = False
                    continue
                first_row = False

                en = row[0].strip() if len(row) >= 1 else ""
                if not en or en.startswith("#"):
                    continue
                ja = row[1].strip() if len(row) >= 2 else ""

                q = RearrangeQuestion(
                    en,
                    ja=ja if config.SHOW_JA else "",
                    bracket_left=config.BRACKET_LEFT,
                    bracket_right=config.BRACKET_RIGHT,
                    auto_punct=True,                     # ← 自動で ? などを外に出す
                    default_punct=config.DEFAULT_TRAILING_PUNCT,
                    space_before_punct=config.SPACE_BEFORE_TRAILING_PUNCT,
                )
                self._questions.append(q)

    def all(self):
        return list(self._questions)

    def meta(self) -> dict:
        return dict(self._meta)
