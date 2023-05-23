import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options #permet de ne pas ouvrir le navigateur
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import pandas as pd
from dotenv import load_dotenv #permet de définir des variables d'environnement pour cacher les identifiants
import os




def authentification_netflix(headless=True):
    """fonction permettant de s'authentifier sur netflix"""
    # Configuration de Chrome
    chrome_options = Options()
    if (headless):
        chrome_options.add_argument("--headless")  # Exécuter Chrome en mode headless
    chrome_options.add_argument("--silent") # Exécuter Chrome en mode silencieux
    chrome_options.add_argument("--disable-logging")  # Désactiver les messages de la console
    chrome_options.add_argument("--log-level=3")  # Définir le niveau de journalisation de la console
    chrome_options.add_argument("--mute-audio") # Désactiver le son

    # Création de l'instance de Chrome avec les options
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 10)
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
    return driver

    

def recuperer_liste_ligne(driver):
    '''récupérer la liste des noms et liens des séries/films situés sur la ligne donnée en paramètre'''
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, 'main-view')))
    # Appuyer sur la touche bas dans la fenêtre active
    for _ in range(300):
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
    df.to_csv('categories.csv', index=False,sep=';')

def recuperer_titres_catégorie(driver,ligne,directory_name):
    """récupérer les titres de la catégorie située sur la ligne donnée en paramètre"""
    wait = WebDriverWait(driver, 10)
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
    df.to_csv(f'./{directory_name}/{ligne[2]}.csv', index=False,sep=';')
    
def recuperer_tous_titres(driver):
    '''récupérer les titres de toutes les catégories'''
    directory_name = "listes_csv"
    if not os.path.exists(directory_name):
        # si le répertoire n'existe pas, créez-le
        os.mkdir(directory_name)
    df = pd.read_csv('categories.csv',sep=';')
    i = 0
    longueur = len(df)
    for lignes in df.itertuples():
        i+=1
        print(f"{i}/{longueur} : {lignes[2]} en cours de récupération...", end='', flush=True)
        recuperer_titres_catégorie(driver,lignes,directory_name)
        print(f"\r{i}/{longueur} : {lignes[2]} récupéré"+" "*50)

def relancer_driver(driver):
    '''relance le driver'''
    driver.quit()
    print("\nLa présence de l'élément n'a pas pu être vérifiée dans le délai imparti.")
    #création d'un nouveau driver pour contourner le ban de Netflix
    driver = authentification_netflix()
    time.sleep(3)
    return driver

def parcourt_csv(driver,file,nom_categorie,longueur_totale,index_total,like=None):
    '''parcourt le fichier csv donné en paramètre et récupère les informations de chaque film/série'''
    wait = WebDriverWait(driver, 10)
    df = pd.read_csv(file, sep=';')
    data = []
    time.sleep(1) #important pour que la requete fonctionne
    longueur = len(df)
    i=0
    for lignes in df.itertuples():
        i+=1
        print(f"\r{index_total}/{longueur_totale} : \"{nom_categorie}\" en cours de traitement... {i}/{longueur}"+" "*50, end='', flush=True)
        driver.get(f"https://www.netflix.com/title/{lignes.ID}")
        time.sleep(1) #important pour l'affichage
        if like in ["like", "dislike", "love"]:
            try:
                wait.until(EC.presence_of_element_located((By.XPATH, '//button[@class="color-supplementary hasIcon round ltr-1ihscfb"]')))
                driver.find_element(By.XPATH, '//button[@class="color-supplementary hasIcon round ltr-1ihscfb"]').click()
                # ActionChains(driver).move_to_element(menu_boutons).perform()
                # time.sleep(1000)
                if like == "like":
                    try: 
                        wait.until(EC.presence_of_element_located((By.XPATH, '//button[@aria-label="Attribuer un Pouce levé"]')))
                        driver.find_element(By.XPATH, '//button[@aria-label="Attribuer un Pouce levé"]').click()
                    except:
                        pass #si le bouton like est déjà activé
                elif like == "dislike":
                    try:
                        wait.until(EC.presence_of_element_located((By.XPATH, '//button[@aria-label="Attribuer un Pouce baissé"]')))
                        driver.find_element(By.XPATH, '//button[@aria-label="Attribuer un Pouce baissé"]').click()
                    except:
                        pass #si le bouton dislike est déjà activé
                else :
                    try:
                        wait.until(EC.presence_of_element_located((By.XPATH, '//button[@aria-label="Attribuer deux pouces levés"]')))
                        driver.find_element(By.XPATH, '//button[@aria-label="Attribuer deux pouces levés"]').click()
                    except:
                        pass  #si le bouton love est déjà activé
            except Exception as e:
                print(f"Une erreur s'est produite : {str(e)}")
    
        try:
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
        except TimeoutException:
            driver = relancer_driver(driver)
            wait = WebDriverWait(driver, 10)
        if div_mise_en_avant_supp is not None:
            div_mise_en_avant_supp = True
        else:
            div_mise_en_avant_supp = False
        try:
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
        except TimeoutException:
            driver = relancer_driver(driver)
            wait = WebDriverWait(driver, 10)
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
            driver = relancer_driver(driver)
            wait = WebDriverWait(driver, 10)
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
    print(f"\r{index_total}/{longueur_totale} : \"{nom_categorie}\"  traité"+" "*50)
    return df, driver


def parcourt_titres_informations(driver, like=None):
    """parcourt les fichiers csv contenant les titres et récupère les informations de chaque titre"""
    directory = "listes_csv"
    longueur = len(os.listdir(directory))
    first = True
    i=0
    for file in os.listdir(directory):
        i+=1
        file_path = os.path.join(directory, file)
        # Vérifier si le chemin correspond à un fichier csv et ne pas inclure les sous-dossiers
        if os.path.isfile(file_path) and file.endswith('.csv'):
            if first:
                df,driver = parcourt_csv(driver, file_path,file[:-4],longueur,i,like)
                df.to_csv('bdd_series.csv', index=False, sep=';')
                first = False
            else:
                df = pd.read_csv('bdd_series.csv',sep=';')
                df_inter, driver = parcourt_csv(driver, file_path,file[:-4],longueur,i,like)
                df = pd.concat([df, df_inter],axis=0)
                df.to_csv('bdd_series.csv', index=False, sep=';')
    return driver
    
def get_first_non_null(values):
    for value in values:
        if value != 'nan':
            return value
    return None

def process_multiple_values(values, aggregation_type=False):
    '''Fonction qui permet de traiter les valeurs multiples d'une colonne :
    - si aggregation_type est False, la fonction retourne une liste de valeurs uniques séparées par des points-virgules
    - si aggregation_type est True, la fonction retourne une liste de valeurs uniques séparées par des virgules'''
    unique_values = set()
    for value in values:
        if value != 'nan':
            unique_values.update(value.split(',') if aggregation_type else [value])
    return (',' if aggregation_type else '|').join(str(v) for v in unique_values) if unique_values!=set() else None

def nombre_mise_en_avant(values):
    if all(value == 'nan' for value in values):
        return None
    return sum(values == "True")

def gestion_doublons(file_path):
    """supprime les doublons dans un fichier csv"""
    # Charger le fichier CSV dans un DataFrame pandas
    df = pd.read_csv(file_path,sep=';')
    df = df.astype(str)
    # Regrouper les données par l'ID et appliquer les opérations d'agrégation sur les colonnes pertinentes
    grouped_df = df.groupby('ID').agg({
        'categorie': lambda x: process_multiple_values(x),
        'titres': lambda x: get_first_non_null(x),
        'liens_images': lambda x: process_multiple_values(x),
        'année': lambda x: get_first_non_null(x),
        'durée': lambda x: get_first_non_null(x),
        'score_recommendation': lambda x: process_multiple_values(x),
        'age_conseillé': lambda x: get_first_non_null(x),
        'description': lambda x: process_multiple_values(x),
        'prévention': lambda x: get_first_non_null(x),
        'mise_en_avant_supplémentaire': lambda x: nombre_mise_en_avant(x),
        'réalisation': lambda x: get_first_non_null(x),
        'distribution': lambda x: get_first_non_null(x),
        'scénariste': lambda x: get_first_non_null(x),
        'genres': lambda x: get_first_non_null(x),
        'avertissement_programme': lambda x: get_first_non_null(x),
        'recommendations': lambda x: process_multiple_values(x,True)
    }).reset_index()
    grouped_df['nombre_occurrence'] = df.groupby('ID').size().reset_index(name='count')['count']
    grouped_df.to_csv(file_path[:-4] + '_modifie.csv', index=False, sep=';')

def archiver_csv():
    """Archive les fichiers CSV contenant les titres dans des dossiers"""
    directory_name = "listes_archivees"
    if not os.path.exists(directory_name):
        # Si le répertoire n'existe pas, créez-le
        os.mkdir(directory_name)

    # Recherche du dernier numéro d'itération
    last_iteration = 0
    for folder in os.listdir(directory_name):
        if folder.startswith("itération"):
            iteration_number = int(folder.split(" ")[1])
            last_iteration = max(last_iteration, iteration_number)

    # Création du nouveau dossier d'itération
    new_iteration = last_iteration + 1
    new_iteration_folder = f"itération {new_iteration}"
    new_iteration_path = os.path.join(directory_name, new_iteration_folder)
    os.mkdir(new_iteration_path)

    for file in os.listdir("listes_csv"):
        file_path = os.path.join("listes_csv", file)
        # Vérifier si le chemin correspond à un fichier CSV et ne pas inclure les sous-dossiers
        if os.path.isfile(file_path) and file.endswith('.csv'):
            # Copie du fichier dans le nouveau dossier d'itération
            new_file_path = os.path.join(new_iteration_path, file)
            os.rename(file_path, new_file_path)

def main():
    """fonction principale"""
    print("Authentification en cours...")
    driver = authentification_netflix()
    print("Authentification réussie\n")
    print("Récupération des catégories en cours...")
    recuperer_liste_ligne(driver)
    print("Catégories récupérées\n")
    print("Récupération des titres en cours...")
    recuperer_tous_titres(driver)
    print("Titres récupérés\n")
    print("Récupération des informations en cours...")
    driver = parcourt_titres_informations(driver, like=None) 
    print("Informations récupérées\n")
    print("Fermeture du navigateur...")
    driver.quit()
    print("Navigateur fermé\n")
    print("Archivage en cours...")
    archiver_csv()
    print("Archivage terminé\n")
    print("Gestion des doublons en cours...")
    gestion_doublons('bdd_series.csv')
    print("Doublons gérés\n")
    print("Fin du programme")
    

if __name__ == "__main__":
    main()
    
    

