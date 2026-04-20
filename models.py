class Post:
    def __init__(self,
                 id, 
                 url, 
                 imag_url,
                 position, 
                 company, 
                 city, 
                 salary, 
                 post_date, 
                 upload_post, 
                 description_full, 
                 applicants_value):
        self.id = id
        self.url = url
        self.imag_url = imag_url
        self.position = position
        self.company = company
        self.city = city
        self.salary = salary
        self.upload_post = upload_post
        self.date = post_date
        self.description_full = description_full
        self.applicants_value = applicants_value
        
        
    def data_dict(self):
        data = {  
            'post_id': self.id,
            'post_url': self.url,
            'imag_url': self.imag_url,
            'position': self.position,
            'company': self.company,
            'city': self.city,
            'salary': self.salary,
            'post_date': self.date,
            'upload_post': self.upload_post,           
            'applicants_value': self.applicants_value,
            'description_full': self.description_full,
        }
        return data


    # def __str__(self):
    #     return f"post_description_full: {self.description_full}, post_id: {self.id}, post_url = {self.url}, position: {self.position}, company: {self.company}, city: {self.city}, salary: {self.salary}, upload_post: {self.upload_post}, post_date: {self.post_date}, applicants_value: {self.applicants_value}, time_now: {self.time_now}"
     