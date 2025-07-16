import os
from locust import HttpUser, task


class GetList(HttpUser):
    host = os.getenv("HOST", "http://localhost:8000")
    endpoint = os.getenv("ENDPOINT", "/zaken/api/v1/zaken")

    @task
    def get(self):
        self.client.get(self.endpoint)
