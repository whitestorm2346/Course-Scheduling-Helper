from course_scheduling_helper import CourseSchedulingHelper, Course
import xlsxwriter

DAY = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']


class MakeSchedule:
    def __init__(self, courses_data: CourseSchedulingHelper) -> None:
        self.course_data = courses_data

    def __init_excel__(self) -> None:
        with xlsxwriter.Workbook('排課資料.xlsx') as workbook:
            worksheet = workbook.add_worksheet()

            for i in range(7):
                worksheet.write(chr(66 + i) + '1', DAY[i])

            for i in range(1, 15):
                worksheet.write('A' + str(i + 1), i)

    def update_optional_courses(self) -> None:
        pass

    def update_schedule(self) -> None:
        pass


if __name__ == "__main__":
    stu_id = input('請輸入學號: ')
    pw = input('請輸入密碼: ')

    scheduling_helper = CourseSchedulingHelper(
        student_id=stu_id,
        password=pw
    )

    scheduling_helper.get_all_course_info()
    scheduling_helper.get_my_course_info()

    make_schedule = MakeSchedule(courses_data=scheduling_helper)

    make_schedule.update_schedule()
    make_schedule.update_optional_courses()
