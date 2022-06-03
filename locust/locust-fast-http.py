import locust
from locust import task, between
from locust.contrib.fasthttp import FastHttpUser
from random import choice

users = ["Sir_Trashbin", "GloriousSushi", "MCRAW36", "DANGERBLOOM", "Shandowarden", "Happytimedean", "equityorasset", "zeren1ty"]
stocks = ["APPS", "JP", "NET", "TSLA"]

class User1(FastHttpUser):
    wait_time=between(3, 7)

    #@task
    #def react_home(self):
    #    self.client.get("")     #index

    @task(weight=3)
    def all_users(self):
        self.client.get(url="/all_users")

    @task(weight=2)
    def user(self):
        url = "/user/"+choice(users)
        self.client.get(url=url)
    
    @task(weight=1)
    def stock(self):
        url = "/stock/"+choice(stocks)
        self.client.get(url=url)