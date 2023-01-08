from tkinter import *
from tkinter import ttk
from course_scheduling_helper import CourseSchedulingHelper
from make_schedule import MakeSchedule
from threading import Thread

ENGLISH = 'Times New Roman'
CHINESE = '微軟正黑體'


class MainUI:
    def __init__(self) -> None:
        self.__init_main_frame__()
        self.__init_login_frame__()
        self.__init_buttons__()

        # need to make a login first

        self.scheduling_helper = CourseSchedulingHelper()
        self.make_schedule = MakeSchedule()
        self.threads = []

    def __init_main_frame__(self) -> None:
        self.root = Tk()
        self.root.resizable(False, False)
        self.root.geometry("300x360")
        self.root.title('Course Scheduling Helper')

    def __init_login_frame__(self) -> None:
        self.login_frame = LabelFrame(self.root)
        self.login_frame.config(text=' Login ', font=(ENGLISH, 12))
        self.login_frame.pack(side=TOP, fill='x', padx=10, pady=10)

        self.student_id_label = Label(self.login_frame)
        self.student_id_label.config(
            text='Student ID', font=(ENGLISH, 14, 'bold'))
        self.student_id_label.pack(side=TOP, pady=5)

        self.student_id = StringVar(self.login_frame)
        self.student_id_entry = Entry(self.login_frame)
        self.student_id_entry.config(
            font=(ENGLISH, 12), textvariable=self.student_id)
        self.student_id_entry.pack(side=TOP, fill='x', padx=5, pady=10)

        self.password_label = Label(self.login_frame)
        self.password_label.config(text='Password', font=(ENGLISH, 14, 'bold'))
        self.password_label.pack(side=TOP, pady=5)

        self.password = StringVar(self.login_frame)
        self.password_entry = Entry(self.login_frame)
        self.password_entry.config(
            font=(ENGLISH, 12), textvariable=self.password)
        self.password_entry.pack(side=TOP, fill='x', padx=5, pady=10)

    def __init_buttons__(self) -> None:
        self.update_optional_courses_btn = Button(self.root)
        self.update_optional_courses_btn.config(
            text='update optional courses', font=(ENGLISH, 14, 'bold'),
            height=2, width=25, command=self.__update_optional_courses_onclick__
        )
        self.update_optional_courses_btn.pack(side=TOP, padx=20, pady=5)

        self.update_schedule_btn = Button(self.root)
        self.update_schedule_btn.config(
            text='update schedule', font=(ENGLISH, 14, 'bold'),
            height=2, width=25, command=self.__update_schedule_onclick__
        )
        self.update_schedule_btn.pack(side=TOP, padx=20, pady=5)

    def __update_optional_courses_onclick__(self):
        self.threads.append(Thread(
            target=self.make_schedule.update_optional_courses,
            args=(self.scheduling_helper, )
        ))
        self.threads[-1].start()

    def __update_schedule_onclick__(self):
        self.threads.append(Thread(
            target=self.make_schedule.update_schedule,
            args=(self.scheduling_helper, )
        ))
        self.threads[-1].start()

    def run(self) -> None:
        self.root.mainloop()


if __name__ == "__main__":
    main_ui = MainUI()
    main_ui.run()
