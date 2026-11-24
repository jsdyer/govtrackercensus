import copy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from collect import normalize_record


class CollectorTests(unittest.TestCase):
    def test_equivalent_request_order_and_duplicates_do_not_create_a_change(self):
        row = {'status': 'ok', 'third_party_domains': ['example.net'], 'cookies': [],
               'requests': [{'host': 'example.net', 'path': '/a', 'type': 'script'},
                            {'host': 'example.net', 'path': '/b', 'type': 'image'}]}
        reordered = copy.deepcopy(row)
        reordered['requests'] = list(reversed(row['requests'])) + [row['requests'][0]]
        before = normalize_record(row)
        self.assertEqual(before['_fingerprint'], normalize_record(reordered)['_fingerprint'])
        self.assertEqual(before['third_party_count'], 1)
        self.assertNotIn('_fingerprint', row)
        reordered['requests'][0] = dict(reordered['requests'][0], path='/changed')
        self.assertNotEqual(before['_fingerprint'], normalize_record(reordered)['_fingerprint'])

    def test_failed_scan_is_not_reported_as_zero_tracking(self):
        row = normalize_record({'status': 'navigation_failed'})
        self.assertIsNone(row['third_party_count'])
        self.assertIsNone(row['cookie_count'])

    def test_every_python_entry_point_parses_even_when_ci_builds_saved_data(self):
        for path in (Path(__file__).resolve().parents[1] / 'scripts').glob('*.py'):
            with self.subTest(path=path.name):
                compile(path.read_text(), str(path), 'exec')
