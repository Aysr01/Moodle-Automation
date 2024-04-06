## 1- Introduction
Moodle is a Learning Management System (LMS) used to create and manage online courses. Manually checking for and installing new courses can be a tedious task. To streamline this process, "moodle-automation" is an automation tool that can discover new courses and automatically install them on your local Moodle instance.

## 2- Run the Program
### 2.1- Create Environment Variables
In your local computer create two environment variables `USER_NAME` and `PASSWORD`, then assign to them respectively your name and password on Moodle platform.
### 2.2- Configure Moodle Automation tool
To configure the Moodle Automation tool, you need to edit the `moodle_utils/constantes.py` file. In this file, you can set a flag to determine whether you want to download all the courses you've taken during your journey at INPT, or just the current, active courses. This allows you to either update your local Moodle instance with all the historical course content, or focus on the most recent and relevant courses. Additionally, you can specify the local file path where you want the downloaded course materials to be saved, ensuring the courses are stored in an organized and accessible location on your computer. By configuring these settings in the constantes.py file, you can tailor the Moodle Automation tool to your specific requirements, making it a more effective and efficient tool for managing your Moodle platform and course content.

![image](https://github.com/Aysr01/moodle-automation/assets/114707989/1bf84d20-7eb1-4bf6-abfb-3e949f3697bc)
### 2.3- Run Automation Tool
To run the bot you should execute the `main.py` file.
