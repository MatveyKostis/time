from browser import document, window
from brython_colection import localstorage, html, timers, bind
from datetime import datetime, timedelta
import random
import time

class Save_Control():
    def __init__(self):
        localstorage.set_storage("KomaruTimeGame")
    def load_save(self):
        localstorage.get_or_create("bought_dvd", False)
        localstorage.get_or_create("bought_party_times", 0)
        localstorage.get_or_create("bought_multiply_times", 0)
        localstorage.get_or_create("party_speed", 1000)
        localstorage.get_or_create("first_button", 0)
        localstorage.get_or_create("ralsei_amount", 0)
        localstorage.get_or_create("price_of_ralsei", 2500)
        localstorage.get_or_create("price_of_party", 1000)
        localstorage.get_or_create("price_of_multiply", 5000)
        localstorage.get_or_create("money", 0)
        localstorage.get_or_create("amount", 1)
        localstorage.get_or_create("speedrun_bought", False)

class Money_shop():
    def __init__(self):
        localstorage.set_storage("KomaruTimeGame")
        self.money = localstorage.get_or_create("money", 0)
        self.amount = localstorage.get_or_create("amount", 1)
        self.party_time = localstorage.get_or_create("party_time", 1000)

    def devide_party_time(self, times):
        self.party_time = int(self.party_time) // times
        print(self.party_time)
        localstorage.set("party_time", self.party_time)

save_control = Save_Control()
save_control.load_save()
# Elements creation
buy_dvd_button = html.getElement('.buy_dvd')
buy_party_button = html.getElement('.buy_party')
buy_multiply = html.getElement('.buy_multiply')
buy_speedrun = html.getElement('.buy_speedrun')
bought_dvd_text = html.getElement(".bought_dvd_or_no")
bought_party_or_no = html.getElement('.bought_party_or_no')
bought_speedrun_text = html.getElement('.speedrun_bought')
first_button_h3 = html.getElement(".first_button_h3")
money_show_text = html.getElement('.money_show')

first_button = ["DVD", "Ralsei Photo"]


bought_dvd = localstorage.get_bool("bought_dvd")
bought_party_times = localstorage.get_int("bought_party_times")
bought_speedrun = localstorage.get_bool("speedrun_bought")

# Инициализация объекта магазина
money = Money_shop()

def update_text():
    if localstorage.get_int("first_button") == 0:
        html.setHTML(".first_button_h3", "DVD button & x2<img src='images/DVD.png' style='height: 20px'>")
        html.setHTML(".buy_dvd", "Buy DVD <img src='images/DVD.png', style='height: 10px'>")
        if bought_dvd:
            html.setText(".bought_dvd_or_no", "Bought: Yes")
        else:
            html.setText(".bought_dvd_or_no", "Bought: No")
    elif localstorage.get_int("first_button") == 1:
        html.setHTML(".first_button_h3", "Ralsei photo in DVD & x2<img src='images/ralseiphoto.png' style='height: 20px'>")
        html.setHTML(".buy_dvd", "BUY RALSEI <img src='images/ralseiphoto.png', style='height: 50px'>")
        html.setHTML(".cost_first", "Cost 2500$")
        if localstorage.get_int("ralsei_amount") == 5:
            html.setText(".bought_dvd_or_no", "Bought: Yes, " + str(localstorage.get_int("ralsei_amount") * 10) + "%")
        elif localstorage.get_int("ralsei_amount") >= 1:
            text = f"Bought times: {localstorage.get_int('ralsei_amount')} ({localstorage.get_int('ralsei_amount') * 10}%)"
            html.setText(".bought_dvd_or_no", text)
        else:
            html.setText(".bought_dvd_or_no", "Bought: No")

    price_of_party = localstorage.get_int("price_of_party")
    html.setText(".price_of_party", f"Cost: {price_of_party} $")

    price_of_multiply = localstorage.get_int("price_of_multiply")
    html.setText(".price_of_multiply", f"Cost: {price_of_multiply} $")

    multiply_bought = localstorage.get_int("bought_multiply_times")
    html.setText(".multiply_bought", f"Bought: {multiply_bought} times")
    money_show_text.text = f"{localstorage.get_int('money')} $"
    if localstorage.get_bool("speedrun_bought"):
        html.setText(".speedrun_bought", "Bought: Yes")
    else:
        html.setText(".speedrun_bought", "Bought: No")

    party_times = localstorage.get_int("bought_party_times")
    print(f"Party times: {party_times}")

    if party_times >= 1:
        html.setText(".bought_party_or_no", f"Bought: {party_times} times")
    elif party_times == 0:
        html.setText(".bought_party_or_no", "Bought: No")
    else:
        html.setText(".bought_party_or_no", "How the fu you even did that!?")

def init():
    update_text()

@bind.bind(".buy_multiply","click")
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


@bind.bind(".buy_party","click")
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

@bind.bind(".buy_speedrun","click")
def buy_speedrun_func(event):
    if localstorage.get_int("money") >= 2500:
        if localstorage.get_bool("speedrun_bought"):
            html.setText(".speedrun_bought", "Bought: Yes")
            timers.set_timeout_seconds(init, 1)
            return
        localstorage.set("money", localstorage.get_int("money") - 2500)
        localstorage.set("speedrun_bought", True)
        init()
    else:
        if localstorage.get_bool("speedrun_bought"):
            html.setText(".speedrun_bought", "Bought: Yes")
            timers.set_timeout_seconds(init, 1)
            return
        html.setText(".speedrun_bought", "Not enough money!")
        timers.set_timeout_seconds(init, 1)


@bind.bind(".buy_dvd","click")
def buy_dvd_button_func(event):
    if localstorage.get_int("first_button") == 1:
        is_bought = localstorage.get_int("ralsei_amount")
        if localstorage.get_int("money") >= localstorage.get_int("price_of_ralsei"):
            if localstorage.get_int("ralsei_amount") >= 5:
                localstorage.set("ralsei_amount", 5)
                update_text()
                return
            localstorage.set("money", localstorage.get_int("money") - 2500)
            localstorage.set("ralsei_amount", localstorage.get_int("ralsei_amount") + 1)
            localstorage.set("price_of_ralsei". localstorage.get_int("price_of_ralsei") * 2)
            html.setText(".bought_dvd_or_no", "Bought times:" + localstorage.get_int("ralsei_amount"), f" ({localstorage.get_int('price_of_ralsei') * 10}%)")
        else:
            html.setText(".bought_dvd_or_no", "Not enough money!")
        update_text()
    else:
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
                localstorage.set("first_button", 1)
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