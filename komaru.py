from browser import document, window, html, timer
from datetime import datetime, timedelta
import random
import time

is_full_screen = False
party_mode_running = False
party_id = None
clock_element = document.querySelector('.clock')
speedrun_button = document.querySelector('.speedrun_mode')
party_button = document.querySelector('.party_toggler')
shop_button = document.querySelector('.Shop_button')
speedrun_bought = window.localStorage.getItem("speedrun_bought")
if speedrun_bought is not bool:
    if type(speedrun_bought) == bool:
        speedrun_bought = False
else:
    speedrun_bought = bool(speedrun_bought)
window.localStorage["speedrun_bought"] = speedrun_bought
dvd_spawn_button = document.querySelector('.DVD_spawn')  # Кнопка для спавна логотипа
is_speedrun_enabled = False
colors = [
    "black", "white", "red", "green", "blue", "yellow", "cyan", "magenta",
    "gray", "silver", "maroon", "olive", "lime", "aqua", "fuchsia", "purple"
]


class Money:
    def __init__(self):
        self.amount = 1
        self.last_clicked_time = datetime.now()
        stored_money_is_ok = window.localStorage.getItem("money")
        if stored_money_is_ok is not int:
            if type(stored_money_is_ok) == str:
                window.localStorage.setItem("money", int(stored_money_is_ok))
            else:
                window.localStorage.setItem("money", 0)
        stored_money = window.localStorage["money"]
        if stored_money is not int:
            if type(stored_money) == str:
                stored_money = int(stored_money)
            else:
                stored_money = 0
        else:
            stored_money = int(stored_money)
        self.money = stored_money

    def save_money(self):
        window.localStorage.setItem("money", str(self.money))

    def return_money(self):
        return self.money

    def add_money(self):
        if datetime.now() > self.last_clicked_time + timedelta(seconds=1):
            self.money += self.amount
            self.last_clicked_time = datetime.now()
            self.save_money()

    def show_on_text_money(self):
        money_element = document.querySelector('.money_show')
        if money_element:
            money_element.textContent = f'TimeCoins: {self.return_money()}'


money = Money()

class Buy_items:
    def __init__(self):
        self.items = [
            ".DVD_spawn",
            ".speedrun_mode",
            ".party_toggler"
        ]
        self.item_prices = {
            ".DVD_spawn": 100,
            ".speedrun_mode": 2000,
            ".party_toggler": 100
        }

    def try_buy_item(self, item):
        if item in self.items:
            if money.money >= self.item_prices[item]:
                if item == ".DVD_spawn":
                    money.money -= self.item_prices[item]
                    self.item_prices[item] *= 2
                    return True
                elif item == ".speedrun_mode":
                    money.money -= self.item_prices[item]
                    return True
                elif item == ".party_toggler":
                    money.money -= self.item_prices[item]
                    self.item_prices[item] *= 2
                    return True
            else:
                return False

    def show_buy_money(self):
        pass

buy_item = Buy_items()


def spawn_logo(event):
    def doing_that_when_answer_false(text):
        # Восстановить текст кнопки и вернуть изображение
        dvd_spawn_button.innerHTML = f'<img src="images/DVD.png" alt="DVD" class="button_img"> DVD spawn {money.return_money()}$'

    # Попытка купить предмет
    answer_from_button = buy_item.try_buy_item(".DVD_spawn")

    # Если денег недостаточно
    if answer_from_button == False:
        # Сохраняем предыдущий текст кнопки
        previous_text = dvd_spawn_button.innerHTML
        dvd_spawn_button.innerHTML = "Not enough money!"  # Меняем текст на сообщение об ошибке

        # Возвращаем предыдущий контент через 500 миллисекунд
        timer.set_timeout(doing_that_when_answer_false, 5000, previous_text)
        return
    else:
        # Здесь код, если покупка успешна
        pass

    randomed_number = random.randint(0, 100)
    logo_element = html.DIV()
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
            money.money += money.amount # 100px ширина логотипа
            logo_speed_x = -logo_speed_x  # Меняем направление по оси X
            logo_element.style.backgroundColor = random.choice(colors)  # Сменить цвет

        if logo_pos_y <= 0 or logo_pos_y + 50 >= window_height:
            money.money += money.amount # 50px высота логотипа
            logo_speed_y = -logo_speed_y  # Меняем направление по оси Y
            logo_element.style.backgroundColor = random.choice(colors)  # Сменить цвет

        # Обновляем стиль для перемещения
        logo_element.style.left = f"{logo_pos_x}px"
        logo_element.style.top = f"{logo_pos_y}px"

    window.setInterval(move_logo, 10)  # Начинаем движение логотипа

def init():
    clock_element.text = datetime.now().strftime("%H:%M:%S")

def update_time():
    dvd_spawn_button.innerHTML = f'<img src="images/DVD.png" alt="DVD" class="button_img"> DVD spawn {buy_item.item_prices[".DVD_spawn"]}$'
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
    if speedrun_bought:
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
            party_id = window.setInterval(party_mode_run_with_setinterval, 1000)
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
