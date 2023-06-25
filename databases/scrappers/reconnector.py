# -*- coding: utf-8 -*-
import os
import time
from urllib import error
from urllib.request import urlopen


def reconnector(func):
    def decorated_func(*args, **kwargs):
        result = func(*args, **kwargs)
        if not result:
            for _ in range(10):
                time.sleep(5)
                result = func(*args, **kwargs)
                if result:
                    break
        if not result:
            print("Ошибка подключения")
            raise ValueError("Не удалось получить данные")
        return result
    return decorated_func


#TODO переписать так, чтобы функция выкидывала исключения, обрабатываемые в GUI
@reconnector
def open_url(url_address, broken_url=None):
    if not broken_url:
        try:
            opened_url = urlopen(url_address)
        except error.HTTPError:
            if os.path.exists("bad_urls.txt"):
                with open("bad_urls.txt", "r", encoding="cp1251") as bad_urls:
                    for line in bad_urls:
                        if url_address in line:
                            correct_url = line.split()[1]
                            opened_url = open_url(correct_url)
                            return opened_url
            broken_url = url_address
            print(broken_url)
            print("Некорректный адрес страницы. Введите корректный адрес:")
            new_url = input()
            opened_url = open_url(new_url, broken_url)
    else:
        try:
            opened_url = urlopen(url_address)
        except error.HTTPError:
            print("Опять некорректный адрес")
            new_url = input()
            opened_url = open_url(new_url, broken_url)
    if broken_url:
        with open("bad_urls.txt", "a+", encoding="cp1251") as bad_urls:
            url_log = broken_url + " " + url_address
            bad_urls.write(url_log)
    return opened_url

