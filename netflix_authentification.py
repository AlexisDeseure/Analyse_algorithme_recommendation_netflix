import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd



def authentification_netflix(driver, wait):
    driver.get("https://www.netflix.com/fr-en/login")  # accès à netflix

    # A changer selon le compte utilisé
    username = "usr"
    password = "mdp"

    '''#On enleve la page qui demande d'accepter les cookies
    refuse_button = wait.until(EC.element_to_be_clickable((By.ID, "cookie-disclosure-reject")))
    refuse_button.click()'''

    # authentification
    username_input = wait.until(EC.visibility_of_element_located((By.ID,
                                                                  "id_userLoginId")))  # le "email" faut aller le chercher dans le coee HTML de la page et c'est ce qu'il y a derrière name=
    username_input.send_keys(username)

    password_input = wait.until(EC.visibility_of_element_located(
        (By.ID, "id_password")))  # pareil pour le password mais j'ai pas encore eu le temps de fairen
    password_input.send_keys(password)
    password_input.submit()
    element = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//a[@href='/SwitchProfile?tkn=ZC5VAV2RCFEEBESIO2SWJWDUN4']")))
    # element = driver.find_element(By.XPATH, "//a[@href='/SwitchProfile?tkn=ZC5VAV2RCFEEBESIO2SWJWDUN4']")
    element.click()

    

def recuperer_liste_ligne(driver,wait, ligne):
    '''récupérer la liste des noms et liens des séries/films situés sur la ligne donnée en paramètre'''
    wait.until(EC.presence_of_element_located((By.ID, ligne)))
    #récupération du code html de la ligne
    html = driver.find_element(By.ID,'row-1').get_attribute('innerHTML')
    #création d'un objet BeautifulSoup pour pouvoir parser le code html
    soup = BeautifulSoup(html, 'html.parser')
    #récupération des balises <a> qui contiennent les liens et les noms des séries/films (class="slider-refocus")
    a_tags = soup.find_all('a', {'class': 'slider-refocus'})
    data = []
    for a in a_tags:
        href = a.get('href')
        title = a.get('aria-label')
        data.append([href, title])
    df = pd.DataFrame(data, columns=['liens', 'titres'])
    # Stockage du DataFrame dans un fichier CSV
    df.to_csv('data.csv', index=False)




def main():
    # Configuration du navigateur
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    authentification_netflix(driver, wait)
    recuperer_liste_ligne(driver, wait,"row-1")
    time.sleep(1000)


if __name__ == "__main__":
    main()
