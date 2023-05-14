import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuration du navigateur
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)


def authentification_netflix():
    driver.get("https://www.netflix.com/fr-en/login")  # accès à netflix

    # A changer selon le compte utilisé
    username = "celpat@free.fr"
    password = "zk98eg!+"

    '''#On enleve la page qui demande d'accepter les cookies
    refuse_button = wait.until(EC.element_to_be_clickable((By.ID, "cookie-disclosure-reject")))
    refuse_button.click()'''

    # authentification
    username_input = wait.until(EC.visibility_of_element_located((By.ID,
                                                                  "id_userLoginId")))  # le "email" faut aller le chercher dans le coee HTML de la page et c'est ce qu'il y a derrière name=
    username_input.send_keys(username)

    password_input = wait.until(EC.visibility_of_element_located(
        (By.ID, "id_password"))) 
    password_input.send_keys(password) 
    password_input.submit()
    element = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//a[@href='/SwitchProfile?tkn=ZC5VAV2RCFEEBESIO2SWJWDUN4']"))) 
    element.click()

    time.sleep(10)


def main():
    authentification_netflix()


if __name__ == "__main__":
    main()
