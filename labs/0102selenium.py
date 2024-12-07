from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://kmpo.eljur.ru/authorize")
driver.find_element (By.XPATH,
'/html/body/div/div/main/div/div/div/div/form/div[1]/div[1]/div/input').send_keys ("Vilkov")
driver.find_element (By.XPATH,
'/html/body/div/div/main/div/div/div/div/form/div[1]/div [2]/div/input') .send_keys ("Sergey")
driver. find_element (By.XPATH,
'/html/body/div/div/main/div/div/div/div/form/div[2]/button').click()

while True:
    pass