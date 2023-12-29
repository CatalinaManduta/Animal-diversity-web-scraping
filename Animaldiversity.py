
# Project: Castration in males
# Author: Catalina Manduta
# Description: Web scrabing life history variables from: https://animaldiversity.org/accounts/

from bs4 import BeautifulSoup
import requests
import pandas as pd


df = pd.read_excel("Species.xlsx")
df['MatingSystem'] = None
df["Parental"] = None
df["Ornamentation"] = None
df["Territorial"] = None
df["Dominance"] = None
df["Movement"] = None
df["Social"] = None

scientific_names = df['lifeExpBaSTA1$vertlife']

url = 'https://animaldiversity.org/accounts/'

parental = ["female parental care", "male parental care"]
movement = ["nomadic", "migratory", "sedentary"]
social = ["solitary", "social"]
reproductive = ["year-round breeding", "seasonal breeding"]
dimo = ["male larger", "female larger", "sexes alike"]


for index, row in df.iterrows():
    name = row['lifeExpBaSTA1$vertlife']
    url_new = url+name+"/"
    print(url_new)
    response = requests.get(url_new)
    page_content = response.text
    soup = BeautifulSoup(page_content, 'html.parser')
    titles = soup.find_all('li', class_="keywords-header")
    for title in titles:
        try:
            if title.text.strip() == "Mating System":
                next_sibling = title.find_next_sibling("li")
                lis = []
                while next_sibling is not None:
                    if next_sibling.find("a"):
                        mating = next_sibling.find("a").text
                    else:
                        mating = next_sibling.find("span").text
                    lis.append(mating)
                    next_sibling = next_sibling.find_next_sibling("li")
                print(lis)
                df.at[index, 'MatingSystem'] = ', '.join(lis)
            if title.text.strip() == "Sexual Dimorphism":
                next_sibling = title.find_next_sibling("li")
                lis1 = []
                while next_sibling is not None:
                    if next_sibling.find("a"):
                        sexual_dimorphism = next_sibling.find("a").text
                    else:
                        sexual_dimorphism = next_sibling.find("span").text
                    lis1.append(sexual_dimorphism)
                    next_sibling = next_sibling.find_next_sibling("li")
                lis1_1 = [i for i in lis1 if i not in dimo]
                df.at[index, "Ornamentation"] = ', '.join(lis1_1)
            if title.text.strip() == "Parental Investment":
                next_sibling = title.find_next_sibling("li")
                lis4 = []
                while next_sibling is not None:
                    if next_sibling.find("a"):
                        par = next_sibling.find("a").text
                    else:
                        par = next_sibling.find("span").text
                    lis4.append(par)
                    next_sibling = next_sibling.find_next_sibling("li")
                print(lis4)
                if all(item in parental for item in lis4):
                    df.at[index, "Parental"] = "Both"
                else:
                    for i in lis4:
                        if i == "female parental care":
                            df.at[index, "Parental"] = "Female"
                        if i == "male parental care":
                            df.at[index, "Parental"] = "Male"
            if title.text.strip() == "Key Behaviors":
                next_sibling = title.find_next_sibling("li")
                lis6 = []
                while next_sibling is not None:
                    if next_sibling.find("a"):
                        active = next_sibling.find("a").text
                    else:
                        active = next_sibling.find("span").text
                    lis6.append(active)
                    next_sibling = next_sibling.find_next_sibling("li")
                intersection = set(lis6).intersection(movement)
                intersection = list(intersection)
                df.at[index, "Movement"] = ', '.join(intersection)
                intersection = set(lis6).intersection(social)
                intersection = list(intersection)
                df.at[index, "Social"] = ', '.join(intersection)
                for i in lis6:
                    if i == "territorial":
                        df.at[index, "Territorial"] = "territorial"
                    if i == "dominance hierarchies":
                        df.at[index, "Dominance"] = "dominance hierarchies"
            df.to_excel("Species_TotalNewCheck.18.April.xlsx", index=False)
        except AttributeError:
            continue



