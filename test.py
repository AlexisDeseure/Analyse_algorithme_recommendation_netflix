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
    
    driver.get("https://www.netflix.com/fr-en/login")   #accès à la page de connexion netflix
    
    #A changer selon le compte utilisé
    username = "usename"
    password = "mdp"

    #authentification
    username_input = wait.until(EC.visibility_of_element_located((By.ID, "id_userLoginId")))   #cherche à partir de l'id l'encart pour l'identifiant
    username_input.send_keys(username)  #envoie l'identifiant
    username_input = wait.until(EC.visibility_of_element_located((By.ID, "id_password")))   #cherche à partir de l'id l'encart pour le mot de passe
    username_input.send_keys(password) #envoie le mot de passe
    driver.find_element(By.CSS_SELECTOR, 'button[data-uia="login-submit-button"]').click() #clique sur le bouton de connexion
    profil_selection = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'button[data-uia="action-select-profile+secondary"]')))
    profil_selection.click()
    time.sleep(500)
    driver.quit() #ferme le navigateur



def main():
    authentification_netflix()
    print("Hello world")


if __name__ == "__main__":
    main()