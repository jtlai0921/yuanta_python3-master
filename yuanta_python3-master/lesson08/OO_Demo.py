class Human:
    name = ''
    age = 0
    sex = ''

    def __str__(self):
        return self.name + ',' + str(self.age) + ',' + self.sex


class Student(Human):
    number = 0
    grade = ''


h = Human()
h.name = 'Vincent'
h.age = 20
h.sex = '男'

print(h.name, h.age, h.sex)
print(h)

student = Student()
student.name = 'Vincent'
student.age = 7
student.sex = '男'
student.number = 6
student.grade = '一年級'
print(student.name)
print(student.age)
print(student.sex)
print(student.number)
print(student.grade)