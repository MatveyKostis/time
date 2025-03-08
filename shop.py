from browser import document, window
from brython_colection import localstorage, html, timers
from datetime import datetime, timedelta
import random
import time


class Money_shop():
    def __init__(self):
        # Инициализация с использованием localstorage.get* методов
        localstorage.set_storage("KomaruTimeGame")
        self.money = localstorage.get_or_create("money", 0)
        self.amount = localstorage.get_or_create("amount", 1)
        self.party_time = localstorage.get_or_create("party_time", 1000)

    def devide_party_time(self, times):
        self.party_time = int(self.party_time) // times
        print(self.party_time)
        localstorage.set("party_time", self.party_time)


class JSON_work():
    def __init__(self):
        json_data = {
            "bought_dvd": localstorage.get_bool("bought_dvd", False),
            "bought_party_times": localstorage.get_int("bought_party_times", 0),
            "bought_multiply_times": localstorage.get_int("bought_multiply_times", 0),
            "party_speed": localstorage.get_int("party_speed", 1000),
            "price_of_party": localstorage.get_int("price_of_party", 1000),
            "price_of_multiply": localstorage.get_int("price_of_multiply", 5000)
        }
        localstorage.set("game_data", json_data)

    def show_json(self):
        print(localstorage.get("game_data"))


# Инициализация localStorage для игры
localstorage.set_storage("KomaruTimeGame")

localstorage.get_or_create("bought_dvd", False)
localstorage.get_or_create("bought_party_times", 0)
localstorage.get_or_create("bought_multiply_times", 0)
localstorage.get_or_create("party_speed", 1000)
localstorage.get_or_create("price_of_party", 1000)
localstorage.get_or_create("price_of_multiply", 5000)
localstorage.get_or_create("money", 0)
localstorage.get_or_create("amount", 1)
localstorage.get_or_create("speedrun_bought", False)


# Инициализация JSON структуры
json_lol = JSON_work()
json_lol.show_json()

# Получение элементов интерфейса
buy_dvd_button = html.getElement('.buy_dvd')
buy_party_button = html.getElement('.buy_party')
buy_multiply = html.getElement('.buy_multiply')
buy_speedrun = html.getElement('.buy_speedrun')
bought_dvd_text = html.getElement(".bought_dvd_or_no")
bought_party_or_no = html.getElement('.bought_party_or_no')
bought_speedrun_text = html.getElement('.speedrun_bought')

# Получение состояния покупок
bought_dvd = localstorage.get_bool("bought_dvd")
bought_party_times = localstorage.get_int("bought_party_times")
bought_speedrun = localstorage.get_bool("speedrun_bought")

# Инициализация объекта магазина
money = Money_shop()


def init():
    # Обновление отображения состояния DVD
    print(f"DVD status: {bought_dvd}")
    if bought_dvd:
        html.setText(".bought_dvd_or_no", "Bought: Yes")
    else:
        html.setText(".bought_dvd_or_no", "Bought: No")

    # Обновление цен и отображения
    price_of_party = localstorage.get_int("price_of_party")
    html.setText(".price_of_party", f"Cost: {price_of_party} $")

    price_of_multiply = localstorage.get_int("price_of_multiply")
    html.setText(".price_of_multiply", f"Cost: {price_of_multiply} $")

    multiply_bought = localstorage.get_int("bought_multiply_times")
    html.setText(".multiply_bought", f"Bought: {multiply_bought} times")

    if localstorage.get_bool("speedrun_bought"):
        html.setText(".speedrun_bought", "Bought: Yes")
    else:
        html.setText(".speedrun_bought", "Bought: No")


    # Обновление отображения состояния Party
    party_times = localstorage.get_int("bought_party_times")
    print(f"Party times: {party_times}")

    if party_times >= 1:
        html.setText(".bought_party_or_no", f"Bought: {party_times} times")
    elif party_times == 0:
        html.setText(".bought_party_or_no", "Bought: No")
    else:
        html.setText(".bought_party_or_no", "How the fu you even did that!?")


def buy_multiply_func(event):
    money_amount = localstorage.get_int("money")
    price = localstorage.get_int("price_of_multiply")

    if money_amount >= price:
        current_amount = localstorage.get_int("amount")
        localstorage.set("amount", current_amount * 2)
        localstorage.set("money", money_amount - price)

        # Увеличиваем счетчик покупок и цену
        times_bought = localstorage.get_int("bought_multiply_times")
        localstorage.set("bought_multiply_times", times_bought + 1)
        localstorage.set("price_of_multiply", price * 2)

    # Обновляем интерфейс
    init()


def buy_party_button_func(event):
    money_amount = localstorage.get_int("money")
    price = localstorage.get_int("price_of_party")

    if money_amount >= price:
        localstorage.set("money", money_amount - price)

        # Уменьшаем время party_speed
        party_speed = localstorage.get_int("party_speed")
        party_speed = int(party_speed / 1.3)
        localstorage.set("party_speed", party_speed)

        # Увеличиваем счетчик покупок и цену
        times_bought = localstorage.get_int("bought_party_times")
        localstorage.set("bought_party_times", times_bought + 1)
        localstorage.set("price_of_party", price * 2)

        # Обновляем интерфейс
        init()

def buy_speedrun_func(event):
    if localstorage.get_int("money") >= 2500:
        localstorage.set("money", localstorage.get_int("money") - 2500)
        localstorage.set("speedrun_bought", True)
        init()
    else:
        html.setText(".speedrun_bought", "Not enough money!")
        timers.set_timeout_seconds(init, 1)

def buy_dvd_button_func(event):
    is_bought = localstorage.get_bool("bought_dvd")

    if not is_bought:
        money_amount = localstorage.get_int("money")

        if money_amount >= 250:
            # Вычитаем деньги и устанавливаем флаг покупки
            localstorage.set("money", money_amount - 250)
            localstorage.set("bought_dvd", True)

            # Увеличиваем amount
            current_amount = localstorage.get_int("amount")
            localstorage.set("amount", current_amount + 1)

            # Обновляем интерфейс немедленно
            init()
        else:
            html.setText(".bought_dvd_or_no", "Bought: No")
            timers.set_timeout_seconds(init, 1)
    else:
        html.setText(".bought_dvd_or_no", "Already bought!")
        timers.set_timeout_seconds(init, 1)


# Инициализируем интерфейс при загрузке
init()

# Привязываем обработчики событий
buy_speedrun.bind("click", buy_speedrun_func)
buy_dvd_button.bind("click", buy_dvd_button_func)
buy_party_button.bind("click", buy_party_button_func)
buy_multiply.bind("click", buy_multiply_func)