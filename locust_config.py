import time
from locust import HttpUser, task, between


class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def fastapi(self):
        self.client.get(url="/fastapi/message/1")

    @task
    def flask(self):
        self.client.get(url="/flask/message/1")

    @task
    def django(self):
        self.client.get(url="/django/message/1")
