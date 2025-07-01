import requests
import unittest
from deepdiff import DeepDiff

OLD_LIST = "/zaken/api/v1/zaken?pageSize=100"
NEW_LIST = "/zaken/api/v1/zaken?pageSize=100"


OLD_LIST = "http://localhost:8000/zaken/api/v1/zaken?pageSize=10"
NEW_LIST = "http://localhost:8001/zaken/api/v1/zaken?pageSize=10"

AUTH_HEADERS = {
    "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJ0ZXN0IiwiaWF0IjoxNzUxMzc0Njc0LCJjbGllbnRfaWQiOiJ0ZXN0IiwidXNlcl9pZCI6InRlc3QiLCJ1c2VyX3JlcHJlc2VudGF0aW9uIjoidGVzdCJ9.-Qm91a4esBnk3S4KcyEd9-mMT_mYgT6Vu_0w_OBVZ1c",
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
    def test_compare_api_responses(self):
        response1 = requests.get(OLD_LIST, headers=AUTH_HEADERS)
        response2 = requests.get(NEW_LIST)

        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)

        data1 = response1.json()
        data2 = response2.json()

        self.assertEqual(set(data1.keys()), set(data2.keys()))

        for e in data1["results"]:
            e.pop("_expand")
            for key, value in e.items():
                e[key] = replace_url(value)

        for e in data2["results"]:
            for key, value in e.items():
                e[key] = replace_url(value)

        self.assertEqual(len(data1["results"]), len(data2["results"]))
        self.assertEqual(data1["count"], data2["count"])

        # self.assertEqual(data1["next"], data2["next"])
        # self.assertEqual(data1["previous"], data2["previous"])

        diff = DeepDiff(
            data1["results"], data2["results"], view="tree", verbose_level=2
        )
        if diff:
            for diff_type, changes in diff.items():
                print(f"{diff_type}:")
                for change in changes:
                    print(f"T1 {change.t1}, T2 {change.t2}")
            self.fail("API responses differ")


if __name__ == "__main__":
    unittest.main()
