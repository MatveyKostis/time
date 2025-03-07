import random
from datetime import datetime, timedelta

from browser import document, window, timer
import browser
from brython_colection import localstorage, html, timers

is_full_screen = False
party_mode_running = False
party_id = None
clock_element = html.getElement('.clock')
speedrun_button = html.getElement('.speedrun_mode')
party_button = html.getElement('.party_toggler')
shop_button = html.getElement('.Shop_button')
speedrun_bought = localstorage.getboolean("speedrun_bought")
localstorage.setItem("speedrun_bought", speedrun_bought)
dvd_spawn_button = html.getElement('.DVD_spawn')
is_speedrun_enabled = False
colors = [
    "black", "white", "red", "green", "blue", "yellow", "cyan", "magenta",
    "gray", "silver", "maroon", "olive", "lime", "aqua", "fuchsia", "purple"
]

class took_from_shop:
    def __init__(self):
        self.bought_dvd = localstorage.getboolean("bought_dvd")
        localstorage.setItem("bought_dvd", self.bought_dvd)
        self.amount = localstorage.getint("amount")
        print(self.amount)
        if self.amount is None:
            self.amount = 1
            localstorage.setItem("amount", self.amount)
        if self.amount < 0:
            self.amount = 1
            localstorage.setItem("amount", self.amount)
        self.amount = localstorage.getItem("amount")
        print(localstorage.getItem("party_speed"))
        if localstorage.getItem("party_speed") == "[object Object]":
            localstorage.setItem("party_speed", 1000)
        self.party_time = localstorage.getint("party_speed")
        localstorage.setItem("party_speed", self.party_time)
shop = took_from_shop()

class Money:
    def __init__(self):
        self.amount = shop.amount
        print(self.amount)
        self.amount = int(shop.amount)
        print(self.amount)
        self.last_clicked_time = datetime.now()
        stored_money = localstorage.getint("money")
        self.money = stored_money

    def save_money(self):
        localstorage.setItem("money", self.money)

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
            money_element.textContent = f'TimeCoins: {self.return_money()}'


money = Money()

def spawn_logo(event):
    if shop.bought_dvd:
        pass
    else:
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
    party_lol.innerHTML = f'Party time: {localstorage.getint("party_speed")}ms'
    if shop.bought_dvd:
        dvd_spawn_button.innerHTML = f'<img src="images/DVD.png" alt="DVD" class="button_img"> DVD spawn (BOUGHT)'
    else:
        dvd_spawn_button.innerHTML = f'<img src="images/DVD.png" alt="DVD" class="button_img"> DVD spawn (NOT BOUGHT)'
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
        party_mode_running = False  # Set to False after stopping
    else:
        if party_id is None:  # Check if the interval is already running
            party_id = window.setInterval(party_mode_run_with_setinterval, localstorage.getint("party_speed"))
            party_mode_running = True  # Set to True after starting


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
window.setInterval(money.show_on_text_money, 10)
window.setInterval(money.save_money, 10)
window.setInterval(money.add_money, 10)