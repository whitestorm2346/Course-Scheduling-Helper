from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager

COURSE_INFO_PAGE = "https://azquery.tku.edu.tw/acad/query.asp"
SCHOOL_ADMINISTRATION_SYSTEM = "http://sinfo.ais.tku.edu.tw/eMis/"
SCHOOL_ADMINISTRATION_SYSTEM_STUDENT = "https://sso.tku.edu.tw/aissinfo/emis/TMW0040.aspx"
SSO_LOGIN_PAGE = "https://sso.tku.edu.tw/NEAI/logineb.jsp?myurl=https://sso.tku.edu.tw/aissinfo/emis/tmw0012.aspx"
SEARCH_PERSONAL_COURSE = "https://sso.tku.edu.tw/aissinfo/emis/TMWC020.aspx"


class Course:
    def __init__(self, grade, id, class_, type, credit, group, name, quota_limit, teacher, time) -> None:
        self.grade: int = grade  # 年級
        self.id: str = id  # 開課序號
        self.class_: str = class_  # 班別
        self.type: bool = type  # 必選修
        self.credit: int = credit  # 學分
        self.group: str = group  # 群別
        self.name: str = name  # 科目名稱
        self.quota_limit: int = quota_limit  # 人數設限
        self.teacher: str = teacher  # 授課老師
        self.time: str = time  # 上課時間/地點

    def __repr__(self) -> str:
        return f'{self.id} {self.name} {self.teacher} {self.time}'

    def __str__(self) -> str:
        return f'{self.id} {self.name} {self.teacher} {self.time}'

    def print(self) -> None:
        print(f'grade = {self.grade}')
        print(f'id = {self.id}')
        print(f'class = {self.class_}')
        print(f'type = {self.type}')
        print(f'credit = {self.credit}')
        print(f'group = {self.group}')
        print(f'name = {self.name}')
        print(f'quota limit = {self.quota_limit}')
        print(f'teacher = {self.teacher}')
        print(f'time = {self.time}')


class CourseSchedulingHelper:
    def __init__(self, student_id='', password='') -> None:
        self.student_id = student_id
        self.password = password
        self.__init_driver__()

    def __init_driver__(self) -> None:
        edge_options = Options()
        edge_options.add_argument('--log-level=3')
        self.driver = webdriver.Edge(
            EdgeChromiumDriverManager().install(),
            options=edge_options,

        )

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

    def __sso_login__(self) -> None:
        self.driver.get(SSO_LOGIN_PAGE)

        account_input = self.driver.find_element(
            By.XPATH, '//*[@id="username"]')
        account_input.clear()
        account_input.send_keys(self.student_id)

        password_input = self.driver.find_element(
            By.XPATH, '//*[@id="password"]')
        password_input.clear()
        password_input.send_keys(self.password)

        login_btn = self.driver.find_element(
            By.XPATH, '//*[@id="loginbtn"]')
        login_btn.click()

        if self.driver.current_url != SCHOOL_ADMINISTRATION_SYSTEM_STUDENT:
            msg = self.driver.find_element(
                By.XPATH, '//*[@id="eaiForm"]/div/article/section/fieldset/p[4]/font')
            print(msg.text)
            exit(1)

    def __close_pop_up_window__(self) -> None:
        handle = self.driver.window_handles
        self.driver.switch_to.window(handle[-1])
        self.driver.close()
        self.driver.switch_to.window(handle[0])

    def get_all_course_info(self) -> None:
        self.all_courses = []

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

                grade_text = course_info[1].text
                id_text = course_info[2].text
                class_text = course_info[6].text
                type_text = course_info[8].text
                credit_text = course_info[9].text
                group_text = course_info[10].text
                name_text = course_info[11].text
                quota_limit_text = course_info[12].text
                teacher_text = course_info[13].text
                time_text = [
                    course_info[14].text,
                    course_info[15].text  # if no class -> ''
                ]

                course = Course(
                    grade=grade_text,
                    id=id_text,
                    class_=class_text,
                    type=type_text,
                    credit=credit_text,
                    group=group_text,
                    name=name_text,
                    quota_limit=quota_limit_text,
                    teacher=teacher_text,
                    time=time_text
                )

                course.print()
                print('\n')

                self.all_courses.append(course)

        self.driver.close()

    def get_my_course_info(self) -> None:
        self.my_courses = []

        self.driver.get(SCHOOL_ADMINISTRATION_SYSTEM)
        self.__close_pop_up_window__()

        entry_link = self.driver.find_element(
            By.XPATH, '/html/body/table/tbody/tr[9]/td[2]/table/tbody/tr[10]/td[1]/a')
        entry_link.click()

        if self.driver.current_url == SSO_LOGIN_PAGE:
            self.__sso_login__()

        inner_entry_link = self.driver.find_element(
            By.XPATH, '//*[@id="form1"]/table/tbody/tr[3]/td/table/tbody/tr[8]/td[1]/p/a')
        inner_entry_link.click()

        start_searching_btn = self.driver.find_element(
            By.XPATH, '//*[@id="Button1"]')
        start_searching_btn.click()

        course_table = self.driver.find_element(
            By.XPATH, '//*[@id="DataGrid1"]')
        tr_list = course_table.find_elements(By.TAG_NAME, 'tr')

        for tr in tr_list:
            course_info = tr.find_elements(By.TAG_NAME, 'td')

            if course_info[1].text == '系所':
                continue
            elif course_info[0].text == '':
                self.my_courses[-1].time[1] = course_info[11].text
            else:
                grade_text = course_info[2].text
                id_text = course_info[0].text
                class_text = course_info[5].text
                type_text = course_info[7].text
                credit_text = course_info[8].text
                group_text = course_info[9].text
                name_text = course_info[3].text.split('\n')[0]
                quota_limit_text = ''
                teacher_text = course_info[10].text
                time_text = [course_info[11].text, '']

                course = Course(
                    grade=grade_text,
                    id=id_text,
                    class_=class_text,
                    type=type_text,
                    credit=credit_text,
                    group=group_text,
                    name=name_text,
                    quota_limit=quota_limit_text,
                    teacher=teacher_text,
                    time=time_text
                )

                self.my_courses.append(course)

        self.driver.close()

    def get_optional_courses(self) -> None:
        pass


if __name__ == "__main__":
    stu_id = input('請輸入學號: ')
    pw = input('請輸入密碼: ')

    course_scheduling_helper = CourseSchedulingHelper(
        student_id=stu_id,
        password=pw
    )
    course_scheduling_helper.get_my_course_info()

    for course in course_scheduling_helper.my_courses:
        course.print()
        print()
