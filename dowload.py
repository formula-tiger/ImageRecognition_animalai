from flickrapi import FlickrAPI
from urllib.request import urlretrieve
from pprint import pprint

import os, time, sys


# API key
key = "2454c11a804149bc02bb96885ba46936"
secret = "0a5d3efdfdb0effe"
wait_time = 1

# save files
animalname = sys.argv[1]
savedir = "./" + animalname

flickr = FlickrAPI(key, secret, format='parsed-json')
result = flickr.photos.search(
    text = animalname,
    per_page = 400,
    media = 'photos',
    sort = 'relevance',
    safe_search = 1,
    extras = 'url_q, license'
)

photos = result['photos']
# pprint(photos)

for i, photo in enumerate(photos['photo']):
    url_q = photo['url_q']
    filepath = savedir + '/' + photo['id'] + '.jpg'
    if os.path.exists(filepath): continue
    # 重複するファイルがない場合はループに戻り、ある場合は以下の処理
    urlretrieve(url_q, filepath)
    time.sleep(wait_time)
