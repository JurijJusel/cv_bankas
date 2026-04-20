import unittest
from utils.try_data_scrap import try_post_date


class CrawlerTestCase(unittest.TestCase):
    
    def test_try_post_date(self):
        self.assertTrue(try_post_date)