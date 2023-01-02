from tkinter import *
from tkinter import ttk
from datetime import datetime
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import threading

COURSE_INFO_PAGE = "https://azquery.tku.edu.tw/acad/query.asp"
SCHOOL_ADMINISTRATION_SYSTEM = "https://sso.tku.edu.tw/aissinfo/emis/TMW0000.aspx"
SCHOOL_ADMINISTRATION_SYSTEM_STUDENT = "https://sso.tku.edu.tw/aissinfo/emis/TMW0040.aspx"
SSO_LOGIN_PAGE = "https://sso.tku.edu.tw/NEAI/logineb.jsp?myurl=https://sso.tku.edu.tw/aissinfo/emis/tmw0012.aspx"


class Course:
    def __init__(self, grade, id, class_, type, credit, group, name, quota_limit, teacher, time) -> None:
        self.grade = grade  # 年級
        self.id = id  # 開課序號
        self.class_ = class_  # 班別
        self.type = type  # 0: 必修, 1: 選修
        self.credit = credit  # 學分
        self.group = group  # 群別
        self.name = name  # 科目名稱
        self.quota_limit = quota_limit  # 人數設限
        self.teacher = teacher  # 授課老師
        self.time = time  # 上課時間/地點

    def get_info(self) -> str:
        return ''

    def print(self) -> None:
        pass


class CourseSchedulingHelper:
    def __init__(self, student_id='', password='') -> None:
        self.student_id = student_id
        self.password = password
        self.__init_driver__()

    def __init_driver__(self) -> None:
        edge_options = webdriver.EdgeOptions()
        edge_options.add_argument('--log-level=3')
        self.driver = webdriver.Edge(EdgeChromiumDriverManager().install())

    def __course_search_setting__(self, value) -> None:
        # 科目時段
        select_by_time = self.driver.find_element(
            By.XPATH, '//*[@id="Radio4"]')
        select_by_time.click()

        # 學院
        academy = Select(self.driver.find_element(
            By.XPATH, '/html/body/table[3]/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[5]/td[2]/select[1]'))
        academy.select_by_value('ALL')

        # 系所
        department = Select(self.driver.find_element(
            By.XPATH, '/html/body/table[3]/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[5]/td[2]/select[2]'))
        department.select_by_value('ALL')

        # 星期一 ~ 五
        day = Select(self.driver.find_element(
            By.XPATH, '/html/body/table[3]/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[5]/td[2]/select[3]'))
        day.select_by_value(str(value))

        # 第一節
        start_time = Select(self.driver.find_element(
            By.XPATH, '/html/body/table[3]/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[5]/td[2]/small/select[1]'))
        start_time.select_by_value('01')

        # 第十節
        end_time = Select(self.driver.find_element(
            By.XPATH, '/html/body/table[3]/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[5]/td[2]/small/select[2]'))
        end_time.select_by_value('10')

        # 需完全符合查詢時段
        time_in_range = self.driver.find_element(
            By.XPATH, '/html/body/table[3]/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[5]/td[3]/input[3]')
        time_in_range.click()

    def run(self) -> None:
        self.student_id = input('請輸入學號: ')
        self.password = input('請輸入密碼: ')

    def get_all_course_info(self) -> None:
        self.courses = []

        for day in range(1, 6):
            self.driver.get(COURSE_INFO_PAGE)

            self.__course_search_setting__(value=day)  # 前置設定

            # 進入查詢
            search = self.driver.find_element(
                By.XPATH, '/html/body/table[2]/tbody/tr/td[5]/input')
            search.click()

            # 課程表
            course_table = self.driver.find_element(
                By.XPATH, '/html/body/div/center/table[2]')
            tr_list = course_table.find_elements(By.TAG_NAME, 'tr')

            for tr in tr_list:
                course_info = tr.find_elements(By.TAG_NAME, 'td')

                try:
                    course_info[0].find_element(By.TAG_NAME, 'img')
                except Exception:
                    continue

                self.courses.append(Course(
                    grade=course_info[1],
                    id=course_info[2],
                    class_=course_info[6],
                    type=course_info[8],
                    credit=course_info[9],
                    group=course_info[10],
                    name=course_info[11],
                    quota_limit=course_info[12],
                    teacher=course_info[13],
                    time=[course_info[14], course_info[15]]
                ))

    def get_my_course_info(self) -> None:
        pass


class MainUI:
    def __init__(self) -> None:
        self.threads = []

    def run(self) -> None:
        pass


if __name__ == "__main__":
    course_scheduling_helper = CourseSchedulingHelper()
    course_scheduling_helper.get_all_course_info()
