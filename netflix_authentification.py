import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
from dotenv import load_dotenv #permet de définir des variables d'environnement pour cacher les identifiants
import os



def authentification_netflix():
    driver.get("https://www.netflix.com/fr-en/login")  # accès à netflix

    # A changer selon le compte utilisé
    load_dotenv('variables_de_connexion.env')
    username = os.getenv('IDENTIFIANT')
    password = os.getenv('MOT_DE_PASSE')

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

    

def recuperer_liste_ligne():
    '''récupérer la liste des noms et liens des séries/films situés sur la ligne donnée en paramètre'''
    wait.until(EC.presence_of_element_located((By.ID, 'main-view')))
    time.sleep(10)
    #récupération du code html
    html = driver.find_element(By.ID,'main-view').get_attribute('innerHTML')
    #création d'un objet BeautifulSoup pour pouvoir parser le code html
    soup = BeautifulSoup(html, 'html.parser')
    #récupération des balises <a> qui contiennent les liens et les noms des séries/films (class="rowTitle ltr-0")
    a_tags = soup.find_all('a', {'class': 'rowTitle ltr-0'})
    # divs = soup.find_all('div', {'class': 'row-header-title'})
    divs = soup.select('a > div.row-header-title')
    textes = [div.text for div in divs]
    data = []
    # print(f"\n\n\n\n{a_tags}")
    # print(textes)
    for a,t in zip(a_tags, textes):
        href = a.get('href')
        data.append([href, t])
    df = pd.DataFrame(data, columns=['liens', 'titres_catégories'])
    # Stockage du DataFrame dans un fichier CSV
    df.to_csv('data.csv', index=False)

def recuperer_titres_catégorie(ligne,directory_name):
    driver.get(f"https://www.netflix.com{ligne[1]}")
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'ltr-1pq5s1g')))
    time.sleep(5)
    html = driver.find_element(By.CLASS_NAME,'ltr-1pq5s1g').get_attribute('innerHTML')
    soup = BeautifulSoup(html, 'html.parser')
    a_tags = soup.find_all('a', {'class': 'slider-refocus'})
    img_tags = soup.find_all('img', {'class': 'boxart-image boxart-image-in-padded-container'})
    ps = soup.find_all('p', {'class': 'fallback-text'})
    textes = [p.text for p in ps]
    data = []
    for a,img,t in zip(a_tags,img_tags,textes):
        href = a.get('href')
        src = img.get('src')
        data.append([t,href,src])
    df = pd.DataFrame(data, columns=['titres', 'liens', 'liens_images'])
    df.to_csv(f'./{directory_name}/{ligne[2]}.csv', index=False)
    
def recuperer_tous_titres():
    directory_name = "listes_csv"
    if not os.path.exists(directory_name):
        # si le répertoire n'existe pas, créez-le
        os.mkdir(directory_name)
    df = pd.read_csv('data.csv')
    for lignes in df.itertuples():
        print(lignes[2]+" en cours de récupération")
        recuperer_titres_catégorie(lignes,directory_name)
        print(lignes[2]+" récupéré")

def main():
    authentification_netflix()
    recuperer_liste_ligne()
    recuperer_tous_titres()
    time.sleep(10)


if __name__ == "__main__":
    # Configuration du navigateur
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    main()
    driver.quit()
    

