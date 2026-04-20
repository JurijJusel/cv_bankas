import requests
import time
# from bs4 import BeautifulSoup as bs
from bs4 import BeautifulSoup
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
# }
start_time = time.perf_counter() 

# post = 0
# page = 1
# with requests.Session() as rs:
#     print("processing.....")
#     while True:
#         req = rs.get(f'https://www.cvbankas.lt/?page={page}')
    
#         soup = BeautifulSoup(req.content, 'lxml')
#         articles = soup.find_all('article')
#         # print(len(articles))
#         post += len(articles)
    
#         if soup.select_one('[rel=next]') is None:
#             break
#         page += 1
#     print(f'count of pages {page}')
#     print(f'count of posts {post}')
# print("Done!!!")
    

def count_pages():
    page_number = 1
    with requests.Session() as rs:
        while True:
            req = rs.get(f'https://www.cvbankas.lt/?page={page}')
            soup = BeautifulSoup(req.content, 'lxml')
        
            if soup.select_one('[rel=next]') is None:
                break
            page_number += 1
        return page_number

print(count_pages())



def count_posts():
    post = 0
    page = 1
    with requests.Session() as rs:
        while True:
            req = rs.get(f'https://www.cvbankas.lt/?page={page}')
            soup = BeautifulSoup(req.content, 'lxml')
            articles = soup.find_all('article')
            post += len(articles)
        
            if soup.select_one('[rel=next]') is None:
                break
            page += 1  
        return post

print(count_posts())

stop_time = time.perf_counter()
print(round(stop_time-start_time, 2))