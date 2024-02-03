
import re


TD_RE = re.compile("td|travaux dirigés|exercices|série", re.IGNORECASE)
TP_RE = re.compile("tp|travaux pratique", re.IGNORECASE)
EXT_RE = re.compile(r"\.[a-z0-9]+")      # Extension of the file
MOODLE_URL = "http://m.inpt.ac.ma/login/index.php"
PDF = "http://m.inpt.ac.ma/theme/image.php/clean/core/1614806513/f/pdf-24"


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
