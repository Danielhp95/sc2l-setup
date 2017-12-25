import os
from subprocess import call
import logging

import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)

unzip_password = 'iagreetotheeula'
blizzard_repo = 'https://github.com/Blizzard/s2client-proto#downloads'


def download_single_link(link):
    return requests.get(link)


def download_multiple_links(links):
    total_number_of_links = len(links)
    zip_files_directories = []
    for number, link in enumerate(links):
        logging.info('Downloading: {} {}/{}'.format(link, number+1, total_number_of_links))
        response  = download_single_link(link)
        file_name = str(number) + 'temp.zip'
        file_path = save_binary_to_file(response.content, file_name)
        zip_files_directories.append(file_path)
    return zip_files_directories


def save_binary_to_file(binary_content, file_name):
    with open(file_name, 'wb') as f:
        f.write(binary_content)
        temporary_file_path = os.path.abspath(f.name)
    return temporary_file_path


def extract_multiple_zip_files_into_directory(zips, directory):
    logging.info('Extracting files')
    for zip_file in zips:
        extract_zip_file_into_directory(zip_file, directory)
    pass


def extract_zip_file_into_directory(zip_file, directory):
    logging.info('Extracting {} into {}'.format(zip_file, directory))
    success = call(['unzip', '-P', unzip_password, zip_file, '-d', directory])
    return success


def remove_temporay_files(temporary_files):
    for zip_file in temporary_files:
        os.remove(zip_file)


def check_if_startcraftII_exists():
    environment_variable_exists = 'SC2PATH' in os.environ
    root_SC2_directory_exists   = os.path.isdir('{}/{}'.format(os.getenv("HOME"), 'StarCraftII'))
    return environment_variable_exists or root_SC2_directory_exists


def get_starcraft_directory():
    return os.getenv('SC2PATH') if 'SC2PATH' in os.environ else os.getenv('HOME')


def parse_blizzard_starcraftII_repository():
    response = requests.get(blizzard_repo)
    return BeautifulSoup(response.content, 'lxml')


def find_latest_starcraftII_link(soup):
    linux_packages_tag  = soup.find('a', href='#linux-packages')
    all_distributions   = linux_packages_tag.parent.findNextSibling()
    latest_distribution = all_distributions.findChildren()[0].findChild()
    download_link = latest_distribution.attrs['href']
    return download_link


def find_all_map_links(soup):
    map_packs_tag       = soup.find('a', href='#map-packs')
    all_map_packs_list  = map_packs_tag.parent.findNextSibling()
    clean_all_map_packs_list = [list_item.findChild() for list_item in all_map_packs_list.findChildren() if list_item.findChild() is not None]
    all_maps  = [map_tag.attrs['href'] for map_tag in clean_all_map_packs_list]
    return all_maps


def find_all_replay_links(soup):
    replay_packs_tag = soup.find('a', href='#replay-packs')
    all_replay_packs_list = replay_packs_tag.parent.findNextSibling()
    clean_all_replay_packs_list = [list_item.findChild() for list_item in all_replay_packs_list.findChildren()]
    clean_all_replay_packs_list = list(filter(lambda x: x is not None, clean_all_replay_packs_list))
    all_replays = [replay_tag.attrs['href'] for replay_tag in clean_all_replay_packs_list]
    return all_replays


def download_latest_starcraftII():
    logging.info('Downloading Starcraft II (linux)')
    logging.info('This will take a while')
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


def download_maps():
    logging.info('Downloading all available MAPS')
    soup = parse_blizzard_starcraftII_repository()
    download_links = find_all_map_links(soup)
    logging.info('Found {} available MAPS'.format(len(download_links)))
    maps_zips = download_multiple_links(download_links)
    return maps_zips


def download_replays():
    logging.info('Downloading all available REPLAYS')
    soup = parse_blizzard_starcraftII_repository()
    download_links = find_all_replay_links(soup)
    logging.info('Found {} available sets of REPLAYS'.format(len(download_links)))
    replay_pack_zips = download_multiple_links(download_links)
    return replay_pack_zips


def download_and_extract_starcraftII():
    logging.info('Downloading StarcraftII from https://github.com/Blizzard/s2client-proto#downloads')
    starcraft_zip = download_latest_starcraftII()
    extract_zip_file_into_directory(starcraft_zip, get_starcraft_directory())
    os.remove(starcraft_zip)


def download_and_extract_maps():
    map_zips = download_maps()
    maps_directory = get_starcraft_directory() + '/StarCraftII/Maps/'
    extract_multiple_zip_files_into_directory(map_zips, maps_directory)
    remove_temporay_files(map_zips)


def download_and_extract_replays():
    replay_zips = download_replays()
    replays_directory = get_starcraft_directory() + '/StarCraftII/Replays/'
    extract_multiple_zip_files_into_directory(replay_zips, replays_directory)
    remove_temporay_files(replay_zips)


def install_sc2le(starcraft_directory=os.getenv('Home')):
    starcraft_exists = check_if_startcraftII_exists()
    logging.info('StarcraftII is {}'.format('PRESENT' if starcraft_exists else 'MISSING'))
    if not starcraft_exists:
        download_and_extract_starcraftII()

    check_for_permission_before_downloading("MAPS", download_and_extract_maps)
    check_for_permission_before_downloading("REPLAYS", download_and_extract_replays)


def check_for_permission_before_downloading(download_name, download_function):
    print("Do you want to download {} [y/n]".format(download_name))
    wants_to_download = check_for_comfirmation()
    if wants_to_download:
        download_function()


def check_for_comfirmation():
    return input() == 'y'


if __name__ == '__main__':
    install_sc2le()
