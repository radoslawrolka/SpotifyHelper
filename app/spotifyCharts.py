import requests
from bs4 import BeautifulSoup


# Get most streamed songs ----------------------------------------------------------------------------------------------
def get_top_songs():
    url = 'https://chartmasters.org/spotify-most-streamed-songs/'
    r = requests.get(url)
    data = r.text
    data = data[data.find('table_3_row_0'):data.find('!-- /Table body -->')]

    soup = BeautifulSoup(data, 'html.parser')
    td_elements = soup.find_all('td', {'style': ''})

    top_songs = []
    for i in range(0, len(td_elements), 6):
        pos = td_elements[i].get_text(strip=True)
        imgLink = td_elements[i+1].find('img')['src']
        titleAuthor = td_elements[i + 2].get_text("|", strip=True).split('|')
        strems = td_elements[i + 3].get_text(strip=True)
        year = td_elements[i + 5].get_text(strip=True)
        top_songs.append((pos, imgLink, titleAuthor[0], titleAuthor[1], strems, year))

    return top_songs

# Get most streamed artists --------------------------------------------------------------------------------------------
def get_top_artists():
    url = 'https://chartmasters.org/most-streamed-artists-ever-on-spotify/?slk=hp'
    r = requests.get(url)
    data = r.text
    data = data[data.find('table_1_row_0'):data.find('!-- /Table body -->')]

    soup = BeautifulSoup(data, 'html.parser')
    td_elements = soup.find_all('td', {'style': ''})

    top_artists = []
    for i in range(0, len(td_elements), 16):
        pos = td_elements[i+1].get_text(strip=True)
        imgLink = td_elements[i + 2].find('img')['src']
        artist = td_elements[i + 3].get_text(strip=True)
        streams = td_elements[i + 5].get_text(strip=True)
        top_artists.append((pos, imgLink, artist, streams))

    return top_artists

# Get most streamed albums ---------------------------------------------------------------------------------------------
def get_top_albums():
    url = 'https://chartmasters.org/spotify-most-streamed-albums/?slk=hp'
    r = requests.get(url)
    data = r.text
    data = data[data.find('table_7_row_0'):data.find('!-- /Table body -->')]

    soup = BeautifulSoup(data, 'html.parser')
    td_elements = soup.find_all('td', {'style': ''})

    top_albums = []
    for i in range(0, len(td_elements), 12):
        pos = td_elements[i + 1].get_text(strip=True)
        imgLink = td_elements[i + 2].find('img')['src']
        albumArtist = td_elements[i + 5].get_text('|', strip=True).split('|')
        streams = td_elements[i + 6].get_text(strip=True)
        top_albums.append((pos, imgLink, albumArtist[0], albumArtist[1], streams))

    return top_albums
