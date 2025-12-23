from pathlib import Path

# ルート
ROOT = Path(__file__).resolve().parents[1]

# 既定メタ（CSV先頭行で上書き可）
TITLE = "Rearrangement Exercises (Grade 9)"
INSTRUCTION_JA = "次の語を正しい順に並べ替え，文を完成させなさい。"
INSTRUCTION_SELECTION = "次の英文の（　）に入れるのに最も適切なものを選びなさい。"
INSTRUCTION_TRANSLATION = "次の英文を日本語に訳しなさい。"

# 入出力（CLIで --input 指定）
INPUT_CSV = str(ROOT / "data" / "unit1.csv")  # 既定値（CLIが優先）
OUTPUT_PDF = str(ROOT / "outputs" / "lesson01.pdf")

# PDF表示設定
PDF_FONT = "NotoSansJP"
PDF_FONT_PATH = ROOT / "assets" / "fonts" / "NotoSansJP-Regular.ttf"
PDF_FONT_SIZE = 12
PDF_MARGIN_TOP = 15
PDF_LINE_HEIGHT = 9  # ちょい広め推奨

# 表示オプション（グローバル固定）
SHOW_JA = True
ANSWER_LINES = 1
BRACKET_LEFT = "("
BRACKET_RIGHT = ")"
DEFAULT_TRAILING_PUNCT = "."      # 自動検出できない場合の既定
SPACE_BEFORE_TRAILING_PUNCT = True
