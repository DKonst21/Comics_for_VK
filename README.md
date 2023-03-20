# Публикация комиксов
Программа по скачиванию комиксов и загрузки их в VK.

## Как установить

Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, если есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```

## Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков dvmn.org.

## Конфигурация проекта
Для работы с проектом потребуется:
- VK_GROUP_ID - id группы в VK, которую можно создать по ссылке https://vk.com/apps?act=manage Информация о id группы можно узнать здесь: https://regvk.com/id/
- VK_ACCESS_TOKEN - access_token пользователя, который можно получить, пройдя по ссылке https://vk.com/dev/implicit_flow_user 

### [download_comic.py](download_comic.py)
Содержит общую функцию по скачиванию картинок по url-адресу.

### [main.py](main.py)
Основной файл проекта. Запустите его с помощью команды:
```
python main.py
```
Результатом его выполнения будет случайный комикс про Python, загруженный на стену ранее созданной группы.

#### get_comics_photo(number_last_comic)
Получает случайный комикс с сайта https://xkcd.com Параметр number_last_comic - номер последнего комикса на момент написания проекта. 

#### get_address_for_upload_photo(access_token, group_id, version)
Получает адрес сервера для загрузки картинки. Параметы: токен и id группы, версия API VK.

#### upload_photos_to_server(access_token, group_id, version)
Загружает на сервер Вконтакте скачанный комикс.

#### save_wall_photo(access_token, group_id, version, server, photo, photo_hash)
Сохраняет загруженное изображение в альбоме группы. Параметры: 
- server - номер сервера, на который загружена картинка; 
- photo - словарь с данными о картинке;
- photo_hash - строка с hash номером картинки.

#### post_comic_on_wall(access_token, group_id, version, owner_id, media_id, message)
Публикует скаченный комикс на стену сообщества в VK. Параметры:
- owner_id — идентификатор владельца медиа-приложения; 
- media_id — идентификатор медиа-приложения; 
- message - содержится комментарий к этому комиксу.
