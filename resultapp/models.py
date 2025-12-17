from django.db import models

class Class(models.Model):
    name = models.CharField(max_length=50)
    numeric = models.IntegerField()
    section = models.CharField(max_length=20)

    creation_date = models.DateTimeField(auto_now_add=True)
    updation_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.section}"


class Subject(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=20)

    creation_date = models.DateTimeField(auto_now_add=True)
    updation_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Student(models.Model):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )

    name = models.CharField(max_length=50)
    roll_id = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)

    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    dob = models.DateField()

    student_class = models.ForeignKey(
        Class, null=True, on_delete=models.SET_NULL
    )

    reg_date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=1)

    def __str__(self):
        return self.name


class SubjectCombination(models.Model):
    student_class = models.ForeignKey(Class, null=True, on_delete=models.SET_NULL)
    subject = models.ForeignKey(Subject, null=True, on_delete=models.SET_NULL)

    status = models.IntegerField(default=1)
    creation_date = models.DateTimeField(auto_now_add=True)
    updation_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student_class} - {self.subject}"


class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    student_class = models.ForeignKey(
        Class, null=True, on_delete=models.SET_NULL
    )
    subject = models.ForeignKey(
        Subject, null=True, on_delete=models.SET_NULL
    )

    marks = models.IntegerField()
    posting_date = models.DateTimeField(auto_now_add=True)
    updation_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student} | {self.subject} | {self.marks}"


class Notice(models.Model):
    title = models.CharField(max_length=100)
    detail = models.TextField()

    posting_date = models.DateTimeField(auto_now_add=True)
    updation_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
