from course_scheduling_helper import CourseSchedulingHelper
import xlsxwriter

DAY = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
CLASS = [i for i in range(1, 15)]
COURSE_INFO = [
    '開課序號', '科目名稱', '授課老師',
    '年級', '必選修', '學分', '上課時間/地點'
]


class MakeSchedule:
    def __init__(self) -> None:
        self.__init_excel__()

    def __init_excel__(self) -> None:
        self.__init_optional_courses_page__()
        self.__init_schedule_page__()

    def __init_optional_courses_page__(self) -> None:
        with xlsxwriter.Workbook('排課資料.xlsx') as workbook:
            worksheet = workbook.add_worksheet(name='未衝堂課程資訊')

            worksheet.write_row(0, 0, COURSE_INFO)

    def __init_schedule_page__(self) -> None:
        with xlsxwriter.Workbook('排課資料.xlsx') as workbook:
            worksheet = workbook.add_worksheet(name='當前個人課表')

            worksheet.write_row(0, 1, DAY)
            worksheet.write_column(1, 0, CLASS)

    def update_optional_courses(self, courses_data: CourseSchedulingHelper) -> None:
        courses_data.get_optional_courses()

        # worksheet: 未衝堂課程資訊

    def update_schedule(self, courses_data: CourseSchedulingHelper) -> None:
        courses_data.get_my_course_info()

        # worksheet: 當前個人課表


if __name__ == "__main__":
    stu_id = input('請輸入學號: ')
    pw = input('請輸入密碼: ')

    scheduling_helper = CourseSchedulingHelper(
        student_id=stu_id,
        password=pw
    )

    scheduling_helper.get_all_course_info()
    scheduling_helper.get_my_course_info()

    make_schedule = MakeSchedule()

    make_schedule.update_schedule(courses_data=scheduling_helper)
    make_schedule.update_optional_courses(courses_data=scheduling_helper)
