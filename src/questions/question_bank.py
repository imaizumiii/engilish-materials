import csv
from .rearrange_question import RearrangeQuestion
from .selection_question import SelectionQuestion
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
            current_type = "rearrange"

            for row in reader:
                if not row:
                    continue
                # 先頭行メタ（'# ...' のみ1回）
                if first_row and len(row) == 1 and row[0].strip().startswith("#"):
                    self._meta.update(_parse_meta_header(row[0]))
                    current_type = self._meta.get("type", "rearrange")
                    first_row = False
                    continue
                first_row = False

                en = row[0].strip() if len(row) >= 1 else ""
                if not en or en.startswith("#"):
                    continue
                ja = row[1].strip() if len(row) >= 2 else ""

                if current_type == "selection":
                    # 4択問題: [問題文, 和訳, 選択1, 選択2, 選択3, 選択4, 正解番号(1-4)]
                    if len(row) >= 7:
                        options = [
                            row[2].strip(),
                            row[3].strip(),
                            row[4].strip(),
                            row[5].strip()
                        ]
                        try:
                            # 正解番号 (1~4) を 0-index (0~3) に変換
                            correct_no = int(row[6].strip())
                            correct_idx = correct_no - 1
                        except ValueError:
                            correct_idx = 0 # エラー時はとりあえず0
                        
                        q = SelectionQuestion(en, ja, options, correct_idx)
                        self._questions.append(q)
                else:
                    # 既存の並べ替え問題 (rearrange)
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
