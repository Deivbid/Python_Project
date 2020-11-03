import numpy as np
from bs4 import BeautifulSoup as bs
import requests
import re
import json
import pandas as pd

url = 'http://sofifa.com/players?offset=0'


def soup_maker(url):
    r = requests.get(url)
    markup = r.content
    soup = bs(markup, 'lxml')
    return soup


def find_top_players(soup):
    players = []
    table = soup.find('table', {'class': 'table-hover'})
    tbody = table.find('tbody')
    all_a = tbody.find_all('a', {'class': 'tooltip'})
    for player in all_a:
        final_details = {}
        final_details['short_name'] = player.text
        print("Importando Jugador: ", final_details['short_name'])
        final_details.update(player_all_details(
            'http://sofifa.com' + player['href']))
        # print(final_details)
        players.append(final_details)
    return players


def find_player_info(soup):
    try:
        player_data = {}
        player_data['image'] = soup.find('img')['data-src']
        player_data['full_name'] = soup.find('h1').text.split(' (')[0]
        span = soup.find(
            'div', attrs={'class': 'bp3-text-overflow-ellipsis'}).text.strip()
        dob = re.search('(\(.*)\)', span).group(0)
        player_data['dob'] = dob.replace('(', '').replace(')', '')
        infos = span.replace(dob + ' ', '').split(' ')
        nPositions = len(soup.find_all('span', {'class': 'pos'}))
        player_data['pref_pos'] = ', '.join(
            infos[0:nPositions]) if nPositions > 1 else infos[0]
        player_data['age'] = int(infos[nPositions].split('y')[0])
        player_data['weight'] = int(infos[nPositions + 2].replace('lbs', ''))
    except: 
        print("Hubo un problema")
    finally:
        return(player_data)


def find_player_stats(soup):
    player_data = {}
    info = re.findall('\d+', soup.text)
    player_data['rating'] = int(info[0])
    player_data['potential'] = int(info[1])
    player_data['value'] = int(info[2])
    player_data['wage'] = int(info[3])
    return(player_data)


def find_player_secondary_info(soup):
    try:
        player_data = {}
        player_data['preff_foot'] = soup.find(
            'label', text='Preferred Foot').parent.contents[1].strip('\n ')
        infoColumns = soup.find_all('div', {'class': 'column col-3'})
        player_data['club'] = infoColumns[len(infoColumns) - 1].find('a').text
        print(player_data['club'])
        player_data['club_pos'] = soup.find('label', text='Position')\
            .parent.find('span').text
        player_data['club_jersey'] = soup.find('label', text='Jersey Number')\
            .parent.contents[1].strip('\n ')
        if soup.find('label', text='Joined'):
            player_data['club_joined'] = soup.find('label', text='Joined')\
                .parent.contents[1].strip('\n ')
        player_data['contract_valid_until'] = soup.find(
            'label', text='Contract Valid Until')\
            .parent.contents[1].strip('\n ')
    except:
        print("Hubo un problema")
    finally:
        return(player_data)


def find_fifa_info(soup):
    try:
        player_data = {}
        for skill in soup:
            lis = skill.find_all('li')
            for stat in lis:
                name = ''
                text = stat.text.split(' ')
                point = text[0]
                if(len(text) > 2):
                    name = '_'.join(text[1:]).replace('"\n"', '').rstrip()
                else:
                    name = text[1]
                player_data[name] = point
    except:
        print('Hubo un problema')
    finally:
        return player_data


def player_all_details(url):
    all_details = {}
    soup = soup_maker(url)
    player_info = soup.find('div', {'class': 'bp3-card player'})
    all_details.update(find_player_info(player_info))
    player_stats = soup.find('section', {'class': 'spacing'})
    all_details.update(find_player_stats(player_stats))
    secondary_info = soup.find_all('div', {'class': 'column col-12'})[2]
    all_details.update(find_player_secondary_info(secondary_info))
    fifa_info = soup.find_all('div', {'class': 'column col-3'})[7:14]
    all_details.update(find_fifa_info(fifa_info))
    return(all_details)


soup = soup_maker(url)
players = find_top_players(soup)
df = pd.DataFrame(players)
print(df['short_name'])
df.to_csv('Players_2.csv', index=False)

