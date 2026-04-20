from utils.file import read_csv
from colorama import Fore, Style
import numpy as np
import pandas as pd
from utils.file import create_csv, read_csv, create_json

# csv_file='companys_full.csv'
csv_file = 'data_python.csv'
# csv_file = 'posts_test.csv'
# csv_file = 'data_new.csv'
# print(create_csv('companys_full.csv',return_companys_df(read_csv(csv_file))))

print(Fore.YELLOW, read_csv(csv_file),  Style.RESET_ALL)





# from cv_bank_full import csv_file
# from cv_bank_python import csv_file

# csv_file = 'data/data_new.csv'





# cities = pd.DataFrame( columns=['posts'])
# data = df.to_csv(csv_file, index=False, mode="a", header=False) 
# posts = pd.DataFrame(data, columns=['posts'])
# print(company)
# posts.to_csv('company.csv')
# print(read_csv(cities))
# print(cities)
# df = pd.read_csv(csv_file, columns=['total_posts'])
# print(df)
# print(df) 