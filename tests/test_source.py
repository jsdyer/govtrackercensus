import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import unittest
from source import domain,classify,sanitize_url
class CensusTests(unittest.TestCase):
 def test_private_suffix_and_subdomains(self):self.assertEqual(domain('a.github.io'),'a.github.io');self.assertEqual(domain('a.gov.bc.ca'),'gov.bc.ca')
 def test_tag_delivery_is_not_analytics(self):self.assertEqual(classify('www.googletagmanager.com')[1],'tag delivery');self.assertIsNone(classify('cdn.example.org'))
 def test_query_credentials_are_not_retained(self):self.assertEqual(sanitize_url('https://example.org/a?token=secret#private'),'https://example.org/a')
