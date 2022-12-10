import requests
from bs4 import BeautifulSoup
import pandas as pd


URL = 'https://www.vgchartz.com/gamedb/'
IMG_URL = 'https://www.vgchartz.com'
query = ''
SEARCH_URL = 'https://www.vgchartz.com/games/games.php?page={pageNo}&results=200&genre={query}&order=Sales&ownership=Both&direction=DESC&showtotalsales=1&shownasales=0&showpalsales=0&showjapansales=0&showothersales=0&showpublisher=1&showdeveloper=0&showreleasedate=1&showlastupdate=1&showvgchartzscore=1&showcriticscore=1&showuserscore=1&showshipped=1'
r = requests.get(URL)

DATASET = {
    'id':[],
    'name':[],
    'publisher':[],
    'vgchartz_score':[],
    'critic_score':[],
    'user_score':[],
    'total_shipped':[],
    'total_sales':[],
    'release_date':[],
    'last_updated':[],
    'genre':[],
    'img_url':[]
}

soup = BeautifulSoup(r.content, 'html.parser')

genres = soup.find('select', attrs={"name":"genre"})
genres_list = [genre.text for genre in genres if len(genre.text)>1]


def create_genreSearch_url(genre, pageNo):

    
    genre = genre.replace(' ','+')
    genresUrl = SEARCH_URL.format(pageNo=pageNo, query=genre)

    return genresUrl

def genreBasedData(genre):

    print("STARTING")
    pageNo = 1
    while True:
        
        url = create_genreSearch_url(genre, pageNo)
        try:
            req = requests.get(url)
        except:
            break    

        soup = BeautifulSoup(req.content, 'html.parser')
        games = soup.find('div', attrs={"id":"generalBody"}).findChild('table')
        
        game = games.findAll('tr', attrs={"style":not None})
        if not game:
            break
        for g in game:

            info = g.findAll('td')
            info_list = []
            for i in info:
                img_div = i.find('div', attrs={"id":"photo3"})
                if img_div is not None:
                    img = img_div.find('img')
                    img_link = IMG_URL + str(img['src'])
                if '\n' not in i.text:
                    info_list.append(i.text)
            info_list.append(genre)
            info_list.append(img_link)

            for i,v in enumerate(DATASET.values()):
                v.append(info_list[i])
        pageNo += 1

for genre in genres_list:
    genreBasedData(genre)
    print(f"DONE WITH {genre}")

df = pd.DataFrame(DATASET)
print(df.head())
print(df.shape)

df.to_csv('games.csv', index=False)






    

    

