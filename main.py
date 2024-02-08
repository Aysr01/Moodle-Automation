from moodle_utils.moodle_api import MoodleAPI

if __name__ == "__main__":
    with MoodleAPI() as session:
        response = session.login()
        sesskey = session.get_sesskey(response)
        courses = session.get_courses_json(sesskey)
        desired_courses = session.desired_courses(courses)
        for course in desired_courses:
            session.download_all_content(course)