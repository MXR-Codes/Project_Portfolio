import wx
from student_management_system import StudentManagementSystem
from grade_editor import GradeEditorDialog

class MainFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MainFrame, self).__init__(parent, title=title, size=(1000, 600))

        self.display_grades_sno = None
        self.panel = wx.Panel(self)
        self.sms = StudentManagementSystem()
        self.init_ui()
        self.Bind(wx.EVT_BUTTON, self.on_refresh)


    def on_refresh(self, event):
        # Refresh the interface
        self.Refresh()

    def init_ui(self):
        # create layout
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Add the student information area
        self.add_student_section(vbox)

        # In the init ui method in your MainFrame class
        self.insert_grades_for_student_section(vbox)

        # View and modify the student information area
        self.view_student_section(vbox)

        # Add modified grade information area
        self.add_update_grade_section(vbox)

        # View and modify the grade information area
        self.view_grade_section(vbox)

        self.panel.SetSizer(vbox)

        # Add the new delete student section
        self.delete_student_section(vbox)

        # View all student and grade information areas
        self.view_all_students_section(vbox)

        # Update students' information
        self.update_student_section(vbox)

        # Query and update the grades
        self.query_and_update_grade_section(vbox)

    def query_and_update_grade_section(self, vbox):
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        st1 = wx.StaticText(self.panel, label='Query and Update Grade: Enter Course')
        self.query_grade_course = wx.ComboBox(self.panel, choices=self.get_course_choices(), style=wx.CB_DROPDOWN)
        query_grade_btn = wx.Button(self.panel, label='Query and Update Grade')
        query_grade_btn.Bind(wx.EVT_BUTTON, self.on_query_and_update_grade)
        hbox.Add(st1, flag=wx.RIGHT, border=8)
        hbox.Add(self.query_grade_course, proportion=1)
        hbox.Add(query_grade_btn, proportion=1)
        vbox.Add(hbox, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)
        self.Refresh()


    def on_query_and_update_grade(self, event):
        course_query = self.query_grade_course.GetValue()  #Get selected courses
        # Method: get_all_students_and_grades_for_course
        students_and_grades = self.sms.get_all_students_and_grades_for_course(
        course_query.lower())  # Converting course to lowercase
        self.Refresh()
        self.panel.Layout()
        self.panel.Refresh()
        wx.PostEvent(self, wx.PyCommandEvent(wx.EVT_BUTTON.typeId, self.GetId()))
        if not students_and_grades:
            wx.MessageBox(f'No information found for Course {course_query}!', 'Error', wx.OK | wx.ICON_ERROR)
        else:
            GradeEditorDialog(self, f'Students and Grades for {course_query.capitalize()}', students_and_grades,
                              course_query.lower())



    def view_grade_section(self, vbox):
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        st1 = wx.StaticText(self.panel, label='View Grade: Enter Sno, Course')
        self.view_grade_sno = wx.TextCtrl(self.panel)
        course_choices = ["math", "english", "python"]
        self.view_grade_course = wx.ComboBox(self.panel, choices=course_choices, style=wx.CB_DROPDOWN)
        view_grade_btn = wx.Button(self.panel, label='View Grade')
        view_grade_btn.Bind(wx.EVT_BUTTON, self.on_view_grade)
        hbox.Add(st1, flag=wx.RIGHT, border=8)
        hbox.Add(self.view_grade_sno, proportion=1)
        hbox.Add(self.view_grade_course, proportion=1)
        hbox.Add(view_grade_btn, proportion=1)
        vbox.Add(hbox, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

    def on_view_grade(self, event):
        sno_to_view = self.view_grade_sno.GetValue()
        course_to_view = self.view_grade_course.GetValue()
        # Method: get_grade
        grade_info = self.sms.get_grade(sno_to_view, course_to_view.lower())  # Converting course to lowercase

        if 'not_found' in grade_info:
            wx.MessageBox(f'Grade not found for Student {sno_to_view} in Course {course_to_view}!', 'Error',
                          wx.OK | wx.ICON_ERROR)
        elif 'error' in grade_info:
            wx.MessageBox(f'Error retrieving grade information for Student {sno_to_view} in Course {course_to_view}!',
                          'Error', wx.OK | wx.ICON_ERROR)
        else:
            course_grade = grade_info.get(course_to_view)
            if course_grade is not None:
                wx.MessageBox(f'Grade Information:\n{course_to_view.capitalize()}: {course_grade}',
                              'Grade Info', wx.OK | wx.ICON_INFORMATION)
            else:
                wx.MessageBox(f'Grade not found for Student {sno_to_view} in Course {course_to_view}!', 'Error',
                              wx.OK | wx.ICON_ERROR)

    def view_student_section(self, vbox):
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        st1 = wx.StaticText(self.panel, label='View Student: Enter Sno')
        self.view_sno = wx.TextCtrl(self.panel)
        view_btn = wx.Button(self.panel, label='View')
        view_btn.Bind(wx.EVT_BUTTON, self.on_view_student)
        hbox.Add(st1, flag=wx.RIGHT, border=8)
        hbox.Add(self.view_sno, proportion=1)
        hbox.Add(view_btn, proportion=1)
        vbox.Add(hbox, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

    def on_view_student(self, event):
        sno_to_view = self.view_sno.GetValue()
        # Method: get_student_info
        student_info = self.sms.get_student(sno_to_view)

        if student_info:
            wx.MessageBox(f'Student Information:\n{student_info}',
                          'Student Info', wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox(f'Student with Sno {sno_to_view} not found!',
                          'Error', wx.OK | wx.ICON_ERROR)

    def add_update_grade_section(self, vbox):
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        st1 = wx.StaticText(self.panel,
        label='Add Or Update Grade: Enter Sno, Course, Grade')
        self.add_grade_sno = wx.TextCtrl(self.panel)
        course_choices = ["math", "english", "python"]
        self.add_grade_course = wx.ComboBox(self.panel, choices=course_choices, style=wx.CB_DROPDOWN)
        # self.add_grade_course = wx.TextCtrl(self.panel)
        self.add_grade_value = wx.TextCtrl(self.panel)
        add_grade_btn = wx.Button(self.panel, label='Add or Update Grade')
        add_grade_btn.Bind(wx.EVT_BUTTON, self.on_add_grade)
        hbox.Add(st1, flag=wx.RIGHT, border=8)
        hbox.Add(self.add_grade_sno, proportion=1)
        hbox.Add(self.add_grade_course, proportion=1)
        hbox.Add(self.add_grade_value, proportion=1)
        hbox.Add(add_grade_btn, proportion=1)
        vbox.Add(hbox, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

    #
    def on_add_grade(self, event):
        sno = self.add_grade_sno.GetValue()
        course = self.add_grade_course.GetValue()
        grade_value = self.add_grade_value.GetValue()
        # Method: add_grade
        # Pass grade information in the form of a dictionary
        grades = {course: grade_value}
        self.sms.add_update_grade(sno, grades)
        wx.MessageBox(f'Grade added/updated successfully for Student {sno} in Course {course}!', 'Info',
                      wx.OK | wx.ICON_INFORMATION)

    def add_student_section(self, vbox):
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        st1 = wx.StaticText(self.panel, label='Add Student: Sno, Sname, Sex, Birthday(2000-01-01)')
        self.add_sno = wx.TextCtrl(self.panel)
        self.add_sname = wx.TextCtrl(self.panel)
        self.add_sex = wx.TextCtrl(self.panel)
        self.add_birthday = wx.TextCtrl(self.panel)
        add_btn = wx.Button(self.panel, label='Add')
        add_btn.Bind(wx.EVT_BUTTON, self.on_add_student)
        hbox.Add(st1, flag=wx.RIGHT, border=8)
        hbox.Add(self.add_sno, proportion=1)
        hbox.Add(self.add_sname, proportion=1)
        hbox.Add(self.add_sex, proportion=1)
        hbox.Add(self.add_birthday, proportion=1)
        hbox.Add(add_btn, proportion=1)
        vbox.Add(hbox, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

    def on_add_student(self, event):
        sno = self.add_sno.GetValue()
        sname = self.add_sname.GetValue()
        sex = self.add_sex.GetValue()
        birthday = self.add_birthday.GetValue()

        # Check out if the student already exists
        cursor = self.sms.connection.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM students WHERE sno = %s", (sno,))
        result = cursor.fetchone()

        if result['count'] > 0:
            # If student already exists, show an error message
            wx.MessageBox(f'Student with Sno {sno} already exists!', 'Error', wx.OK | wx.ICON_ERROR)
        else:
            # If student doesn't exist, perform an insert operation
            cursor.execute("INSERT INTO students (sno, sname, sex, birthday) VALUES (%s, %s, %s, %s)",
                           (sno, sname, sex, birthday))
            self.sms.connection.commit()
            wx.MessageBox(f'Student {sname} added successfully!', 'Info', wx.OK | wx.ICON_INFORMATION)

        cursor.close()

    def view_all_students_section(self, vbox):
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        st1 = wx.StaticText(self.panel, label='View All Students and Grades')
        view_all_students_btn = wx.Button(self.panel, label='View All Students and Grades')
        view_all_students_btn.Bind(wx.EVT_BUTTON, self.on_view_all_students)
        hbox.Add(st1, flag=wx.RIGHT, border=8)
        hbox.Add(view_all_students_btn, proportion=1)
        vbox.Add(hbox, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

    def on_view_all_students(self, event):
        # Method: get all students and their grades
        all_students_info = self.sms.get_all_students_info()

        if all_students_info:
            info_text = '\n'.join([f"Student: {info['sname']}, Sno: {info['sno']}, Grades: {info['grades']}" for info in
                                   all_students_info])
            wx.MessageBox(f'All Students Information:\n{info_text}', 'All Students Info', wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox(f'No student information available!', 'Error', wx.OK | wx.ICON_ERROR)

    #
    def insert_grades_for_student_section(self, vbox):
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        st1 = wx.StaticText(self.panel, label='Insert Grades for Student: Enter Sno, Math, English, Python')
        self.insert_grades_sno = wx.TextCtrl(self.panel)
        self.insert_grades_math = wx.TextCtrl(self.panel)
        self.insert_grades_english = wx.TextCtrl(self.panel)
        self.insert_grades_python = wx.TextCtrl(self.panel)
        insert_grades_btn = wx.Button(self.panel, label='Insert Grades for Student')
        insert_grades_btn.Bind(wx.EVT_BUTTON,
                               self.on_insert_grades_for_student)
        hbox.Add(st1, flag=wx.RIGHT, border=8)
        hbox.Add(self.insert_grades_sno, proportion=1)
        hbox.Add(self.insert_grades_math, proportion=1)
        hbox.Add(self.insert_grades_english, proportion=1)
        hbox.Add(self.insert_grades_python, proportion=1)
        hbox.Add(insert_grades_btn, proportion=1)
        vbox.Add(hbox, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

    #
    def on_insert_grades_for_student(self, event):
        sno = self.insert_grades_sno.GetValue()
        math_grade = self.insert_grades_math.GetValue()
        english_grade = self.insert_grades_english.GetValue()
        python_grade = self.insert_grades_python.GetValue()

        # Method: insert grades for a specific student
        grades_dict = {'math': math_grade, 'english': english_grade, 'python': python_grade}
        self.sms.insert_grades_for_student(sno, grades_dict)
        wx.MessageBox(f'Grades inserted successfully for Student {sno}!', 'Info',
                      wx.OK | wx.ICON_INFORMATION)


    def delete_student_section(self, vbox):
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        st1 = wx.StaticText(self.panel, label='Delete Student: Enter Sno')
        self.delete_sno = wx.TextCtrl(self.panel)
        delete_btn = wx.Button(self.panel, label='Delete Student')
        delete_btn.Bind(wx.EVT_BUTTON, self.on_delete_student)
        hbox.Add(st1, flag=wx.RIGHT, border=8)
        hbox.Add(self.delete_sno, proportion=1)
        hbox.Add(delete_btn, proportion=1)
        vbox.Add(hbox, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

    def on_delete_student(self, event):
        sno_to_delete = self.delete_sno.GetValue()

        # Method: delete_student
        delete_result = self.sms.delete_student(sno_to_delete)

        if delete_result == 'success':
            wx.MessageBox(f'Student with Sno {sno_to_delete} deleted successfully!', 'Info',
                          wx.OK )
        elif delete_result == 'not_found':
            wx.MessageBox(f'Student with Sno {sno_to_delete} not found!', 'Error', wx.OK | wx.ICON_ERROR)
        else:
            wx.MessageBox(f'Error deleting student with Sno {sno_to_delete}!', 'Error', wx.OK | wx.ICON_ERROR)

    def update_student_section(self, vbox):
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        st1 = wx.StaticText(self.panel, label='Update Student: Enter Sno, Sname, Sex, Birthday(2000-01-01)')
        self.update_sno = wx.TextCtrl(self.panel)
        self.update_sname = wx.TextCtrl(self.panel)
        self.update_sex = wx.TextCtrl(self.panel)
        self.update_birthday = wx.TextCtrl(self.panel)
        update_btn = wx.Button(self.panel, label='Update')
        update_btn.Bind(wx.EVT_BUTTON, self.on_update_student)
        hbox.Add(st1, flag=wx.RIGHT, border=8)
        hbox.Add(self.update_sno, proportion=1)
        hbox.Add(self.update_sname, proportion=1)
        hbox.Add(self.update_sex, proportion=1)
        hbox.Add(self.update_birthday, proportion=1)
        hbox.Add(update_btn, proportion=1)
        vbox.Add(hbox, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

    def on_update_student(self, event):
        sno = self.update_sno.GetValue()
        sname = self.update_sname.GetValue()
        sex = self.update_sex.GetValue()
        birthday = self.update_birthday.GetValue()

        # Method: update student information
        update_result = self.sms.update_student(sno, sname, sex, birthday)

        if update_result == 'success':
            wx.MessageBox(f'Student with Sno {sno} updated successfully!', 'Info', wx.OK | wx.ICON_INFORMATION)
        elif update_result == 'not_found':
            wx.MessageBox(f'Student with Sno {sno} not found!', 'Error', wx.OK | wx.ICON_ERROR)
        else:
            wx.MessageBox(f'Error updating student with Sno {sno}!', 'Error', wx.OK | wx.ICON_ERROR)

    def get_course_choices(self):
        # Return the available course choices
        return ["math", "english", "python"]

    def on_display_grades_for_student(self, event):
        sno = self.display_grades_sno.GetValue()

        # Obtain all subject scores for designated students
        grades_info = self.sms.get_all_grades_for_student(sno)

        # Show pop-up box
        dlg = wx.Dialog(self, title=f'Grades for Student: {sno}', size=(400, 150))
        panel = wx.Panel(dlg)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Show student grades
        st1 = wx.StaticText(panel, label=f'Math: {grades_info.get("math", "NotApplicable")}')
        st2 = wx.StaticText(panel, label=f'English: {grades_info.get("english", "NotApplicable")}')
        st3 = wx.StaticText(panel, label=f'Python: {grades_info.get("python", "NotApplicable")}')

        vbox.Add(st1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)
        vbox.Add(st2, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)
        vbox.Add(st3, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        panel.SetSizer(vbox)
        dlg.ShowModal()
        dlg.Destroy()


if __name__ == '__main__':
    app = wx.App(False)
    frame = MainFrame(None, "Student Information And Grade System")
    frame.Show()
    app.MainLoop()
