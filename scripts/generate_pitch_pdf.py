"""Regenerate the Digital Bridge pitch from verified product screenshots."""

from pathlib import Path

from reportlab.graphics import renderPDF
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.lib.colors import HexColor, white
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "docs" / "assets"
OUT = ROOT / "Play_Bro_Digital_Bridge.pdf"
WEB = "https://azirali.github.io/play-bro-showcase/"
REPO = "https://github.com/azirali/play-bro-showcase"
W, H = 960, 540

INK = HexColor("#211A3B")
MUTED = HexColor("#706B80")
VIOLET = HexColor("#7458E8")
CORAL = HexColor("#ED6CA3")
LILAC = HexColor("#F3F0FB")
LINE = HexColor("#E8E2F1")
DARK = HexColor("#17142E")
MINT = HexColor("#B9F1D6")
GOLD = HexColor("#E6C67E")


def setup():
    pdfmetrics.registerFont(TTFont("PB", "/System/Library/Fonts/Supplemental/Arial.ttf"))
    pdfmetrics.registerFont(TTFont("PB-Bold", "/System/Library/Fonts/Supplemental/Arial Bold.ttf"))


def box(c, x, y, w, h, color, r=16):
    c.setFillColor(color)
    c.roundRect(x, y, w, h, r, fill=1, stroke=0)


def txt(c, value, x, y, size, color=INK, bold=False):
    c.setFillColor(color)
    c.setFont("PB-Bold" if bold else "PB", size)
    c.drawString(x, y, value)


def multiline(c, value, x, y, width, size, color=MUTED, leading=None, bold=False):
    font = "PB-Bold" if bold else "PB"
    leading = leading or size * 1.35
    c.setFont(font, size)
    words = value.split()
    lines, current = [], ""
    for word in words:
        next_line = (current + " " + word).strip()
        if pdfmetrics.stringWidth(next_line, font, size) <= width:
            current = next_line
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    for line in lines:
        txt(c, line, x, y, size, color, bold)
        y -= leading
    return y


def image(c, name, x, y, w, h, mode="crop", radius=14):
    path = ASSETS / name
    reader = ImageReader(str(path))
    iw, ih = reader.getSize()
    c.saveState()
    clip = c.beginPath()
    clip.roundRect(x, y, w, h, radius)
    c.clipPath(clip, stroke=0, fill=0)
    scale = max(w / iw, h / ih) if mode == "crop" else min(w / iw, h / ih)
    dw, dh = iw * scale, ih * scale
    c.drawImage(reader, x + (w - dw) / 2, y + (h - dh) / 2, dw, dh, mask="auto")
    c.restoreState()


def header(c, number, label, title, sub=None, dark=False):
    c.setFillColor(DARK if dark else LILAC)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    txt(c, label.upper(), 52, 489, 11, GOLD if dark else VIOLET, True)
    txt(c, title, 52, 435, 34, white if dark else INK, True)
    if sub:
        multiline(c, sub, 52, 405, 830, 15, HexColor("#C9C3D8") if dark else MUTED)
    footer(c, number, dark)


def footer(c, number, dark=False):
    color = HexColor("#89819F") if dark else HexColor("#A39BB5")
    c.setStrokeColor(HexColor("#51486E") if dark else LINE)
    c.line(52, 34, 908, 34)
    txt(c, "PLAY BRO  /  DIGITAL BRIDGE 2026", 52, 18, 8, color, True)
    c.setFont("PB-Bold", 8)
    c.setFillColor(color)
    c.drawRightString(908, 18, f"{number:02d}")


def label(c, value, x, y, color=VIOLET):
    txt(c, value.upper(), x, y, 10, color, True)


def cover(c):
    c.setFillColor(DARK)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(HexColor("#2B2451"))
    c.circle(750, 305, 310, fill=1, stroke=0)
    c.setFillColor(HexColor("#544093"))
    c.circle(754, 309, 239, fill=1, stroke=0)
    image(c, "profile-current.png", 600, 45, 210, 452, radius=26)
    image(c, "room-chat.png", 775, 75, 151, 327, radius=22)
    image(c, "bro-icon.png", 50, 442, 48, 48, mode="contain", radius=8)
    txt(c, "PLAY BRO", 108, 461, 18, white, True)
    label(c, "KAZAKHSTAN · MOBILE SOCIAL GAMING", 52, 381, GOLD)
    txt(c, "Вместе", 48, 296, 75, white, True)
    txt(c, "в игре.", 48, 215, 75, HexColor("#F48DB9"), True)
    multiline(c, "Комнаты, друзья и совместные игры в одном мобильном приложении.", 52, 154, 490, 18, HexColor("#DDD6EB"), 23)
    box(c, 52, 49, 310, 45, HexColor("#3B3457"), 13)
    txt(c, "Digital Bridge 2026  ·  Olzhas Azirali", 66, 66, 11, white, True)
    c.linkURL(WEB, (52, 49, 362, 94), relative=0)
    footer(c, 1, True)


def idea(c):
    header(c, 2, "01 / Зачем", "Игры начинаются с людей.")
    multiline(c, "Компании нужен короткий путь от «позвать друзей» до «сыграть вместе». Play Bro соединяет этот путь в одном интерфейсе.", 52, 386, 800, 20, INK, 29)
    cards = [
        ("01", "Общение", "Комната, приглашения и чат собирают компанию."),
        ("02", "Выбор", "В каталоге есть форматы для разных настроений."),
        ("03", "Возвращение", "Профиль, XP, монеты и история дают повод для реванша."),
    ]
    for i, (n, title, body) in enumerate(cards):
        x = 52 + i * 291
        box(c, x, 113, 273, 193, white, 21)
        box(c, x + 18, 235, 41, 43, HexColor("#EDE7FF"), 11)
        txt(c, n, x + 27, 250, 15, VIOLET, True)
        txt(c, title, x + 19, 207, 21, INK, True)
        multiline(c, body, x + 19, 177, 232, 14, MUTED, 19)


def journey(c):
    header(c, 3, "02 / Сценарий", "Один вечер — один понятный путь.", "От комнаты к игре и обратно к компании.")
    steps = [
        ("1", "Создать комнату", "Открытая или по ссылке"),
        ("2", "Позвать друзей", "Чат и места участников"),
        ("3", "Выбрать игру", "Trivia, Дурак, Бункер"),
        ("4", "Вернуться", "Прогресс и реванш"),
    ]
    for i, (n, title, desc) in enumerate(steps):
        x = 52 + i * 220
        box(c, x, 263, 206, 96, white, 16)
        txt(c, n, x + 16, 326, 21, VIOLET, True)
        txt(c, title, x + 16, 301, 15, INK, True)
        txt(c, desc, x + 16, 280, 11, MUTED)
        if i < 3:
            txt(c, "→", x + 208, 307, 17, CORAL, True)
    image(c, "room-create.png", 58, 70, 160, 158)
    image(c, "room-chat.png", 246, 70, 160, 158)
    image(c, "trivia-lobby.png", 434, 70, 160, 158)
    image(c, "profile-current.png", 622, 70, 160, 158)
    box(c, 803, 89, 104, 120, HexColor("#E9DFFF"), 17)
    txt(c, "REAL", 820, 165, 18, VIOLET, True)
    txt(c, "APP", 820, 142, 18, VIOLET, True)
    multiline(c, "Все кадры — из запущенного прототипа.", 820, 119, 73, 9, INK, 12)


def product(c):
    header(c, 4, "03 / Приложение", "Социальный слой виден в каждом экране.", "Реальные кадры мобильной сборки, локальный тестовый сервер.")
    screens = [
        ("profile-current.png", "Профиль", "XP, серия и баланс"),
        ("room-chat.png", "Комната", "Места и чат"),
        ("shop-current.png", "Магазин", "Косметика и коллекции"),
        ("feed.png", "Лента", "Посты и общение"),
    ]
    for i, (name, title, desc) in enumerate(screens):
        x = 54 + i * 224
        box(c, x, 87, 205, 270, white, 18)
        image(c, name, x + 12, 147, 181, 198, radius=12)
        txt(c, title, x + 13, 123, 17, INK, True)
        txt(c, desc, x + 13, 103, 11, MUTED)


def games(c):
    header(c, 5, "04 / Игры", "Игры под разную компанию.", "В центре витрины — Trivia, Дурак и Бункер. Для сетевой партии нужна компания.")
    entries = [
        ("trivia-brawl.jpg", "Trivia Brawl", "2–6 игроков · 5 раундов", "ОБЛОЖКА"),
        ("durak-lobby.png", "Дурак", "Сетевой стол · 1 на 1", "ЭКРАН ИГРЫ"),
        ("bunker.jpg", "Бункер", "Роли и обсуждение · 4–8", "ОБЛОЖКА"),
    ]
    for i, (name, title, desc, kind) in enumerate(entries):
        x = 52 + i * 291
        box(c, x, 84, 273, 280, white, 20)
        image(c, name, x + 11, 168, 251, 185, radius=13)
        box(c, x + 19, 323, 102, 22, HexColor("#F6F4FB"), 6)
        txt(c, kind, x + 26, 330, 9, INK, True)
        txt(c, title, x + 17, 137, 20, INK, True)
        txt(c, desc, x + 17, 113, 12, MUTED)
    txt(c, "Лобби Trivia и Бункера также доступны в публичной витрине.", 52, 60, 11, VIOLET, True)


def belka(c):
    c.setFillColor(HexColor("#0D2118"))
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(HexColor("#205138"))
    c.circle(785, 295, 300, fill=1, stroke=0)
    label(c, "05 / ОТДЕЛЬНАЯ БРАУЗЕРНАЯ ИГРА", 52, 483, GOLD)
    txt(c, "Белка.", 52, 408, 56, white, True)
    txt(c, "Своя игра,", 52, 346, 49, white, True)
    txt(c, "свой характер.", 52, 289, 49, GOLD, True)
    multiline(c, "Казахстанская командная карточная игра уже работает против ботов: четыре места за столом, две команды и взятки.", 52, 238, 430, 16, HexColor("#D6E8DC"), 22)
    box(c, 52, 88, 438, 75, HexColor("#28503D"), 14)
    multiline(c, "Отдельный проект. Онлайн-режим ещё не открыт; интеграция в мобильный Play Bro впереди.", 69, 138, 402, 13, white, 18)
    image(c, "belka-game.png", 590, 48, 206, 445, radius=23)
    image(c, "belka-menu.png", 776, 81, 146, 317, radius=19)
    footer(c, 6, True)


def status(c):
    header(c, 7, "06 / Готовность", "Готовый к показу продукт. Честный статус.")
    box(c, 52, 105, 414, 278, white, 20)
    box(c, 484, 105, 424, 278, white, 20)
    label(c, "ПОДТВЕРЖДЕНО", 76, 349)
    lines = [
        "Комнаты, чат, каталог, лента, профиль и магазин.",
        "Лобби Trivia, Дурака и Бункера открываются локально.",
        "264 Flutter-теста; отдельный серверный сценарий Дурака.",
    ]
    yy = 314
    for line in lines:
        c.setFillColor(HexColor("#5ABD8C"))
        c.circle(83, yy + 4, 4, fill=1, stroke=0)
        yy = multiline(c, line, 99, yy, 337, 14, INK, 19) - 16
    label(c, "ДО ВНЕШНЕЙ БЕТЫ", 508, 349, CORAL)
    lines = [
        "Восстановить доступный извне backend.",
        "Проверить голос, push и поведение на устройствах.",
        "Выдать работающую сборку по приглашению.",
    ]
    yy = 314
    for line in lines:
        c.setFillColor(CORAL)
        c.circle(515, yy + 4, 4, fill=1, stroke=0)
        yy = multiline(c, line, 531, yy, 345, 14, INK, 19) - 16
    txt(c, "Скриншоты в этом документе сняты с локально запущенных продуктов.", 52, 72, 11, MUTED)


def ask(c):
    header(c, 8, "07 / Следующий шаг", "Что Play Bro ищет на Digital Bridge.")
    items = [
        ("01", "Пилотные компании", "Небольшие группы игроков для проверки полного цикла: комната → игра → реванш."),
        ("02", "Экспертная обратная связь", "Взгляд на удержание, удобство входа и упаковку продукта."),
        ("03", "Партнёрства", "Помощь с доступной инфраструктурой, тестированием и первыми сообществами."),
    ]
    yy = 309
    for num, title, body in items:
        box(c, 52, yy - 32, 856, 101, white, 18)
        box(c, 71, yy + 2, 42, 42, HexColor("#E9E1FF"), 11)
        txt(c, num, 80, yy + 17, 14, VIOLET, True)
        txt(c, title, 132, yy + 30, 19, INK, True)
        multiline(c, body, 132, yy + 8, 733, 13, MUTED, 18)
        yy -= 115


def qr(c, url, x, y, size):
    code = QrCodeWidget(url)
    bounds = code.getBounds()
    drawing = Drawing(size, size, transform=[
        size / (bounds[2] - bounds[0]), 0, 0,
        size / (bounds[3] - bounds[1]), 0, 0,
    ])
    drawing.add(code)
    renderPDF.draw(drawing, c, x, y)


def close(c):
    c.setFillColor(DARK)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(HexColor("#32275C"))
    c.circle(730, 270, 270, fill=1, stroke=0)
    image(c, "bro-icon.png", 49, 422, 70, 70, mode="contain", radius=12)
    label(c, "PLAY BRO / KAZAKHSTAN", 51, 386, GOLD)
    txt(c, "Давайте играть", 49, 307, 55, white, True)
    txt(c, "вместе.", 49, 244, 55, HexColor("#F48DB9"), True)
    multiline(c, "Публичная витрина, реальные экраны и контакты — по ссылке справа.", 52, 188, 450, 17, HexColor("#CBC4DE"), 24)
    box(c, 563, 102, 344, 333, white, 22)
    qr(c, WEB, 637, 190, 190)
    txt(c, "ОТКРЫТЬ ВИТРИНУ", 645, 158, 13, INK, True)
    txt(c, "azirali.github.io/play-bro-showcase", 593, 133, 11, MUTED)
    c.linkURL(WEB, (563, 102, 907, 435), relative=0)
    txt(c, "Olzhas Azirali  ·  github.com/azirali", 52, 75, 12, white)
    c.linkURL(REPO, (52, 62, 440, 88), relative=0)
    footer(c, 9, True)


def main():
    setup()
    c = canvas.Canvas(str(OUT), pagesize=(W, H), pageCompression=1)
    c.setTitle("Play Bro — Digital Bridge 2026")
    c.setAuthor("Play Bro / Olzhas Azirali")
    for page in (cover, idea, journey, product, games, belka, status, ask, close):
        page(c)
        c.showPage()
    c.save()
    print(OUT)


if __name__ == "__main__":
    main()
