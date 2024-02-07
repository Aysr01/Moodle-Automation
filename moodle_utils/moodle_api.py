import requests
import os
from moodle_utils.constantes import MOODLE_URL, REQUEST_URL, RAW_DATA, SAVING_PATH, DOWNLOAD_ALL
from moodle_utils.saver import Saver
from bs4 import BeautifulSoup
import logging
import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"   
)

logger = logging.getLogger(__name__)


class MoodleAPI(requests.Session):

    def __init__(self) -> None:
        self.user_name = os.environ['USER_NAME']
        self.password = os.environ['PASSWORD']
        self.saver = Saver()
        super().__init__()

    def get_login_token(self):
        response = self.get(MOODLE_URL)
        if response.status_code != 200:
            logger.error(
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
        try:
            response = self.post(
                MOODLE_URL,
                data=payload
            )
        except Exception as e:
            logger.error(f"Error while logger in")
            return None
        return response

    def get_sesskey(self, response):
        if (response.status_code != 200):
            raise Exception(f"Error while logger in, status code: {response.status_code}")
        soup = BeautifulSoup(response.text, "html.parser")
        page_title = soup.find("title").text
        if page_title.__contains__("moodle.inpt.ac.ma"):
            message = "make sure your credentials are correct"
            raise Exception(
                f"Error while logger in: {message}"
            )
        soup = BeautifulSoup(response.text, "html.parser")
        return (soup.find("script", {"type": "text/javascript"})
                    .text
                    .split('"sesskey":')[1]
                    .split(",")[0]
                    .replace('"', '')
                )

    def get_courses_json(self, sshkey):
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

    def desired_courses(self, courses_data):
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
        if not DOWNLOAD_ALL:
            max = df["enddate"].max()
            df = df[
                (df["enddate"] == max) | 
                (df["fullname"].str.contains("AFFICHAGE", case=False))
            ]
        df["viewurl"] = df["viewurl"] + "&lang=en"   # force the language to be english
        desired_courses_info = df[["viewurl", "fullname"]].values 
        return desired_courses_info

    def get_lectures(self, course_info, cls="activityinstance"):
        course_url = course_info[0]
        course_name = (
            course_info[1].encode("iso-8859-1")
                          .decode('utf-8')
                          .strip(" ")
        )                                     
        response = self.get(course_url)
        if response.status_code != 200:
            raise Exception(f"Error while getting the course page: {response.status_code}")
        soup = BeautifulSoup(response.text, "html.parser")
        elements = soup.find_all(class_=cls)
        links_and_types = [
            (
            element.find("a")["href"],
            element.find("span", {"class": "instancename"})
            )
            for element in elements[int(cls!="fileuploadsubmission"):]
        ]
        return course_name, links_and_types
    
    def download_file(self, url, download_path):
        response = self.get(url, stream=True)
        if response.status_code != 200:
            raise Exception(f"Error while getting the file: {response.status_code}")
        file_name = (response.headers["Content-Disposition"]
                             .split("filename=")[1]
                             .strip('"'))
        self.saver.save_file(response, download_path, file_name)
        self.saver.notify(file_name)

    def download_folder(self, folder_url, path, folder_name, fcls="fp-filename-icon"):
        _, lectures = self.get_lectures(folder_url, cls = fcls)
        if len(lectures) == 0:
            return None
        os.makedirs(os.path.join(path, folder_name), exist_ok=True)
        for lecture in lectures:
            lecture_link = lecture[0]
            self.download_file(lecture_link, os.path.join(path, folder_name))

    def download_assignement(self, Assignement_url, path, Assignement_name):
        acls = "fileuploadsubmission"
        self.download_folder(Assignement_url, path, Assignement_name, acls)

    def download_all_content(self, course_url):
        course_name, lectures = self.get_lectures(course_url)
        os.makedirs(os.path.join(SAVING_PATH, course_name), exist_ok=True)
        for lecture in lectures:
            lecture_link = lecture[0]
            lecture_name = lecture[1].text.split("span")[0].strip(" ")
            lecture_type = lecture[1].span.text
            path = SAVING_PATH / course_name
            if "Folder" in lecture_type:
                self.download_folder(lecture_link, path, lecture_name)
            elif "Assignment" in lecture_type:
                self.download_assignement(lecture_link, path, lecture_name)
            else:
                self.download_file(lecture_link, path)




