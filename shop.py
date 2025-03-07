from browser import document, window, html, timer
from datetime import datetime, timedelta
import random
import time

class Money_shop():
    def __init__(self):
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
        self.money = int(stored_money)
        self.amount = window.localStorage.getItem("amount")
        if self.amount is not int:
            if type(self.amount) == str:
                window.localStorage.setItem("amount", int(self.amount))
            else:
                window.localStorage.setItem("amount", 1)
        self.amount = window.localStorage["amount"]
buy_dvd_button = document.querySelector('.buy_dvd')
bought_dvd = window.localStorage.getItem("bought_dvd")
if bought_dvd == "true":
    bought_dvd = True
elif bought_dvd == "false":
    bought_dvd = False
if bought_dvd != "false" or "true":
    print(bought_dvd)
    if type(bought_dvd) != bool:
        bought_dvd = False
else:
    bought_dvd = bool(bought_dvd)
window.localStorage["bought_dvd"] = bought_dvd
bought_dvd_text = document.querySelector(".bought_dvd_or_no")

money = Money_shop()


def init():
    print(bought_dvd)
    if bought_dvd == str:
        bought_dvd_text.text = "Bought: ERROR"
    elif bought_dvd:
        bought_dvd_text.text = "Bought: Yes"
    elif not bought_dvd:
        bought_dvd_text.text = "Bought: No"

def buy_dvd_button_func(event):
    global bought_dvd
    if not bought_dvd:
        if int(money.money) >= 250:
            money.money -= 250
            bought_dvd = True
            window.localStorage["bought_dvd"] = bought_dvd
            window.localStorage["money"] = money.money
            money_lol = window.localStorage["amount"]
            money_lol = int(money_lol)
            money_lol += 1
            window.localStorage["amount"] = money_lol
            init()
        else:
            bought_dvd_text.text = f"Not enough money: {int(money.amount) - 250}"
            timer.set_timeout(init, 1000)
    else:
        bought_dvd_text.text = "Bought: Yes"
init()
buy_dvd_button.bind("click", buy_dvd_button_func)