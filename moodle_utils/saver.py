from plyer import notification
from playsound import playsound
import os
import json
import re

class Saver:

    def __init__(
        self, 
        path = os.path.join("consulted_courses\consulted_courses.json")
    ) -> None:
        # The path of the file that contains the consulted courses
        self.json_file_path = path
    
    def to_utf8(self, name):
        try:
            name = name.encode("iso-8859-1").decode('utf-8')
        except:
            pass
        return name
    
    def to_valid_name(self, name):
        new_name = re.sub(r'[\\/:*?"<>|]', "", name)
        new_name = self.to_utf8(new_name)
        return new_name

    def notify(self, file_name):
        notification.notify(
            title = 'Attention !!!',
            message = f"The file {file_name} has been downloaded successfully",
            app_icon = os.path.join("images/moodle.ico"),
            timeout = 10,
        )
        playsound(os.path.join('sounds/mixkit-arcade-magic-notification-2342.wav'))

    def get_consulted_courses(self):
        if not os.path.isfile(self.json_file_path):
            with open(self.json_file_path, "w") as file:
                json.dump({}, file)
        return json.load(open(self.json_file_path))
    
    def is_not_consulted(self, consulted_lectures, lecture_key):
        is_consulted = consulted_lectures.get(lecture_key, None)
        if is_consulted:
            return False
        else:
            return True
    
    def save_consulted_courses(self, consulted_courses):
        with open(self.json_file_path, "w") as file:
            json.dump(consulted_courses, file, indent=4)

    def save_file(self, response, download_path, file_name):
        file_saving_path = os.path.join(download_path, file_name)
        with open(file_saving_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)


if __name__ == "__main__":
    saver = Saver()
    