import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

# 定义 user_agent 信息

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
cookie = 'uuid_n_v=v1; uuid=C2C06F60CEE711EABF2811F0086C462EC73E1442521E44A392F8EDEEDB127326; _csrf=877585097759b4e156e19320c832497b7a2714a53ae15cbc573457e5cc242cf8; mojo-uuid=baa751e8805797b99e88440a6fa7b6e1; _lxsdk_cuid=17388f3c882c8-0431ab1f72bf05-15356650-1aeaa0-17388f3c882c8; _lxsdk=C2C06F60CEE711EABF2811F0086C462EC73E1442521E44A392F8EDEEDB127326; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1595730543,1595734848; __mta=45347483.1595730545658.1595734071438.1595734848725.9; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1595734972; _lxsdk_s=1738b7c42ac-75a-ca2-b73%7C%7C1'

# 模拟 header 信息

# header['user-agent'] = user_agent
# response = requests.get(url, headers=header)
header = {'user-agent': user_agent, 'Cookie': cookie}


# 定义请求地址

requestUrl = 'https://maoyan.com/films?showType=3'

# 通过 request 获取网页信息

response = requests.get(requestUrl, headers=header)
bs_info = bs(response.text, 'html.parser')
movie_list=[]

# 获取 top10 影片信息

for items,tags in enumerate(bs_info.find_all('div', attrs={'class':'movie-item-hover'})):
    movie_name = tags.find(class_='name').text
    movie_type = tags.find_all(class_='movie-hover-title')[1].text[5:].strip()
    release_time = tags.find(class_='movie-hover-brief').text[7:].strip()
    movie_list.append((movie_name,movie_type,release_time))
    if items == 9 :
        break

movies = pd.DataFrame(movie_list)
movies.to_csv("movies.csv",encoding="utf-8")