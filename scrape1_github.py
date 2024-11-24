import requests
import re
from bs4 import BeautifulSoup
import csv
# URL de la page à scraper
url=""
# Faire une requête GET
response = requests.get(url)

# Vérifier si la requête a réussi
try:
    html_content = response.text
    print("Requête réussie")
    soup = BeautifulSoup(response.content, 'html.parser')
     
    # Trouver toutes les balises <a>
    a_tags = soup.find_all('a')

    # Liste pour stocker les données
    data = []
    i=0
    # Parcourir chaque balise <a> pour extraire les informations
    for a_tag in a_tags:
        i+=1
        if a_tag.find('b'):
            #initialization
            desc_lieu = None
            horaires = None
            Tarifs = None
            Acces = None
            Distinctions = None
            b_tag = a_tag.find('b')  # Trouver la balise <b>
            href = "https"+a_tag["href"].lstrip("..")
            resp = requests.get(href)
            html_content = resp.text
            soup1 = BeautifulSoup(resp.content, 'html.parser')
            #extraire les deux lignes d addresses
            adresse=soup1.find('fieldset')
            if adresse!=None:
                adresse_td=adresse.find('td')
                result = []
                for child in adresse_td.contents:
                    # Si on rencontre <a>, arrêter l'extraction
                    if child.name == "a":
                        break
                    # Ajouter le texte ou la balise précédente
                    result.append(str(child).strip())
                if 2<=len(result):
                    adresse=result[2] 
                    adresse = re.sub(r'\d+','',adresse).strip() #annuler l adresse postale
            print(href)
            print(adresse)
           
            #fin
            h3_tags = soup1.find_all('h3')
            for h3_tag in h3_tags:
                p_tag = h3_tag.find_next('p')
                if p_tag:
                    h3_tag_text=h3_tag.text
                    p_tag_text=p_tag.get_text(strip=True)
                    match h3_tag_text:
                        case "Ce qu'il faut savoir :" :
                            desc_lieu = p_tag_text
                        case "Horaires :":
                            horaires = p_tag_text
                        case "Tarifs :":
                            Tarifs =p_tag_text
                        case "Accès :":
                            Acces=p_tag_text
                        case "Distinctions, labels :":
                            Distinctions = p_tag_text

                        
                    

        

        
            if b_tag:
                theme = b_tag.text.strip()
                theme = re.sub(r'\(\d+ photos\)','',theme)# supprimer (* photos)
                theme= re.sub(r'\d+ -','',theme) #supprimer (*  - )
                lieu = theme  # Lieu statique dans cet exemple (à adapter selon les besoins)
                
                # Ajouter les données à la liste
            data.append({"theme": "archéologie - musées et fouilles",
                        "lieu": lieu,
                        "adresse":adresse,
                        "description du lieu": desc_lieu,
                        "Tarifs":Tarifs,
                        "Distinction, labels":Distinctions,
                        "Acces":Acces,
                        "horaires":horaires,   
                        })
        
           
       
    # Chemin du fichier CSV
    csv_file = "archéologie - musées et fouilles"

    # Écrire les données dans le fichier CSV
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["theme", "lieu","adresse","description du lieu","Tarifs","Distinction, labels",
                                 "Acces","horaires" ],escapechar='\\')
        writer.writeheader()  # Écrire l'en-tête
        writer.writerows(data)  # Écrire les lignes de données

    print(f"Fichier CSV '{csv_file}' enregistré avec succès.")

except requests.exceptions.HTTPError as http_err:
    print("Erreur lors de la requête :")
    # Handle HTTP errors (e.g., 404, 403, 500)
    print(f"HTTP error occurred: {http_err}")  # e.g., 404 Not Found
except requests.exceptions.ConnectionError as conn_err:
    # Handle connection errors (e.g., DNS failure, refused connection)
    print(f"Connection error occurred: {conn_err}")
except requests.exceptions.Timeout as timeout_err:
    # Handle timeout errors
    print(f"Timeout error occurred: {timeout_err}")
except requests.exceptions.RequestException as req_err:
    # Handle any other request-related errors
    print(f"An error occurred: {req_err}")
    