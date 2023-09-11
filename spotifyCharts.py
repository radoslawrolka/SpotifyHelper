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
        titleAuthor = td_elements[i + 2].get_text("|", strip=True).split('|')
        strems = td_elements[i + 3].get_text(strip=True)
        year = td_elements[i + 5].get_text(strip=True)
        top_songs.append((pos, titleAuthor[0], titleAuthor[1], strems, year))

    return top_songs


# Get most streamed artists --------------------------------------------------------------------------------------------
def get_top_artists():
    pass


# Get most streamed albums ---------------------------------------------------------------------------------------------

get_top_songs()
# get_top_artists()
# get_top_albums()
