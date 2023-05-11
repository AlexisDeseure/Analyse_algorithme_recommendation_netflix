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
    driver.get("https://www.netflix.com/fr-en/login")   #accès à netflix
    
    #A changer selon le compte utilisé
    username = "mail"
    password = "mot_de_passe"
    
    #On enleve la page qui demande d'accepter les cookies
    refuse_button = wait.until(EC.element_to_be_clickable((By.ID, "cookie-disclosure-reject")))
    refuse_button.click()

    #authentification
    username_input = wait.until(EC.visibility_of_element_located((By.ID, "email")))   #le "email" faut aller le chercher dans le coee HTML de la page et c'est ce qu'il y a derrière name=
    username_input.send_keys(username)
    username_input.submit()

    password_input = wait.until(EC.visibility_of_element_located((By.ID, "password")))  #pareil pour le password mais j'ai pas encore eu le temps de fairen
    password_input.send_keys(password)
    password_input.submit()



def main():
    authentification_netflix()
    print("Hello world")


if __name__ == "__main__":
    main()
