from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from os import mkdir
from os.path import exists
from os import system
from requests import get
if not exists("songs"):
    mkdir("songs")
firefox = webdriver.Firefox()
firefox.get("https://babysongs.ru")
cats = firefox.find_elements(By.CLASS_NAME, "j_item")
lnks = []
sleep(5)
for cat in cats:
    lnks.append(cat.get_attribute("href"))

for lnk in lnks:
    firefox.get(lnk)
    sleep(1)
    downloads = firefox.find_elements(By.CLASS_NAME, "download-svg")
    for download_button in downloads:
        path = download_button.get_attribute("href")
        print(path)
        let = path.split("/")
        filename = let[len(let) - 1]
        songfile = open("songs/" + filename, "wb")
        for chunk in get(path).iter_content(chunk_size=8192):
            songfile.write(chunk)
        print("Downloaded: " + filename)