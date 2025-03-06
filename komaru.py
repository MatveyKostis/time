from browser import document, window, html
from datetime import datetime
import random

is_full_screen = False
party_mode_running = False
party_id = None
is_warned = False
clock_element = document.querySelector('.clock')
speedrun_button = document.querySelector('.speedrun_mode')
party_button = document.querySelector('.party_toggler')
dvd_spawn_button = document.querySelector('.DVD_spawn')  # Кнопка для спавна логотипа
is_speedrun_enabled = False
colors = [
    "black", "white", "red", "green", "blue", "yellow", "cyan", "magenta",
    "gray", "silver", "maroon", "olive", "lime", "aqua", "fuchsia", "purple"
]

# Функции для создания и движения логотипа
def spawn_logo(event):
    # Создаем новый элемент логотипа
    logo_element = html.DIV()
    logo_element.style.position = "absolute"
    logo_element.style.width = "100px"
    logo_element.style.height = "50px"
    logo_element.style.backgroundImage = "url('images/DVD.png')"  # Устанавливаем изображение логотипа
    logo_element.style.backgroundSize = "contain"
    logo_element.style.backgroundRepeat = "no-repeat"
    document.body.appendChild(logo_element)

    # Переменные для движения логотипа
    logo_speed_x = random.randint(1, 5)  # Скорость по оси X
    logo_speed_y = random.randint(1, 5)  # Скорость по оси Y
    logo_pos_x = random.randint(0, window.innerWidth - 100)  # Начальная позиция по оси X
    logo_pos_y = random.randint(0, window.innerHeight - 50)  # Начальная позиция по оси Y

    def move_logo():
        nonlocal logo_pos_x, logo_pos_y, logo_speed_x, logo_speed_y

        # Получаем размеры экрана
        window_width = window.innerWidth
        window_height = window.innerHeight

        # Обновляем позицию логотипа
        logo_pos_x += logo_speed_x
        logo_pos_y += logo_speed_y

        # Проверяем, не выходит ли логотип за пределы экрана
        if logo_pos_x <= 0 or logo_pos_x + 100 >= window_width:  # 100px ширина логотипа
            logo_speed_x = -logo_speed_x  # Меняем направление по оси X
            logo_element.style.backgroundColor = random.choice(colors)  # Сменить цвет

        if logo_pos_y <= 0 or logo_pos_y + 50 >= window_height:  # 50px высота логотипа
            logo_speed_y = -logo_speed_y  # Меняем направление по оси Y
            logo_element.style.backgroundColor = random.choice(colors)  # Сменить цвет

        # Обновляем стиль для перемещения
        logo_element.style.left = f"{logo_pos_x}px"
        logo_element.style.top = f"{logo_pos_y}px"

    window.setInterval(move_logo, 10)  # Начинаем движение логотипа

def init():
    clock_element.text = datetime.now().strftime("%H:%M:%S")

def update_time():
    if is_speedrun_enabled:
        clock_element.style.backgroundColor = "green"
        milliseconds = datetime.now().strftime('%f')
        milliseconds = int(milliseconds) // 1000
        clock_element.text = datetime.now().strftime(f"%H:%M:%S:{milliseconds}")
    else:
        clock_element.text = datetime.now().strftime("%H:%M:%S")
        clock_element.style.backgroundColor = "gray"

def enable_speed_run(event):
    global is_speedrun_enabled
    if is_speedrun_enabled:
        clock_element.style.backgroundColor = "green"
        is_speedrun_enabled = False
    else:
        clock_element.style.backgroundColor = "gray"
        is_speedrun_enabled = True

def party_mode_run_with_setinterval():
    global party_mode_running
    color = random.choice(colors)
    document.body.style.backgroundColor = color

def party_mode(event):
    global party_mode_running, party_id, is_warned
    if party_mode_running:
        window.clearInterval(party_id)
        party_id = None  # Reset party_id to None
        document.body.style.backgroundColor = "black"
   else:
        party_mode_running = False
        if party_id is None:  # Check if the interval is already running
            party_id = window.setInterval(party_mode_run_with_setinterval, 100)
        party_mode_running = True

def go_full_screen(event):
    global is_full_screen
    if is_full_screen:
        window.document.exitFullscreen()
        is_full_screen = False
    else:
        document.documentElement.requestFullscreen()
        is_full_screen = True

init()

dvd_spawn_button.bind("click", spawn_logo)
speedrun_button.bind("click", enable_speed_run)
clock_element.bind("click", go_full_screen)
party_button.bind("click", party_mode)

# Устанавливаем интервалы для обновления времени
window.setInterval(update_time, 10)
