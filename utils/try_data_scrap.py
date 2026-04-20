

def try_post_date(article):
    try:
        post_date = article.find('span', {'class': 'txt_list_2'}).text  
    except:
        post_date = article.find('span', class_ = 'txt_list_important').text      
    return post_date   

    
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
