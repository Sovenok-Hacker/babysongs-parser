from bs4 import BeautifulSoup as BS
from requests import get
from os import mkdir
from os.path import exists
from rich.progress import track
if not exists('songs'):
    mkdir('songs')
headers = {
    'Users-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:96.0) Gecko/20100101 Firefox/96.0',
    'Accept': '*/*'
}
data = get('https://babysongs.ru/artisty', headers=headers).content.decode('utf-8')
artisty = []
links = []
soup = BS(data, 'lxml')
for artist in soup.find_all('a', class_='sda link-type_1'):
    if 'artisty' in artist.get('href'):
        artisty.append('https://babysongs.ru' + artist.get('href'))
for step in track(range(len(artisty))):
    data = get(artisty[step], headers=headers).content.decode('utf-8')
    soup = BS(data, 'lxml')
    for link in soup.find_all(class_='download-svg'):
        print('Found: https://babysongs.ru' + link.get('href'))
        links.append('https://babysongs.ru' + link.get('href'))
for step in track(range(len(links))):
    let = links[step].split("/")
    filename = let[-1]
    songfile = open("songs/" + filename, "wb")
    for chunk in get(links[step]).iter_content(chunk_size=512):
        songfile.write(chunk)
    songfile.close()
    print("Downloaded: " + filename)
