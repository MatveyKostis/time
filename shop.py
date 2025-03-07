from browser import document, window, timer
from brython_colection import localstorage, html, timers
from datetime import datetime, timedelta
import random
import time

class Money_shop():
    def __init__(self):
        stored_money_is_ok = localstorage.getItem("money")
        self.money = localstorage.getint("money")
        self.amount = localstorage.getint("amount")
        self.amount = localstorage.getint("amount")
        self.party_time = localstorage.getint("party_time")
    def devide_party_time(self, times):
        self.party_time = int(self.party_time)
        self.party_time = self.party_time / times
        print(self.party_time)
        localstorage.setItem("party_time", self.party_time)

buy_dvd_button = html.getElement('.buy_dvd')
buy_party_button = html.getElement('.buy_party')
bought_dvd = localstorage.getboolean("bought_dvd")
bought_party_times = localstorage.getint("bought_party_times")
bought_party_or_no = html.getElement('.bought_party_or_no')
if localstorage.getint("party_speed") is None:
    localstorage.setItem("party_speed", 1000)
print(localstorage.getint("party_speed"))
if localstorage.getint("price_of_party") is None:
    localstorage.setItem("price_of_party", 1000)
print(localstorage.getint("price_of_party"))
localstorage.setItem("bought_party_times", bought_party_times)
localstorage.setItem("bought_dvd", bought_dvd)
bought_dvd_text = html.getElement(".bought_dvd_or_no")
money = Money_shop()
def init():
    print(bought_dvd)
    if bought_dvd:
        bought_dvd_text.text = "Bought: Yes"
    elif not bought_dvd:
        bought_dvd_text.text = "Bought: No"
    print(bought_party_times)
    price_of_party = html.getElement(".price_of_party")
    price_of_party.text = f"Cost: {localstorage.getint('price_of_party')} $"
    if bought_party_times >= int(1):
        bought_party_or_no.text = f"Bought: {localstorage.getint('bought_party_times')} times"
    elif int(bought_party_times) == 0:
        bought_party_or_no.text = "Bought: No"
    else:
        bought_party_or_no.text = "How the fu you even did that!?"

def buy_party_button_func(event):
    global party_speed
    if localstorage.getint("money") >= localstorage.getint("price_of_party"):
        localstorage.setItem("money", localstorage.getint("money") - localstorage.getint("price_of_party"))
        party_speed = localstorage.getint("party_speed")
        party_speed = party_speed / 1.3
        localstorage.setItem("party_speed", int(party_speed))
        localstorage.setItem("bought_party_times", localstorage.getint("bought_party_times") + 1)
        localstorage.setItem("price_of_party", localstorage.getint("price_of_party") * 2)
        init()

def buy_dvd_button_func(event):
    global bought_dvd
    if not bought_dvd:
        if int(money.money) >= 250:
            money.money -= 250
            bought_dvd = True
            window.localStorage["bought_dvd"] = bought_dvd
            window.localStorage["money"] = money.money
            money_lol = localstorage.getint("amount")
            money_lol += 1
            localstorage.setItem("amount", money_lol)
            init()
        else:
            bought_dvd_text.text = "Bought: No"
            timers.set_timeout_seconds(init, 1)
    else:
        bought_dvd_text.text = "Bought: Yes"
init()
buy_dvd_button.bind("click", buy_dvd_button_func)
buy_party_button.bind("click", buy_party_button_func)