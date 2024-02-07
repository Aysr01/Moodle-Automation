import pathlib
import re
import os


MOODLE_URL = "http://m.inpt.ac.ma/login/index.php"


RAW_DATA = (
    '[{"index":0,'
    '"methodname":"core_course_get_enrolled_courses_by_timeline_classification",'
    '"args":{"offset":0,"limit":96,"classification":"inprogress","sort":"fullname"}}]'
)    # This is the raw data that will be sent to the server to get the courses data


REQUEST_URL = (
        "http://m.inpt.ac.ma/lib/ajax/service.php?"
        "sesskey={}&"
        "info=core_course_get_enrolled_courses_by_timeline_classification"
)   # This is a template string that will be formatted with the sesskey


SAVING_PATH = pathlib.Path.home() / "Downloads" / "Moodle"
os.makedirs(SAVING_PATH, exist_ok=True)

# Download all files from the moodle, even the old ones
DOWNLOAD_ALL = False