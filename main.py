import requests
import os
import random
from download_comics import download_comics
from dotenv import load_dotenv


def get_comics_photo():

    number_comics = str(random.randrange(1, 2750, 1))
    response = requests.get(f'https://xkcd.com/{number_comics}/info.0.json')
    response.raise_for_status()
    return response.json()


def get_response_api_vk(access_token):

    response = requests.get(f"https://api.vk.com/method/groups.get?PARAMS&access_token={access_token}&v=5.131")
    response.raise_for_status()
    return response.json()


def get_wall_upload_server(access_token, group_id):

    response = requests.get(f"https://api.vk.com/method/photos.getWallUploadServer?group_id={group_id}"
                            f"&access_token={access_token}&v=5.131")
    response.raise_for_status()
    return response.json()['response']


def uploading_photos_to_server(access_token, group_id):

    with open('image.png', 'rb') as file:
        url = get_wall_upload_server(access_token, group_id)['upload_url']
        files = {
            'photo': file,
        }
        response = requests.post(url, files=files)
        response.raise_for_status()
        server = response.json()['server']
        photo = response.json()['photo']
        hash_photo = response.json()['hash']
        file.close()
        return save_wall_photo(access_token, group_id, server, photo, hash_photo)


def save_wall_photo(access_token, group_id, server, photo, hash_photo):

    response = requests.post(f"https://api.vk.com/method/photos.saveWallPhoto?group_id={group_id}&photo={photo}"
                             f"&server={server}&hash={hash_photo}&access_token={access_token}&v=5.131")
    response.raise_for_status()
    return response.json()['response'][0]


def post_comic_on_wall(access_token, group_id, message):

    response_server = uploading_photos_to_server(access_token, group_id)
    owner_id = str(response_server['owner_id'])
    from_group = True
    media_id = str(response_server['id'])
    attachments = f'photo{owner_id}_{media_id}'
    response = requests.post(f"https://api.vk.com/method/wall.post?owner_id={-group_id}&group_id={group_id}"
                             f"&from_group={from_group}&attachments={attachments}&message={message}"
                             f"&access_token={access_token}&v=5.131")
    response.raise_for_status()
    return response.json()


def main():
    load_dotenv()
    access_token = os.environ['ACCESS_TOKEN_VK']
    group_id = int(os.environ['GROUP_ID'])
    image = get_comics_photo()

    get_response_api_vk(access_token)
    download_comics(image['img'], 'image.png')
    post_comic_on_wall(access_token, group_id, image['alt'])
    os.remove('image.png')


if __name__ == '__main__':
    main()
