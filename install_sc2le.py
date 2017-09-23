import os
from subprocess import call
import logging

import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)

unzip_password = 'iagreetotheeula'


def check_if_startcraftII_exists():
    environment_variable_exists = 'SC2PATH' in os.environ
    root_SC2_directory_exists   = os.path.isdir('{}/{}'.format(os.getenv("HOME"),'StarCraftII'))
    return environment_variable_exists or root_SC2_directory_exists


def find_latest_starcraftII_link(soup):
    linux_packages_tag  = soup.find('a', href='#linux-packages')
    all_distributions   = linux_packages_tag.parent.findNextSibling()
    latest_distribution = all_distributions.findChildren()[0].findChild() 
    download_link = latest_distribution.attrs['href']
    return download_link


def download_latest_starcraftII():
    logging.info('Downloading Starcraft II (linux)')
    logging.info('This will take a while')
    blizzard_repo = 'https://github.com/Blizzard/s2client-proto#downloads'
    response = requests.get(blizzard_repo)
    soup = BeautifulSoup(response.content, 'lxml')

    download_link = find_latest_starcraftII_link(soup)

    request = requests.get(download_link, stream=True)
    logging.info('Size of StarcraftII distribution: {}'.format(len(request.content)))
    with open('StarcraftII.zip', 'wb') as f:
        for chunk in request.iter_content(chunk_size=4096):
            if chunk: 
                f.write(chunk)
        starcraft_zip = os.path.abspath(f.name)
    logging.info('Starcraft II finished downloading')
    return starcraft_zip


def extract_starcraftII(starcraft_zip):
    logging.info('Extracting Starcraft II in directory {}'.format(get_starcraft_directory()))
    extract_zip_file_into_directory(starcraft_zip, get_starcraft_directory())


def find_all_map_links(soup):
    map_packs_tag       = soup.find('a', href='#map-packs')
    all_map_packs_list  = map_packs_tag.parent.findNextSibling()
    clean_all_map_packs_list = [ list_item.findChild() for list_item in all_map_packs_list.findChildren() if list_item.findChild() is not None]
    all_maps  = [map_tag.attrs['href'] for map_tag in clean_all_map_packs_list]
    return all_maps


# test
def download_maps():
    logging.info('Downloading all available maps')
    blizzard_repo = 'https://github.com/Blizzard/s2client-proto#downloads'
    response = requests.get(blizzard_repo)
    soup = BeautifulSoup(response.content, 'lxml')

    download_links = find_all_map_links(soup)
    number_of_map_sets = len(download_links)
    logging.info('Found {} available sets of maps'.format(number_of_map_sets))

    map_zips = []
    for number, map_link in enumerate(download_links):
        logging.info('Downloading: {} {}/{}'.format(map_link, number+1, number_of_map_sets))
        map_zip_binary = requests.get(map_link)
        with open(str(number) + 'temp.zip','wb') as f:
            f.write(map_zip_binary.content)
            map_zips.append(os.path.abspath(f.name))

    return map_zips


def extract_maps(map_zips):
    logging.info('Extracting maps')
    for map_zip in map_zips:
        logging.info('Extracting {} into Starcraft Maps Folder'.format(map_zip))
        extract_zip_file_into_directory(map_zip, get_starcraft_directory() + 'Maps/')
    pass


def extract_zip_file_into_directory(zip_file, directory):
    success = call(['unzip','-P', unzip_password, zip_file,'-d',directory])
    return success


def get_starcraft_directory():
    return os.getenv('SC2PATH') if 'SC2PATH' in os.environ else os.getenv('HOME') + '/StarCraftII/'


# Main
def install_sc2le(starcraft_directory=os.getenv('Home')):
    starcraft_exists = check_if_startcraftII_exists()
    logging.info('StarcraftII is {}'.format('PRESENT' if starcraft_exists else 'MISSING'))
    if not starcraft_exists:
        logging.info('Downloading StarcraftII from https://github.com/Blizzard/s2client-proto#downloads')
        starcraft_zip = download_latest_starcraftII()
        extract_starcraftII(starcraft_zip)
        os.remove(starcraft_zip)

    map_zips = download_maps()
    extract_maps(map_zips)
    for zip_file in map_zips:
        os.remove(zip_file)

    # Add replays as well?

install_sc2le()
