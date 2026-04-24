from bs4 import BeautifulSoup
import requests
from rich.progress import track
from constants import BASE_URL, PYTHON_URL
from models.post_model import JobPostModel
from utils import safe_text


def get_soup(url: str) -> BeautifulSoup | None:
    """
    Fetches and parses a webpage into a BeautifulSoup object.
    Args:
        page_url (str): The full URL of the page to fetch.
    Returns:
        BeautifulSoup: Parsed HTML content of the page.
    """
    try:
        response = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=10
        )
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "lxml")
        return soup

    except requests.RequestException as e:
        print(f"[ERROR] Failed to fetch {url}: {e}")
        return None


def get_all_count_of_posts(count_pages, base_url):
    """
    Extracts the total count of posts from the webpage.
    Args:
        count_pages (int): The number of pages to iterate through.
        base_url (str): The base URL for the pages.
    Returns:
        int: Total count of posts.
    """
    total_posts = 0
    for page in track(range(count_pages), description="Processing..."):
        url = f"{base_url}{page+1}"
        print(url)
        soup = get_soup(url)
        articles = soup.find_all("article")
        articles_search = int(len(articles))
        total_posts += articles_search
    return total_posts


def get_total_count_pages(soup):
    """
    Extracts the total number of pages from the pagination section of the webpage.
    Args:
        soup (BeautifulSoup): Parsed HTML content of the page.
    Returns:
        int: The total number of pages.
    """
    pages_ul = soup.find("ul", class_="pages_ul_inner")
    pages_li = pages_ul.find_all("li")[-1:]
    last_page_number = pages_li[0].find("a").get_text()
    return int(last_page_number)


def scrape_post(job_card):
    post_id = job_card.find("div", class_= "jobadlist_ad_anchor").get("id")[6:]
    post_url = job_card.find("a", class_="list_a can_visited list_a_has_logo").attrs["href"]
    company_logo_url = job_card.find("img").get("src")
    position = job_card.find("h3").text
    company = job_card.find("span", class_="heading_secondary").get_text().strip()
    salary_tag = job_card.find("span", class_="salary_amount")
    salary = salary_tag.get_text(strip=True) if salary_tag else None
    salary_type_tag = job_card.find("span", class_="salary_calculation")
    salary_type = salary_type_tag.get_text(strip=True) if salary_type_tag else None
    #tag_upload = job_card.find("span", class_="txt_list_2")
    #post_upload = tag_upload.text.strip() if tag_upload else None
    post_upload = safe_text(job_card, "span", "txt_list_2")

    post_url_soup = get_soup(post_url)
    company_city = post_url_soup.find('span', {'itemprop': 'addressLocality'}).get_text().strip()
    strong_selector = post_url_soup.find_all('strong', class_='jobad_stat_value')
    people_viewed = int(strong_selector[0].get_text(strip=True)) if len(strong_selector) > 0 else 0
    raw_applied = (strong_selector[1].get_text(strip=True) if len(strong_selector) > 1 else None)
    people_applied = int(raw_applied.replace(">", "").replace("+", "").strip()) if len(strong_selector) > 1 else 0

    data =  {
        "post_id": post_id,
        "company": company,
        "company_city": company_city,
        "position": position,
        "salary": salary,
        "salary_type": salary_type,
        "post_url": post_url,
        "company_logo_url": company_logo_url,
        "post_upload": post_upload,
        "people_viewed": people_viewed,
        "people_applied": people_applied
    }

    return data


def scrape_all_posts(url):
    soup = get_soup(url)
    count_pages = get_total_count_pages(soup)
    print(f"Total pages: {count_pages}")

    for page in track(range(count_pages), description="Processing..."):
        page_url = f"{url}{page+1}"
        page_soup = get_soup(page_url)
        print(f"Scraping page: {page_url}")
        articles = page_soup.find_all("article")
        for article in articles:
            scrape_post_card = scrape_post(article)
            post_obj_model = JobPostModel(**scrape_post_card)
            print("= "*20)
            print(post_obj_model)





if __name__ == "__main__":
    #soup = get_soup(BASE_URL)
    #soup = get_soup(PYTHON_URL)
    #total_pages = get_total_count_pages(soup)
    #print(f"Total pages: {total_pages}")
    #total_posts = get_all_count_of_posts(total_pages, PYTHON_URL)
    #print(f"Total posts: {total_posts}")

    #scrape_post(PYTHON_URL)
    print(scrape_all_posts(PYTHON_URL))
    print("DONE!!!")




#print('wait.....')

#count_all_posts = count_posts()
## count_all_pages = count_pages()
## print(count_all_posts)
## print(count_all_pages)

#posts_list = []
#for article in tqdm(articles, ncols=100, colour="green", desc='Posts scraping progress'):
#    post_id = article.find('div', {'class': 'jobadlist_ad_anchor'}).get("id")[6:]
#    post_url = article.find("a", {"class": "list_a can_visited list_a_has_logo"}).attrs['href']
#    img_url = article.find('img').get('src')
#    position = article.find('h3').text
#    company = article.find('span', {'class': 'dib mt5 mr10'}).text
#    city = article.find('span', {'class': 'list_city'}).text
#    salary = try_salary(article)
#    post_date = try_post_date(article)
#    upload_post = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(upload_time(post_date)))

#    post_source = requests.get(post_url)
#    post_soup = BeautifulSoup(post_source.text, 'lxml')
#    post_description_full = post_soup.find_all('section', itemprop='description')[0].get_text()
#    applicants_value = try_applicants(post_soup)

#    post_data = {
#        "post_descrip": post_description_full,
#        "post_id": post_id,
#        "applicants": applicants_value,
#        "company": company,
#        "position": position,
#        "post_url": post_url,
#        "img_url": img_url,
#        "salary": salary,
#        "city": city,
#        "upload_post": upload_post,
#        "time_public": post_date,
#    }

#    posts_list.append(post_data)


#stop_time = time.perf_counter()


#data = {
#    'website': "www.cvbankas.lt",
#    'extract_time': count_time(start_time, stop_time),
#    'total_posts': count_all_posts,
#    'posts_python': articles_search,
#    'posts': [posts_list],
#    'created_date': time_now,
#}

#df = pd.DataFrame(data, columns=['website', 'extract_time', 'total_posts', 'posts_python', 'posts', 'created_date'])

#csv_file = 'data_python.csv'
## json_file = 'data_python.json'

#print(Fore.BLUE, create_csv(csv_file, df), Style.RESET_ALL)
## print(create_json(posts_list, json_file))
## print(Fore.YELLOW, read_csv(csv_file))
## print(create_csv('companys.csv', create_companies_df(read_csv(csv_file))))
#print(create_csv('companys.csv', create_companies_df(read_csv(csv_file), read_csv('companys.csv'))))

#print(Fore.GREEN,f'web information extraction time', stopwatch_time(start_time, stop_time), Style.RESET_ALL)

#print('Posts scraping done!')



#def scrape_post(url):
#    soup = get_soup(url)
#    count_pages = get_total_count_pages(soup)
#    print(f"Total pages: {count_pages}")

#    for page in track(range(count_pages), description="Processing..."):
#        page_url = f"{url}{page+1}"
#        page_soup = get_soup(page_url)
#        print(f"Scraping page: {page_url}")
#        articles = page_soup.find_all("article")
#        for job_card in articles:

#    #job_card = get_soup(url)
#    #article = job_card.find("article")

#            post_id = int(job_card.find("div", class_= "jobadlist_ad_anchor").get("id")[6:])
#            print(f"Post ID: {post_id}")
#            post_url = job_card.find("a", class_="list_a can_visited list_a_has_logo").attrs["href"]
#            print(f"Post URL: {post_url}")
#            company_logo_url = job_card.find("img").get("src")
#            print(f"Company Logo URL: {company_logo_url}")
#            position = job_card.find("h3").text
#            print(f"Position: {position}")
#            company = job_card.find("span", class_="heading_secondary").get_text().strip()
#            print(f"Company: {company}")
#            #salary = job_card.find("span", class_="salary_amount").get_text().strip()
#            salary_tag = job_card.find("span", class_="salary_amount")
#            salary = salary_tag.get_text(strip=True) if salary_tag else None
#            salary_type_tag = job_card.find("span", class_="salary_calculation")
#            salary_type = salary_type_tag.get_text(strip=True) if salary_type_tag else None
#            print(f"Salary: {salary}")
#            print(f"Salary type: {salary_type}")
#            tag_upload = job_card.find("span", class_="txt_list_2")
#            post_upload = tag_upload.text.strip() if tag_upload else None
#            # post_upload = job_card.find("span", class_="txt_list_2").text
#            print(f"Post Upload: {post_upload}")

#            post_url_soup = get_soup(post_url)
#            company_city = post_url_soup.find('span', {'itemprop': 'addressLocality'}).get_text().strip()
#            print(f"Company City: {company_city}")
#            strong_selector = post_url_soup.find_all('strong', class_='jobad_stat_value')
#            people_viewed = int(strong_selector[0].get_text(strip=True)) if len(strong_selector) > 0 else 0

#            #people_applied = int(strong_selector[1].get_text(strip=True)) if len(strong_selector) > 1 else 0

#            raw_applied = (strong_selector[1].get_text(strip=True) if len(strong_selector) > 1 else None)
#            people_applied = int(raw_applied.replace(">", "").replace("+", "").strip()) if len(strong_selector) > 1 else 0
#            print(f"Viewed: {people_viewed}")
#            print(f"Applied: {people_applied}")

#            return {
#                "post_id": post_id,
#                "company": company,
#                "company_city": company_city,
#                "position": position,
#                "salary": salary,
#                "salary_type": salary_type,
#                "post_url": post_url,
#                "company_logo_url": company_logo_url,
#                "post_upload": post_upload,
#                "people_viewed": people_viewed,
#                "people_applied": people_applied
#           }
