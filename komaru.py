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
dvd_spawn_button = document.querySelector('.DVD_spawn')
remove_dvd_button = document.querySelector('.remove_dvd')
is_speedrun_enabled = False
colors = [
    "black", "white", "red", "green", "blue", "yellow", "cyan", "magenta",
    "gray", "silver", "maroon", "olive", "lime", "aqua", "fuchsia", "purple"
]


class Money:
    def __init__(self):
        self.amount = 1
        self.last_clicked_time = datetime.now()
        self.money = int(window.localStorage.getItem("money")) if window.localStorage.getItem("money") else 0
        self.check_offline_earnings()

    def save_offline_time(self):
        window.localStorage.setItem("last_saved_time", str(window.Date.new().getTime()))

    def check_offline_earnings(self):
        last_saved = window.localStorage.getItem("last_saved_time")
        if last_saved:
            try:
                delta = (window.Date.new().getTime() - float(last_saved)) / 1000
                if delta > 5:
                    self.money += int(delta) * self.amount
                    self.save_money()
            except Exception as e:
                print("Offline error:", e)

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
            ".DVD_spawn": int(window.localStorage.getItem("DVD_price")) if window.localStorage.getItem(
                "DVD_price") else 100,
            ".speedrun_mode": 2000,
            ".party_toggler": int(window.localStorage.getItem("party_price")) if window.localStorage.getItem(
                "party_price") else 100
        }

    def try_buy_item(self, item):
        if item in self.items:
            if money.money >= self.item_prices[item]:
                money.money -= self.item_prices[item]
                if item == ".DVD_spawn":
                    self.item_prices[item] *= 2
                    window.localStorage.setItem("DVD_price", str(self.item_prices[item]))
                    return self.item_prices[item] // 2
                elif item == ".party_toggler":
                    self.item_prices[item] *= 2
                    window.localStorage.setItem("party_price", str(self.item_prices[item]))
                    return self.item_prices[item] // 2
                elif item == ".speedrun_mode":
                    return True
            else:
                return False


buy_item = Buy_items()


def spawn_logo(event):
    answer = buy_item.try_buy_item(".DVD_spawn")

    if answer is False:
        original = dvd_spawn_button.innerHTML
        dvd_spawn_button.innerHTML = "Not enough money!"
        timer.set_timeout(lambda: setattr(dvd_spawn_button, 'innerHTML', original), 1000)
        return

    logo_element = html.DIV(class_name="dvd-logo")
    logo_element.style.position = "absolute"
    logo_element.style.width = "100px"
    logo_element.style.height = "50px"

    if random.randint(0, 100) == 68:
        logo_element.style.backgroundImage = "url('images/komaru.png')"
    else:
        logo_element.style.backgroundImage = "url('images/DVD.png')"

    logo_element.style.backgroundSize = "contain"
    logo_element.style.backgroundRepeat = "no-repeat"
    document.body.appendChild(logo_element)

    logo_element.dataset.cost = answer
    logo_speed_x = random.randint(1, 5)
    logo_speed_y = random.randint(1, 5)
    logo_pos_x = random.randint(0, window.innerWidth - 100)
    logo_pos_y = random.randint(0, window.innerHeight - 50)

    def move_logo():
        nonlocal logo_pos_x, logo_pos_y, logo_speed_x, logo_speed_y
        logo_pos_x += logo_speed_x
        logo_pos_y += logo_speed_y

        if logo_pos_x <= 0 or logo_pos_x + 100 >= window.innerWidth:
            money.money += money.amount
            logo_speed_x = -logo_speed_x
            logo_element.style.backgroundColor = random.choice(colors)

        if logo_pos_y <= 0 or logo_pos_y + 50 >= window.innerHeight:
            money.money += money.amount
            logo_speed_y = -logo_speed_y
            logo_element.style.backgroundColor = random.choice(colors)

        logo_element.style.left = f"{logo_pos_x}px"
        logo_element.style.top = f"{logo_pos_y}px"

    timer.set_interval(move_logo, 10)


def remove_dvd(event):
    total = 0
    for logo in document.querySelectorAll(".dvd-logo"):
        try:
            total += int(logo.dataset.cost)
            logo.remove()
        except:
            continue

    if total > 0:
        money.money += total
        money.save_money()
        money.show_on_text_money()


def update_time():
    dvd_spawn_button.innerHTML = f'<img src="images/DVD.png" class="button_img"> DVD spawn {buy_item.item_prices[".DVD_spawn"]}$'
    if is_speedrun_enabled:
        clock_element.style.backgroundColor = "green"
        milliseconds = datetime.now().strftime('%f')[:-3]
        clock_element.text = datetime.now().strftime(f"%H:%M:%S:{milliseconds}")
    else:
        clock_element.text = datetime.now().strftime("%H:%M:%S")
        clock_element.style.backgroundColor = "gray"


def enable_speed_run(event):
    global is_speedrun_enabled
    if is_speedrun_enabled:
        is_speedrun_enabled = False
    else:
        is_speedrun_enabled = True
    update_time()


def party_mode_run():
    document.body.style.backgroundColor = random.choice(colors)


def party_mode(event):
    global party_mode_running, party_id
    if party_mode_running:
        window.clearInterval(party_id)
        party_mode_running = False
        document.body.style.backgroundColor = "black"
    else:
        party_id = window.setInterval(party_mode_run, 1000)
        party_mode_running = True


def go_full_screen(event):
    global is_full_screen
    if is_full_screen:
        window.document.exitFullscreen()
        is_full_screen = False
    else:
        document.documentElement.requestFullscreen()
        is_full_screen = True


def handle_beforeunload(event):
    money.save_offline_time()


# Инициализация
window.addEventListener("beforeunload", handle_beforeunload)
dvd_spawn_button.bind("click", spawn_logo)
speedrun_button.bind("click", enable_speed_run)
clock_element.bind("click", go_full_screen)
party_button.bind("click", party_mode)
remove_dvd_button.bind("click", remove_dvd)

# Интервалы обновления
timer.set_interval(update_time, 10)
timer.set_interval(money.show_on_text_money, 100)
timer.set_interval(money.save_money, 30000)
timer.set_interval(money.add_money, 1000)