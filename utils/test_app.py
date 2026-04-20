import unittest
from app import Crawler
from utils.try_data_scrap import try_post_date

class CrawlerTestCase(unittest.TestCase):
    
    def test_download_url(self):
        downl_url=Crawler('https://www.cvbankas.lt?page=')
        self.assertTrue(downl_url.download_url())

    def test_download_content(self):
        downl_url=Crawler('https://www.cvbankas.lt?page=')
        self.assertTrue(downl_url.download_content)
    
    def test_try_post_date(self):
        self.assertTrue(try_post_date)

if __name__ == '__main__':
    unittest.main()
