
import requests
import datetime as dt
import pandas as pd
import os
from dotenv import load_dotenv

# переменные
load_dotenv()

TOKEN_USER = os.getenv('TOKEN_USER_VK') # Токен пропиши в .env TOKEN_USER_VK=ТОКЕН или замените вызов os.getenv своим токеном
VERSION = '5.131'
DOMAIN = '1tsprint'
csv_path = "csv"
posts_csv_path = 'csv/posts.csv'
users_csv_path = 'csv/users.csv'
group_info_csv_path = 'csv/group_info.csv'

# через api vk читаем посты в группе '1tsprint'
def get_all_vk_wall_posts(TOKEN_USER, VERSION, DOMAIN):
    posts_dict = {'count': 0, 'posts': []}
    offset = 0
    count = 100
    def req(posts_dict, offset, count):
        try:
            response = requests.get('https://api.vk.com/method/wall.get',
                                    params={'access_token': TOKEN_USER,
                                            'v': VERSION,
                                            'domain': DOMAIN,
                                            'offset': offset,
                                            'count': 100,
                                            'filter': str('all')})

            data = response.json()['response']
            data_posts = data['items']
            data_count = data['count']
            if len(data_posts) > 0:
                offset += count
                posts_dict['count'] = data_count
                posts_dict['posts'] = [*posts_dict['posts'], *data_posts]

                return req(posts_dict, offset, count)

        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print("OOps: Something Else", err)
        finally:
            return posts_dict

    return req(posts_dict, offset, count)


# через api vk читаем количество пользователей группы '1tsprint'
def get_all_vk_group_user(TOKEN_USER, VERSION, DOMAIN):
    users_dict = {'count': 0, 'ids': []}
    offset = 0
    count = 1000
    def req(users_dict, offset, count):
        try:
            response = requests.get('https://api.vk.com/method/groups.getMembers',
                                    params={'access_token': TOKEN_USER,
                                            'v': VERSION,
                                            'group_id': DOMAIN,
                                            'offset': offset,
                                            'count': count
                                            })

            data = response.json()['response']
            data_users_ids = data['items']
            data_count = data['count']
            if len(data_users_ids) > 0:
                offset += count
                users_dict['count'] = data_count
                users_dict['ids'] = [*users_dict['ids'], *data_users_ids]

                return req(users_dict, offset, count)

        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print("OOps: Something Else", err)
        finally:
            return users_dict

    return req(users_dict, offset, count)


group_posts = get_all_vk_wall_posts(TOKEN_USER, VERSION, DOMAIN)
group_users = get_all_vk_group_user(TOKEN_USER, VERSION, DOMAIN)

posts_data = []
for post in group_posts['posts']:
    posts_data.append({
        'post_text': post['text'],
        'date': (dt.datetime.fromtimestamp(post['date']).strftime('%Y-%m-%d %H:%M:%S')),
        'hash': post['hash'],
        'reposts_count': post['reposts']['count'],
        'likes_count': post['likes']['count'],
        'id': post['id']
    })

posts_dataframe = pd.DataFrame(posts_data)
users_dataframe = pd.DataFrame(group_users['ids'], columns=['id'])
group_info_dataframe = pd.DataFrame(data={
    'Количество постов в группе': [group_posts['count']],
    'Количество подписчиков в группе': [group_users['count']],
    'Количество подписчиков в репостов': [posts_dataframe['reposts_count'].sum()]
})

print(group_info_dataframe.to_string())

isExist = os.path.exists(csv_path)
if not isExist:
    os.makedirs(csv_path)


posts_dataframe.to_csv(posts_csv_path, index=False, sep=';', encoding='utf-8-sig')
users_dataframe.to_csv(users_csv_path, index=False, sep=';')
group_info_dataframe.to_csv(group_info_csv_path, index=False, sep=';', encoding='utf-8-sig')

print('CSV c постами из группы %(d)s в: %(posts_csv_path)s' % {'d': DOMAIN, 'posts_csv_path': posts_csv_path})
print('CSV c id пользователей группы %(d)s в: %(users_csv_path)s' % {'d': DOMAIN, 'users_csv_path': users_csv_path})


