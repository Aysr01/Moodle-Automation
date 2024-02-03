import requests
import os
from moodle_utils.constantes import MOODLE_URL, REQUEST_URL, RAW_DATA
from bs4 import BeautifulSoup
import logging
import pandas as pd


os.environ['USER_NAME'] = "sarab.ayoub"
os.environ['PASSWORD'] = "ayoubsarab2002@"


class MoodleAPI(requests.Session):

    def __init__(self) -> None:
        self.user_name = os.environ['USER_NAME']
        self.password = os.environ['PASSWORD']
        super().__init__()

    def get_login_token(self):
        response = self.get(MOODLE_URL)
        if response.status_code != 200:
            logging.error(
                f"Error while getting the login page: {response.status_code}"
            )
            return None
        soup0 = BeautifulSoup(response.text, "html.parser")
        return soup0.find("input", {"name": "logintoken"})["value"]

    def login(self):
        payload = {
            'username': self.user_name,
            'password': self.password,
            'logintoken': self.get_login_token(),
        }
        response = self.post(
            MOODLE_URL,
            data=payload
        )
        return response

    def get_sesskey(self, response):
        if (response.status_code != 200):
            raise Exception(f"Error while logging in, status code: {response.status_code}")
        soup = BeautifulSoup(response.text, "html.parser")
        page_title = soup.find("title").text
        if page_title.__contains__("moodle.inpt.ac.ma"):
            message = "make sure your credentials are correct"
            raise Exception(
                f"Error while logging in: {message}"
            )
        soup = BeautifulSoup(response.text, "html.parser")
        return (soup.find("script", {"type": "text/javascript"})
                    .text
                    .split('"sesskey":')[1]
                    .split(",")[0]
                    .replace('"', '')
                )

    def get_course_json(self, sshkey):
        response = self.post(
            REQUEST_URL.format(sshkey),
            data=RAW_DATA,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        if response.status_code != 200:
            raise Exception(f"Error while getting the courses error code: {response.status_code}")
        response_json = response.json()
        if response_json[0]["error"]:
            raise Exception("An error occured while trying to retrieve courses data")
        return response_json[0]["data"]["courses"]
    
    def current_courses(self, courses_data):
        useful_columns = [
            "id", "fullname",
            "enddate", "viewurl",
        ]
        useful_data = [
            {
                col: course.get(col, None)
                for col in useful_columns
            }
            for course in courses_data
        ]
        df = pd.DataFrame(useful_data)
        max = df["enddate"].max()
        current_courses = df[(df["enddate"] == max) | (df["fullname"].str.contains("AFFICHAGE", case=False))]
        return current_courses
