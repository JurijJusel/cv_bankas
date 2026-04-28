import time
import requests
from bs4 import BeautifulSoup
from time import strftime
from time import gmtime

   
def try_post_date(article):
    try:
        post_date = article.find('span', {'class': 'txt_list_2'}).text
    except AttributeError:
        try:
            post_date = article.find('span', {'class': 'txt_list_important'}).text
        except AttributeError:
            try:
                post_date = article.find('span', {'class': 'txt_list_err'}).text
                if post_date == 'negalioja':
                    post_date = 'negalioja 31 d.'
            except AttributeError:
                post_date = 'negalioja 31 d.'
    return post_date  


def upload_time(post_date):
    current_time = round(time.time())
    post_date_split = post_date.split()
    data_number = post_date_split[1]
    current_time = round(time.time())
    time_values = ['d.', 'val.', 'min.']

    for x in post_date_split:
        if x in time_values:
            if x == "d.":
                temp_days = int(data_number) * 86400
                post_upload = current_time - temp_days
                return post_upload
                            
            if x == "val.":
                temp_hour = int(data_number) * 3600
                post_upload = current_time - temp_hour
                return post_upload
                            
            if x == "min.":
                temp_min = int(data_number) * 60
                post_upload = current_time - temp_min
                return post_upload
        else:
            return current_time
 

def try_city(article):
    try:
        city = article.find('span', {'class': 'list_city'}).text 
    except:
        city = 'not specified'     
    return city   


def try_post_description_full(post_soup):
    try:
        post_description_full = post_soup.find_all('section', itemprop='description')[0].get_text()
    except:
        post_description_full = "no description"
    return post_description_full
    
    
    
    
def try_salary(article):
    try:
        salary = article.find('span', class_ = 'salary_amount').text
        salary_split = salary.split('-')
        salary =list(map(int, salary_split))
    except Exception:
        salary = [0]
    return salary    

          
def try_applicants(post_soup):   
    try:
        applicants_full = post_soup.find_all('div', class_='jobad_stat')[1].text
        applicants_value = applicants_full.split()[0]
    except:
        applicants_value = "0"
    return applicants_value  

        
def count_pages():
    page_number = 1
    with requests.Session() as rs:
        while True:
            req = rs.get(f'https://www.cvbankas.lt/?page={page_number}')
            soup = BeautifulSoup(req.content, 'lxml')
            if soup.select_one('[rel=next]') is None:
                break
            page_number += 1
    return page_number


def count_posts():
    amount_post = 0
    page_number = 1
    with requests.Session() as rs:
        while True:
            req = rs.get(f'https://www.cvbankas.lt/?page={page_number}')
            soup = BeautifulSoup(req.content, 'lxml')
            articles = soup.find_all('article')
            amount_post += len(articles)
            if soup.select_one('[rel=next]') is None:
                break
            page_number += 1  
    return amount_post    
        
           
def count_time(start, stop):
    duration = (stop - start)
    return round(duration, 2)


def stopwatch_time(start, stop):
    st = count_time(start, stop)
    st_strf = strftime("%Hh:%Mm:%Ss", gmtime(st))
    return st_strf

