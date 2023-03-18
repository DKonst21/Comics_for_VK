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


def get_response_api_vk(access_token):
    payload = {"PARAMS": "", "access_token": f"{access_token}", "v": "5.131"}
    response = requests.get('https://api.vk.com/method/groups.get', params=payload)
    response.raise_for_status()
    return response.json()


def get_address_for_download_photo(access_token, group_id):
    payload = {"group_id": f"{group_id}", "access_token": f"{access_token}", "v": "5.131"}
    response = requests.get('https://api.vk.com/method/photos.getWallUploadServer', params=payload)
    response.raise_for_status()
    return response.json()['response']


def upload_photos_to_server(access_token, group_id):
    with open('image.png', 'rb') as file:
        url = get_address_for_download_photo(access_token, group_id)['upload_url']
        files = {
            'photo': file,
        }
        response = requests.post(url, files=files)
        file.close()
        response.raise_for_status()
        uploading_photo = [response.json()['server'], response.json()['photo'], response.json()['hash']]
        return uploading_photo


def save_wall_photo(access_token, group_id, uploading_photo):
    payload = {"group_id": f"{group_id}", "photo": f"{uploading_photo[1]}", "server": f"{uploading_photo[0]}",
               "hash": f"{uploading_photo[2]}", "access_token": f"{access_token}", "v": "5.131"}
    response = requests.post('https://api.vk.com/method/photos.saveWallPhoto', params=payload)
    response.raise_for_status()
    return response.json()['response'][0]


def post_comic_on_wall(access_token, group_id, info_image, message):
    owner_id = info_image['owner_id']
    media_id = info_image['id']
    attachments = f'photo{owner_id}_{media_id}'
    payload = {"owner_id": f"{-group_id}", "group_id": f"{group_id}", "from_group": True,
               "attachments": f"{attachments}", "message": f"{message}", "access_token": f"{access_token}",
               "v": "5.131"}
    response = requests.post('https://api.vk.com/method/wall.post', params=payload)
    response.raise_for_status()
    return response.json()


def main():
    load_dotenv()
    access_token = os.environ['VK_ACCESS_TOKEN']
    group_id = int(os.environ['VK_GROUP_ID'])
    number_last_comic = 2750
    comic_info = get_comic_photo(number_last_comic)
    try:
        get_response_api_vk(access_token)
        download_comic(comic_info['img'], 'image.png')
        uploading_photo = upload_photos_to_server(access_token, group_id)
        save_photo = save_wall_photo(access_token, group_id, uploading_photo)
        post_comic_on_wall(access_token, group_id, save_photo, comic_info['alt'])
    except ValueError:
        print("Environment variables error!")
    finally:
        print("Comics uploaded to the wall of the VK group!")
    os.remove('image.png')


if __name__ == '__main__':
    main()
