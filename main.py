from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from datetime import datetime
import configparser
import os
import sys

config = configparser.ConfigParser()

config.read('configs.ini')

logado = config['LOGIN'].getboolean('logado')
link = config['LINK']['classroom']

if logado:
    now = datetime.now()

    current_hour = int(now.strftime('%H'))
    current_minutes = int(now.strftime('%M'))

    minutes_left = 60 - current_minutes

    if current_hour < 8:
        if current_minutes == 0:
            hours_left = (24 - current_hour) + 8
        else:
            hours_left = 7 - current_hour
    else:
        if current_minutes == 0:
            hours_left = (24 - current_hour) + 8
        else:
            hours_left = (24 - current_hour) + 7

    print(f'Agirei daqui {hours_left} horas e {minutes_left} minutos...')

    sleep(hours_left*3600 + minutes_left*60)
else:
    c_options = webdriver.ChromeOptions()
    c_options.add_argument(f'--user-data-dir={os.getcwd()}' + '\\User Data\\')
    driver = webdriver.Chrome(options = c_options)
    driver.get(link)
    config.set('LOGIN', 'logado', 'true')
    with open('configs.ini', 'w') as f:
        config.write(f)
    input('Pressione enter quando acabar o login')
    driver.quit()
    sys.exit()

path = os.getcwd() + '\\User Data\\'

c_options = webdriver.ChromeOptions()

c_options.add_argument(f'--user-data-dir={path}')
c_options.add_argument("--mute-audio")
c_options.add_argument("allow-file-access-from-files")
c_options.add_argument("use-fake-device-for-media-stream")
c_options.add_argument("use-fake-ui-for-media-stream")

driver = webdriver.Chrome(options=c_options)

driver.get(link)

try:
    meet = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'https://meet.google.com/lookup/')]"))
    )
finally:
    meet.click()

driver.switch_to.window(driver.window_handles[1])

sleep(3)

action = ActionChains(driver)
action.key_down(Keys.CONTROL)
action.send_keys('e')
action.send_keys('d')
action.key_up(Keys.CONTROL)
action.perform()

try:
    participate = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Participar agora')]"))
    )
finally:
    p2 = participate.find_element_by_xpath('..').find_element_by_xpath('..')
    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of(p2)
        )
    finally:
        print('Clicando...')
        p2.click()