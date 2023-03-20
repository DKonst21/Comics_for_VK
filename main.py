import requests
import os
import random
from download_comic import download_comic
from dotenv import load_dotenv


def get_comic_photo(number_last_comic):
    number_comic = random.randrange(1, number_last_comic, 1)
    response = requests.get(f'https://xkcd.com/{number_comic}/info.0.json')
    response.raise_for_status()
    return response.json()


def get_address_for_upload_photo(access_token, group_id, version):
    payload = {"group_id": {group_id}, "access_token": {access_token}, "v": {version}}
    response = requests.get('https://api.vk.com/method/photos.getWallUploadServer', params=payload)
    response.raise_for_status()
    return response.json()['response']['upload_url']


def upload_photos_to_server(access_token, group_id, version):
    with open('image.png', 'rb') as file:
        url = get_address_for_upload_photo(access_token, group_id, version)
        files = {
            'photo': file,
        }
        response = requests.post(url, files=files)
        response.raise_for_status()
    uploading_photo = response.json()
    return uploading_photo


def save_wall_photo(access_token, group_id, version, server, photo, photo_hash):
    payload = {"group_id": {group_id}, "photo": {photo}, "server": {server},
               "hash": {photo_hash}, "access_token": {access_token}, "v": {version}}
    response = requests.post('https://api.vk.com/method/photos.saveWallPhoto', params=payload)
    response.raise_for_status()
    return response.json()['response'][0]


def post_comic_on_wall(access_token, group_id, version, owner_id, media_id, message):
    attachments = f'photo{owner_id}_{media_id}'
    payload = {"owner_id": {-group_id}, "group_id": {group_id}, "from_group": True,
               "attachments": {attachments}, "message": {message}, "access_token": {access_token},
               "v": {version}}
    response = requests.post('https://api.vk.com/method/wall.post', params=payload)
    response.raise_for_status()
    return response.json()


def main():
    load_dotenv()
    access_token = os.environ['VK_ACCESS_TOKEN']
    group_id = int(os.environ['VK_GROUP_ID'])
    version = '5.131'
    number_last_comic = 2750
    comic_info = get_comic_photo(number_last_comic)
    try:
        download_comic(comic_info['img'], 'image.png')
        uploading_photo = upload_photos_to_server(access_token, group_id, version)
        server = uploading_photo['server']
        photo = uploading_photo['photo']
        photo_hash = uploading_photo['hash']
        save_photo = save_wall_photo(access_token, group_id, version, server, photo, photo_hash)
        owner_id = save_photo['owner_id']
        media_id = save_photo['id']
        post_comic_on_wall(access_token, group_id, version, owner_id, media_id, comic_info['alt'])
    except ValueError:
        print("Environment variables error!")
    finally:
        os.remove('image.png')


if __name__ == '__main__':
    main()
