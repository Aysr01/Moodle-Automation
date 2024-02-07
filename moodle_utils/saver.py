from plyer import notification
from playsound import playsound
import os

class Saver:
    
    def save_file(self, response, download_path, file_name):
        file_name = file_name.encode("iso-8859-1").decode('utf-8')
        with open(download_path / file_name, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)

    def notify(self, file_name):
        notification.notify(
            title = 'Attention !!!',
            message = f"The file {file_name} has been downloaded successfully",
            app_icon = os.path.join("images\moodle.ico"),
            timeout = 10,
        )
        playsound(os.path.join('sounds\mixkit-arcade-magic-notification-2342.wav'))


if __name__ == "__main__":
    saver = Saver()
    for i in range(1):
       saver.notify("moodle.png")
    