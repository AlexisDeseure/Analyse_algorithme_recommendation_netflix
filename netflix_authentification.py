import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options #permet de ne pas ouvrir le navigateur
from bs4 import BeautifulSoup
import pandas as pd
from dotenv import load_dotenv #permet de définir des variables d'environnement pour cacher les identifiants
import os



def authentification_netflix():
    """fonction permettant de s'authentifier sur netflix"""
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
        (By.XPATH, f"//a[@href='/SwitchProfile?tkn={os.getenv('TOKEN')}']")))
    element.click()

    

def recuperer_liste_ligne():
    '''récupérer la liste des noms et liens des séries/films situés sur la ligne donnée en paramètre'''
    wait.until(EC.presence_of_element_located((By.ID, 'main-view')))
    # Appuyer sur la touche bas dans la fenêtre active
    for _ in range(150):
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)
    
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
        data.append([f"https://www.netflix.com{href}", t])
    df = pd.DataFrame(data, columns=['liens', 'titres_catégories'])
    # Stockage du DataFrame dans un fichier CSV
    df.to_csv('categories.csv', index=False)

def recuperer_titres_catégorie(ligne,directory_name):
    """récupérer les titres de la catégorie située sur la ligne donnée en paramètre"""
    driver.get(ligne[1])
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
        data.append([t,href.split('?')[0][7:],src]) #href.split('?')[0][7:] permet de récupérer l'ID du film/série à partir du href de la balise <a>
    df = pd.DataFrame(data, columns=['titres', 'ID', 'liens_images'])
    df.to_csv(f'./{directory_name}/{ligne[2]}.csv', index=False)
    
def recuperer_tous_titres():
    '''récupérer les titres de toutes les catégories'''
    directory_name = "listes_csv"
    if not os.path.exists(directory_name):
        # si le répertoire n'existe pas, créez-le
        os.mkdir(directory_name)
    df = pd.read_csv('categories.csv')
    i = 0
    longueur = len(df)
    for lignes in df.itertuples():
        i+=1
        print(f"{i}/{longueur} : {lignes[2]} en cours de récupération...", end='', flush=True)
        recuperer_titres_catégorie(lignes,directory_name)
        print(f"\r{i}/{longueur} : {lignes[2]} récupéré"+" "*50)

def parcourt_csv(file,nom_categorie):
    df = pd.read_csv(file)
    data = []
    time.sleep(1) #important pour que la requete fonctionne
    for lignes in df.itertuples():
        driver.get(f"https://www.netflix.com/title/{lignes.ID}")
        time.sleep(1) #important pour l'affichage
        wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="previewModal--detailsMetadata detail-modal has-smaller-buttons"]')))
        html = driver.find_element(By.XPATH, '//div[@class="previewModal--detailsMetadata detail-modal has-smaller-buttons"]').get_attribute('innerHTML')
        soup = BeautifulSoup(html, 'html.parser')
        div_year = soup.find('div', {'class': 'year'})
        span_duration = soup.find('span', {'class': 'duration'})
        span_score = soup.find('span', {'class': 'match-score'})
        span_maturity = soup.find('span', {'class': 'maturity-number'})
        div_description = soup.find('div', {'class': 'ptrack-content'})
        span_prevent = soup.find('span', {'class': 'ltr-1q4vxyr'})
        div_mise_en_avant_supp = soup.find('div', {'class': 'supplemental-message'})
        if div_mise_en_avant_supp is not None:
            div_mise_en_avant_supp = True
        else:
            div_mise_en_avant_supp = False
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'about-wrapper')))
        html = driver.find_element(By.CLASS_NAME, 'about-wrapper').get_attribute('innerHTML')
        soup = BeautifulSoup(html, 'html.parser')
        div_tags = soup.find_all('div', {'class': 'previewModal--tags'})
        tab_a_propos=[None,None,None,None,None]
        dic_a_propos = {"Réalisation": 0,
                        "Distribution": 1,
                        "Scénariste": 2,
                        "Genres": 3, 
                        "Ce film est": 4,
                        "Ce programme est": 4
                        }
        for tags in div_tags:
            categ=tags.find('span', {'class': 'previewModal--tags-label'})
            for key in dic_a_propos.keys():
                if key in categ.text:
                    valeurs = tags.find_all('a', {'historystate': '[object Object]'})
                    for valeur in valeurs:
                        if tab_a_propos[dic_a_propos[key]] is None:
                            tab_a_propos[dic_a_propos[key]] = valeur.text.strip().replace(',', '')
                        else:
                            tab_a_propos[dic_a_propos[key]] += f",{valeur.text.strip().replace(',', '')}"
        try:
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'moreLikeThis--container')))
            html = driver.find_element(By.CLASS_NAME, 'moreLikeThis--container')
            html = html.get_attribute('innerHTML')
            soup = BeautifulSoup(html, 'html.parser')
            div_container = soup.find_all('div', {'class': 'titleCard-imageWrapper'})
            recommendations = ""
            for div in div_container:
                div = div.find('div', {'class': 'ptrack-content'}).get("data-ui-tracking-context")
                start_index = div.find('%22video_id%22:') + len('%22video_id%22:') #on cherche l'index du début de l'ID
                end_index = div.find(',', start_index) #on cherche l'index de la fin de l'ID
                recommendations += div[start_index:end_index]+"," #on récupère l'ID
            recommendations = recommendations[:-1] #on enlève la dernière virgule
        except:
            recommendations = None
        data.append([nom_categorie,
                     lignes.titres,
                     lignes.ID,
                     lignes.liens_images,
                     div_year.text if div_year is not None else None,
                     span_duration.text if span_duration is not None else None,
                     span_score.text if span_score is not None else None,
                     span_maturity.text if span_maturity is not None else None,
                     div_description.text if div_description is not None else None,
                     span_prevent.text if span_prevent.text is not None else None,
                     div_mise_en_avant_supp,
                     tab_a_propos[0],
                     tab_a_propos[1],
                     tab_a_propos[2],
                     tab_a_propos[3],
                     tab_a_propos[4],
                     recommendations])
    df = pd.DataFrame(data, columns=['categorie',
                                     'titres', 
                                     'ID', 
                                     'liens_images', 
                                     'année', 
                                     'durée', 
                                     'score_recommendation', 
                                     'age_conseillé', 
                                     'description', 
                                     'prévention', 
                                     'mise_en_avant_supplémentaire', 
                                     'réalisation', 
                                     'distribution', 
                                     'scénariste', 
                                     'genres', 
                                     'avertissement_programme',
                                     'recommendations'])
    return df


def parcourt_titres_informations():
    """parcourt les fichiers csv contenant les titres et récupère les informations de chaque titre"""
    directory = "listes_csv"
    longueur = len(os.listdir(directory))
    i=0
    first = True
    for file in os.listdir(directory):
        i+=1
        print(f"{i}/{longueur} : {file} en cours de traitement...", end='', flush=True)
        file_path = os.path.join(directory, file)
        # Vérifier si le chemin correspond à un fichier csv et ne pas inclure les sous-dossiers
        if os.path.isfile(file_path) and file.endswith('.csv'):
            if first:
                df = parcourt_csv(file_path,file[:-4])
                df.to_csv('bdd_series.csv', index=False)
                first = False
            else:
                df = pd.read_csv('bdd_series.csv')
                df = pd.concat([df, parcourt_csv(file_path,file[:-4])],axis=0)
                df.to_csv('bdd_series.csv', index=False)
        print(f"\r{i}/{longueur} : {file}  traité"+" "*50)
    


def main():
    print("Authentification en cours...")
    authentification_netflix()
    print("Authentification réussie\n")
    print("Récupération des catégories en cours...")
    recuperer_liste_ligne()
    print("Catégories récupérées\n")
    print("Récupération des titres en cours...")
    recuperer_tous_titres()
    print("Titres récupérés\n")
    print("Récupération des informations en cours...")
    parcourt_titres_informations()
    print("Informations récupérées\n")
    time.sleep(10)


if __name__ == "__main__":

    # Configuration de Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Exécuter Chrome en mode headless

    # Création de l'instance de Chrome avec les options
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 10)
    main()
    driver.quit()
    

