import pymysql
import datetime
import wx

class StudentManagementSystem:
    def __init__(self):
        self.connection = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            database='StudentManagement2',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

    def update_grade_one(self, sno, course, grade):
        with self.connection.cursor() as cursor:
            try:
                cursor.execute('set session transaction isolation level read committed')
                # Check out if the student and grade exist
                cursor.execute("SELECT COUNT(*) as count FROM grades WHERE sno = %s",
                               (sno,))
                result = cursor.fetchone()

                if result['count'] == 0:
                    insert_sql = f"INSERT INTO grades (sno, {course}) VALUES (%s, %s)"
                    cursor.execute(insert_sql, (sno, grade))
                    self.connection.commit()
                    return 'success'

                if result['count'] > 0:
                    # Student exists, perform the update
                    update_sql = f"UPDATE grades SET {course} = %s WHERE sno = %s"
                    cursor.execute(update_sql, (grade, sno))
                    self.connection.commit()
                    return 'success'
                else:
                    # Student or grade not found, return an error message
                    return 'not_found'
            except Exception as e:
                print(f"Error in update_grade_one: {e}")
                self.connection.rollback()
                return 'error'

    def get_all_students_and_grades_for_course(self, course):
        with self.connection.cursor() as cursor:
            try:
                # Query all students and their grades for the specified course
                query_sql = f"SELECT students.sno, students.sname, grades.{course} " \
                            f"FROM students LEFT JOIN grades ON students.sno = grades.sno"
                cursor.execute(query_sql)
                results = cursor.fetchall()

                # Create a dictionary to store the results
                students_and_grades = {}
                for result in results:
                    sno = result['sno']
                    sname = result['sname']
                    grade = result[course]

                    # Add the information to the dictionary
                    students_and_grades[sno] = {'sname': sname, 'grade': grade}

                return students_and_grades
            except Exception as e:
                print(f"Error in get_all_students_and_grades_for_course: {e}")
                return {}

    def add_student(self, sno, sname, sex, birthday):
        with self.connection.cursor() as cursor:
            # Check if the student already exists
            cursor.execute("SELECT COUNT(*) as count FROM students WHERE sno = %s",
                           (sno,))
            result = cursor.fetchone()

            if result['count'] > 0:
                # Student already exists, return an error message
                return f'Student with Sno {sno} already exists!'
            else:
                # Student doesn't exist, perform an insert
                sql = "INSERT INTO students (sno, sname, sex, birthday) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (sno, sname, sex, birthday))
                self.connection.commit()
                return f'Student {sname} added successfully!'


    def delete_student(self, sno):
        with self.connection.cursor() as cursor:
            try:
                # Check if the student exists
                cursor.execute("SELECT COUNT(*) as count FROM students WHERE sno = %s",
                               (sno,))
                result_student = cursor.fetchone()
                if result_student['count'] > 0:
                    # Student exists, proceed with deletion

                    # Check out if the student has corresponding grades
                    cursor.execute("SELECT COUNT(*) as count FROM grades WHERE sno = %s",
                                   (sno,))
                    result_grades = cursor.fetchone()

                    if result_grades['count'] > 0:
                        # Student has corresponding grades, proceed with deletion
                        # Delete corresponding grades from grades table
                        delete_grades_sql = "DELETE FROM grades WHERE sno = %s"
                        cursor.execute(delete_grades_sql, (sno,))

                    # Delete student from students table
                    delete_student_sql = "DELETE FROM students WHERE sno = %s"
                    cursor.execute(delete_student_sql, (sno,))

                    self.connection.commit()
                    return 'success'
                else:
                    # Student not found, return an error message
                    return 'not_found'
            except Exception as e:
                print(f"Error in delete_student: {e}")
                self.connection.rollback()
                return 'error'

    def add_grade(self, sno, grades):
        with self.connection.cursor() as cursor:
            # Build SQL query statements
            columns = ', '.join(grades.keys())
            values = ', '.join(['%s'] * len(grades))
            sql = f"INSERT INTO grades (sno, {columns}) VALUES (%s, {values})"

            # Add grade information to the parameters
            params = [sno] + list(grades.values())

            cursor.execute(sql, tuple(params))
            self.connection.commit()


    def get_grade(self, sno, course):
        with self.connection.cursor() as cursor:
            try:
                # Query the grades of specified students and courses
                query_grade_sql = (f"SELECT {course} FROM grades "
                                   f"WHERE sno = %s")
                cursor.execute(query_grade_sql, (sno,))
                result = cursor.fetchone()

                if result:
                    return result
                else:
                    return {'not_found': None}
            except Exception as e:
                print(f"Error in get_grade: {e}")
                return {'error': None}

    def get_student(self, sno):
        with self.connection.cursor() as cursor:
            sql = "SELECT * FROM students WHERE sno = %s"
            cursor.execute(sql, (sno,))
            return cursor.fetchone()


    def add_update_grade(self, sno, grades):
        with self.connection.cursor() as cursor:
            try:
                # Check if the student exists
                cursor.execute("SELECT COUNT(*) as count FROM "
                               "grades WHERE sno = %s", (sno,))
                result = cursor.fetchone()

                if result['count'] > 0:
                    # If student exists, perform an update operation
                    update_set = ', '.join([f"{column} = %s" for column
                                            in grades.keys()])
                    params = list(grades.values()) + [sno]
                    sql = f"UPDATE grades SET {update_set} WHERE sno = %s"
                    cursor.execute(sql, tuple(params))
                else:
                    # If student doesn't exist, perform an insert operation
                    columns = ', '.join(grades.keys())
                    values = ', '.join(['%s'] * len(grades))
                    sql = (f"INSERT INTO grades (sno, {columns})"
                           f" VALUES (%s, {values})")
                    params = [sno] + list(grades.values())
                    cursor.execute(sql, tuple(params))

                self.connection.commit()
            except Exception as e:
                print(f"Error in add_grade: {e}")

    def update_grade(self, sno, math, english, python):
        with self.connection.cursor() as cursor:
            sql = "UPDATE grades SET math = %s, english = %s, python = %s WHERE sno = %s"
            cursor.execute(sql, (math, english, python, sno))
            self.connection.commit()

    def get_all_students_info(self):
        with self.connection.cursor() as cursor:
            # Select all students
            cursor.execute("SELECT * FROM students")
            students = cursor.fetchall()

            # Fetch grades for each student
            for student in students:
                sno = student['sno']
                cursor.execute("SELECT math,english,python FROM grades "
                               "WHERE sno = %s", (sno,))
                grades = cursor.fetchone()

                # Add grades information to the student
                student['grades'] = grades

        return students


    def insert_grades_for_student(self, sno, grades_dict):
        with self.connection.cursor() as cursor:
            # Check out if grades already exist for the student
            cursor.execute("SELECT COUNT(*) as count FROM grades WHERE sno = %s",
                           (sno,))
            result = cursor.fetchone()

            if result['count'] > 0:
                # If grades already exist for the student, show an error message
                wx.MessageBox(f'Grades already exist for Student with Sno {sno}!',
                              'Error', wx.OK | wx.ICON_ERROR)
            else:
                # If student exists, perform an insert operation
                columns = ', '.join(grades_dict.keys())
                values = ', '.join(['%s'] * len(grades_dict))
                sql = f"INSERT INTO grades (sno, {columns}) VALUES (%s, {values})"
                params = [sno] + list(grades_dict.values())
                cursor.execute(sql, tuple(params))

        self.connection.commit()

    def update_student(self, sno, sname=None, sex=None, birthday=None):
        with self.connection.cursor() as cursor:
            try:
                # Check out if the student exists
                cursor.execute("SELECT COUNT(*) as count FROM students WHERE sno = %s",
                               (sno,))
                result_student = cursor.fetchone()

                if result_student['count'] > 0:
                    # Student exists, proceed with update

                    # Check out if any parameter is provided for update
                    if sname is None and sex is None and birthday is None:
                        # No parameters provided, no update needed
                        return 'no_update'

                    # Build the update_set string
                    update_set_list = []
                    if sname is not None and sname != '':
                        update_set_list.append("sname = %s")
                    if sex is not None and sex != '':
                        update_set_list.append("sex = %s")
                    if birthday is not None and birthday != '':
                        # Check out if birthday is a valid date
                        try:
                            datetime.datetime.strptime(birthday, '%Y-%m-%d')
                            update_set_list.append("birthday = %s")
                        except ValueError:
                            return 'invalid_date'

                    update_set = ', '.join(update_set_list)

                    # Prepare parameters for the query
                    params = []
                    if sname is not None and sname != '':
                        params.extend([sname])
                    if sex is not None and sex != '':
                        params.extend([sex])
                    if birthday is not None and birthday != '':
                        params.extend([birthday])

                    params.extend([sno])  # Add sno to the end of the parameter list

                    # Check if there's something to update
                    if update_set:
                        # Execute the update query
                        sql = f"UPDATE students SET {update_set} WHERE sno = %s"
                        cursor.execute(sql, tuple(params))

                        self.connection.commit()
                        return 'success'
                    else:
                        # No parameters provided, no update needed
                        return 'no_update'
                else:
                    # Student not found, return an error message
                    return 'not_found'
            except Exception as e:
                print(f"Error in update_student: {e}")
                self.connection.rollback()
                return 'error'

    def get_all_grades_for_student(self, sno):
        with self.connection.cursor() as cursor:
            try:
                # Query the results of all subjects for a specified student
                query_grades_sql = f"SELECT * FROM grades WHERE sno = %s"
                cursor.execute(query_grades_sql, (sno,))
                result = cursor.fetchone()

                # If the student does not have a grade, return an empty dictionary
                if result is None:
                    return {}

                # Return to the student grades dictionary
                return {
                    'math': result['math'],
                    'english': result['english'],
                    'python': result['python']
                }
            except Exception as e:
                print(f"get_all_grades_for_student error：{e}")
                return {}

    def close(self):
        self.connection.close()
