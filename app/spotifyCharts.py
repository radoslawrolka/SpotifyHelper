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
        titleAuthor = td_elements[i + 2].get_text("|", strip=True).split('|')
        top_songs.append({
            'position': td_elements[i].get_text(strip=True),
            'image': td_elements[i + 1].find('img')['src'],
            'title': titleAuthor[0],
            'artist': titleAuthor[1],
            'streams': td_elements[i + 3].get_text(strip=True),
            'year': td_elements[i + 5].get_text(strip=True)
        })

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
        top_artists.append({
            'position': td_elements[i + 1].get_text(strip=True),
            'image': td_elements[i + 2].find('img')['src'],
            'artist': td_elements[i + 3].get_text(strip=True),
            'streams': td_elements[i + 5].get_text(strip=True)
        })

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
        albumArtist = td_elements[i + 5].get_text('|', strip=True).split('|')
        top_albums.append({
            'position': td_elements[i + 1].get_text(strip=True),
            'image': td_elements[i + 2].find('img')['src'],
            'album': albumArtist[0],
            'artist': albumArtist[1],
            'streams': td_elements[i + 6].get_text(strip=True)
        })

    return top_albums
