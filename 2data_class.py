import pandas as pd
from pathlib import Path 

class Data_summary:
    def __init__(self, website, extract_time, total_posts, posts_python, posts, created_date):

        self.website = website
        self.extract_time = extract_time
        self.total_posts = total_posts
        self.posts_python = posts_python
        self.posts = posts
        self.created_date = created_date
       
    def data_dict(self):
        data = {
            'website': self.website,
            'extract_time': self.extract_time, #count_time(start_time, stop_time),
            'total_posts': self.total_posts,#count_all_posts,
            'posts_python': self.posts_python,#articles_search,
            'posts':  self.posts,#[posts_list],
            'created_date':  self.created_date,#time_now,
            }
        return data
    
    def create_df(self, data):
        self.df = pd.DataFrame(data, columns=['website', 'extract_time', 'total_posts', 'posts_python', 'posts', 'created_date'])
        return self.df

    def data_to_csv(self):
        # self.data = pd.DataFrame(self.data, columns=['website', 'extract_time', 'total_posts', 'posts_python', 'posts', 'created_date'])
        self.data = self.df.to_csv(file_path, index=False, mode="a", header=False)
        return self.data
    
    def get_dimension(self):
        print(file_path, 'Rows:', len(self.df))
        print(file_path, 'Columns:', len(list(self.df.columns)))
        
        
    def print_csv(self):
        self.df = pd.read_csv(file_path)
        print(self.df)
        # print(self.df.head())

file_csv = 'data_python.csv'
file_path = Path('data/' + file_csv)
website = 'www.cv_bankas.lt'

a = Data_summary(website,125,30,5,'[posts:2, 5:4]','2023.01.06 15:00')
a.print_csv()
# a.get_dimension()
print(a.data_dict())


# a.create_df()


# print('extract_time in seconds', a.website)
# print('extract_time in seconds', a.extract_time)
# print('total posts', a.total_posts)
# print('posts_python', a.posts_python)
# print('posts',a.posts)
# print('created_date', a.created_date)
# a.data_to_csv()




        # pd.set_option('display.max_columns', None)
        # pd.set_option('display.max_rows', None)
        # self.df = pd.read_csv(file_path)