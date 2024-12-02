from subject import Subject
from observer import Observer
from channel import *

class Follower(Observer):
    def __init__(self, follower_name: str):
        self.__follower_name = follower_name
        self.__last_status: str = ""

    def update(self, status: str):
        self.__last_status = status
        print(f"{self.__follower_name} received update: {status}")

    def play(self) -> None:
        if self.__last_status:
            print(f"{self.__follower_name} is now playing: {self.__last_status}")
        else:
            print(f"{self.__follower_name} has no new content to play.")