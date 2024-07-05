from datetime import datetime

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.http import JsonResponse

# ---------------------------------  admin --------------------------------------
from TushionApp.models import *


def login(req):
    return render(req,'Login.html')

def login_post(req):
    username1=req.POST['username1']
    password2=req.POST['password1']

    lg = Login.objects.filter(username=username1,password=password2)
    if lg.exists():
        lg2=Login.objects.get(username=username1,password=password2)
        req.session['lid']=lg2.id

        if lg2.type == 'admin':
            return  HttpResponse('''<script> alert("Admin Login success "); window.location='/tushionapp/HomeAdmin/' </script>''')
        elif lg2.type == 'tutor':
            return  HttpResponse('''<script> alert("Tutor Login success "); window.location='/tushionapp/TutorHome/' </script>''')
        else:
            return HttpResponse('''<script>alert("not found"); window.location='/tushionapp/login/'</script>''')
    else:
        return HttpResponse('''<script> alert("not found"); window.location='/tushionapp/login/' </script>''')


def HomeAdmin(req):
    return render(req,'Admin/AdminHome.html')

def verifyTutor(req):
    s=Tutor.objects.filter(status='pending')
    return render(req,'Admin/verifyTutor.html',{'data':s})

def verifyTutor_post(req):
    data=req.POST['tutorSearch']
    sd=Tutor.objects.filter(status='pending',name__icontains=data)
    return render(req,'Admin/verifyTutor.html',{"data":sd})

def approveTutor(req,id):
    Tutor.objects.filter(Login=id).update(status="approve")
    Login.objects.filter(id=id).update(type="tutor")
    return HttpResponse("""<script>alert("approved success");window.location='/tushionapp/HomeAdmin/'</script>""")

def approvedTutor(req):
    a=Tutor.objects.filter(status='approve')
    return render(req,'Admin/TutorApproved.html',{'data':a})
def approvedTutor_post(req):
    data = req.POST['tutorSearch']
    sd = Tutor.objects.filter(status='approve', name__icontains=data)
    return render(req,'Admin/TutorApproved.html',{"data":sd})
def rejectTutor(req,id):
    Tutor.objects.filter(Login=id).update(status="reject")
    Login.objects.filter(id=id).update(type="reject")
    return HttpResponse("""<script>alert("reject success");window.location='/tushionapp/HomeAdmin/'</script>""")
def rejectedTutor(req):
    rT=Tutor.objects.filter(status='reject')
    return render(req,'Admin/TutorRejected.html',{'data':rT})
def rejectedTutor_post(req):
    data = req.POST['tutorSearch']
    sd = Tutor.objects.filter(status='reject', name__icontains=data)
    return render(req,'Admin/TutorRejected.html',{"data":sd})


def studentVerify(req):
    v=Student.objects.filter(status='pending')
    cla=ClassStudy.objects.all()
    return render(req,'Admin/StudentVerify.html',{'data':v,'class':cla})

#--------------------- ajax

def get_class_students(request, class_id):
    # print(class_id)

    students = Student.objects.filter(Class_id=class_id,status="pending").values(
        'id', 'photo', 'name', 'dob', 'gender', 'email', 'phone', 'place', 'id_proof','Class__className','Login_id',
    )
    # print(students)
    return JsonResponse(list(students), safe=False)


def studentVerify_post(req):
    data=req.POST['Studentsearch']
    s=Student.objects.filter(status='pending',name__icontains=data)
    return render(req,'Admin/StudentVerify.html',{"data":s})

def studentApprove(req,id):
    Student.objects.filter(Login=id).update(status="approve")
    Login.objects.filter(id=id).update(type="student")
    return HttpResponse("""<script>alert("Student Approved");window.location='/tushionapp/studentApproved/'</script>""")


def studentApproved(req):
    a=Student.objects.filter(status='approve')
    cla = ClassStudy.objects.all()
    return  render(req,'Admin/StudentApproved.html',{'data':a,"class":cla})

def StudentApproved_search(request, class_id):
    print(class_id)

    students = Student.objects.filter(Class_id=class_id,status="approve").values(
        'id', 'photo', 'name', 'dob', 'gender', 'email', 'phone', 'place', 'id_proof','Class__className','Login_id',
    )
    # print(students)
    return JsonResponse(list(students), safe=False)


def studentApproved_post(req):
    return  render(req,'Admin/StudentApproved.html')
def studentReject(req,id):
    Student.objects.filter(Login=id).update(status="reject")
    Login.objects.filter(id=id).update(type="rejected")
    return HttpResponse("""<script>alert("Student rejected");window.location='/tushionapp/studentRejected/'</script>""")
def studentRejected(req):
    a=Student.objects.filter(status="reject")
    cla = ClassStudy.objects.all()
    return render(req,'Admin/StudentRejected.html',{"data":a,"class":cla})

def StudentReject_search(request, class_id):
    print(class_id)

    students = Student.objects.filter(Class_id=class_id,status="reject").values(
        'id', 'photo', 'name', 'dob', 'gender', 'email', 'phone', 'place', 'id_proof','Class__className','Login_id',
    )
    # print(students)
    return JsonResponse(list(students), safe=False)

def studentRejected_post(req):
    return render(req,'Admin/StudentRejected.html')
def StudentComplaint(req):
    c=Complaints.objects.all()
    return render(req,'Admin/StudentComplaints.html',{'data':c})

def StudentComplaint_post(req):
    from12 = req.POST["fromdate"]
    to12 = req.POST["todate"]
    data = Complaints.objects.filter(Date__range=[from12, to12])
    return render(req,'Admin/StudentComplaints.html',{"data":data})

def ReplyStudentComplaint(req,id):
    return render(req,'Admin/StudentComplaintReply.html',{'id':id})

def ReplyStudentComplaint_post(req):
    a=req.POST["reply"]
    cid=req.POST["id"]
    data=Complaints.objects.filter(id=cid).update(status="replied",replay=a)
    return redirect('/tushionapp/StudentComplaint/')

def ViewFeedback(req):
    data=Feedback.objects.all()
    return render(req,'Admin/ViewFeedback.html',{"data":data})

def ViewFeedback_post(req):
    from12=req.POST["fromdate"]
    to12=req.POST["todate"]
    data=Feedback.objects.filter(Date__range=[from12,to12])
    return render(req,'Admin/ViewFeedback.html',{'data':data})

def ViewClass(req):
    c=ClassStudy.objects.all()
    return render(req,'Admin/ViewClass.html',{"data":c})

def ViewClass_post(req):
    s=req.POST["clsearch"]
    data=ClassStudy.objects.filter(className__icontains=s)
    return render(req,'Admin/ViewClass.html',{"data":data})

def AddClass(req):
    return render(req,'Admin/AddClass.html')

def AddClass_post(req):
    cl=req.POST['class']
    data=ClassStudy()
    data.className=cl
    data.save()
    return HttpResponse("""<script>alert("Class added");window.location='/tushionapp/ViewClass/' </script>""")

def EditClass(req,id):
    a=ClassStudy.objects.get(id=id)
    return render(req,'Admin/EditClass.html',{"data":a})
def EditClass_post(req):
    cl=req.POST['class']
    cid=req.POST['cid']
    data=ClassStudy.objects.get(id=cid)
    data.className=cl
    data.save()
    return HttpResponse("""<script>alert("edited");window.location='/tushionapp/ViewClass/' </script>""")

def deleteClass(req,id):
    data=ClassStudy.objects.get(id=id).delete()
    return HttpResponse("""<script>alert("deleted");window.location='/tushionapp/ViewClass/' </script>""")


def ViewSubjects(req):
    sub=Subjects.objects.all()
    return render(req,'Admin/ViewSubject.html',{"data":sub})
def ViewSubjects_post(req):
    vs=req.POST['search']
    data=Subjects.objects.filter(SubjectName__icontains=vs)
    return render(req,'Admin/ViewSubject.html',{"data":data})
def AddSubjects(req):
    res=ClassStudy.objects.all()
    return render(req,'Admin/AddSubject.html',{'data':res})
def AddSubjects_post(req):
    # sid=req.POST['sid']
    c=req.POST['cls']
    s=req.POST['subject']
    data=Subjects()
    data.Class_id=c
    data.SubjectName=s
    data.save()
    return HttpResponse("""<script>alert("subject added successfully");window.location='/tushionapp/ViewSubjects/' </script>""")
def EditSubjects(req,id):
    s=Subjects.objects.get(id=id)
    res = ClassStudy.objects.all()
    return render(req,'Admin/EditSubjects.html',{'data':res,'data2':s})
def EditSubjects_post(req):
    sid=req.POST['sid']
    c = req.POST['cls']
    s = req.POST['subject']
    data = Subjects.objects.get(id=sid)
    data.Class_id = c
    data.SubjectName = s
    data.save()
    return HttpResponse("""<script>alert("subject edited successfully");window.location='/tushionapp/ViewSubjects/' </script>""")
def DeleteSubjects(req,id):
    Subjects.objects.get(id=id).delete()
    return HttpResponse("""<script>alert("subject deleted successfully");window.location='/tushionapp/ViewSubjects/' </script>""")

def AddTimeTable(req):
    data=Subjects.objects.all()
    return render(req,'Admin/AddTimeTable.html',{'data':data})

def AddTimeTable_post(req):
    sid=req.POST["sid"]
    h=req.POST["hour"]
    d=req.POST["day"]
    data=Timetable()
    data.Subject_id=sid
    data.hour=h
    data.day=d
    data.save()
    return HttpResponse("""<script>alert("TimeTable added successfully");window.location='/tushionapp/ViewTimeTable/' </script>""")

def ViewTimeTable(req):
    data=Timetable.objects.all()
    return render(req,'Admin/ViewTimeTable.html',{"data":data})

def ViewTimeTable_post(req):
    ts=req.POST['tsearch']
    data=Timetable.objects.filter(day__icontains=ts)
    return render(req,'Admin/ViewTimeTable.html/',{"data":data})

def EditTimeTable(req,id):
    data=Timetable.objects.get(id=id)
    data1=Subjects.objects.all()
    return render(req,'Admin/EditTimeTable.html',{"data":data,"data1":data1})

def EditTimeTable_post(req):
    sid=req.POST["sid"]
    tid=req.POST["tid"]
    h=req.POST["hour"]
    d=req.POST["day"]
    data=Timetable.objects.get(id=tid)
    data.Subject_id=sid
    data.hour=h
    data.day=d
    data.save()
    return HttpResponse("""<script>alert("TimeTable Edited");window.location='/tushionapp/ViewTimeTable/' </script>""")

def DeleteTimeTable(req,id):
    Timetable.objects.get(id=id).delete()
    return HttpResponse("""<script>alert("TimeTable deleted");window.location='/tushionapp/ViewTimeTable/' </script>""")

def SubjectAllocate(req):
    sub=Subjects.objects.all()
    tut=Tutor.objects.filter(status="approve")
    return render(req,'Admin/SubjectAllocateTeacher.html',{"sub":sub,"tut":tut})

def SubjectAllocate_post(req):
    sub=req.POST['subject']
    tut=req.POST['tutor']
    data=Mysubject()
    data.Subject_id=sub
    data.Tutor_id=tut
    data.save()
    return HttpResponse("""<script>alert("allocation success");window.location='/tushionapp/ViewAllocateTeacher/'</script>""")

def ViewAllocateTeacher(req):
    data=Mysubject.objects.all()
    return render(req,'Admin/ViewAllocateTeachers.html',{"data":data})
def ViewAllocateTeacher_post(req):
    data=req.POST["search"]
    search=Mysubject.objects.filter(Tutor__name__icontains=data)
    return render(req,'Admin/ViewAllocateTeachers.html',{"data":search})


def EditAllocateTeacher(req,id):
    data=Mysubject.objects.get(id=id)
    sub=Subjects.objects.all()
    tut=Tutor.objects.filter(status="approve")
    return render(req,'Admin/EditAllocateTeacher.html',{"data":data,"sub":sub,"tut":tut})

def EditAllocateTeacher_post(req):
    eid=req.POST['eid']
    subject=req.POST['subject']
    tutor=req.POST['tutor']
    data=Mysubject.objects.get(id=eid)
    data.Subject_id=subject
    data.Tutor_id=tutor
    data.save()
    return HttpResponse("""<script>alert("Edit allocation success");window.location='/tushionapp/ViewAllocateTeacher/'</script>""")

def DeleteAllocateTeacher(req,id):
    Mysubject.objects.get(id=id).delete()
    return HttpResponse("""<script>alert("deleted allocation success");window.location='/tushionapp/ViewAllocateTeacher/'</script>""")

def Logout(req):
    req.session['lid']=" "
    return HttpResponse("""<script>alert("logout successfully done");window.location='/tushionapp/login/'</script>""")


                    # ------------------------------------------------------------------------
                    # --------------------         TUTOR        ------------------------------
                    # ------------------------------------------------------------------------


def TutorHome(req):
    return render(req,'Tutor/TutorHome.html')

def TutorHome_post(req):
    return render(req,'Tutor/TutorHome.html')

def SignupTutor(req):
    return render(req,'Tutor/SignupTutor.html')

def SignupTutor_post(req):
    name=req.POST['name']
    gender=req.POST['gender']
    q=req.POST['qulaification']
    dob1=req.POST['dob']
    pht=req.FILES['photo']
    eml=req.POST['email']
    phn=req.POST['phone']
    exp=req.POST['experience']
    plc=req.POST['place']
    idp=req.FILES['idproof']
    pswd=req.POST['password']
    cpswd=req.POST['cpassword']


    if pswd == cpswd:
        if Login.objects.filter(username=eml).exists():
            return HttpResponse("""<script>alert("user already exits");window.location='/tushionapp/login/'</script>""")
        else:
            logindata = Login()
            logindata.username = eml
            logindata.password = pswd
            logindata.type = 'pending'
            logindata.save()

            date = datetime.now().strftime('%Y%m%d-%H%M%S') + ".jpg"
            fs = FileSystemStorage()
            fs.save(date, pht)
            photopath = fs.url(date)

            date = datetime.now().strftime('%Y%m%d-%H%M%S') + ".jpg"
            fs12 = FileSystemStorage()
            fs12.save(date, idp)
            idppath = fs12.url(date)

            r = Tutor()
            r.Login=logindata
            r.name = name
            r.dob = dob1
            r.email = eml
            r.place = plc
            r.gender = gender
            r.password = pswd
            r.phone = phn
            r.qualification = q
            r.experience = exp
            r.id_proof = idppath
            r.photo = photopath
            r.LOGIN = logindata
            r.status = 'pending'
            r.save()
            return HttpResponse("""<script>alert(" signup successfull");window.location='/tushionapp/login/'</script>""")
    else:
      return  HttpResponse("""<script>alert("password and confirm password not match ");window.location='/tushionapp/SignupTutor/'</script>""")

def ViewProfile(req):
    data=Tutor.objects.get(Login=req.session['lid'])
    print('zxcvbnm,.',Tutor.objects.get(Login=req.session['lid']))
    return render(req,'Tutor/ViewProfile.html',{"data":data})

def EditProfile(req):
    return render(req,'Tutor/ViewProfile.html')

def EditProfile_post(req):
    name = req.POST['name']
    gender = req.POST['gender']
    q = req.POST['qulaification']
    dob1 = req.POST['dob']
    eml = req.POST['email']
    phn = req.POST['phone']
    exp = req.POST['experience']
    plc = req.POST['place']
    # lid=req.POST['lid']
    r = Tutor.objects.get(Login=req.session['lid'])

    if 'photo' in req.FILES:
        pht = req.FILES['photo']

        date = datetime.now().strftime('%Y%m%d-%H%M%S') + ".jpg"
        fs = FileSystemStorage()
        fs.save(date, pht)
        photopath = fs.url(date)
        r.photo = photopath
        r.save()
    if 'idproof' in req.FILES:
        idp = req.FILES['idproof']

        date = datetime.now().strftime('%Y%m%d-%H%M%S') + ".jpg"
        fs12 = FileSystemStorage()
        fs12.save(date, idp)
        idppath = fs12.url(date)
        r.id_proof = idppath
        r.save()
    r.name = name
    r.dob = dob1
    r.email = eml
    r.place = plc
    r.gender = gender
    r.phone = phn
    r.qualification = q
    r.experience = exp
    r.save()
    return HttpResponse("""<script>alert(" edit profile successfull");window.location='/tushionapp/ViewProfile/'</script>""")

def ViewMySubject(req):
    data=Mysubject.objects.filter(Tutor__Login=req.session['lid'])
    print(data)
    ss=ClassStudy.objects.all()
    return render(req,'Tutor/ViewMySubjects.html',{"data":data,'cdata':ss})

def ViewMySubject_post(req):
    cls=req.POST['class']
    print(cls)
    ss=ClassStudy.objects.all()
    search=Mysubject.objects.filter(Tutor__Login=req.session['lid'],Subject__Class_id=cls)
    return render(req,'Tutor/ViewMySubjects.html',{"data":search,'cdata':ss})

def ViewTimeTabelTutor(req):
    data=Timetable.objects.all()
    # data1=Timetable.objects.get()
    return render(req,'Tutor/ViewTimeTable.html',{"data":data})

def ViewTimeTabel_post(req):
    d=req.POST['day']
    data=Timetable.objects.filter(day__icontains=d)
    return render(req,'Tutor/ViewTimeTable.html',{"data":data})

def SendNotification(req):
    data=Mysubject.objects.filter(Tutor__Login_id=req.session['lid'])
    # print(data.Mysubject.Tutor_id)
    return render(req,'Tutor/SendNotification.html',{"data":data})

def SendNotification_post(req):
    msg=req.POST['message']
    subject=req.POST['subject']
    res=Notification()
    res.Tutor=Tutor.objects.get(Login_id=req.session['lid'])
    print(Tutor.objects.get(Login_id=req.session['lid']),"asdfghjkl;")
    res.Date=datetime.now().today()
    res.Time=datetime.now().strftime('%H:%M')
    res.message=msg
    res.mysubject_id=subject
    res.save()
    return HttpResponse("""<script>window.alert("notification send");window.location='/tushionapp/TutorHome/'</script>""")


def ViewNotification(req):
    data=Notification.objects.filter(Tutor__Login_id=req.session['lid'])
    return render(req,'Tutor/ViewNotification.html',{"data":data})
def ViewNotification_post(req):
    frm=req.POST['from']
    to=req.POST['to']
    data = Notification.objects.filter(Date__range=[frm,to])
    return render(req,'Tutor/ViewNotification.html',{"data":data})

def EditNotification(req,id):
    data=Notification.objects.get(id=id)
    # print(data.mysubject_id)
    return render(req,'Tutor/EditNotification.html',{"data":data})
def EditNotification_post(req):
    msg = req.POST['message']
    subject = req.POST['subject']
    eid=req.POST["eid"]
    res=Notification.objects.get(id=eid)
    res.Date = datetime.now().today()
    res.Time = datetime.now().strftime('%H:%M')
    res.message = msg
    res.mysubject_id = subject
    res.save()
    return HttpResponse("""<script>window.alert("Notification edited");window.location='/tushionapp/ViewNotification/' </script>""")

def DeleteNotification(req,id):
    Notification.objects.get(id=id).delete()
    return HttpResponse("""<script>window.alert("Notification Deleted");window.location='/tushionapp/ViewNotification/'</script>""")
def AddAttendence(req):
    sd=Student.objects.all()
    cls=ClassStudy.objects.all()
    return render(req,'Tutor/AddAttendence.html',{"student":sd,"class":cls})

def AddAttendence_post(req):
    stu = req.POST['student1']
    cls = req.POST['class']
    date = req.POST['date']
    hour = req.POST['hour']
    pstatus = req.POST['pstatus']

    attd = Attendence()
    attd.Student_id = stu
    attd.Class_id = cls
    attd.Date = date
    attd.pstatus = pstatus
    attd.hour = hour
    attd.save()
    return HttpResponse("""<script>window.alert("attendence added ");window.location='/tushionapp/ViewAttendence/'</script>""")

def ViewAttendence(req):
    data=Attendence.objects.all()
    return render(req,'Tutor/ViewAttendence.html',{"data":data})
def ViewAttendence_post(req):
    return render(req,'Tutor/ViewAttendence.html')

def EditAttendence(req,id):
    student=Student.objects.all()
    cls=ClassStudy.objects.all()
    data=Attendence.objects.get(id=id)
    return render(req,'Tutor/EditAttendence.html',{"data":data,"student":student,"class":cls})
def EditAttendence_post(req):
    id=req.POST["aid"]
    stu = req.POST['student1']
    cls = req.POST['class']
    date = req.POST['date']
    hour = req.POST['hour']
    pstatus = req.POST['pstatus']

    attd=Attendence.objects.get(id=id)
    attd.Student_id = stu
    attd.Class_id = cls
    attd.Date = date
    attd.pstatus = pstatus
    attd.hour = hour
    attd.save()
    return HttpResponse("""<script>alert(" edit attendence successfull");window.location='/tushionapp/ViewAttendence/'</script>""")

def deleteAttendence(req,id):
    data=Attendence.objects.get(id=id).delete()
    return HttpResponse("""<script>alert(" delete attendence successfull");window.location='/tushionapp/ViewAttendence/'</script>""")


def AddTests(req):
    data=Subjects.objects.all()
    tutor = Tutor.objects.get(Login_id=req.session['lid'])
    id1=tutor
    return render(req,'Tutor/AddTestDetails.html',{"data":data,"id":id1})
def AddTests_post(req):
    # print(Tutor.objects(Login_id=req.session['lid']),"srtyuiolkjhgfdsadfghjklhgfdsaer565wq3456789")
    sub=req.POST["subject"]
    tname=req.POST["tname"]
    date=req.POST["date"]
    ft=req.POST["fromt"]
    tt=req.POST["totime"]
    tutor=req.POST["tid"]
    TD=TestDetails()
    TD.Tutor_id=tutor
    TD.Subject_id=sub
    TD.Test_name=tname
    TD.Date=date
    TD.FromTime=ft
    TD.ToTime=tt
    TD.save()
    return HttpResponse("""<script>window.alert("Add test");window.location='/tushionapp/ViewTest/';</script>""")

def ViewTest(req):
    data=TestDetails.objects.all()
    sub=Subjects.objects.all()
    return render(req,'Tutor/ViewTests.html',{"data":data,"class":sub})
def ViewTest_post(req):
    cls=req.POST['cls']
    print(cls,"sdfghjkl;")
    sub=Subjects.objects.all()
    data=TestDetails.objects.filter(Subject__Class__ClassName=cls)
    return render(req,'Tutor/ViewTests.html',{"data":data,"class":sub})
def EditTest(req,id):
    sub=Subjects.objects.all()
    data=TestDetails.objects.get(id=id)
    return render(req,'Tutor/EditTest.html',{"data":data,"sub":sub,})

def EditTest_post(req):
    sub = req.POST["subject"]
    tname = req.POST["tname"]
    date = req.POST["date"]
    ft = req.POST["fromt"]
    tt = req.POST["totime"]
    id = req.POST["tid"]

    TD = TestDetails.objects.get(id=id)
    TD.Subject_id = sub
    TD.Test_name = tname
    TD.Date = date
    TD.FromTime = ft
    TD.ToTime = tt
    TD.save()
    return HttpResponse("""<script>window.alert("edited");window.location='/tushionapp/ViewTest/' </script>""")

def DeleteTest(req,id):
    data=TestDetails.objects.get(id=id).delete()
    return HttpResponse("""<script>window.alert("deleted");window.location='/tushionapp/ViewTest/' </script>""")

def AddTestResult(req):
    student=Student.objects.all()
    testd=TestDetails.objects.all()
    return render(req,'Tutor/UploadTestResult.html',{"student":student,"test":testd})

def AddTestResult_post(req):
    test=req.POST['testdetails']
    student=req.POST['student']
    mark=req.POST['mark']

    r=Result()
    r.TestDetails_id=test
    r.Student_id=student
    r.mark=mark
    r.save()
    return HttpResponse("""<script>window.alert("add result"); window.location='/tushionapp/ViewTestResult/'</script>""")

def ViewTestResult(req):
    data=Result.objects.all()
    sub=Subjects.objects.all()
    return render(req,'Tutor/ViewTestResult.html',{"data":data,"sub":sub})

def ViewTestResult_post(req):
    cls=req.POST['cls']
    name1=req.POST['sname']
    sub=Subjects.objects.all()
    data=Result.objects.filter(Student__Class__ClassName=cls,Student__name=name1)
    return render(req,'Tutor/ViewTestResult.html',{"data":data,"sub":sub})

def EditTestResult(req,id):
    data=Result.objects.get(id=id)
    student = Student.objects.all()
    testd = TestDetails.objects.all()
    return render(req,'Tutor/EditTestResult.html',{"student":student,"test":testd,"data":data})
def EditTestResult_post(req):
    id=req.POST['rid']
    test = req.POST['testdetails']
    student = req.POST['student']
    mark = req.POST['mark']
    result=Result.objects.get(id=id)
    result.TestDetails_id=test
    result.Student_id=student
    result.mark=mark
    result.save()
    return HttpResponse("""<script>window.alert("edited");window.location='/tushionapp/ViewTestResult/'</script>""")
def DeleteTestResult(req,id):
    Result.objects.get(id=id).delete()
    return HttpResponse("""<script>window.alert("deleted");window.location='/tushionapp/ViewTestResult/'</script>""")

def ViewStudent(req):
    data=Student.objects.all()
    return render(req,'Tutor/ViewStudent.html',{"data":data})
def ViewStudent_post(req):
    student=req.POST['student']
    data=Student.objects.filter(name__icontains=student)
    return render(req,'Tutor/ViewStudent.html',{"data":data})

def ViewFeedbackTutor(req):
    data=Feedback.objects.all()
    return render(req,'Tutor/ViewFeedback.html',{"data":data})
def ViewFeedbackTutor_post(req):
    frm=req.POST['fromdate']
    to=req.POST['todate']
    data=Feedback.objects.filter(Date__range=[frm, to])
    # data = Notification.objects.filter(Date_range=[frm, to])
    return render(req,'Tutor/ViewFeedback.html',{"data":data})

def ChangePassword(req):
    return render(req,'Tutor/Changepassword.html')

def ChangePassword_post(req):
    crnt=req.POST['current']
    new=req.POST['new']
    cnfm=req.POST['confirm']

    check=Login.objects.filter(id=req.session['lid'],password=crnt)
    if check.exists():
        get=Login.objects.get(id=req.session['lid'],password=crnt)
        if new==cnfm:
            update=Login.objects.filter(id=req.session['lid']).update(password=cnfm)
        else:
            return HttpResponse("""<script>window.alert("newpassword and confirm password not equal");window.location='/tushionapp/ChangePassword/'</script>""")
    else:
        return HttpResponse("""<script>window.alert("no password found");window.location='/tushionapp/ChangePassword/'</script>""")

    return HttpResponse("""<script>window.alert("password Changed");window.location='/tushionapp/ChangePassword/'</script>""")


def Logout_tutor(req):
    req.session['lid']=" "
    return HttpResponse("""<script>alert("logout tutor successfully done");window.location='/tushionapp/login/'</script>""")

        #--------------------------------------------------------------------------------------------------------------------------------
        #---------------------------------------------------------   STUDENT ------------------------------------------------------------
        #--------------------------------------------------------------------------------------------------------------------------------

def StudentSignup(req):
    return render(req,'')
