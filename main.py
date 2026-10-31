
import os
import sys
import json
import math
import pygame

# ==========================================
# СИМУЛЯТОР ЧЕКУШКИ MOBILE v1.0
# ==========================================

pygame.init()

WIDTH = 900
HEIGHT = 500
FPS = 60

BASE = os.path.dirname(os.path.abspath(__file__))

ANDROID = (
    sys.platform == "android"
    or bool(os.environ.get("ANDROID_ARGUMENT"))
)

# На Android файлы игры могут быть только
# для чтения. Сохранения храним отдельно.
if ANDROID:
    SAVE_DIR = os.environ.get(
        "ANDROID_PRIVATE",
        os.path.expanduser("~")
    )
else:
    SAVE_DIR = BASE

try:
    os.makedirs(SAVE_DIR, exist_ok=True)
except OSError:
    SAVE_DIR = BASE

SAVE_FILE = os.path.join(
    SAVE_DIR,
    "skins_save.json"
)

# ==========================================
# ЦВЕТА
# ==========================================

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 40, 220)
GREEN = (30, 190, 50)
DARK_GREEN = (15, 130, 35)
RED = (230, 20, 20)
YELLOW = (255, 220, 50)
BROWN = (135, 80, 40)

# ==========================================
# ЭКРАН
# ==========================================

screen = pygame.Surface((WIDTH, HEIGHT))

fullscreen = True

info = pygame.display.Info()

MONITOR_W = info.current_w
MONITOR_H = info.current_h

display = None

scale = 1.0
offset_x = 0
offset_y = 0

game_w = WIDTH
game_h = HEIGHT


def setup_display():
    global display
    global scale
    global offset_x, offset_y
    global game_w, game_h

    if ANDROID:
        display = pygame.display.set_mode(
            (0, 0),
            pygame.FULLSCREEN
        )

    elif fullscreen:
        display = pygame.display.set_mode(
            (MONITOR_W, MONITOR_H),
            pygame.FULLSCREEN
        )

    else:
        display = pygame.display.set_mode(
            (WIDTH, HEIGHT)
        )

    dw, dh = display.get_size()

    scale = min(
        dw / WIDTH,
        dh / HEIGHT
    )

    game_w = max(
        1,
        round(WIDTH * scale)
    )

    game_h = max(
        1,
        round(HEIGHT * scale)
    )

    offset_x = (dw - game_w) // 2
    offset_y = (dh - game_h) // 2

    pygame.display.set_caption(
        "СИМУЛЯТОР ЧЕКУШКИ MOBILE v1.0"
    )


def toggle_fullscreen():
    global fullscreen

    if not ANDROID:
        fullscreen = not fullscreen
        setup_display()


def to_game(pos):
    return (
        int((pos[0] - offset_x) / scale),
        int((pos[1] - offset_y) / scale)
    )


def finger_to_game(event):
    dw, dh = display.get_size()

    return to_game((
        event.x * dw,
        event.y * dh
    ))


def in_game(pos):
    return (
        0 <= pos[0] < WIDTH
        and 0 <= pos[1] < HEIGHT
    )


def present():
    display.fill(BLACK)

    if (game_w, game_h) == (WIDTH, HEIGHT):
        display.blit(
            screen,
            (offset_x, offset_y)
        )

    else:
        scaled = pygame.transform.scale(
    screen,
    (game_w, game_h)
)

        display.blit(
            scaled,
            (offset_x, offset_y)
        )

    pygame.display.flip()


setup_display()

clock = pygame.time.Clock()

# ==========================================
# ШРИФТЫ
# ==========================================

# Для Android лучше положить
# DejaVuSans.ttf рядом с main.py.

font_path = os.path.join(
    BASE,
    "DejaVuSans.ttf"
)

if os.path.exists(font_path):
    font = pygame.font.Font(font_path, 30)
    small_font = pygame.font.Font(font_path, 22)
    big_font = pygame.font.Font(font_path, 58)
    title_font = pygame.font.Font(font_path, 38)
    intro_font = pygame.font.Font(font_path, 80)
    version_font = pygame.font.Font(font_path, 17)

else:
    font = pygame.font.SysFont(
        "arial", 36, bold=True
    )

    small_font = pygame.font.SysFont(
        "arial", 24, bold=True
    )

    big_font = pygame.font.SysFont(
        "arial", 60, bold=True
    )

    title_font = pygame.font.SysFont(
        "arial", 42, bold=True
    )

    intro_font = pygame.font.SysFont(
        "arial", 85, bold=True
    )

    version_font = pygame.font.SysFont(
        "arial", 18
    )

# ==========================================
# ЗАГРУЗКА КАРТИНОК
# ==========================================

def load_image(filename, size):
    path = os.path.join(BASE, filename)

    if not os.path.isfile(path):
        return None

    try:
        image = pygame.image.load(
            path
        ).convert_alpha()

        return pygame.transform.smoothscale(
            image,
            size
        )

    except (pygame.error, OSError) as error:
        print(
            "Ошибка картинки:",
            filename,
            error
        )

        return None


menu_bg = load_image(
    "fon.png",
    (WIDTH, HEIGHT)
)

bottle_img = load_image(
    "bottle.png",
    (40, 75)
)

level_backgrounds = {}

for number in range(1, 21):
    level_backgrounds[number] = load_image(
        f"level{number}.png",
        (WIDTH, HEIGHT)
    )

# ==========================================
# ТЕКСТ И КНОПКИ
# ==========================================

def draw_text(text, used_font, color, center):
    image = used_font.render(
        str(text),
        True,
        color
    )

    screen.blit(
        image,
        image.get_rect(center=center)
    )


def draw_button(rect, label, color=GREEN):
    pygame.draw.rect(
        screen,
        color,
        rect,
        border_radius=12
    )

    pygame.draw.rect(
        screen,
        (100, 255, 110),
        rect,
        3,
        border_radius=12
    )

    draw_text(
        label,
        small_font,
        WHITE,
        rect.center
    )


def draw_arrows():
    pygame.draw.polygon(
        screen,
        WHITE,
        [
            (275, 255),
            (325, 215),
            (325, 295)
        ]
    )

    pygame.draw.polygon(
        screen,
        WHITE,
        [
            (625, 255),
            (575, 215),
            (575, 295)
        ]
    )


play_button = pygame.Rect(
    330, 170, 240, 75
)

skins_button = pygame.Rect(
    360, 260, 180, 50
)

music_button = pygame.Rect(
    370, 325, 160, 45
)

back_button = pygame.Rect(
    15, 15, 135, 50
)

left_button = pygame.Rect(
    260, 210, 90, 90
)

right_button = pygame.Rect(
    550, 210, 90, 90
)

buy_button = pygame.Rect(
    335, 405, 230, 55
)

music_toggle = pygame.Rect(
    335, 345, 230, 60
)

reset_button = pygame.Rect(
    765, 90, 120, 45
)


def draw_back():
    draw_button(
        back_button,
        "НАЗАД"
    )

# ==========================================
# МОБИЛЬНОЕ УПРАВЛЕНИЕ
# ==========================================

# СЛЕВА:
# ВЛЕВО и ВПРАВО рядом друг с другом.
#
# СПРАВА:
# ВВЕРХ и ВНИЗ рядом друг с другом.

control_rects = {
    "left": pygame.Rect(
        20, 410, 85, 70
    ),

    "right": pygame.Rect(
        115, 410, 85, 70
    ),

    "up": pygame.Rect(
        700, 410, 85, 70
    ),

    "down": pygame.Rect(
        795, 410, 85, 70
    )
}

# Здесь хранятся удерживаемые кнопки.
# Каждый палец работает отдельно.
held_controls = {}


def control_at(pos):
    for name, rect in control_rects.items():
        if rect.collidepoint(pos):
            return name

    return None


def held(name):
    return name in held_controls.values()


def clear_controls():
    held_controls.clear()


def draw_control(rect, name):
    button_surface = pygame.Surface(
        rect.size,
        pygame.SRCALPHA
    )

    if held(name):
        color = (30, 180, 75, 220)
    else:
        color = (12, 85, 155, 205)

    pygame.draw.rect(
        button_surface,
        color,
        button_surface.get_rect(),
        border_radius=13
    )

    pygame.draw.rect(
        button_surface,
        (255, 255, 255, 230),
        button_surface.get_rect(),
        3,
        border_radius=13
    )

    screen.blit(
        button_surface,
        rect.topleft
    )

    cx, cy = rect.center

    if name == "left":
        points = [
            (cx - 18, cy),
            (cx + 12, cy - 17),
            (cx + 12, cy + 17)
        ]

    elif name == "right":
        points = [
            (cx + 18, cy),
            (cx - 12, cy - 17),
            (cx - 12, cy + 17)
        ]

    elif name == "up":
        points = [
            (cx, cy - 18),
            (cx - 17, cy + 12),
            (cx + 17, cy + 12)
        ]

    else:
        points = [
            (cx, cy + 18),
            (cx - 17, cy - 12),
            (cx + 17, cy - 12)
        ]

    pygame.draw.polygon(
        screen,
        WHITE,
        points
    )


def draw_mobile_controls():
    for name, rect in control_rects.items():
        draw_control(rect, name)

# ==========================================
# ЗВУКИ И МУЗЫКА
# ==========================================

def load_sound(filename):
    if not pygame.mixer.get_init():
        return None

    path = os.path.join(
        BASE,
        filename
    )

    if not os.path.isfile(path):
        return None

    try:
        return pygame.mixer.Sound(path)

    except (pygame.error, OSError) as error:
        print(
            "Ошибка звука:",
            filename,
            error
        )

        return None


intro_sound = load_sound("intro.mp3")
win_sound = load_sound("win.mp3")

TRACKS = [
    ("Музыка 1", "music1.mp3"),
    ("Музыка 2", "music2.mp3"),
    ("Музыка 3", "music3.mp3")
]

music_index = 0
music_enabled = False


def stop_music():
    if pygame.mixer.get_init():
        pygame.mixer.music.stop()


def play_music():
    if not pygame.mixer.get_init():
        return

    filename = TRACKS[music_index][1]

    path = os.path.join(
        BASE,
        filename
    )

    if not os.path.isfile(path):
        print(
            "Нет музыкального файла:",
            filename
        )
        return

    try:
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(0.35)
        pygame.mixer.music.play(-1)

    except (pygame.error, OSError) as error:
        print(
            "Ошибка музыки:",
            error
        )

# ==========================================
# МАГАЗИН СКИНОВ
# ==========================================

SKINS = [
    {
        "name": "Обычный",
        "file": "player.png",
        "price": 0
    },
    {
        "name": "Красный",
        "file": "skin_red.png",
        "price": 20
    },
    {
        "name": "Зелёный",
        "file": "skin_green.png",
        "price": 40
    },
    {
        "name": "Испуганость",
        "file": "skin_scared.png",
        "price": 30
    },
    {
        "name": "Серьёзность",
        "file": "skin_serious.png",
        "price": 40
    },
    {
        "name": "Артур",
        "file": "skin_artur.png",
        "price": 60
    }
]


def make_placeholder(index):
    image = pygame.Surface(
        (75, 100),
        pygame.SRCALPHA
    )

    colors = [
        (255, 230, 70),
        (230, 50, 50),
        (40, 210, 60),
        (170, 100, 210),
        (90, 90, 90),
        (60, 110, 220)
    ]

    color = colors[index % len(colors)]

    pygame.draw.circle(
        image,
        (255, 220, 170),
        (37, 18),
        15
    )

    pygame.draw.rect(
        image,
        color,
        (18, 34, 38, 43)
    )

    pygame.draw.rect(
        image,
        BLACK,
        (18, 75, 15, 24)
    )

    pygame.draw.rect(
        image,
        BLACK,
        (41, 75, 15, 24)
    )

    pygame.draw.rect(
        image,
        color,
        (5, 38, 13, 33)
    )

    pygame.draw.rect(
        image,
        color,
        (57, 38, 13, 33)
    )

    return image


skin_images = []

for index, skin in enumerate(SKINS):
    image = load_image(
        skin["file"],
        (75, 100)
    )

    if image is None:
        image = make_placeholder(index)

    skin_images.append(image)


coins = 100
owned = [0]
selected_skin = 0
shop_index = 0


def save_data():
    data = {
        "coins": coins,
        "owned": owned,
        "selected": selected_skin
    }

    try:
        with open(
            SAVE_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=2
            )

    except OSError as error:
        print(
            "Ошибка сохранения:",
            error
        )


def load_save():
    global coins, owned, selected_skin

    if not os.path.isfile(SAVE_FILE):
        return

    try:
        with open(
            SAVE_FILE,
            "r",
            encoding="utf-8"
        ) as file:
            data = json.load(file)

        coins = max(
            0,
            int(data.get("coins", 100))
        )

        owned = [
            x
            for x in data.get("owned", [0])
            if type(x) is int
            and 0 <= x < len(SKINS)
        ]

        if 0 not in owned:
            owned.append(0)

        selected_skin = int(
            data.get("selected", 0)
        )

        if selected_skin not in owned:
            selected_skin = 0

    except (
        OSError,
        ValueError,
        TypeError,
        KeyError,
        json.JSONDecodeError
    ) as error:
        print(
            "Ошибка сохранения:",
            error
        )


def reset_shop():
    global coins, owned
    global selected_skin, shop_index

    coins = 0
    owned = [0]
    selected_skin = 0
    shop_index = 0

    save_data()


load_save()

# ==========================================
# УРОВНИ
# ==========================================

LEVELS = {
    1: {
        "boxes": [
            pygame.Rect(0, 340, 145, 160),
            pygame.Rect(165, 340, 180, 160),
            pygame.Rect(420, 340, 190, 160),
            pygame.Rect(740, 330, 160, 170),
            pygame.Rect(423, 0, 174, 174)
        ],
        "anchor": (350, 15),
        "length": 120,
        "bottle": (810, 255)
    },

    2: {
        "boxes": [
            pygame.Rect(0, 0, 260, 103),
            pygame.Rect(366, 0, 193, 160),
            pygame.Rect(775, 0, 125, 63),
            pygame.Rect(740, 224, 160, 170),
            pygame.Rect(373, 360, 173, 140)
        ],
        "anchor": (130, 30),
        "length": 135,
        "bottle": (810, 149)
    },

    3: {
        "boxes": [
            pygame.Rect(0, 0, 230, 108),
            pygame.Rect(440, 0, 270, 132),
            pygame.Rect(112, 345, 788, 155)
        ],
        "anchor": (95, 30),
        "length": 125,
        "bottle": (850, 270)
    },

    4: {
        "boxes": [
            pygame.Rect(0, 0, 310, 140),
            pygame.Rect(685, 0, 215, 145),
            pygame.Rect(320, 405, 165, 95),
            pygame.Rect(485, 365, 220, 135),
            pygame.Rect(710, 405, 170, 95)
        ],
        "anchor": (390, 35),
        "length": 315,
        "bottle": (735, 245)
    }
}

# Временные уровни до v1.2
for number in range(5, 21):
    LEVELS[number] = {
        "boxes": [
            pygame.Rect(0, 0, 220, 100),
            pygame.Rect(340, 0, 180, 130),
            pygame.Rect(650, 0, 180, 105),
            pygame.Rect(150, 365, 180, 135),
            pygame.Rect(440, 340, 180, 160),
            pygame.Rect(735, 350, 165, 150)
        ],
        "anchor": (100, 25),
        "length": 140,
        "bottle": (825, 275)
    }


def get_level_reward(number):
    return min(number * 10, 40)


level_number = 1
current_level = 1

anchor_x = 350.0
anchor_y = 15.0

rope_length = 120.0

angle = 0.0
angular_speed = 0.0

bottle_collected = False
win_time = 0
earned_reward = 0


def get_boxes():
    return LEVELS[current_level]["boxes"]


def get_player_position():
    x = anchor_x + math.sin(angle) * rope_length
    y = anchor_y + math.cos(angle) * rope_length

    return x, y


def get_player_rect():
    x, y = get_player_position()

    return skin_images[selected_skin].get_rect(
        center=(
            round(x),
            round(y)
        )
    )


def get_bottle_rect():
    x, y = LEVELS[current_level]["bottle"]

    return pygame.Rect(
        x, y, 40, 75
    )


def reset_level(number):
    global current_level
    global anchor_x, anchor_y
    global rope_length, angle
    global angular_speed
    global bottle_collected
    global earned_reward

    clear_controls()

    current_level = number

    info = LEVELS[number]

    anchor_x, anchor_y = info["anchor"]
    rope_length = float(info["length"])

    angle = 0.0
    angular_speed = 0.0

    bottle_collected = False
    earned_reward = 0


def hits_box():
    player_rect = get_player_rect().inflate(
        -24, -12
    )

    return any(
        player_rect.colliderect(box)
        for box in get_boxes()
    )


def attach_rope(pos):
    global anchor_x, anchor_y
    global rope_length, angle
    global angular_speed

    # Верёвка цепляется только за коробки.
    if not any(
        box.collidepoint(pos)
        for box in get_boxes()
    ):
        return

    px, py = get_player_position()

    dx = px - pos[0]
    dy = py - pos[1]

    distance = math.hypot(dx, dy)

    if distance < 10:
        return

    anchor_x = float(pos[0])
    anchor_y = float(pos[1])

    rope_length = distance
    angle = math.atan2(dx, dy)
    angular_speed = 0.0


def complete_level():
    global bottle_collected
    global earned_reward, coins
    global win_time, scene

    if bottle_collected:
        return

    bottle_collected = True

    clear_controls()

    earned_reward = get_level_reward(
        current_level
    )

    coins += earned_reward

    save_data()

    if win_sound:
        win_sound.play()

    win_time = pygame.time.get_ticks()
    scene = "win"

def update_level(dt):
    global angle, angular_speed
    global rope_length

    keys = pygame.key.get_pressed()

    old_angle = angle
    old_length = rope_length

    # Скорость относительно 60 FPS
    step = min(dt * 60, 3)

    # Раскачивание влево
    if keys[pygame.K_a] or held("left"):
        angular_speed -= 0.003 * step

    # Раскачивание вправо
    if keys[pygame.K_d] or held("right"):
        angular_speed += 0.003 * step

    # Укоротить верёвку
    if keys[pygame.K_w] or held("up"):
        rope_length -= 3 * step

    # Удлинить верёвку
    if keys[pygame.K_s] or held("down"):
        rope_length += 3 * step

    rope_length = max(40, min(800, rope_length))

    # Гравитация
    angular_speed -= 0.003 * math.sin(angle) * step

    # Трение
    angular_speed *= 0.995 ** step

    # Ограничение скорости
    angular_speed = max(-0.06, min(0.06, angular_speed))

    # Обновление положения
    angle += angular_speed * step

    # Столкновение с коробками
    if hits_box():
        angle = old_angle
        rope_length = old_length
        angular_speed = -angular_speed * 0.3

    # Проверка бутылки
    if get_player_rect().colliderect(get_bottle_rect()):
        complete_level()

# ==========================================
# ЗАСТАВКА
# ==========================================

INTRO_DURATION = 9000

intro_start = pygame.time.get_ticks()
intro_played = False


def draw_intro():
    screen.fill(BLACK)

    draw_text(
        "ЗНАТЬ",
        intro_font,
        RED,
        (450, 170)
    )

    draw_text(
        "данная игра не хочет никого",
        small_font,
        WHITE,
        (450, 285)
    )

    draw_text(
        "оскорбить или унизить",
        small_font,
        WHITE,
        (450, 325)
    )

    draw_text(
        "спасибо за внимание",
        small_font,
        WHITE,
        (450, 365)
    )

# ==========================================
# ГЛАВНОЕ МЕНЮ
# ==========================================

def draw_menu():
    if menu_bg:
        screen.blit(
            menu_bg,
            (0, 0)
        )
    else:
        screen.fill(BLUE)

    draw_text(
        "СИМУЛЯТОР ЧЕКУШКИ",
        title_font,
        WHITE,
        (450, 115)
    )

    draw_button(
        play_button,
        "ИГРАТЬ"
    )

    draw_button(
        skins_button,
        "СКИНЫ"
    )

    draw_button(
        music_button,
        "МУЗЫКА"
    )

    draw_back()

    draw_text(
        "-v.1.0",
        version_font,
        WHITE,
        (450, 480)
    )

# ==========================================
# ВЫБОР УРОВНЯ
# ==========================================

def draw_levels():
    screen.fill(BLUE)

    draw_back()

    draw_text(
        "ВЫБОР УРОВНЯ",
        title_font,
        WHITE,
        (450, 85)
    )

    pygame.draw.circle(
        screen,
        GREEN,
        (450, 255),
        75
    )

    pygame.draw.circle(
        screen,
        DARK_GREEN,
        (450, 255),
        75,
        5
    )

    draw_text(
        str(level_number),
        big_font,
        WHITE,
        (450, 255)
    )

    draw_arrows()

    draw_text(
        f"Награда: {get_level_reward(level_number)} монет",
        small_font,
        YELLOW,
        (450, 380)
    )

# ==========================================
# МАГАЗИН СКИНОВ
# ==========================================

def draw_shop():
    screen.fill(BLUE)

    draw_back()

    draw_text(
        "МАГАЗИН СКИНОВ",
        title_font,
        WHITE,
        (450, 65)
    )

    draw_text(
        f"Монеты: {coins}",
        small_font,
        YELLOW,
        (760, 45)
    )

    draw_button(
        reset_button,
        "СБРОС"
    )

    skin = SKINS[shop_index]

    draw_text(
        skin["name"],
        font,
        WHITE,
        (450, 125)
    )

    preview = pygame.transform.smoothscale(
        skin_images[shop_index],
        (115, 155)
    )

    screen.blit(
        preview,
        preview.get_rect(
            center=(450, 250)
        )
    )

    draw_arrows()

    if shop_index == selected_skin:
        status = "ВЫБРАН"
        button_text = "ВЫБРАН"

    elif shop_index in owned:
        status = "УЖЕ КУПЛЕН"
        button_text = "ВЫБРАТЬ"

    else:
        status = (
            f"Цена: {skin['price']} монет"
        )

        button_text = "КУПИТЬ"

    draw_text(
        status,
        small_font,
        YELLOW,
        (450, 370)
    )

    draw_button(
        buy_button,
        button_text
    )

# ==========================================
# МУЗЫКА
# ==========================================

def draw_music_menu():
    screen.fill(BLUE)

    draw_back()

    draw_text(
        "ВЫБОР МУЗЫКИ",
        title_font,
        WHITE,
        (450, 90)
    )

    draw_text(
        TRACKS[music_index][0],
        font,
        WHITE,
        (450, 255)
    )

    draw_arrows()

    if music_enabled:
        label = "ВЫКЛЮЧИТЬ"
    else:
        label = "ВКЛЮЧИТЬ"

    draw_button(
        music_toggle,
        label
    )

# ==========================================
# ОТРИСОВКА УРОВНЯ
# ==========================================

def draw_level():
    background = level_backgrounds[
        current_level
    ]

    if background:
        screen.blit(
            background,
            (0, 0)
        )

    else:
        screen.fill(
            (85, 175, 245)
        )

        for box in get_boxes():
            pygame.draw.rect(
                screen,
                BROWN,
                box
            )

            pygame.draw.rect(
                screen,
                BLACK,
                box,
                3
            )

    px, py = get_player_position()

    pygame.draw.line(
        screen,
        BLACK,
        (
            int(anchor_x),
            int(anchor_y)
        ),
        (
            int(px),
            int(py - 30)
        ),
        3
    )

    pygame.draw.circle(
        screen,
        BLACK,
        (
            int(anchor_x),
            int(anchor_y)
        ),
        6
    )

    screen.blit(
        skin_images[selected_skin],
        get_player_rect()
    )

    if not bottle_collected:
        bottle_rect = get_bottle_rect()

        if bottle_img:
            screen.blit(
                bottle_img,
                bottle_rect
            )

        else:
            pygame.draw.rect(
                screen,
                GREEN,
                bottle_rect,
                border_radius=8
            )

            pygame.draw.rect(
                screen,
                WHITE,
                (
                    bottle_rect.x + 12,
                    bottle_rect.y - 8,
                    16,
                    12
                )
            )

    draw_back()

    draw_text(
        f"Уровень {current_level}",
        small_font,
        WHITE,
        (760, 35)
    )

    # КНОПКИ ДЛЯ ТЕЛЕФОНА
    draw_mobile_controls()


def draw_win():
    draw_level()

    overlay = pygame.Surface(
        (WIDTH, HEIGHT),
        pygame.SRCALPHA
    )

    overlay.fill(
        (0, 0, 0, 185)
    )

    screen.blit(
        overlay,
        (0, 0)
    )

    draw_text(
        "УРОВЕНЬ ПРОЙДЕН!",
        title_font,
        WHITE,
        (450, 180)
    )

    draw_text(
        f"+{earned_reward} МОНЕТ",
        big_font,
        YELLOW,
        (450, 255)
    )

    draw_text(
        f"Всего монет: {coins}",
        small_font,
        WHITE,
        (450, 330)
    )

# ==========================================
# ЗАТЕМНЕНИЕ КРАЁВ
# ==========================================

vignette = pygame.Surface(
    (WIDTH, HEIGHT),
    pygame.SRCALPHA
)

for i in range(45):
    pygame.draw.rect(
        vignette,
        (0, 0, 0, 4),
        (
            i,
            i,
            WIDTH - i * 2,
            HEIGHT - i * 2
        ),
        2
    )

# ==========================================
# ПЕРЕХОДЫ МЕЖДУ ЭКРАНАМИ
# ==========================================

scene = "intro"

fade_from = "menu"
fade_to = "levels"

fade_alpha = 0
fade_phase = "out"


def start_fade(source, target):
    global scene
    global fade_from, fade_to
    global fade_alpha, fade_phase

    clear_controls()

    fade_from = source
    fade_to = target

    fade_alpha = 0
    fade_phase = "out"

    scene = "fade"


def draw_scene(name):
    if name == "intro":
        draw_intro()

    elif name == "menu":
        draw_menu()

    elif name == "levels":
        draw_levels()

    elif name == "shop":
        draw_shop()

    elif name == "music":
        draw_music_menu()

    elif name == "level":
        draw_level()

    elif name == "win":
        draw_win()


def draw_fade(dt):
    global fade_alpha
    global fade_phase, scene

    # Полное затемнение за 0.35 секунды
    fade_speed = 255 / 0.35

    if fade_phase == "out":
        draw_scene(fade_from)

        fade_alpha = min(
            255,
            fade_alpha + fade_speed * dt
        )

        if fade_alpha >= 255:
            fade_alpha = 255
            fade_phase = "in"

    else:
        draw_scene(fade_to)

        fade_alpha = max(
            0,
            fade_alpha - fade_speed * dt
        )

        if fade_alpha <= 0:
            fade_alpha = 0
            scene = fade_to

    overlay = pygame.Surface(
        (WIDTH, HEIGHT),
        pygame.SRCALPHA
    )

    overlay.fill((0, 0, 0, int(fade_alpha)))
    screen.blit(overlay, (0, 0))

# ==========================================
# КНОПКА НАЗАД
# ==========================================

running = True


def go_back():
    global running

    if scene == "menu":
        running = False

    elif scene == "level":
        start_fade(
            "level",
            "levels"
        )

    elif scene == "win":
        start_fade(
            "win",
            "levels"
        )

    elif scene == "levels":
        start_fade(
            "levels",
            "menu"
        )

    elif scene in ("shop", "music"):
        start_fade(
            scene,
            "menu"
        )

# ==========================================
# ОБРАБОТКА НАЖАТИЙ
# ==========================================

def handle_tap(pos):
    global running
    global level_number
    global shop_index
    global selected_skin
    global coins
    global music_index
    global music_enabled

    if not in_game(pos):
        return

    # НАЗАД
    if (
        scene in (
            "menu",
            "levels",
            "shop",
            "music",
            "level"
        )
        and back_button.collidepoint(pos)
    ):
        go_back()
        return

    # ГЛАВНОЕ МЕНЮ
    if scene == "menu":

        if play_button.collidepoint(pos):
            start_fade(
                "menu",
                "levels"
            )

        elif skins_button.collidepoint(pos):
            start_fade(
                "menu",
                "shop"
            )

        elif music_button.collidepoint(pos):
            start_fade(
                "menu",
                "music"
            )

    # ВЫБОР УРОВНЯ
    elif scene == "levels":

        if left_button.collidepoint(pos):
            level_number = max(
                1,
                level_number - 1
            )

        elif right_button.collidepoint(pos):
            level_number = min(
                20,
                level_number + 1
            )

        elif math.hypot(
            pos[0] - 450,
            pos[1] - 255
        ) <= 75:

            reset_level(level_number)

            start_fade(
                "levels",
                "level"
            )

    # МАГАЗИН
    elif scene == "shop":

        if reset_button.collidepoint(pos):
            reset_shop()

        elif left_button.collidepoint(pos):
            shop_index = (
                shop_index - 1
            ) % len(SKINS)

        elif right_button.collidepoint(pos):
            shop_index = (
                shop_index + 1
            ) % len(SKINS)

        elif buy_button.collidepoint(pos):

            if shop_index in owned:
                selected_skin = shop_index
                save_data()

            else:
                price = SKINS[
                    shop_index
                ]["price"]

                if coins >= price:
                    coins -= price
                    owned.append(
                        shop_index
                    )

                    selected_skin = shop_index
                    save_data()

    # МУЗЫКА
    elif scene == "music":

        if left_button.collidepoint(pos):
            music_index = (
                music_index - 1
            ) % len(TRACKS)

            if music_enabled:
                stop_music()
                play_music()

        elif right_button.collidepoint(pos):
            music_index = (
                music_index + 1
            ) % len(TRACKS)

            if music_enabled:
                stop_music()
                play_music()

        elif music_toggle.collidepoint(pos):
            music_enabled = not music_enabled

            if music_enabled:
                play_music()
            else:
                stop_music()

    # УРОВЕНЬ
    elif scene == "level":

        if control_at(pos) is None:
            attach_rope(pos)

# ==========================================
# ГЛАВНЫЙ ЦИКЛ
# ==========================================

while running:
    dt = clock.tick(FPS) / 1000.0

    # Звук заставки один раз.
    if scene == "intro" and not intro_played:
        intro_played = True

        if intro_sound:
            intro_sound.play()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # КЛАВИАТУРА
        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_F11:
                toggle_fullscreen()

            elif event.key in (
                pygame.K_ESCAPE,
                getattr(pygame, "K_AC_BACK", -999)
            ):
                go_back()

        # МЫШЬ: НАЖАТИЕ
        elif (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
        ):

            # Некоторые Android-сборки создают
            # событие мыши при касании пальцем.
            # Игнорируем повторное событие.
            if getattr(event, "touch", False):
                continue

            pos = to_game(event.pos)

            control = None

            if scene == "level" and in_game(pos):
                control = control_at(pos)

            if control:
                held_controls["mouse"] = control
            else:
                handle_tap(pos)

        # МЫШЬ: ОТПУСКАНИЕ
        elif (
            event.type == pygame.MOUSEBUTTONUP
            and event.button == 1
        ):
            if not getattr(event, "touch", False):
                held_controls.pop(
                    "mouse",
                    None
                )

        # МЫШЬ: ПЕРЕМЕЩЕНИЕ
        elif event.type == pygame.MOUSEMOTION:

            if "mouse" in held_controls:
                held_controls.pop(
                    "mouse",
                    None
                )

                pos = to_game(event.pos)

                if scene == "level" and in_game(pos):
                    control = control_at(pos)

                    if control:
                        held_controls["mouse"] = control

        # ПАЛЕЦ: НАЖАТИЕ
        elif event.type == pygame.FINGERDOWN:

            pos = finger_to_game(event)

            control = None

            if scene == "level" and in_game(pos):
                control = control_at(pos)

            if control:
                held_controls[
                    event.finger_id
                ] = control

            else:
                handle_tap(pos)

        # ПАЛЕЦ: ПЕРЕМЕЩЕНИЕ
        elif event.type == pygame.FINGERMOTION:

            finger_id = event.finger_id

            if finger_id in held_controls:
                pos = finger_to_game(event)

                control = None

                if scene == "level" and in_game(pos):
                    control = control_at(pos)

                if control:
                    held_controls[finger_id] = control
                else:
                    held_controls.pop(
                        finger_id,
                        None
                    )

        # ПАЛЕЦ: ОТПУСКАНИЕ
        elif event.type == pygame.FINGERUP:

            held_controls.pop(
                event.finger_id,
                None
            )

        # ПОТЕРЯ ФОКУСА
        elif event.type == pygame.WINDOWFOCUSLOST:
            clear_controls()

    # ======================================
    # ОБНОВЛЕНИЕ
    # ======================================

    if (
        scene == "intro"
        and pygame.time.get_ticks() - intro_start
        >= INTRO_DURATION
    ):
        if intro_sound:
            intro_sound.stop()

        scene = "menu"

    if scene == "level":
        update_level(dt)

    if scene == "win":
        if (
            pygame.time.get_ticks() - win_time
            >= 1500
        ):
            start_fade(
                "win",
                "levels"
            )

    # ======================================
    # ОТРИСОВКА
    # ======================================

    if scene == "fade":
        draw_fade(dt)
    else:
        draw_scene(scene)

    if scene != "intro":
        screen.blit(
            vignette,
            (0, 0)
        )

    present()

# ==========================================
# ВЫХОД
# ==========================================

save_data()
stop_music()

pygame.quit()
sys.exit()
