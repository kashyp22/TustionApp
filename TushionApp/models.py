from django.db import models

# Create your models here.

class Login(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    type=models.CharField(max_length=50)

class Tutor(models.Model):
    Login=models.ForeignKey(Login,on_delete=models.CASCADE) # fk
    name=models.CharField(max_length=50)
    photo=models.CharField(max_length=50)
    gender=models.CharField(max_length=50)
    qualification=models.CharField(max_length=50)
    dob=models.DateField(max_length=15)
    email=models.EmailField(max_length=50)
    phone=models.BigIntegerField()
    experience=models.CharField(max_length=100)
    place=models.CharField(max_length=50)
    id_proof=models.CharField(max_length=100)
    status=models.CharField(max_length=100)

class ClassStudy(models.Model):
    ClassName=models.CharField(max_length=50)

class Student(models.Model):
    Login=models.ForeignKey(Login,on_delete=models.CASCADE) # fk
    Class=models.ForeignKey(ClassStudy,on_delete=models.CASCADE)  #fk
    name = models.CharField(max_length=50)
    photo = models.CharField(max_length=50)
    gender = models.CharField(max_length=50)
    dob = models.DateField(max_length=15)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=15)
    place = models.CharField(max_length=50)
    id_proof = models.CharField(max_length=100)
    status=models.CharField(max_length=50)

class Subjects(models.Model):
    Class=models.ForeignKey(ClassStudy,on_delete=models.CASCADE)  #fk
    SubjectName=models.CharField(max_length=100)

class Complaints(models.Model):
    Student=models.ForeignKey(Student,on_delete=models.CASCADE) #fk
    complaint=models.CharField(max_length=100)
    replay=models.CharField(max_length=100)
    status=models.CharField(max_length=100)
    Date=models.DateField(max_length=15)

class Feedback(models.Model):
    Tutor=models.ForeignKey(Tutor,on_delete=models.CASCADE) #fk
    Student=models.ForeignKey(Student,on_delete=models.CASCADE) #fk
    feedback=models.CharField(max_length=100)
    Date=models.DateField(max_length=15)

class Mysubject(models.Model):
    Subject=models.ForeignKey(Subjects,on_delete=models.CASCADE) #fk
    Tutor=models.ForeignKey(Tutor,on_delete=models.CASCADE) #fk

class Timetable(models.Model):
    Subject=models.ForeignKey(Subjects,on_delete=models.CASCADE) #fk
    hour=models.CharField(max_length=10)
    day=models.CharField(max_length=20)

class Notification(models.Model):
    Tutor = models.ForeignKey(Tutor,on_delete=models.CASCADE)  # fk
    mysubject=models.ForeignKey(Mysubject,on_delete=models.CASCADE)
    Date=models.DateTimeField(max_length=50)
    Time=models.TimeField(max_length=10)
    message=models.CharField(max_length=100)

class TestDetails(models.Model):
    Subject=models.ForeignKey(Subjects,on_delete=models.CASCADE) #fk
    Tutor=models.ForeignKey(Tutor,on_delete=models.CASCADE) #fk
    Test_name=models.CharField(max_length=100)
    Date=models.DateTimeField(max_length=20)
    FromTime=models.TimeField(max_length=20)
    ToTime=models.TimeField(max_length=20)

class Result(models.Model):
    TestDetails=models.ForeignKey(TestDetails,on_delete=models.CASCADE) # fk
    Student=models.ForeignKey(Student, on_delete=models.CASCADE)  # fk
    mark=models.BigIntegerField()

class Attendence(models.Model):
    Student=models.ForeignKey(Student, on_delete=models.CASCADE)  # fk
    Class = models.ForeignKey(ClassStudy, on_delete=models.CASCADE)  # fk
    Date=models.DateTimeField(max_length=20)
    pstatus=models.CharField(max_length=50)
    hour=models.CharField(max_length=50)




