from locust import HttpUser, task


class GetList(HttpUser):
    @task
    def get(self):
        self.client.get("/zaken/api/v1/zaken?pageSize=100")
