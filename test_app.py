import unittest
import requests
from app import Crawler
# from app import create_df

class CrawlerTestCase(unittest.TestCase):
    
    def setUp(self):
        self.url = 'https://www.cvbankas.lt?page='
        
        
    def test_download_url(self):
        downl_url=Crawler(self.url)
        response = requests.get(self.url)
        self.assertTrue(downl_url.download_url())
        self.assertEqual(200, response.status_code)
        self.assertNotEqual(response.status_code, 404)


    def test_download_content(self):
        downl_url=Crawler(self.url)
        self.assertTrue(downl_url.download_content)
        response = requests.get(self.url)
        self.assertTrue(response.headers)
    
    # def test_create_df(self):
    #     result = create_df()
    #     self.assertIsInstance(result, dict)
   

# if __name__ == '__main__':
#     unittest.main()

# # test_sample.py
# import unittest
 
# class TestStringMethods(unittest.TestCase):
 
#     def test_upper(self):
#         self.assertEqual('foo'.upper(), 'FOO')
 
#     def test_split(self):
#         s = 'hello world'
#         self.assertEqual(s.split(), ['hello', 'world'])
#         # check that s.split fails when the separator is not a string
#         with self.assertRaises(TypeError):
#             s.split(2)
 
# if __name__ == '__main__':
#     unittest.main()