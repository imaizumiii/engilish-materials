from .questions.question_bank import QuestionBank
from .formatters.pdf_formatter import PDFFormatter
from . import config
from pathlib import Path
import argparse

def resolve_font_path() -> str:
    fp = Path(config.PDF_FONT_PATH)
    if fp.exists():
        return str(fp)
    fonts_dir = Path(config.ROOT) / "assets" / "fonts"
    candidates = list(fonts_dir.glob("*.ttf"))
    if candidates:
        return str(candidates[0])
    raise FileNotFoundError(
        f"日本語フォントTTFが見つかりません。\n"
        f"想定: {fp}\n"
        f"または {fonts_dir} 配下に .ttf を配置してください。"
    )

def build_one(csv_path: Path, out_dir: Path, font_path: str):
    bank = QuestionBank(csv_path.stem)
    bank.load_from_csv(str(csv_path))
    questions = bank.all()
    meta = bank.meta()

    title = meta.get("title", config.TITLE)
    instruction = meta.get("instruction", config.INSTRUCTION_JA)

    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{csv_path.stem}.pdf"

    fmt = PDFFormatter()
    fmt.export(
        questions,
        str(out_path),
        title=title,
        instruction=instruction,
        font=config.PDF_FONT,
        font_path=font_path,
        font_size=config.PDF_FONT_SIZE,
        margin_top=config.PDF_MARGIN_TOP,
        line_h=config.PDF_LINE_HEIGHT,
        show_ja=config.SHOW_JA,
        answer_lines=config.ANSWER_LINES,
    )
    print(f"[OK] {csv_path} -> {out_path}")

def main():
    parser = argparse.ArgumentParser(description="Build rearrangement PDFs")
    parser.add_argument("--input", "-i", required=True, help="CSVファイル or フォルダ（再帰）")
    parser.add_argument("--outdir", "-o", default=str(Path(config.ROOT) / "outputs"))
    args = parser.parse_args()

    font_path = resolve_font_path()
    in_path = Path(args.input)
    out_dir = Path(args.outdir)

    if in_path.is_file() and in_path.suffix.lower() == ".csv":
        build_one(in_path, out_dir, font_path)
    elif in_path.is_dir():
        csvs = sorted(in_path.rglob("*.csv"))
        if not csvs:
            print(f"[WARN] CSVが見つかりません: {in_path}")
            return
        for p in csvs:
            build_one(p, out_dir, font_path)
    else:
        raise FileNotFoundError(f"--input に指定したパスが不正です: {in_path}")

if __name__ == "__main__":
    main()
