# -*- coding: utf8 -*-

import time
import requests
from selenium import webdriver
from fake_useragent import UserAgent

user_agent = UserAgent()
options = webdriver.ChromeOptions()

options.add_argument("--disable-blink-features=AutomationControlled")
# сохранение куки
options.add_argument(r"user-data-dir=C:\Users\Govard\AppData\Local\Google\Chrome\User Data\profile 2") #Path to your chrome profile
# работа в фоновом режиме
# options.add_argument("--headless")
# Открыть в полный экран браузер
options.add_argument('--start-maximized')
# рандомный юзер агент
# options.add_argument(f"user-agent={user_agent.random}")

login_email = 'ваш_логин_up_work'
password_email = 'пароль'

while True:
    driver = webdriver.Chrome(executable_path=r"chromedriver.exe", options=options)
    driver.get("https://www.upwork.com/")

    try:
        while driver.find_element_by_class_name('page-title'):

            res_post = requests.post(f'http://rucaptcha.com/in.php?key=ваш_api_key&method=userrecaptcha&googlekey=6LdymF8bAAAAAADi0cY2Z1roKRBaDigDrEgrB8Ob&pageurl=https://www.upwork.com/')
            print(res_post.text)
            print_res = res_post.text
            res_post = print_res.replace("OK|", "")
            result = requests.get(f'http://rucaptcha.com/res.php?key=ваш_api_key&action=get&id={res_post}')

            while result.text == "CAPCHA_NOT_READY":
                time.sleep(5)
                print(result.text)
                result = requests.get(f'http://rucaptcha.com/res.php?key=ваш_api_key&action=get&id={res_post}')

            token = result.text
            new_token = token.replace("OK|", "")
            print(new_token)

            element = driver.find_element_by_class_name('g-recaptcha-response')
            driver.execute_script("arguments[0].removeAttribute('style')", element)

            driver.find_element_by_class_name('g-recaptcha-response').send_keys(new_token)

            # переходим в iframe для добавление кнопки
            driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="px-captcha"]/div/div/div/iframe'))
            driver.execute_script('document.getElementById("rc-anchor-container").insertAdjacentHTML("afterbegin", `<input type="submit" value="send">`);')
            driver.find_element_by_xpath('//*[@id="rc-anchor-container"]/input').click()
            # возвращаемся к основному контенту
            driver.switch_to.default_content()
            time.sleep(5)

    except Exception as ex:
        print(ex)

    driver.find_element_by_class_name('nav-item.login-link.d-none.d-lg-block.px-20').click()

    time.sleep(5)
    login = driver.find_element_by_id('login_username')
    login.send_keys(login_email)
    driver.find_element_by_id('login_password_continue').click()
    time.sleep(5)
    password = driver.find_element_by_id('login_password')
    password.send_keys(password_email)
    driver.find_element_by_id('login_control_continue').click()
    time.sleep(5)

    driver.get("https://www.upwork.com/ab/jobs/search/?q=python%20selenium&sort=recency")

    card = driver.find_elements_by_xpath('//*[@id="layout"]/div[2]/div/div[2]/div/div/div/div/div/div/section[2]/div/div/div/div/div[1]/small[1]/span[5]/span/time')
    url_card = driver.find_elements_by_xpath('//*[@id="layout"]/div[2]/div/div[2]/div/div/div/div/div/div/section[2]/div/div/div/div/div[1]/h4')

    # чекает минуты
    for i in range(1, 11):
        i_int = str(i) + ' minutes ago'
        for cd in card:
            content = driver.execute_script('return arguments[0].textContent;', cd)

            # сообщение в телегу
            if content == i_int:
                # ссылка на карточку работы
                url_a = ''
                url_b = ''
                for ul in url_card:
                    url_a = ul.find_element_by_xpath('//*[@id="layout"]/div[2]/div/div[2]/div/div/div/div/div/div/section[2]/div/div/div/div/div[1]/h4/a').get_attribute('href')
                    url_b += url_a

                token = "ваш_токен_бота_телеграм"
                url = "https://api.telegram.org/bot"
                channel_id = "id_канала"
                url += token
                method = url + "/sendMessage"
                text = f"Свежая запись, ей всего: {content}. \nВот ссылка на неё - {url_a}"

                r = requests.post(method, data={
                    "chat_id": channel_id,
                    "text": text
                })
                if r.status_code != 200:
                    raise Exception("post_text error")
    driver.quit()
    time.sleep(300)


