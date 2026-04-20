import unittest
import requests
from app import Crawler
# from app import create_df

class CrawlerTestCase(unittest.TestCase):
    
    def test_download_url(self):
        downl_url=Crawler('https://www.cvbankas.lt?page=')
        response = requests.get('https://www.cvbankas.lt?page=')
        self.assertTrue(downl_url.download_url())
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.status_code, 404)


    def test_download_content(self):
        downl_url=Crawler('https://www.cvbankas.lt?page=')
        self.assertTrue(downl_url.download_content)
        response = requests.get('https://www.cvbankas.lt?page=')
        self.assertTrue(response.headers)
    
    # def test_create_df(self):
    #     result = create_df()
    #     self.assertIsInstance(result, dict)
   

if __name__ == '__main__':
    unittest.main()