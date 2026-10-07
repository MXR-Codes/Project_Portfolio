import wx
from student_management_system import StudentManagementSystem as student_management_system


class GradeEditorDialog(wx.Dialog):
    def __init__(self, parent, title, grades_information, course_query):
        super(GradeEditorDialog, self).__init__(parent, title=title, size=(400, 300))
        self.panel = wx.Panel(self)
        self.grades_information = grades_information
        self.course_query = course_query
        self.student_management_system = student_management_system()  # Create an instance
        self.init_ui()

    def init_ui(self):
        vbox = wx.BoxSizer(wx.VERTICAL)

        for sno, info in self.grades_information.items():
            hbox = wx.BoxSizer(wx.HORIZONTAL)
            st1 = wx.StaticText(self.panel, label=f'Student: {info["sname"]}, Sno: {sno}, Grade: {info["grade"]}')
            update_grade_btn = wx.Button(self.panel, label='Update Grade')
            update_grade_btn.Bind(wx.EVT_BUTTON, lambda event, student=sno, course=self.course_query:
            self.on_update_grade(student, course))

            hbox.Add(st1, proportion=1, flag=wx.ALIGN_CENTER)
            hbox.Add(update_grade_btn, proportion=0, flag=wx.ALIGN_CENTER)
            vbox.Add(hbox, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=5)

        self.panel.SetSizer(vbox)
        self.Centre()
        self.ShowModal()

    def on_update_grade(self, student, course):
        # Open a dialog to input the grade for the selected student and course
        wx.PostEvent(self, wx.PyCommandEvent(wx.EVT_BUTTON.typeId, self.GetId()))
        self.Refresh()
        self.panel.Layout()
        self.panel.Refresh()
        wx.CallAfter(self.Refresh)

        course_input_dialog = CourseInputDialog(self, student, course)
        result = course_input_dialog.ShowModal()

        if result == wx.ID_OK:
            # User clicked OK, retrieve the input grade and course
            new_grade = course_input_dialog.get_input_grade()
            selected_course = course_input_dialog.course_query

            # Update the grade in the database
            update_result = self.update_grade_in_database(student, selected_course, new_grade)

            if update_result == 'success':
                print(f"Updating grade for Student {student} in Course {selected_course} to {new_grade}")
                self.Refresh()
                self.panel.Layout()
                self.panel.Refresh()
                wx.PostEvent(self, wx.PyCommandEvent(wx.EVT_BUTTON.typeId, self.GetId()))
                self.Refresh()
            elif update_result == 'not_found':
                print(f"Student {student} or course {selected_course} not found.")
            else:
                print(f"Error updating grade for Student {student} in Course {selected_course}.")

        course_input_dialog.Destroy()

    def update_grade_in_database(self, student, new_grade, name):
        # Use the update_grade_one method from the StudentManagementSystem class
        # to update the grade in the database
        return self.student_management_system.update_grade_one(student, new_grade, name)


class CourseInputDialog(wx.Dialog):
    def __init__(self, parent, student, course_query):
        (super(CourseInputDialog, self).__init__
         (parent, title=f"Input Grade for {course_query.capitalize()}", size=(200, 150)))
        self.panel = wx.Panel(self)
        self.student = student
        self.course_query = course_query
        self.input_grade = None
        self.init_ui()

    def init_ui(self):
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.grade_input = wx.TextCtrl(self.panel)
        btn_ok = wx.Button(self.panel, label="OK")
        btn_ok.Bind(wx.EVT_BUTTON, self.on_ok)

        vbox.Add(wx.StaticText(self.panel, label=f"Input Grade for {self.course_query.capitalize()}:"),
                 flag=wx.EXPAND | wx.ALL, border=5)
        vbox.Add(self.grade_input, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        vbox.Add(btn_ok, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        self.panel.SetSizer(vbox)

    def on_ok(self, event):
        # Validate and store the input grade
        input_grade = self.grade_input.GetValue().strip()
        if input_grade.isdigit():
            self.input_grade = int(input_grade)
            self.EndModal(wx.ID_OK)
        else:
            wx.MessageBox("Please enter a valid numeric grade.", "Error", wx.OK | wx.ICON_ERROR)

    def get_input_grade(self):
       return self.input_grade

