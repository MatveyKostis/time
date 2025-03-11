import random
from datetime import datetime, timedelta

from browser import document, window
import browser
from brython_colection import localstorage, html, timers, bind


class Save_Control:
    def __init__(self):
        localstorage.set_storage("KomaruTimeGame")

    def load_save(self):
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


save_control = Save_Control()
save_control.load_save()
is_full_screen = False
party_mode_running = False
party_id = None
time_komaru = 1
is_speedrun_enabled = False

buffer = ""
interval_timer = None
# Получение элементов интерфейса
useless_button = html.getElement('.useless_button')
clock_element = html.getElement('.clock')
money_element = html.getElement('.money_show')
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
        self.last_add_money = datetime.now()
        self.money = localstorage.get_int("money")
        self.last_login_time = localstorage.get_or_create("last_login_time", datetime.now().isoformat())
        self.calculate_offline_earnings()

    def save_money(self):
        localstorage.set("money", self.money)
        localstorage.set("last_login_time", datetime.now().isoformat())

    def return_money(self):
        return self.money

    def add_money(self):
        self.money += self.amount
        self.last_add_money = datetime.now()
        self.save_money()

    def calculate_offline_earnings(self):
        try:
            # Convert stored ISO format string back to datetime
            last_login = datetime.fromisoformat(self.last_login_time)
            current_time = datetime.now()

            # Calculate time difference in seconds
            time_diff = (current_time - last_login).total_seconds()

            # Calculate earnings (at 50% efficiency of online earnings)
            offline_rate = 0.5  # 50% efficiency rate
            offline_earnings = int(time_diff * self.amount * offline_rate)

            # Cap the maximum offline earnings (e.g., 24 hours worth)
            max_offline_seconds = 24 * 60 * 60  # 24 hours in seconds
            max_earnings = int(max_offline_seconds * self.amount * offline_rate)

            if offline_earnings > max_earnings:
                offline_earnings = max_earnings

            # Add the offline earnings to the current money
            if offline_earnings > 0:
                self.money += offline_earnings
                self.save_money()
        except Exception as e:
            print(f"Error calculating offline earnings: {e}")


    def show_on_text_money(self):
        if money_element:
            html.setText('.money_show', f'TimeCoins: {self.return_money()}')

money = Money()
@timers.set_interval_decorator("seconds", 1)
def do_operation_with_money():
    money.add_money()
    money.show_on_text_money()
    money.save_money()


def delete_cheat_activated():
    for element in document.getElementsByClassName("cheat-alert"):
        element.remove()

@bind.keyboard_reaction()
def key_buffer(key):
    global buffer
    print(key, buffer)
    buffer += key
    buffer = buffer[-10:]

    if "hesoyam" in buffer.lower():
        html.createElement("DIV", "CHEAT ACTIVATED", class_ok="cheat-alert")
        money.money += 250000
        timers.set_timeout_seconds(delete_cheat_activated, 3)
        buffer = ""

@bind.bind(".DVD_spawn", "click")
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
    if localstorage.get_int("ralsei_amount") == 1:
        if randomed_number <= 10:
            logo_element.style.backgroundImage = "url('images/ralseiphoto.png')"
    elif localstorage.get_int("ralsei_amount") == 2:
        if randomed_number <= 20:
            logo_element.style.backgroundImage = "url('images/ralseiphoto.png')"
    elif localstorage.get_int("ralsei_amount") == 3:
        if randomed_number <= 30:
            logo_element.style.backgroundImage = "url('images/ralseiphoto.png')"
    elif localstorage.get_int("ralsei_amount") == 4:
        if randomed_number <= 40:
            logo_element.style.backgroundImage = "url('images/ralseiphoto.png')"
    elif localstorage.get_int("ralsei_amount") == 5:
        if randomed_number <= 50:
            logo_element.style.backgroundImage = "url('images/ralseiphoto.png')"

    if localstorage.get_int("ralsei_amount") >= 1:
        logo_element.style.backgroundSize = "100% 100%"
    else:
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

    timers.set_interval_seconds(move_logo, 0.01)  # Начинаем движение логотипа


def init():
    useless_button.style.left = f"{random.randint(0, window.innerWidth - 100)}px"
    useless_button.style.top = f"{random.randint(0, window.innerHeight - 50)}px"
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


def update_time_speedrun():
    milliseconds = datetime.now().strftime('%f')
    milliseconds = int(milliseconds) // 1000
    html.setText('.clock', datetime.now().strftime(f"%H:%M:%S:{milliseconds}"))


@timers.set_interval_decorator("seconds", 0.4)
def update_time():
    global is_speedrun_enabled

    if not is_speedrun_enabled:
        html.setText('.clock', datetime.now().strftime("%H:%M:%S"))
        clock_element.style.background = "linear-gradient(145deg, #2a2a2a, #333333)"

@bind.bind(".speedrun_mode", "click")
def enable_speed_run(event):
    global is_speedrun_enabled, interval_timer

    # Проверяем, куплен ли speedrun режим
    if not localstorage.get_bool("speedrun_bought"):
        print(html.getHTML(".speedrun_mode"))
        html.setHTML(".speedrun_mode", '<img src="images/background.png" alt="Speedrun"> You need to buy speedrun mode!')
        timers.set_timeout_seconds(init, 1)
        return

    is_speedrun_enabled = not is_speedrun_enabled

    if is_speedrun_enabled:
        clock_element.style.background = "green"
        interval_timer = timers.set_interval_seconds(update_time_speedrun, 0.02)
    else:
        clock_element.style.background = "linear-gradient(145deg, #2a2a2a, #333333)"
        timers.clear_interval(interval_timer)


def party_mode_run_with_setinterval():
    global party_mode_running
    color = random.choice(colors)
    document.body.style.background = color

@bind.bind('.party_lol', 'click')
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

@bind.bind('.useless_button', 'click')
def useless_button_func(event):
    useless_button.style.left = f"{random.randint(0, window.innerWidth - 100)}px"
    useless_button.style.top = f"{random.randint(0, window.innerHeight - 50)}px"

@bind.bind('.clock', 'click')
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
