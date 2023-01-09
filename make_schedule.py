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
        self.workbook = xlsxwriter.Workbook('排課資料.xlsx')
        self.worksheets = {}
        self.__init_excel__()

    def __init_excel__(self) -> None:
        self.__init_schedule_page__()
        self.__init_optional_courses_page__()

    def __init_optional_courses_page__(self) -> None:
        self.worksheets['course_info'] = self.workbook.add_worksheet(
            name='未衝堂課程資訊')

        self.worksheets['course_info'].write_row(0, 0, COURSE_INFO)

    def __init_schedule_page__(self) -> None:
        self.worksheets['schedule'] = self.workbook.add_worksheet(
            name='當前個人課表')

        self.worksheets['schedule'].write_row(0, 1, DAY)
        self.worksheets['schedule'].write_column(1, 0, CLASS)

    def __get_coor__(self, time_info) -> None:
        rows = time_info[1].split(',')
        rows = [int(row) for row in rows]

        if time_info[0] == "一":
            col = 1
        elif time_info[0] == "二":
            col = 2
        elif time_info[0] == "三":
            col = 3
        elif time_info[0] == "四":
            col = 4
        elif time_info[0] == "五":
            col = 5
        else:
            col = 6

        return rows, col

    def update_optional_courses(self, courses_data: CourseSchedulingHelper) -> None:
        courses_data.get_all_course_info()
        row = 1

        for course in courses_data.all_courses:
            self.worksheets['course_info'].write(row, 0, course.id)
            self.worksheets['course_info'].write(row, 1, course.name)
            self.worksheets['course_info'].write(row, 2, course.teacher)
            self.worksheets['course_info'].write(row, 3, course.grade)
            self.worksheets['course_info'].write(row, 4, course.type)
            self.worksheets['course_info'].write(row, 5, course.credit)
            self.worksheets['course_info'].write(row, 6, course.time)

            row += 1

    def update_schedule(self, courses_data: CourseSchedulingHelper) -> None:
        courses_data.get_my_course_info()

        for course in courses_data.my_courses:
            for time in course.time:
                if time == '':
                    continue

                time_infos = time.split(' /')
                rows, col = self.__get_coor__(time_info=time_infos)

                for row in rows:
                    self.worksheets['schedule'].write(row, col, course.name)

    def save(self) -> None:
        self.workbook.close()


if __name__ == "__main__":
    stu_id = input('請輸入學號: ')
    pw = input('請輸入密碼: ')

    scheduling_helper = CourseSchedulingHelper(
        student_id=stu_id,
        password=pw
    )

    make_schedule = MakeSchedule()

    make_schedule.update_schedule(courses_data=scheduling_helper)
    # make_schedule.update_optional_courses(courses_data=scheduling_helper)

    scheduling_helper.close()
    make_schedule.save()
