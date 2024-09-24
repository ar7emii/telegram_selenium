from selenium import webdriver  # Через него делаем браузер
from selenium.webdriver.common.keys import Keys  # Импорт подмодуля для работы с кнопками
from selenium.webdriver.common.by import By  # Необходим для внутренней работы (выбора способа поиска элементов)
from selenium.common.exceptions import NoSuchElementException  # Импорт ошибки
from datetime import datetime, timedelta
from time import sleep  # Для остановки кода на паузу
from config import login_phone_number, login_password  # Импорт двух переменных с пользовательскими данными
from xpath import *


class Browser:
    chrome_browser = None

    def create_browser(self):  # Создание браузера Хром и установка размеров окна
        self.chrome_browser = webdriver.Chrome()
        self.chrome_browser.set_window_size(600, 600)

    def smart_sleep(self, xpath):
        start_time = datetime.now()
        while start_time + timedelta(seconds=10) >= datetime.now():
            try:
                self.chrome_browser.find_element(By.XPATH, xpath)
                print("  smart_sleep() Элемент найден за {} ({})".format(datetime.now() - start_time, xpath))
                return True
            except NoSuchElementException:
                sleep(0.01)
        return False

    def login_by_phone_number(self):  # весь процесс входа в тг аккаунт
        if self.smart_sleep(xpath_login_by_phone_number_button):  # нажатие на кнопку 'login by phone number' вместо qr
            elm_login_by_phone_number = self.chrome_browser.find_element(By.XPATH, xpath_login_by_phone_number_button)
            elm_login_by_phone_number.click()
        if self.smart_sleep(xpath_input_phone_number):  # ввод номера телефона в поле
            elm_input_phone_number = self.chrome_browser.find_element(By.XPATH, xpath_input_phone_number)
            elm_input_phone_number.clear()  # очищение input поля перед вводом своего номера
            elm_input_phone_number.send_keys(login_phone_number)
        if self.smart_sleep(xpath_next_button):  # нажатие кнопки для отправки номера
            elm_next = self.chrome_browser.find_element(By.XPATH, xpath_next_button)
            elm_next.click()
        if self.smart_sleep(xpath_sign_in_code):  # ввод одноразового ключа через input
            elm_sign_in_code = self.chrome_browser.find_element(By.XPATH, xpath_sign_in_code)
            sign_in_code = input('=========================================================\nВВЕДИТЕ КЛЮЧ ДЛЯ ВХОДА: ')
            elm_sign_in_code.send_keys(sign_in_code)
        if self.smart_sleep(xpath_input_password):  # у меня двухфакторная аутентификация - я должен еще ввести пароль
            elm_input_password = self.chrome_browser.find_element(By.XPATH, xpath_input_password)
            elm_input_password.send_keys(login_password)
            elm_input_password.send_keys(Keys.ENTER)  # ввод пароля с помощью кнопки Enter

    def send_messages_to_chat(self):  # процесс отправки сообщений в чат
        if self.smart_sleep(xpath_saved_messages_chat):  # поиск чата
            elm_saved_messages_chat = self.chrome_browser.find_element(By.XPATH, xpath_saved_messages_chat)
            elm_saved_messages_chat.click()
        while True:  # while цикл, который позволяет отправлять сообщения, пока не будет введено слово stop
            if self.smart_sleep(xpath_send_message_field):  # поиск поля для ввода сообщения
                elm_send_message_field = self.chrome_browser.find_element(By.XPATH, xpath_send_message_field)
                message_text = input('\n\n=======================================================\nВВЕДИТЕ СООБЩЕНИЕ: ')
                print('ВВЕДЕННОЕ СООБЩЕНИЕ: ', message_text)
                if message_text.upper() == 'STOP':  # break условие чтобы остановить цикл отправки сообщений
                    break
                elm_send_message_field.send_keys(message_text)
                sleep(0.5)
                elm_send_message_field.send_keys(Keys.ENTER)  # ввод сообщения
        #            if self.smart_sleep(xpath_send_message_button):
        #                elm_send_message_button = self.chrome_browser.find_element(By.XPATH, xpath_send_message_button)
        #                elm_send_message_button.click()

    def read_messages_from_chat(self):  # процесс вывода последних 5 сообщений
        if self.smart_sleep(xpath_last_messages):  # поиск сообщений
            elm_last_messages = self.chrome_browser.find_elements(By.XPATH, xpath_last_messages)
            to_print_messages = elm_last_messages[-5:]  # срез последних 5ти
            for message_element in to_print_messages:
                message_text = message_element.text
                print('\n', message_text)


browser = Browser()
browser.create_browser()
browser.chrome_browser.get("https://web.telegram.org/a")
browser.login_by_phone_number()
sleep(2)
browser.send_messages_to_chat()
input('=====================================================================\n Нажмите Enter чтобы вывести сообщение\n')
browser.read_messages_from_chat()
sleep(999)
