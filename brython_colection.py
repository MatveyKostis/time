from browser import document, window, html, timer
from datetime import datetime, timedelta
import json
import random
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


localstorage = LocalStorageManager()
html = HTML_Elements()
timers = Timers()