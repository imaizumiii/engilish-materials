from fpdf import FPDF

def effective_page_width(pdf: FPDF) -> float:
    """余白を除いたページ横幅"""
    return pdf.w - pdf.l_margin - pdf.r_margin

def safe_multicell(pdf: FPDF, w: float, h: float, text: str, **kwargs):
    """
    fpdf2のmulti_cellで日本語（スペースなし）でも落ちないように、
    文字単位で手動折り返しにフォールバックする。
    """
    try:
        # まずは素直にmulti_cellに任せる
        pdf.multi_cell(w, h, text, **kwargs)
    except Exception:
        # フォールバック：文字単位ラップ
        line = ""
        for ch in text:
            if ch == "\n":
                pdf.cell(w, h, line, ln=1)
                line = ""
                continue
            # 1文字でもはみ出すなら改行
            if line and pdf.get_string_width(line + ch) > w:
                pdf.cell(w, h, line, ln=1)
                line = ch
            else:
                line += ch
        if line:
            pdf.cell(w, h, line, ln=1)
