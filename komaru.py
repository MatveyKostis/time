import random
from datetime import datetime, timedelta

from browser import document, window
import browser
from brython_colection import localstorage, html, timers

localstorage.set_storage("KomaruTimeGame")

# Инициализация настроек игры при первом запуске
localstorage.get_or_create("speedrun_bought", False)
localstorage.get_or_create("bought_dvd", False)
localstorage.get_or_create("amount", 1)
localstorage.get_or_create("party_speed", 1000)
localstorage.get_or_create("money", 0)
localstorage.get_or_create("party_time", 1000)
localstorage.get_or_create("bought_party_times", 0)
localstorage.get_or_create("bought_multiply_times", 0)
localstorage.get_or_create("price_of_party", 1000)
localstorage.get_or_create("price_of_multiply", 5000)

# Глобальные переменные состояния
is_full_screen = False
party_mode_running = False
party_id = None
is_speedrun_enabled = False

# Получение элементов интерфейса
clock_element = html.getElement('.clock')
speedrun_button = html.getElement('.speedrun_mode')
party_button = html.getElement('.party_toggler')
shop_button = html.getElement('.Shop_button')
dvd_spawn_button = html.getElement('.DVD_spawn')

# Список цветов для эффектов
colors = [
    "black", "white", "red", "green", "blue", "yellow", "cyan", "magenta",
    "gray", "silver", "maroon", "olive", "lime", "aqua", "fuchsia", "purple"
]


class ShopManager:
    def __init__(self):
        self.bought_dvd = localstorage.get_bool("bought_dvd")
        self.amount = localstorage.get_int("amount")
        self.party_time = localstorage.get_int("party_speed")

        # Проверка и корректировка значений
        if self.amount <= 0:
            self.amount = 1
            localstorage.set("amount", self.amount)

        # Проверка корректности party_speed
        if not isinstance(self.party_time, int) or self.party_time <= 0:
            self.party_time = 1000
            localstorage.set("party_speed", self.party_time)


shop = ShopManager()


class Money:
    def __init__(self):
        self.amount = shop.amount
        self.last_clicked_time = datetime.now()
        self.money = localstorage.get_int("money")

    def save_money(self):
        localstorage.set("money", self.money)

    def return_money(self):
        return self.money

    def add_money(self):
        if datetime.now() > self.last_clicked_time + timedelta(seconds=1):
            self.money += self.amount
            self.last_clicked_time = datetime.now()
            self.save_money()

    def show_on_text_money(self):
        money_element = html.getElement('.money_show')
        if money_element:
            html.setText('.money_show', f'TimeCoins: {self.return_money()}')


money = Money()


def spawn_logo(event):
    if not localstorage.get_bool("bought_dvd"):
        return

    randomed_number = random.randint(0, 100)
    logo_element = browser.html.DIV()
    logo_element.style.position = "absolute"
    logo_element.style.width = "100px"
    logo_element.style.height = "50px"
    if randomed_number == 68:
        logo_element.style.backgroundImage = "url('images/komaru.png')"
    else:
        logo_element.style.backgroundImage = "url('images/DVD.png')"
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
        if logo_pos_x <= 0 or logo_pos_x + 100 >= window_width:
            logo_speed_x = -logo_speed_x  # Меняем направление по оси X
            logo_element.style.backgroundColor = random.choice(colors)  # Сменить цвет

        if logo_pos_y <= 0 or logo_pos_y + 50 >= window_height:
            logo_speed_y = -logo_speed_y  # Меняем направление по оси Y
            logo_element.style.backgroundColor = random.choice(colors)  # Сменить цвет

        # Обновляем стиль для перемещения
        logo_element.style.left = f"{logo_pos_x}px"
        logo_element.style.top = f"{logo_pos_y}px"

    window.setInterval(move_logo, 10)  # Начинаем движение логотипа


def init():
    party_lol = html.getElement('.party_lol')
    html.setHTML('.party_lol', f'Party time: {localstorage.get_int("party_speed")}ms')

    if localstorage.get_bool("bought_dvd"):
        html.setHTML('.DVD_spawn', '<img src="images/DVD.png" alt="DVD" class="button_img"> DVD spawn (BOUGHT)')
    else:
        html.setHTML('.DVD_spawn', '<img src="images/DVD.png" alt="DVD" class="button_img"> DVD spawn (NOT BOUGHT)')

    if localstorage.get_bool("speedrun_bought"):
        html.setHTML('.speedrun_mode', '<img src="images/background.png" alt="Speedrun"> Speedrun Mode (BOUGHT)')
    else:
        html.setHTML('.speedrun_mode', '<img src="images/background.png" alt="Speedrun"> Speedrun Mode (NOT BOUGHT)')

    html.setText('.clock', datetime.now().strftime("%H:%M:%S"))


def update_time():
    global is_speedrun_enabled

    if is_speedrun_enabled:
        clock_element.style.backgroundColor = "green"
        milliseconds = datetime.now().strftime('%f')
        milliseconds = int(milliseconds) // 1000
        html.setText('.clock', datetime.now().strftime(f"%H:%M:%S:{milliseconds}"))
    else:
        html.setText('.clock', datetime.now().strftime("%H:%M:%S"))
        clock_element.style.backgroundColor = "gray"


def enable_speed_run(event):
    global is_speedrun_enabled

    # Проверяем, куплен ли speedrun режим
    if not localstorage.get_bool("speedrun_bought"):
        print(html.getHTML(".speedrun_mode"))
        html.setHTML(".speedrun_mode", '<img src="images/background.png" alt="Speedrun"> You need to buy speedrun mode!')
        timers.set_timeout_seconds(init, 1)
        return

    is_speedrun_enabled = not is_speedrun_enabled

    if is_speedrun_enabled:
        clock_element.style.background = "green"
    else:
        clock_element.style.background = "linear-gradient(145deg, #2a2a2a, #333333)"


def party_mode_run_with_setinterval():
    global party_mode_running
    color = random.choice(colors)
    document.body.style.background = color


def party_mode(event):
    global party_mode_running, party_id

    if party_mode_running:
        window.clearInterval(party_id)
        party_id = None  # Reset party_id to None
        document.body.style.background = "linear-gradient(135deg, var(--primary-bg), var(--secondary-bg))"
        party_mode_running = False  # Set to False after stopping
    else:
        if party_id is None:  # Check if the interval is already running
            party_id = window.setInterval(party_mode_run_with_setinterval, localstorage.get_int("party_speed"))
            party_mode_running = True  # Set to True after starting


def go_full_screen(event):
    global is_full_screen
    if is_full_screen:
        window.document.exitFullscreen()
        is_full_screen = False
    else:
        document.documentElement.requestFullscreen()
        is_full_screen = True


# Инициализация
init()

# Привязка событий к элементам
dvd_spawn_button.bind("click", spawn_logo)
speedrun_button.bind("click", enable_speed_run)
clock_element.bind("click", go_full_screen)
party_button.bind("click", party_mode)

# Устанавливаем интервалы для обновления времени и деньг
timers.set_interval_seconds(update_time, 0.01)  # Эквивалент 10мс
timers.set_interval_seconds(money.show_on_text_money, 0.01)
timers.set_interval_seconds(money.save_money, 0.01)
timers.set_interval_seconds(money.add_money, 0.01)