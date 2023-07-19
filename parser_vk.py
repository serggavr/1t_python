
import requests
import datetime as dt
import pandas as pd
import os
from dotenv import load_dotenv
import time

# переменные
load_dotenv()

TOKEN_USER = os.getenv('TOKEN_USER_VK') # Токен пропиши в .env TOKEN_USER_VK=ТОКЕН или замените вызов os.getenv своим токеном
VERSION = '5.131'
DOMAIN = '1tsprint'
OWNER_ID = -215426617
csv_path = "csv"
posts_csv_path = '%s/posts.csv' % csv_path
users_csv_path = '%s/users.csv' % csv_path
group_info_csv_path = '%s/group_info.csv' % csv_path

liked_post_top_ten_path = '%s/group_TOP_TEN_LIKED_posts.csv' % csv_path
commented_post_top_ten_path = '%s/group_TOP_TEN_COMMENTED_posts.csv' % csv_path
post_with_found_comment_path = '%s/group_post_with_found_text.csv' % csv_path

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
        'id': post['id'],
        'date': (dt.datetime.fromtimestamp(post['date']).strftime('%Y-%m-%d %H:%M:%S')),
        # 'hash': post['hash'],
        'reposts_count': post['reposts']['count'],
        'likes_count': post['likes']['count'],
        'comments_count': post['comments']['count']
    })


def get_all_comments_under_posts(posts_data, TOKEN_USER, VERSION, OWNER_ID):
    comments_under_posts = []
    for post in posts_data:

        if post['comments_count'] > 0:
            time.sleep(1)
            try:
                response = requests.get('https://api.vk.com/method/wall.getComments',
                                        params={'access_token': TOKEN_USER,
                                                'v': VERSION,
                                                'owner_id': OWNER_ID,
                                                'post_id': post['id']
                                                })
                data = response.json()['response']
                post_comments = data['items']
                for comment in post_comments:
                    if comment['text'].lower().find('data engineering') >= 0:
                        comments_under_posts.append({
                            'post_id': post['id'],
                            'post_date': post['date'],
                            'post_text': post['post_text'],
                            'comment_id': comment['id'],
                            'comment_date': (dt.datetime.fromtimestamp(comment['date']).strftime('%Y-%m-%d %H:%M:%S')),
                            'comment_text': comment['text'],
                            'comment_owner': comment['from_id']
                        })
            except requests.exceptions.HTTPError as errh:
                print("Http Error:", errh)
            except requests.exceptions.ConnectionError as errc:
                print("Error Connecting:", errc)
            except requests.exceptions.Timeout as errt:
                print("Timeout Error:", errt)
            except requests.exceptions.RequestException as err:
                print("OOps: Something Else", err)

    return comments_under_posts


posts_dataframe = pd.DataFrame(posts_data)
users_dataframe = pd.DataFrame(group_users['ids'], columns=['id'])

group_info_dataframe = pd.DataFrame(data={
    'Количество постов в группе': [group_posts['count']],
    'Количество подписчиков в группе': [group_users['count']],
    'Количество репостов в группе': [posts_dataframe['reposts_count'].sum()]
})
liked_post_top_ten_dataframe = posts_dataframe.sort_values(by='likes_count', ascending=False, ignore_index=True)[:10]
commented_post_top_ten_dataframe = posts_dataframe.sort_values(by='comments_count', ascending=False)[:10]
post_with_found_comment = pd.DataFrame(get_all_comments_under_posts(posts_data, TOKEN_USER, VERSION, OWNER_ID))

isExist = os.path.exists(csv_path)
if not isExist:
    os.makedirs(csv_path)


group_info_dataframe.to_csv(group_info_csv_path, index=False, sep=';', encoding='utf-8-sig')
liked_post_top_ten_dataframe[['likes_count', 'post_text']].to_csv(liked_post_top_ten_path, index=False, sep=';', encoding='utf-8-sig')
commented_post_top_ten_dataframe[['comments_count', 'post_text']].to_csv(commented_post_top_ten_path, index=False, sep=';', encoding='utf-8-sig')
post_with_found_comment.to_csv(post_with_found_comment_path, index=False, sep=';', encoding='utf-8-sig')
