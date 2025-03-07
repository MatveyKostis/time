from browser import document, window, html, timer
from datetime import datetime, timedelta
import random
import time


class LocalStorage:
    """
    A Python wrapper for browser's localStorage.
    """

    def __init__(self):
        """
        Initializes the LocalStorage class.
        """
        pass

    def checkItem(self, item: str) -> bool:
        """
        Checks if an item exists in localStorage.

        :param item: The key of the item to check.
        :return: True if the item exists, False otherwise.
        """
        return bool(window.localStorage.getItem(item))
    def getItemtext(self, item: str) -> str | None:
        """
        Retrieves an item from localStorage.

        :param item: The key of the item to retrieve.
        :return: The value stored in localStorage, or None if the key does not exist.
        """
        if self.checkItem(item) is not True:
            return None
        return window.localStorage.getItem(item)

    def getItem(self, item: str) -> str | None:
        """
        Retrieves an item from localStorage.

        :param item: The key of the item to retrieve.
        :return: Returning a localstorage ELEMENT, not str/int/float/etc
        """
        if self.checkItem(item) is not True:
            return None
        return window.localStorage[item]

    def setItem(self, item: str, value: str) -> None:
        """
        Stores an item in localStorage.

        :param item: The key of the item.
        :param value: The value to store.
        """
        window.localStorage.setItem(item, value)

    def createItem(self, item: str, value: str) -> None:
        """
        Creates a new item in localStorage, but does not overwrite existing items.

        :param item: The key of the item.
        :param value: The value to store.
        """
        if self.checkItem(item) is not True:
            window.localStorage.setItem(item, value)
    def addtoItem(self, item: str, value: str) -> None:
        """
        Appends a value to an existing item in localStorage.

        :param item: The key of the item.
        :param value: The value to append.
        """
        self.checkItem(item)
        window.localStorage.setItem(item, window.localStorage.getItem(item) + value)

    def getint(self, item: str) -> int:
        """
        Retrieves an item from localStorage and converts it to an integer.

        :param item: The key of the item.
        :return: The integer value of the stored item.
        """
        if self.checkItem(item) is not True:
            return None
        value = window.localStorage.getItem(item)
        if value is None or value == "[object Object]":
            return 0
        return int(value)

    def getfloat(self, item: str) -> float:
        """
        Retrieves an item from localStorage and converts it to a float.

        :param item: The key of the item.
        :return: The float value of the stored item.
        """
        if self.checkItem(item) is not True:
            return None
        return float(window.localStorage.getItem(item))

    def getboolean(self, item: str) -> bool:
        """
        Retrieves an item from localStorage and converts it to a boolean.

        :param item: The key of the item.
        :return: True if the stored value is "true", False if it's "false".
        """
        if self.checkItem(item) is not True:
            return None
        return window.localStorage.getItem(item).lower() == "true"

    def removeItem(self, item: str) -> None:
        """
        Removes an item from localStorage.

        :param item: The key of the item to remove.
        """
        window.localStorage.removeItem(item)

    def clear(self) -> None:
        """
        Clears all items from localStorage.
        """
        window.localStorage.clear()

    def key(self, index: int) -> str | None:
        """
        Retrieves the key at a specific index in localStorage.

        :param index: The index of the key.
        :return: The key name at the specified index, or None if out of bounds.
        """
        return window.localStorage.key(index)
    def getType(self, item: str) -> str:
        """
        Retrieves the type of an item from localStorage.

        :param item: The key of the item.
        :return: The type of the stored item.
        """
        if window.localStorage.getItem(item).isdigit():
            return int
        elif window.localStorage.getItem(item).replace(".", "", 1).isdigit():
            return float
        elif window.localStorage.getItem(item) == "true" or "false":
            return bool
        else:
            return str

class HTML_Elements:
    def getText(self, query: str) -> str:
        """
        Returning a text from a given query
        :param query: A query (like a class that starting from ".", or a id that starting from "#")
        :return: A text from query
        """
        return document.querySelector(query).textContent
    def setText(self, query: str, text: str) -> None:
        """
        Setting a text to a given query
        :param query: A query (like a class that starting from ".", or a id that starting from "#")
        :param text: A text to be set
        :return: None
        """
        document.querySelector(query).textContent = text
    def removeElement(self, query: str) -> None:
        """
        Removing an element from a given query
        :param query: A query (like a class that starting from ".", or a id that starting from "#")
        :return: None
        """
        document.querySelector(query).remove()
    def createElement(self, tag: str, text: str, src = None) -> None:
        """
        Creating an element from a given tag
        :param tag: A tag of the element
        :param text: A text to be set
        :param src: A source (if needed)
        :return: Element
        """
        element = document.createElement(tag)
        element.textContent = text
        if src:
            element.src = src
        return element
    def addStyle(self, name: str, value: str, id_class: str):
        """
        Adding a style to a given element
        :param name: A name of the style
        :param value: A value of the style
        :param id_class: An id or a class
        :return: None
        """
        document.querySelector(id_class).style[name] = value
    def getElement(self, query: str) -> None:
        """
        Returning an element from a given query
        :param query: A query (like a class that starting from ".", or a id that starting from "#")
        :return: Element
        """
        return document.querySelector(query)
    def setHTML(self, query: str, html: str) -> None:
        """
        Setting a html to a given query
        :param query: A query (like a class that starting from ".", or a id that starting from "#")
        :param html: A html to be set
        :return: None
        """
        document.querySelector(query).innerHTML = html

class Timers:
    def __init__(self):
        pass
    def set_timeout_seconds(self, func, seconds: int):
        """
        Set a function to be called after a specified number of seconds.

        :param func: The function to be called.
        :param seconds: The number of seconds to wait before calling the function.
        """
        window.setTimeout(func, seconds * 1000)
    def set_timeout_minutes(self, func, minutes: int):
        """
        Set a function to be called after a specified number of minutes.

        :param func: The function to be called.
        :param minutes: The number of minutes to wait before calling the function.
        """
        window.setTimeout(func, minutes * 60 * 1000)
    def set_timeout_hours(self, func, hours: int):
        """

        Set a function to be called after a specified number of hours.
        :param func:
        :param hours:
        :return:
        """
        window.setTimeout(func, hours * 60 * 60 * 1000)

    def set_interval_seconds(self, func, seconds: int):
        """
        Set a function to be called repeatedly at specified intervals in seconds.

        :param func: The function to be called.
        :param seconds: The number of seconds between each function call.
        """
        window.setInterval(func, seconds * 1000)

    def set_interval_minutes(self, func, minutes: int):
        """
        Set a function to be called repeatedly at specified intervals in minutes.

        :param func: The function to be called.
        :param minutes: The number of minutes between each function call.
        """
        window.setInterval(func, minutes * 60 * 1000)

    def set_interval_hours(self, func, hours: int):
        """
        Set a function to be called repeatedly at specified intervals in hours.

        :param func: The function to be called.
        :param hours: The number of hours between each function call.
        """
        window.setInterval(func, hours * 60 * 60 * 1000)


localstorage = LocalStorage()
html = HTML_Elements()
timers = Timers()