import requests
from bs4 import BeautifulSoup
import urllib.request
import os
import argparse


def check_positive(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError(
            f"{value} is an invalid positive int value")
    return ivalue


ap = argparse.ArgumentParser()
ap.add_argument('-s', '--search_query', help='Search Query', required=True)
ap.add_argument('-n', '--pages', default=10, type=check_positive,
                help='Number of Pages to Loop Through', required=True)
ap.add_argument('p', '--save_folder', required=True, help='path to save iamges')
args = vars(ap.parse_args())

search_term = args['search_query']
encoded_term = urllib.parse.quote_plus(search_term)
num_pages = args['pages']

for page in range(num_pages):
    search_url = f"https://www.google.com/search?q={encoded_term}&tbm=isch&start={page*100}"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    image_tags = soup.find_all('img')
    results = []

    for image in image_tags:
        src = image.get('src')
        if src and src.startswith('http'):
            alt = image.get('alt', 'image')
            image_data = {'src': src, 'alt': alt}
            results.append(image_data)

    save_folder = args['save_folder']
    os.makedirs(save_folder, exist_ok=True)

    for idx, image in enumerate(results):
        url = image['src']
        title = image['alt']
        filename = f'{save_folder}/{search_term.replace(" ", "_")}_{page*100 + idx}.jpg'
        try:
            urllib.request.urlretrieve(url, filename)
            print(f"Downloaded: {filename}")
        except Exception as e:
            print(f"Failed to download {filename}: {e}")
