import locust
from locust import HttpUser, task, between
from random import choice

users = ["Sir_Trashbin", "GloriousSushi", "MCRAW36", "DANGERBLOOM", "Shandowarden", "Happytimedean", "equityorasset", "zeren1ty"]
stocks = ["APPS", "JP", "NET", "TSLA"]

class User1(HttpUser):
    wait_time=between(3, 7)

    #@task
    #def react_home(self):
    #    self.client.get("")     #index
    
    @task(weight=3)
    def all_users(self):
        self.client.get(url="/all_users")

    @task(weight=1)
    def user(self):
        url = "/user/"+choice(users)
        print(url)
        self.client.get(url=url)
    
    @task(weight=1)
    def stock(self):
        url = "/stock/"+choice(stocks)
        print(url)
        self.client.get(url=url)