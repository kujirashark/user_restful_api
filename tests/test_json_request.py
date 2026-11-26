"""_json_request must accept JSON bodies, form data and query strings, and still reject JSON arrays.

common/common_request_process.py read request.data (raw body only), so form-encoded and query-string
requests came back empty and every required-param check failed. The issue's proposed fix
(request.values.to_dict()) fixed that but dropped JSON body support entirely. The fix reads the JSON
body with get_json(force=True, silent=True), still rejects JSON arrays, and merges query/form params.

Run from the repository root: python -m unittest tests/test_json_request.py
"""
import unittest

from common.common_request_process import req


class FakeValues(dict):
    def to_dict(self):
        return dict(self)


class FakeRequest(object):
    def __init__(self, body=None, values=None):
        self._body = body
        self.values = FakeValues(values or {})

    def get_json(self, force=True, silent=True):
        if self._body is None:
            return None
        import json
        try:
            return json.loads(self._body)
        except Exception:
            if silent:
                return None
            raise


class JsonRequestTest(unittest.TestCase):
    def test_json_body_still_works(self):
        data = req._json_request(FakeRequest(body='{"name": "ops", "count": 2}'))
        self.assertEqual(data, {"name": "ops", "count": 2})

    def test_empty_body_returns_empty_dict(self):
        self.assertEqual(req._json_request(FakeRequest(body=None)), {})

    def test_invalid_body_does_not_raise(self):
        data = req._json_request(FakeRequest(body=b'\xff\xfe not json'))
        self.assertEqual(data, {})

    def test_json_array_is_rejected(self):
        self.assertFalse(req._json_request(FakeRequest(body='[1, 2, 3]')))

    def test_form_and_query_params_are_merged(self):
        data = req._json_request(FakeRequest(body=None, values={"name": "ops"}))
        self.assertEqual(data, {"name": "ops"})

    def test_query_params_fill_empty_body(self):
        data = req._json_request(FakeRequest(body='{"page_size": 10}', values={"current_page": "2"}))
        self.assertEqual(data, {"page_size": 10, "current_page": "2"})


if __name__ == "__main__":
    unittest.main()
