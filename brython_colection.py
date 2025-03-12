from browser import document, window, html, timer
from datetime import datetime, timedelta
import json
import random
from typing import Optional
import time


class LocalStorageManager:
    """
    Manager for working with a specific JSON store in localStorage.
    All operations are automatically directed to the selected storage.
    """

    def __init__(self, storage_name=None):
        """
        Initializes the manager, binding it to a specific storage.

        :param storage_name: Name of the JSON store in localStorage
        """
        self.storage_name = storage_name
        # Create storage if it doesn't exist
        if storage_name and not self._check_storage_exists():
            self._create_storage({})

    def set_storage(self, storage_name):
        """
        Sets the storage name for all operations.

        :param storage_name: Name of the JSON store in localStorage
        """
        self.storage_name = storage_name
        # Create storage if it doesn't exist
        if not self._check_storage_exists():
            self._create_storage({})
        return self

    def _check_storage_exists(self):
        """Checks if the selected storage exists."""
        return bool(window.localStorage.getItem(self.storage_name))

    def _create_storage(self, initial_data={}):
        """Creates storage with initial data."""
        window.localStorage.setItem(self.storage_name, json.dumps(initial_data))

    def _get_storage(self, default=None):
        """Gets all contents of the storage."""
        if not self._check_storage_exists():
            return default if default is not None else {}

        json_str = window.localStorage.getItem(self.storage_name)
        try:
            return json.loads(json_str)
        except:
            # If not JSON, return value as is or empty dict
            raw_value = window.localStorage.getItem(self.storage_name)
            if isinstance(raw_value, str) and raw_value in ["true", "false"]:
                return raw_value == "true"
            try:
                if "." in raw_value:
                    return float(raw_value)
                return int(raw_value)
            except:
                return raw_value if raw_value is not None else default if default is not None else {}

    def _save_storage(self, data):
        """Saves data to storage."""
        window.localStorage.setItem(self.storage_name, json.dumps(data))

    # Operations with elements inside storage
    def get(self, key, default=None):
        """
        Returns a value by key from storage.

        :param key: Key to get value for
        :param default: Default value if key not found
        :return: Value from storage or default
        """
        if not self.storage_name:
            raise ValueError("Storage name is not set")

        storage_data = self._get_storage()
        if isinstance(storage_data, dict):
            return storage_data.get(key, default)
        return default

    def set(self, key, value):
        """
        Sets a value by key in storage.

        :param key: Key to set value for
        :param value: Value to set
        """
        if not self.storage_name:
            raise ValueError("Storage name is not set")

        storage_data = self._get_storage({})
        if isinstance(storage_data, dict):
            storage_data[key] = value
            self._save_storage(storage_data)
        else:
            # If storage is not a dict, convert it to a dict
            self._save_storage({key: value})
        return self

    def update(self, new_data):
        """
        Updates storage with new data.

        :param new_data: Dictionary with new data
        """
        if not self.storage_name:
            raise ValueError("Storage name is not set")

        if not isinstance(new_data, dict):
            raise ValueError("new_data must be a dictionary")

        storage_data = self._get_storage({})
        if isinstance(storage_data, dict):
            storage_data.update(new_data)
            self._save_storage(storage_data)
        else:
            self._save_storage(new_data)
        return self

    def delete(self, key):
        """
        Deletes a value by key from storage.

        :param key: Key to delete
        """
        if not self.storage_name:
            raise ValueError("Storage name is not set")

        storage_data = self._get_storage()
        if isinstance(storage_data, dict) and key in storage_data:
            del storage_data[key]
            self._save_storage(storage_data)
        return self

    def clear_data(self):
        """Clears all contents of storage."""
        if not self.storage_name:
            raise ValueError("Storage name is not set")

        self._create_storage({})
        return self

    def remove_storage(self):
        """Completely removes storage from localStorage."""
        if not self.storage_name:
            raise ValueError("Storage name is not set")

        window.localStorage.removeItem(self.storage_name)
        return self

    def get_all(self):
        """
        Returns all contents of storage.

        :return: Data from storage
        """
        if not self.storage_name:
            raise ValueError("Storage name is not set")

        return self._get_storage()

    def append_to_list(self, key, value):
        """
        Adds a value to a list stored at the specified key.

        :param key: List key
        :param value: Value to add
        """
        if not self.storage_name:
            raise ValueError("Storage name is not set")

        storage_data = self._get_storage({})
        if isinstance(storage_data, dict):
            if key not in storage_data:
                storage_data[key] = []
            elif not isinstance(storage_data[key], list):
                storage_data[key] = [storage_data[key]]

            storage_data[key].append(value)
            self._save_storage(storage_data)
        return self

    def increment(self, key, amount=1):
        """
        Increases the value at the key by the specified amount.

        :param key: Counter key
        :param amount: Increment amount
        """
        if not self.storage_name:
            raise ValueError("Storage name is not set")

        storage_data = self._get_storage({})
        if isinstance(storage_data, dict):
            current = storage_data.get(key, 0)
            try:
                storage_data[key] = current + amount
                self._save_storage(storage_data)
            except:
                # If addition is not possible, just set the value
                storage_data[key] = amount
                self._save_storage(storage_data)
        return self

    # Additional useful methods
    def keys(self):
        """Returns a list of keys in storage."""
        if not self.storage_name:
            raise ValueError("Storage name is not set")

        storage_data = self._get_storage({})
        if isinstance(storage_data, dict):
            return list(storage_data.keys())
        return []

    def has_key(self, key):
        """Checks if a key exists in storage."""
        if not self.storage_name:
            raise ValueError("Storage name is not set")

        storage_data = self._get_storage({})
        if isinstance(storage_data, dict):
            return key in storage_data
        return False

    def get_int(self, key, default=0):
        """Gets a value as an integer."""
        value = self.get(key)
        if value is None:
            return default
        try:
            return int(value)
        except:
            return default

    def get_float(self, key, default=0.0):
        """Gets a value as a floating point number."""
        value = self.get(key)
        if value is None:
            return default
        try:
            return float(value)
        except:
            return default

    def get_bool(self, key, default=False):
        """Gets a value as a boolean."""
        value = self.get(key)
        if value is None:
            return default
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() == "true"
        return bool(value)

    def get_str(self, key, default=""):
        """Gets a value as a string."""
        value = self.get(key)
        if value is None:
            return default
        return str(value)

    def exists(self):
        """Checks if storage exists."""
        return self._check_storage_exists() if self.storage_name else False

    def size(self):
        """Returns the number of items in the storage."""
        if not self.storage_name:
            raise ValueError("Storage name is not set")

        storage_data = self._get_storage({})
        if isinstance(storage_data, dict):
            return len(storage_data)
        return 0

    def get_or_create(self, key, default_value):
        """
        Gets a value by key or creates it if it doesn't exist.

        :param key: Key to get or create
        :param default_value: Value to set if key doesn't exist
        :return: Value from storage or default_value
        """
        if not self.has_key(key):
            self.set(key, default_value)
            return default_value
        return self.get(key)

    def toggle_bool(self, key):
        """
        Toggles a boolean value by key.

        :param key: Key to toggle
        :return: New boolean value
        """
        current = self.get_bool(key)
        new_value = not current
        self.set(key, new_value)
        return new_value

    def merge_objects(self, key, new_data):
        """
        Merges an object at the specified key with new_data.

        :param key: Key containing the object
        :param new_data: Data to merge with
        """
        if not isinstance(new_data, dict):
            raise ValueError("new_data must be a dictionary")

        current = self.get(key, {})
        if not isinstance(current, dict):
            current = {}

        current.update(new_data)
        self.set(key, current)
        return self

class HTML_Elements:
    def getText(self, query: str) -> str:
        """
        Returning a text from a given query
        :param query: A query (like a class that starting from ".", or a id that starting from "#")
        :return: A text from query
        """
        return document.querySelector(query).textContent
    def getHTML(self, query: str) -> str:
        """
        Returning an HTML from a given query
        :param query: A query (like a class that starting from ".", or a id that starting from "#")
        :return: An HTML from query
        """
        return document.querySelector(query).innerHTML
    def setHTML(self, query: str, html: str) -> None:
        """
        Setting an HTML to a given query
        :param query: A query (like a class that starting from ".", or a id that starting from "#")
        :param html: An HTML to be set
        :return: None
        """
        document.querySelector(query).innerHTML = html
    def setText(self, query: str, text: str) -> None:
        """
        Setting a text to a given query
        :param query: A query (like a class that starting from ".", or a id that starting from "#")
        :param text: A text to be set
        :return: None
        """
        document.querySelector(query).textContent = text

    def createElement(self, tag: str, text: str, src: Optional[str] = None,
                      class_ok: Optional[str] = None) -> 'Element':
        """
        Create an element with the given tag, text, and optional attributes src and class.

        :param tag: The tag of the element
        :param text: The text to be set
        :param src: The source (if needed, e.g., for an image)
        :param class_ok: The class (if needed)
        :return: The element
        """
        element = document.createElement(tag)

        if class_ok:
            element.className = class_ok

        element.textContent = text

        if src:
            element.src = src

        document.body.appendChild(element)
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

    def removeElement(self, query: str) -> None:
        """
        Removing an element from a given query
        :param query: A query (like a class that starting from ".", or a id that starting from "#")
        :return: None
        """
        document.querySelector(query).remove()
        document.body.removeChild(self.getElement(query))
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
        :return interval, which can be used to clear the interval
        """
        interval = window.setInterval(func, seconds * 1000)
        return interval

    def set_interval_minutes(self, func, minutes: int):
        """
        Set a function to be called repeatedly at specified intervals in minutes.

        :param func: The function to be called.
        :param minutes: The number of minutes between each function call.
        :return interval, which can be used to clear the interval
        """
        interval = window.setInterval(func, minutes * 60 * 1000)
        return interval

    def set_interval_hours(self, func, hours: int):
        """
        Set a function to be called repeatedly at specified intervals in hours.

        :param func: The function to be called.
        :param hours: The number of hours between each function call.
        :return interval, which can be used to clear the interval
        """
        interval = window.setInterval(func, hours * 60 * 60 * 1000)
        return interval

    def clear_interval(self, interval):
        """
        clearing an interval
        :param interval:
        :return: nothing
        """
        if interval == None:
            return None
        window.clearInterval(interval)

    def set_timeout_decorator(self, type, time: int):
        """
        Creating interval through decorator

        :param type:
        :param time:
        :return: nothing
        """
        def decorator(func):
            def wrapper(*args, **kwargs):
                if args or kwargs:
                    return func(*args, **kwargs)
                else:
                    return func()

            if type == "seconds":
                self.set_timeout_seconds(wrapper, time)
            elif type == "minutes":
                self.set_timeout_minutes(wrapper, time)
            elif type == "hours":
                self.set_timeout_hours(wrapper, time)
            return wrapper

        return decorator

    def set_interval_decorator(self, type, time: int):
        """
        Creating interval through decorator

        :param type:
        :param time:
        :return: nothing
        """
        def decorator(func):
            def wrapper(*args, **kwargs):
                if args or kwargs:
                    return func(*args, **kwargs)
                else:
                    return func()

            if type == "seconds":
                self.set_interval_seconds(wrapper, time)
            elif type == "minutes":
                self.set_interval_minutes(wrapper, time)
            elif type == "hours":
                self.set_interval_hours(wrapper, time)
            return wrapper

        return decorator

class Bind:
    def __init__(self):
        pass

    def bind(self, query, event_name):
        """
        binding a function to an event (for example, a click)
        :param query:
        :param event_name:
        :return:
        """
        def decorator(func):
            html.getElement(query).bind(event_name, func)
            return func

        return decorator

    def keyboard_reaction(self):
        """
        Returning a keyboard pressed key, through decorator
        :return: key
        """
        def decorator(func):
            def wrapper(event):
                key = event.key
                func(key)

            window.addEventListener("keydown", wrapper)
            return func

        return decorator

class Input_Handle:
    def __init__(self):
        pass

    def handle_checkbox(self, query):
        """
        Returning a checkbox value, through decorator
        :return: boolean (True/False)
        """
        def decorator(func):
            def wrapper(event):
                value = event.target.checked
                func(value)

            html.getElement(query).addEventListener("change", wrapper)
            return func

        return decorator

    def handle_input(self, query):
        """
        Returning an input value, through decorator
        :return: string value
        """
        def decorator(func):
            def wrapper(event):
                value = event.target.value
                func(value)

            html.getElement(query).addEventListener("input", wrapper)
            return func

        return decorator

    def handle_select(self, query):
        """
        Returning a select value, through decorator
        :return: string value
        """
        def decorator(func):
            def wrapper(event):
                value = event.target.value
                func(value)

            html.getElement(query).addEventListener("change", wrapper)
            return func

        return decorator

    def handle_button(self, query):
        """
        Returning a button value, through decorator
        :return: string value or None
        """
        def decorator(func):
            def wrapper(event):
                value = event.target.value if hasattr(event.target, 'value') else None
                func(value)

            html.getElement(query).addEventListener("click", wrapper)
            return func

        return decorator

    def handle_submit(self, query):
        """
        Handling form submission, through decorator
        :return: event object
        """
        def decorator(func):
            def wrapper(event):
                event.preventDefault()
                func(event)

            html.getElement(query).addEventListener("submit", wrapper)
            return func

        return decorator

    def handle_reset(self, query):
        """
        Handling form reset, through decorator
        :return: event object
        """
        def decorator(func):
            def wrapper(event):
                func(event)

            html.getElement(query).addEventListener("reset", wrapper)
            return func

        return decorator

    def handle_text(self, query):
        """
        Returning a text value, through decorator
        :return: string value
        """
        def decorator(func):
            def wrapper(event):
                value = event.target.value
                func(value)

            html.getElement(query).addEventListener("input", wrapper)
            return func

        return decorator

    def handle_email(self, query):
        """
        Returning a email value, through decorator
        :return: string value
        """
        def decorator(func):
            def wrapper(event):
                value = event.target.value
                func(value)

            html.getElement(query).addEventListener("input", wrapper)
            return func

        return decorator

class Brython_etc:
    def __init__(self):
        """
        A class containing miscellaneous Brython functions

        Note that this class is not meant to be instantiated.
        """
        pass

    def redirect(self, url):
        """
        Redirects the user to a given URL

        :param url: The URL to redirect to
        """
        window.location.href = url

    def alert(self, message):
        """
        Displays an alert box with the given message

        :param message: The message to be displayed
        """
        window.alert(message)

    def ask(self, message):
        """
        Displays a confirmation dialog box with the given message
        and returns True if the user clicks OK, False if the user clicks Cancel

        :param message: The message to be displayed
        :return: boolean (True/False)
        """
        return window.confirm(message)

    def prompt(self, message):
        """
        Displays a prompt dialog box with the given message
        and returns the value input by the user

        :param message: The message to be displayed
        :return: string value
        """
        return window.prompt(message)

    def open(self, url=None):
        """
        Opens a new window with the given URL

        If no URL is given, opens a new window with a link to the rickroll

        :param url: The URL to open (optional)
        """
        if url is None:
            window.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        else:
            window.open(url)

    def get_window_size(self):
        """
        Returns the size of the window

        :return: tuple (width, height)
        """
        return window.innerWidth, window.innerHeight
localstorage = LocalStorageManager()
html = HTML_Elements()
timers = Timers()
input_handle = Input_Handle()
bind = Bind()
brython_etc = Brython_etc()