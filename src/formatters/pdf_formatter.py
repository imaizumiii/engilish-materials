from .base_formatter import BaseFormatter
from fpdf import FPDF
from ..utils.pdf_utils import effective_page_width, safe_multicell
from ..questions.selection_question import SelectionQuestion

class PDFFormatter(BaseFormatter):
    def export(self, questions, filename: str, **kwargs):
        title = kwargs.get("title", "Rearrangement Exercises")
        instruction = kwargs.get("instruction", "")
        font = kwargs.get("font", "Arial")
        font_path = kwargs.get("font_path")
        font_size = kwargs.get("font_size", 12)
        margin_top = kwargs.get("margin_top", 15)
        line_h = kwargs.get("line_h", 8)
        show_ja = kwargs.get("show_ja", True)
        answer_lines = int(kwargs.get("answer_lines", 1))

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_margins(left=15, top=margin_top, right=15)

        if font_path:
            pdf.add_font(family=font, style="", fname=str(font_path), uni=True)
            pdf.add_font(family=font, style="B", fname=str(font_path), uni=True)

        w = effective_page_width(pdf)

        # 問題ページ
        pdf.add_page()
        pdf.set_font(font, size=font_size + 2)
        pdf.cell(0, 10, txt=title, ln=True, align="C")
        pdf.ln(2)

        if instruction:
            pdf.set_font(font, size=font_size)
            pdf.set_x(pdf.l_margin)
            safe_multicell(pdf, w, line_h, instruction)
            pdf.ln(2)

        pdf.set_font(font, size=font_size)
        for i, q in enumerate(questions, start=1):
            pdf.set_x(pdf.l_margin)
            safe_multicell(pdf, w, line_h, f"{i}. {q.text()}")
            
            if show_ja and q.ja():
                pdf.set_text_color(90, 90, 90)
                pdf.set_x(pdf.l_margin)
                safe_multicell(pdf, w, line_h, f"和訳：{q.ja()}")
                pdf.set_text_color(0, 0, 0)

            # 4択問題の場合、選択肢を表示
            if isinstance(q, SelectionQuestion):
                opts = q.get_options()
                # 選択肢のフォーマット (1) opt1        (2) opt2 ...
                # 間隔を広げる（スペース8つ）
                gap = " " * 8
                opt_str = f"(1) {opts[0]}{gap}(2) {opts[1]}{gap}(3) {opts[2]}{gap}(4) {opts[3]}"
                
                # 少しインデントして表示
                pdf.set_x(pdf.l_margin + 5)
                safe_multicell(pdf, w - 5, line_h, opt_str)
            
            # 解答線（並べ替え問題のみ）
            if not isinstance(q, SelectionQuestion):
                pdf.set_x(pdf.l_margin)
                pdf.cell(w, line_h + 2, "", ln=True, border="B")
                pdf.ln(1)
            else:
                # 選択問題は線なしで少し空ける
                pdf.ln(4)

        # 解答ページ
        pdf.add_page()
        pdf.set_font(font, size=font_size + 1)
        pdf.cell(0, 10, txt="Answer Key", ln=True, align="C")
        pdf.ln(2)
        pdf.set_font(font, size=font_size)
        for i, q in enumerate(questions, start=1):
            pdf.set_x(pdf.l_margin)
            safe_multicell(pdf, w, line_h, f"{i}. {q.answer()}")
            if show_ja and q.ja():
                pdf.set_text_color(90, 90, 90)
                pdf.set_x(pdf.l_margin)
                safe_multicell(pdf, w, line_h, f"和訳：{q.ja()}")
                pdf.set_text_color(0, 0, 0)
            pdf.ln(1)

        pdf.output(filename)
