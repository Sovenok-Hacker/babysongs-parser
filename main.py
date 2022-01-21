from bs4 import BeautifulSoup as bs
import requests
from os import mkdir
from os.path import exists
data = requests.get('https://babysongs.ru/jenre').content.decode('utf-8')
soup = bs(data, 'lxml')
jenres = soup.find_all("a", class_="sda link-type_1")
jtext = []
links = []
for jenre in jenres:
    if not jenre == '/terms-conditions':
        jtext.append('https://babysongs.ru' + jenre.get('href'))
for jenre in jtext:
    data = requests.get(jenre).content.decode('utf-8')
    soup = bs(data, 'lxml')
    songs = soup.find_all(class_="download-svg")
    for song in songs:
        links.append('https://babysongs.ru' + song.get('href'))
if not exists("songs"):
    mkdir("songs")
for link in links:
    let = link.split("/")
    filename = let[-1]
    songfile = open("songs/" + filename, "wb")
    for chunk in requests.get(link).iter_content(chunk_size=512):
        songfile.write(chunk)
    songfile.close()
    print("Downloaded: " + filename)