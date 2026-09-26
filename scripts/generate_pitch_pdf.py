from pathlib import Path

from reportlab.lib.colors import Color, HexColor, white
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "Play_Bro_Digital_Bridge.pdf"
ASSETS = ROOT / "assets"
W, H = A4

BG = HexColor("#F7F6FF")
INK = HexColor("#201B3D")
MUTED = HexColor("#6F6887")
PURPLE = HexColor("#7055D7")
LILAC = HexColor("#E8E2FF")
MINT = HexColor("#CFF2E4")
ORANGE = HexColor("#FFC66D")
WHITE = white


def font_setup():
    regular = "/System/Library/Fonts/Supplemental/Arial.ttf"
    bold = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
    pdfmetrics.registerFont(TTFont("PB", regular))
    pdfmetrics.registerFont(TTFont("PBBold", bold))


def rounded(c, x, y, w, h, fill, radius=18):
    c.setFillColor(fill)
    c.roundRect(x, y, w, h, radius, stroke=0, fill=1)


def text(c, value, x, y, size=12, color=INK, bold=False, leading=None):
    c.setFillColor(color)
    c.setFont("PBBold" if bold else "PB", size)
    if isinstance(value, str):
        c.drawString(x, y, value)
        return y
    leading = leading or size * 1.35
    for line in value:
        c.drawString(x, y, line)
        y -= leading
    return y


def wrap(c, value, max_width, size=12, bold=False):
    c.setFont("PBBold" if bold else "PB", size)
    words = value.split()
    lines, current = [], ""
    for word in words:
        proposal = (current + " " + word).strip()
        if c.stringWidth(proposal, "PBBold" if bold else "PB", size) <= max_width:
            current = proposal
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def footer(c, page):
    c.setStrokeColor(HexColor("#DDD8F3"))
    c.line(42, 34, W - 42, 34)
    text(c, "PLAY BRO  |  DIGITAL BRIDGE 2026", 42, 19, 8, MUTED, True)
    c.setFont("PB", 8)
    c.setFillColor(MUTED)
    c.drawRightString(W - 42, 19, str(page))


def bullet(c, label, detail, x, y, w, color=PURPLE):
    c.setFillColor(color)
    c.circle(x + 5, y + 4, 4, stroke=0, fill=1)
    text(c, label, x + 18, y, 12, INK, True)
    lines = wrap(c, detail, w - 18, 10)
    text(c, lines, x + 18, y - 15, 10, MUTED, False, 13)
    return y - 15 - len(lines) * 13 - 13


def card_copy(c, value, x, y, width, size=12, color=INK, bold=False, leading=None):
    """Draw bounded copy inside a card so long Russian text never runs off page."""
    lines = wrap(c, value, width, size, bold)
    text(c, lines, x, y, size, color, bold, leading)
    return lines


def cover(c):
    c.setFillColor(BG)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    c.setFillColor(LILAC)
    c.circle(W - 50, H - 25, 180, stroke=0, fill=1)
    c.setFillColor(MINT)
    c.circle(15, 105, 95, stroke=0, fill=1)
    rounded(c, 42, H - 112, 110, 34, PURPLE, 17)
    text(c, "PLAY BRO", 58, H - 100, 13, WHITE, True)
    text(c, "Социальные игры,", 42, H - 205, 36, INK, True)
    text(c, "в которые легко войти", 42, H - 250, 36, INK, True)
    text(c, "Social gaming platform from Kazakhstan", 44, H - 286, 15, MUTED)
    rounded(c, 42, 122, W - 84, 110, WHITE, 24)
    text(c, "Digital Bridge 2026", 66, 193, 16, PURPLE, True)
    text(c, ["Мобильная платформа, объединяющая игры, комнаты, друзей", "и прогрессию в одном коротком социальном цикле."], 66, 168, 13, INK, False, 18)
    text(c, "Olzhas Azirali  |  Founder", 42, 65, 11, MUTED)


def product(c):
    text(c, "Одна точка входа в совместную игру", 42, H - 75, 25, INK, True)
    text(c, "Play Bro превращает поиск игры в естественное продолжение общения.", 42, H - 103, 12, MUTED)
    steps = [
        ("1", "Зайти", "Открыть приложение и увидеть, что можно сделать прямо сейчас."),
        ("2", "Найти", "Выбрать игру, комнату или пригласить друга."),
        ("3", "Сыграть", "Короткая сессия с realtime-механикой и понятным результатом."),
        ("4", "Вернуться", "Получить XP, историю матча и повод для реванша."),
    ]
    y = H - 205
    for n, title, detail in steps:
        rounded(c, 42, y - 34, 50, 50, PURPLE, 15)
        text(c, n, 60, y - 17, 16, WHITE, True)
        text(c, title, 112, y, 16, INK, True)
        text(c, wrap(c, detail, W - 160, 11), 112, y - 18, 11, MUTED, False, 15)
        y -= 104
    rounded(c, 42, 88, W - 84, 74, LILAC, 20)
    text(c, "Цель продукта", 64, 134, 12, PURPLE, True)
    card_copy(c, "Сделать онлайн-время с друзьями проще: один профиль, одна компания, много форматов игры.", 64, 119, W - 128, 12, INK, False, 15)
    footer(c, 2)


def games(c):
    text(c, "Три формата, один социальный слой", 42, H - 75, 25, INK, True)
    games = [
        ("Trivia Brawl", "2-6 игроков, 5 раундов", "Быстрые вопросы для компании.", HexColor("#507BE8")),
        ("Дурак", "1 на 1, онлайн", "Карточная игра с авторитарной логикой сервера.", HexColor("#1D5A9B")),
        ("Бункер", "4-8 игроков, голос", "Социальная дедукция и обсуждение в комнате.", HexColor("#C98416")),
    ]
    y = H - 235
    for title, meta, desc, accent in games:
        rounded(c, 42, y, W - 84, 104, WHITE, 22)
        c.setFillColor(accent)
        c.circle(76, y + 52, 18, stroke=0, fill=1)
        text(c, title, 112, y + 63, 16, INK, True)
        text(c, meta, 112, y + 42, 10, accent, True)
        text(c, wrap(c, desc, W - 185, 10), 112, y + 22, 10, MUTED, False, 13)
        y -= 126
    rounded(c, 42, 95, W - 84, 74, MINT, 20)
    text(c, "Принцип каталога", 64, 141, 12, HexColor("#217A62"), True)
    card_copy(c, "Не обещаем недоступные режимы и не показываем вымышленный онлайн. Каждая карточка ведёт к реальному сценарию.", 64, 125, W - 128, 10, INK, False, 13)
    footer(c, 3)


def screenshots(c):
    text(c, "Интерфейс: знакомый, лёгкий, игровой", 42, H - 75, 25, INK, True)
    text(c, "Светлая визуальная система, короткие действия и единый аватар во всех социальных местах.", 42, H - 103, 12, MUTED)
    images = [("profile.jpg", "Профиль игрока"), ("shop.jpg", "Прогрессия и косметика"), ("settings.jpg", "Настройки и приватность")]
    x = 42
    for filename, caption in images:
        rounded(c, x, 172, 156, 442, WHITE, 22)
        image = ImageReader(str(ASSETS / filename))
        c.drawImage(image, x + 9, 212, 138, 373, preserveAspectRatio=True, mask="auto")
        text(c, caption, x + 14, 190, 10, INK, True)
        x += 178
    footer(c, 4)


def platform(c):
    text(c, "Платформа для роста, а не одна игра", 42, H - 75, 25, INK, True)
    text(c, "Новые форматы используют уже готовые социальные и продуктовые сервисы.", 42, H - 103, 12, MUTED)
    layers = [
        ("Опыт игрока", "Flutter iOS / Android", PURPLE),
        ("Социальный слой", "Профиль, друзья, комнаты, приглашения, лента", HexColor("#4E82D7")),
        ("Игровой слой", "Авторитарные realtime-матчи и общий matchmaking", HexColor("#4DAD83")),
        ("Продуктовый слой", "XP, монеты, история, достижения, косметика", HexColor("#D98F29")),
        ("Надёжность", "PostgreSQL, push, мониторинг, Sentry", HexColor("#7C6A9F")),
    ]
    y = H - 185
    for label, detail, color in layers:
        rounded(c, 42, y, W - 84, 58, WHITE, 16)
        c.setFillColor(color)
        c.rect(42, y, 12, 58, stroke=0, fill=1)
        text(c, label, 74, y + 32, 13, INK, True)
        text(c, detail, 74, y + 15, 10, MUTED)
        y -= 76
    footer(c, 5)


def maturity(c):
    text(c, "Что уже подтверждено", 42, H - 75, 25, INK, True)
    text(c, "Работаем от пользовательского сценария и проверяем критичные состояния автоматически.", 42, H - 103, 12, MUTED)
    y = H - 175
    y = bullet(c, "Realtime-сценарии", "Проверены комнаты, ход игры, переподключение и выдача наград в локальном изолированном окружении.", 50, y, W - 100, PURPLE)
    y = bullet(c, "Прогрессия", "XP, монеты, история матча и достижения связаны с результатом игры, включая онлайн-Дурак.", 50, y, W - 100, HexColor("#4DAD83"))
    y = bullet(c, "Социальная безопасность", "Есть фильтрация контента, блокировки, жалобы, управление видимостью и сценарий удаления аккаунта.", 50, y, W - 100, HexColor("#D98F29"))
    y = bullet(c, "Качество", "264 Flutter-теста, HTTP-проверки backend и CI для основных сценариев на момент подготовки материалов.", 50, y, W - 100, HexColor("#4E82D7"))
    rounded(c, 42, 86, W - 84, 72, LILAC, 20)
    text(c, "Текущий этап", 64, 132, 12, PURPLE, True)
    card_copy(c, "Beta prototype. Следующие задачи: production-инфраструктура, тесты на устройствах и расширение контентной базы Trivia.", 64, 117, W - 128, 10, INK, False, 13)
    footer(c, 6)


def market(c):
    text(c, "Куда развивается Play Bro", 42, H - 75, 25, INK, True)
    text(c, "Движение от ранней компании игроков к повторяемому социальному продукту.", 42, H - 103, 12, MUTED)
    columns = [
        ("Сейчас", ["Закрытая beta", "3 игровых режима", "Единый профиль и прогресс"], PURPLE),
        ("Следующий этап", ["Надёжный production backend", "Тестирование на устройствах", "Расширение Trivia и реванши"], HexColor("#4E82D7")),
        ("Дальше", ["Новые социальные игры", "Creator / community механики", "Региональные сообщества"], HexColor("#4DAD83")),
    ]
    x = 42
    for title, points, color in columns:
        rounded(c, x, 272, 160, 260, WHITE, 22)
        c.setFillColor(color)
        c.circle(x + 30, 494, 12, stroke=0, fill=1)
        text(c, title, x + 24, 456, 15, INK, True)
        yy = 416
        for point in points:
            c.setFillColor(color)
            c.circle(x + 29, yy + 3, 4, stroke=0, fill=1)
            lines = wrap(c, point, 105, 10, True)
            text(c, lines, x + 42, yy, 10, INK, True, 13)
            yy -= len(lines) * 13 + 17
        x += 176
    rounded(c, 42, 104, W - 84, 80, MINT, 20)
    text(c, "Для Digital Bridge", 64, 147, 12, HexColor("#217A62"), True)
    card_copy(c, "Ищем экспертную обратную связь, пилотные сообщества и партнёров, которые помогут вывести продукт к первым активным группам пользователей.", 64, 138, W - 128, 10, INK, False, 13)
    footer(c, 7)


def close(c):
    c.setFillColor(BG)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    c.setFillColor(LILAC)
    c.circle(W - 35, H - 5, 160, stroke=0, fill=1)
    c.setFillColor(MINT)
    c.circle(30, 80, 110, stroke=0, fill=1)
    text(c, "Play Bro", 42, H - 150, 38, INK, True)
    text(c, "Игры, в которые проще зайти вместе.", 42, H - 193, 18, MUTED)
    rounded(c, 42, 220, W - 84, 124, WHITE, 24)
    text(c, "Публичная витрина", 66, 302, 12, PURPLE, True)
    text(c, "shutovBro.github.io/play-bro-showcase", 66, 274, 14, INK, True)
    text(c, "Olzhas Azirali  |  Founder  |  Kazakhstan", 66, 242, 12, MUTED)
    text(c, "Спасибо", 42, 128, 22, INK, True)
    text(c, "Thank you", 42, 99, 13, MUTED)
    footer(c, 8)


def main():
    font_setup()
    c = canvas.Canvas(str(OUT), pagesize=A4, pageCompression=1)
    for page in [cover, product, games, screenshots, platform, maturity, market, close]:
        page(c)
        c.showPage()
    c.save()
    print(OUT)


if __name__ == "__main__":
    main()
