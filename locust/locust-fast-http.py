import locust
from locust import task, between
from locust.contrib.fasthttp import FastHttpUser
from urllib3 import PoolManager
from random import choice

users = ["Sir_Trashbin", "GloriousSushi", "MCRAW36", "DANGERBLOOM", "Shandowarden", "Happytimedean", "equityorasset", "zeren1ty"]
stocks = ["APPS", "JP", "NET", "TSLA"]

class User1(FastHttpUser):
    wait_time=between(1, 6)
    pool_manager = PoolManager(maxsize=10, block=True)
    #@task
    #def react_home(self):
    #    self.client.get("")     #index

    @task(weight=3)
    def all_users(self):
        self.client.get(url="/all_users",
            headers={"Connection": "keep-alive"}
        )

    @task(weight=2)
    def user(self):
        url = "/user/"+choice(users)
        self.client.get(url=url,
            headers={"Connection": "keep-alive"}
        )
    
    @task(weight=1)
    def stock(self):
        url = "/stock/"+choice(stocks)
        self.client.get(url=url,
            headers={"Connection": "keep-alive"}
        )