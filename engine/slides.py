"""module.yaml -> slides PDF (for students) + one PNG per slide (for the video).

The look copies the approved Module 1.2 PDF: white page, navy titles,
blue module numbers, navy table headers, dark terminal boxes.
Pages are 16:9 so they fill a 1920x1080 video frame exactly.
"""
import glob
import io
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, KeepInFrame, PageBreak,
                                PageTemplate, Paragraph, Spacer, Table,
                                TableStyle, XPreformatted)

from common import COLORS, fail, run, say

PAGE_W, PAGE_H = 960, 540          # points; 16:9
MARGIN_X, MARGIN_TOP, MARGIN_BOTTOM = 40, 30, 26
CONTENT_W = PAGE_W - 2 * MARGIN_X
CONTENT_H = PAGE_H - MARGIN_TOP - MARGIN_BOTTOM


def C(name):
    return colors.HexColor(COLORS.get(name, name))


# --------------------------------------------------------------------------
# Fonts: use real TTF fonts so arrows and box lines (──>) render.
# --------------------------------------------------------------------------
FONT_DIRS = ["/usr/share/fonts/truetype/liberation", "/usr/share/fonts/truetype/dejavu",
             "/usr/share/fonts/truetype/liberation2"]
SANS, MONO = "Helvetica", "Courier"
SUPPORTED = {}                      # font name -> set of characters it can draw
REPLACE = {"→": "->", "←": "<-", "⇒": "=>", "─": "-", "━": "-", "│": "|", "▶": ">",
           "✓": "v", "✔": "v", "✗": "x", "“": '"', "”": '"', "’": "'", "‘": "'"}


def _find(name):
    for d in FONT_DIRS:
        p = Path(d) / name
        if p.exists():
            return str(p)
    return None


def setup_fonts():
    global SANS, MONO
    sans = (_find("LiberationSans-Regular.ttf"), _find("LiberationSans-Bold.ttf"))
    if not all(sans):
        sans = (_find("DejaVuSans.ttf"), _find("DejaVuSans-Bold.ttf"))
    mono = (_find("DejaVuSansMono.ttf"), _find("DejaVuSansMono-Bold.ttf"))
    for family, (reg, bold) in (("CSans", sans), ("CMono", mono)):
        if reg and bold:
            pdfmetrics.registerFont(TTFont(family, reg))
            pdfmetrics.registerFont(TTFont(family + "-Bold", bold))
            pdfmetrics.registerFontFamily(family, normal=family, bold=family + "-Bold",
                                          italic=family, boldItalic=family + "-Bold")
            chars = set(chr(c) for c in pdfmetrics.getFont(family).face.charToGlyph)
            SUPPORTED[family] = SUPPORTED[family + "-Bold"] = chars
            if family == "CSans":
                SANS = family
            else:
                MONO = family
    if SANS == "Helvetica" or MONO == "Courier":
        say("  note: DejaVu/Liberation fonts not found - using basic PDF fonts "
            "(install: sudo apt install fonts-dejavu-core fonts-liberation)")


def clean(text, font):
    out = []
    ok = SUPPORTED.get(font)
    for ch in str(text):
        if ok is not None and ch in ok:
            out.append(ch)
        elif ok is None and (ord(ch) < 256 or ch in "•–—"):
            out.append(ch)
        elif ch in REPLACE:
            out.append(REPLACE[ch])
        elif ch in "\n\t ":
            out.append(ch)
        # anything else (emoji etc.) is dropped
    return "".join(out)


# --------------------------------------------------------------------------
# Markup: **bold**  `code`  [red]..[/red]  newline -> line break
# --------------------------------------------------------------------------
def rl(text, font=None, code_color=None):
    s = clean(text, font or SANS)
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s, flags=re.S)
    color = f' color="{code_color}"' if code_color else ""
    s = re.sub(r"`([^`]+)`", lambda m: f'<font face="{MONO}"{color}>{m.group(1)}</font>', s)
    s = re.sub(r"\[(red|orange|green|blue|muted)\]",
               lambda m: f'<font color="{COLORS[m.group(1)]}">', s)
    s = re.sub(r"\[/(red|orange|green|blue|muted)\]", "</font>", s)
    return s.strip("\n").replace("\n", "<br/>")


def rl_pre(text):
    """Same markup for monospace blocks, keeping spaces and line breaks."""
    s = clean(text, MONO).rstrip("\n")
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = s.replace("`", "")
    s = re.sub(r"\[(red|orange|green|blue|muted)\]",
               lambda m: f'<font color="{COLORS[m.group(1)]}">', s)
    return re.sub(r"\[/(red|orange|green|blue|muted)\]", "</font>", s)


def lines_of(value):
    if isinstance(value, list):
        return "\n".join(str(v) for v in value)
    return str(value or "")


# --------------------------------------------------------------------------
# Styles
# --------------------------------------------------------------------------
def styles():
    S = {}

    def st(name, size, color="text", bold=False, leading=None, font=None, **kw):
        f = font or SANS
        S[name] = ParagraphStyle(name, fontName=f + ("-Bold" if bold and f in ("CSans", "CMono") else ""),
                                 fontSize=size, leading=leading or size * 1.32,
                                 textColor=C(color), **kw)
        if bold and f == "Helvetica":
            S[name].fontName = "Helvetica-Bold"
        if bold and f == "Courier":
            S[name].fontName = "Courier-Bold"

    st("title", 28, "navy", bold=True, leading=33, spaceAfter=4)
    st("subtitle", 16, "muted", leading=21, spaceAfter=16)
    st("body", 16, "text", leading=22)
    st("body_dark", 15, "#CBD5E1", leading=21)
    st("bullet", 16, "text", leading=22, leftIndent=16, bulletIndent=2, spaceBefore=3)
    st("bullet_dark", 15, "#CBD5E1", leading=21, leftIndent=16, bulletIndent=2, spaceBefore=3)
    st("cell", 14.5, "text", leading=19)
    st("cell_head", 15, "white", bold=True, leading=19)
    st("h", 17, "navy", bold=True, leading=22, spaceAfter=7)
    st("code", 15, "blue", bold=True, font=MONO, leading=20)
    st("code_light", 15, "module", bold=True, font=MONO, leading=20)
    st("mod_label", 18, "blue", bold=True, leading=23)
    st("main_title", 44, "navy", bold=True, leading=52)
    st("main_sub", 21, "muted", leading=29)
    return S


# --------------------------------------------------------------------------
# Slide builders: each returns a list of flowables for one page
# --------------------------------------------------------------------------
def header(S, s):
    return [Paragraph(f'<font color="{COLORS["module"]}">MODULE {rl(s["number"])}</font> | {rl(s["title"])}',
                      S["title"]),
            Paragraph(rl(s["subtitle"]), S["subtitle"])]


def bullets(S, items, dark=False):
    style = S["bullet_dark" if dark else "bullet"]
    return [Paragraph(rl(b), style, bulletText="•") for b in items or []]


def box(content, width, bg, border, border_w=1, pad=16):
    t = Table([[content]], colWidths=[width])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), C(bg)),
                           ("BOX", (0, 0), (-1, -1), border_w, C(border)),
                           ("PADDING", (0, 0), (-1, -1), pad),
                           ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


def side_by_side(cells, bgs, borders, border_w=1, pad=16, gap=0):
    n = len(cells)
    w = CONTENT_W / n
    t = Table([cells], colWidths=[w] * n)
    cmds = [("PADDING", (0, 0), (-1, -1), pad), ("VALIGN", (0, 0), (-1, -1), "TOP")]
    for i in range(n):
        cmds.append(("BACKGROUND", (i, 0), (i, 0), C(bgs[i])))
        cmds.append(("BOX", (i, 0), (i, 0), border_w, C(borders[i])))
    t.setStyle(TableStyle(cmds))
    return t


def slide_title(S, s, m):
    info = m["module"]
    boxes = [[Paragraph(f'<b>{rl(b["heading"])}</b><br/>{rl(b["text"])}', S["body"])
              for b in info["info"]]]
    t = Table(boxes, colWidths=[CONTENT_W / len(info["info"])] * len(info["info"]))
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), C("bg")),
                           ("PADDING", (0, 0), (-1, -1), 12),
                           ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                           ("LINEBELOW", (0, 0), (-1, -1), 2.5, C("blue"))]))
    return [Spacer(1, 30),
            Paragraph(f'MODULE {rl(info["number"])}: {rl(info["label"])}', S["mod_label"]),
            Spacer(1, 16),
            Paragraph(rl(info["title"]), S["main_title"]),
            Spacer(1, 10),
            Paragraph(rl(info["subtitle"]), S["main_sub"]),
            Spacer(1, 44), t]


def panel_cell(S, p, light=True):
    color = COLORS.get(p.get("color", "blue"), COLORS["blue"])
    cell = [Paragraph(f'<font color="{color}"><b>{rl(p["heading"])}</b></font>', S["h"])]
    if p.get("example"):
        cell.append(Paragraph(f"<b>Example:</b> {rl(p['example'])}", S["body"]))
        cell.append(Spacer(1, 6))
    if p.get("text"):
        cell.append(Paragraph(rl(p["text"]), S["body"]))
        cell.append(Spacer(1, 6))
    cell += bullets(S, p.get("bullets"))
    if p.get("code"):
        cell.append(Spacer(1, 8))
        cell.append(XPreformatted(rl_pre(lines_of(p["code"])), S["code_light"]))
    return cell, color


def slide_two_columns(S, s, m):
    left, lc = panel_cell(S, s["left"])
    right, rc = panel_cell(S, s["right"])
    return header(S, s) + [side_by_side([left, right], ["bg", "bg"], [lc, rc])]


def slide_table(S, s, m):
    cols = s["columns"]
    widths = s.get("widths") or [1] * len(cols)
    total = float(sum(widths))
    col_w = [CONTENT_W * w / total for w in widths]
    data = [[Paragraph(f"<b>{rl(c)}</b>", S["cell_head"]) for c in cols]]
    for row in s["rows"]:
        cells = []
        for j, cell in enumerate(row):
            txt = rl(cell)
            if j == 0 and "<b>" not in txt:
                txt = f"<b>{txt}</b>"
            cells.append(Paragraph(txt, S["cell"]))
        data.append(cells)
    t = Table(data, colWidths=col_w, repeatRows=1)
    cmds = [("BACKGROUND", (0, 0), (-1, 0), C("navy")),
            ("PADDING", (0, 0), (-1, -1), 9),
            ("GRID", (0, 0), (-1, -1), 0.5, C("border")),
            ("VALIGN", (0, 0), (-1, -1), "TOP")]
    for r in range(1, len(data), 2):
        cmds.append(("BACKGROUND", (0, r), (-1, r), C("bg")))
    t.setStyle(TableStyle(cmds))
    return header(S, s) + [t]


def slide_diagram(S, s, m):
    inner = []
    if s.get("heading"):
        inner += [Paragraph(f"<b>{rl(s['heading'])}</b>", ParagraphStyle(
            "dh", parent=S["h"], textColor=C("blue"))), Spacer(1, 4)]
    inner.append(XPreformatted(rl_pre(lines_of(s["lines"])), S["code"]))
    if s.get("takeaways"):
        inner += [Spacer(1, 12), Paragraph("<b>KEY TAKEAWAYS:</b>", ParagraphStyle(
            "kt", parent=S["h"], textColor=C("orange"), fontSize=15))]
        inner += bullets(S, s["takeaways"], dark=True)
    return header(S, s) + [box(inner, CONTENT_W, "code_bg", "blue", 2, 18)]


def slide_panel(S, s, m):
    inner = [Paragraph(f"<b>{rl(s['heading'])}</b>", S["h"])]
    if s.get("text"):
        inner += [Paragraph(rl(s["text"]), S["body"]), Spacer(1, 10)]
    if s.get("subheading"):
        inner.append(Paragraph(f"<b>{rl(s['subheading'])}</b>", ParagraphStyle(
            "sh", parent=S["h"], fontSize=16)))
    inner += bullets(S, s.get("bullets"))
    return header(S, s) + [box(inner, CONTENT_W, "bg", "border", 1, 16)]


def slide_terminal(S, s, m):
    cells, borders = [], []
    for p in s["panels"]:
        color = COLORS.get(p.get("color", "blue"), COLORS["blue"])
        cells.append([Paragraph(f'<font color="{color}"><b>{rl(p["heading"])}</b></font>',
                                ParagraphStyle("th", parent=S["h"], fontSize=15)),
                      XPreformatted(rl_pre(lines_of(p["lines"])), S["code"])])
        borders.append(color)
    out = header(S, s) + [side_by_side(cells, ["code_bg"] * len(cells), borders, 1.5, 14)]
    if s.get("takeaways"):
        out += [Spacer(1, 10), Paragraph("<b>Key Takeaways:</b>", S["h"])]
        out += bullets(S, s["takeaways"])
    if s.get("note"):
        out += [Spacer(1, 10), Paragraph(rl(s["note"]), S["body"])]
    return out


def slide_quiz(S, s, m):
    n = s.get("question", 1)
    q = m["quiz"][n - 1]
    letters = "ABCDE"
    ans = str(q["answer"]).strip().upper()
    opts = []
    for i, o in enumerate(q["options"]):
        line = f"{letters[i]}) {rl(o)}"
        opts.append(f"<b>{line} (CORRECT)</b>" if letters[i] == ans else line)
    topic = f": {rl(q['topic'])}" if q.get("topic") else ""
    quiz = [Paragraph(f"<b>QUIZ QUESTION {n}{topic}</b>", S["h"]),
            Paragraph(f"<b>Q:</b> {rl(q['question'])}", S["body"]), Spacer(1, 8),
            Paragraph("<br/>".join(opts), S["body"])]
    tutor = [Paragraph("<b>EMBEDDED AI TUTOR EXPLANATION</b>", ParagraphStyle(
                 "ai", parent=S["h"], textColor=C("#1E1B4B"))),
             Paragraph(f"<b>Why Option {ans} is Correct:</b><br/>{rl(q['explanation'])}", S["body"])]
    if q.get("tip"):
        tutor += [Spacer(1, 8), Paragraph(f"<b>SRE Pro-Tip:</b> {rl(q['tip'])}", S["body"])]
    return header(S, s) + [box(quiz, CONTENT_W, "bg", "border", 1, 12), Spacer(1, 12),
                           box(tutor, CONTENT_W, "lavender_bg", "lavender", 1, 12)]


def slide_lab(S, s, m):
    steps = s.get("steps") or [st["title"] for st in m["lab"]["steps"]]
    lab = [Paragraph("<b>KILLERCODA INTERACTIVE LAB CHALLENGE</b>", ParagraphStyle(
               "lh", parent=S["h"], textColor=C("green"))),
           Paragraph("<br/>".join(f"{i + 1}. {rl(x)}" for i, x in enumerate(steps)), S["body"])]
    out = header(S, s) + [box(lab, CONTENT_W, "mint_bg", "green", 1, 12)]
    nxt = m["module"].get("next")
    if nxt:
        body = [Paragraph(f"<b>UP NEXT: MODULE {rl(nxt['number'])} - {rl(nxt['title'])}</b>", S["h"])]
        if s.get("next_text"):
            body.append(Paragraph(rl(s["next_text"]), S["body"]))
        out += [Spacer(1, 12), box(body, CONTENT_W, "bg", "border", 1, 12)]
    return out


BUILDERS = {"title": slide_title, "two_columns": slide_two_columns, "table": slide_table,
            "diagram": slide_diagram, "panel": slide_panel, "terminal": slide_terminal,
            "quiz": slide_quiz, "lab": slide_lab}


# --------------------------------------------------------------------------
# Fit check + PDF/PNG output
# --------------------------------------------------------------------------
def needed_height(flowables):
    total = 0
    for f in flowables:
        _, h = f.wrap(CONTENT_W, 10_000)
        total += h + f.getSpaceBefore() + f.getSpaceAfter()
    return total


def build_slides(module, out_pdf, png_dir, scenes_with_slides):
    setup_fonts()
    S = styles()
    pages, problems = [], []
    for sc in scenes_with_slides:
        s = sc["slide"]
        flow = BUILDERS[s["type"]](S, s, module)
        h = needed_height(flow)
        if h > CONTENT_H:
            scale = CONTENT_H / h
            msg = f"slide for scene '{sc['id']}' has too much text ({int(scale * 100)}% fit)"
            if scale < 0.85:
                problems.append(msg + " - shorten it")
            else:
                say(f"  note: {msg} - shrunk slightly to fit")
        # rebuild fresh flowables (wrap() above may have cached sizes)
        pages.append(KeepInFrame(CONTENT_W, CONTENT_H, BUILDERS[s["type"]](S, s, module), mode="shrink"))
    if problems:
        fail("Some slides do not fit:\n  - " + "\n  - ".join(problems))

    story = []
    for i, p in enumerate(pages):
        story.append(p)
        if i < len(pages) - 1:
            story.append(PageBreak())

    def paint_bg(canvas, doc):
        canvas.setFillColor(colors.white)
        canvas.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)

    doc = BaseDocTemplate(str(out_pdf), pagesize=(PAGE_W, PAGE_H),
                          title=module["module"]["title"],
                          author=module.get("_author", ""),
                          leftMargin=MARGIN_X, rightMargin=MARGIN_X,
                          topMargin=MARGIN_TOP, bottomMargin=MARGIN_BOTTOM)
    frame = Frame(MARGIN_X, MARGIN_BOTTOM, CONTENT_W, CONTENT_H, id="f",
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id="slide", frames=[frame], onPage=paint_bg)])
    doc.build(story)

    if png_dir is not None:
        png_dir.mkdir(parents=True, exist_ok=True)
        for old in png_dir.glob("slide-*.png"):
            old.unlink()
        run(["pdftoppm", "-png", "-scale-to-x", "1920", "-scale-to-y", "1080",
             str(out_pdf), str(png_dir / "slide")])
        pngs = sorted(glob.glob(str(png_dir / "slide-*.png")))
        if len(pngs) != len(pages):
            fail(f"Expected {len(pages)} slide images, got {len(pngs)}")
        return [Path(p) for p in pngs]
    return []
