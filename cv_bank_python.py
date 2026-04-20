from bs4 import BeautifulSoup
import requests
import time
from srap_preprocessing import upload_time, count_time, try_salary, try_applicants, try_post_date, count_posts,count_pages, stopwatch_time
from utils.file import create_json, create_csv, read_csv, create_companies_df
import pandas as pd
from tqdm import tqdm
from colorama import Fore, Style


start_time = time.perf_counter()
time_now = time.strftime("%Y-%m-%d %H:%M:%S")
print(Fore.GREEN, time_now, Style.RESET_ALL)

source = requests.get('https://www.cvbankas.lt/?location=606&padalinys%5B%5D=76&keyw=python').text
soup = BeautifulSoup(source, 'lxml')

articles = soup.find_all('article')
articles_search = len(articles)
print(f"amount of post in search of python: {articles_search}")
print('wait.....')

count_all_posts = count_posts()
# count_all_pages = count_pages()
# print(count_all_posts)
# print(count_all_pages)

posts_list = []
for article in tqdm(articles, ncols=100, colour="green", desc='Posts scraping progress'):
    post_id = article.find('div', {'class': 'jobadlist_ad_anchor'}).get("id")[6:]
    post_url = article.find("a", {"class": "list_a can_visited list_a_has_logo"}).attrs['href']
    img_url = article.find('img').get('src')
    position = article.find('h3').text
    company = article.find('span', {'class': 'dib mt5 mr10'}).text
    city = article.find('span', {'class': 'list_city'}).text
    salary = try_salary(article)
    post_date = try_post_date(article)
    upload_post = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(upload_time(post_date)))

    post_source = requests.get(post_url)
    post_soup = BeautifulSoup(post_source.text, 'lxml')
    post_description_full = post_soup.find_all('section', itemprop='description')[0].get_text()
    applicants_value = try_applicants(post_soup)

    post_data = {
        "post_descrip": post_description_full,
        "post_id": post_id,
        "applicants": applicants_value,
        "company": company,
        "position": position,
        "post_url": post_url,
        "img_url": img_url,
        "salary": salary,
        "city": city,
        "upload_post": upload_post,
        "time_public": post_date,
    }

    posts_list.append(post_data)


stop_time = time.perf_counter()


data = {
    'website': "www.cvbankas.lt",
    'extract_time': count_time(start_time, stop_time),
    'total_posts': count_all_posts,
    'posts_python': articles_search,
    'posts': [posts_list],
    'created_date': time_now,
}

df = pd.DataFrame(data, columns=['website', 'extract_time', 'total_posts', 'posts_python', 'posts', 'created_date'])

csv_file = 'data_python.csv'
# json_file = 'data_python.json'

print(Fore.BLUE, create_csv(csv_file, df), Style.RESET_ALL)
# print(create_json(posts_list, json_file))
# print(Fore.YELLOW, read_csv(csv_file))
# print(create_csv('companys.csv', create_companies_df(read_csv(csv_file))))
print(create_csv('companys.csv', create_companies_df(read_csv(csv_file), read_csv('companys.csv'))))

print(Fore.GREEN,f'web information extraction time', stopwatch_time(start_time, stop_time), Style.RESET_ALL)

print('Posts scraping done!')
