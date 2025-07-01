import unittest

import requests
from deepdiff import DeepDiff

OLD_LIST = "http://localhost:8000/zaken/api/v1/zaken?pageSize=100"  # OpenZaak
NEW_LIST = "http://localhost:8001/zaken/api/v1/zaken?pageSize=100"  # FastApi

AUTH_HEADERS = {
    "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJ0ZXN0IiwiaWF0IjoxNzUxMzc5MDMwLCJjbGllbnRfaWQiOiJ0ZXN0IiwidXNlcl9pZCI6InRlc3QiLCJ1c2VyX3JlcHJlc2VudGF0aW9uIjoidGVzdCJ9.mFEKhaCGnXOw_nLJE9nOwR-18q0i3MNhRJHEcQbNJ8g",
    "Accept-Crs": "EPSG:4326",
}


def replace_url(data):
    if isinstance(data, dict):
        return {k: replace_url(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [replace_url(item) for item in data]
    elif isinstance(data, str):
        return data.replace("http://localhost:8001/", "http://localhost:8000/")
    else:
        return data


class TestAPIResponses(unittest.TestCase):
    def fetch_all_results(self, url, headers=None):
        results = []
        i = 0
        while url and i < 20:
            print(f"Requests: {url}")
            response = requests.get(url, headers=headers)
            self.assertEqual(response.status_code, 200)
            data = response.json()
            for e in data["results"]:
                e.pop("_expand", None)
                for key, value in e.items():
                    e[key] = replace_url(value)
            results.extend(data["results"])
            url = data.get("next")
            i += 1
        return results

    def test_compare_api_responses(self):
        results_old = self.fetch_all_results(OLD_LIST, headers=AUTH_HEADERS)
        results_new = self.fetch_all_results(NEW_LIST)

        self.assertEqual(len(results_old), len(results_new))

        diff = DeepDiff(results_old, results_new, view="tree", verbose_level=2)
        if diff:
            for diff_type, changes in diff.items():
                print(f"{diff_type}:")
                for change in changes:
                    print(change)
            self.fail("API responses differ")


if __name__ == "__main__":
    unittest.main()
