from datetime import datetime

from django.core.checks import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.http import JsonResponse

# ---------------------------------  admin --------------------------------------
from TushionApp.models import *


def login(req):
    return render(req,'LoginIndex.html')

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
        elif lg2.type == 'student':
            return HttpResponse("""<script>window.alert('Studen login success');window.location='/tushionapp/StudentHome/'</script>""")
        else:
            return HttpResponse('''<script>alert("user not found"); window.location='/tushionapp/login/'</script>''')
    else:
        return HttpResponse('''<script> alert("username or password wrong or no user "); window.location='/tushionapp/login/' </script>''')


def HomeAdmin(req):
    if req.session['lid']==' ':
        return HttpResponse('''<script> alert("please Login"); window.location='/tushionapp/login/';wi </script>''')
    else:
        return render(req,'Admin/AdminIndex.html')

def verifyTutor(req):
    if req.session['lid']=='':
        return HttpResponse('''<script> alert("please Login"); window.location='/tushionapp/login/';wi </script>''')
    else:
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
    print(class_id)

    students = Student.objects.filter(Class_id=class_id,status="pending").values(
        'id', 'photo', 'name', 'dob', 'gender', 'email', 'phone', 'place', 'id_proof','Class__ClassName','Login_id',
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

def StudentApproved_search(req,classId):
    print(classId,"class")

    students = Student.objects.filter(Class_id=classId,status="approve").values(
        'id', 'photo', 'name', 'dob', 'gender', 'email', 'phone', 'place', 'id_proof','Class__ClassName','Login_id',
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

def StudentReject_search(request,class_id):
    print(class_id)

    students = Student.objects.filter(Class_id=class_id,status="reject").values(
        'id', 'photo', 'name', 'dob', 'gender', 'email', 'phone', 'place', 'id_proof','Class__ClassName','Login_id',
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
    data=ClassStudy.objects.filter(ClassName__icontains=s)
    return render(req,'Admin/ViewClass.html',{"data":data})

def AddClass(req):
    return render(req,'Admin/AddClass.html')

def AddClass_post(req):
    cl=req.POST['class']
    data=ClassStudy()
    data.ClassName=cl
    data.save()
    return HttpResponse("""<script>alert("Class added");window.location='/tushionapp/ViewClass/' </script>""")

def EditClass(req,id):
    a=ClassStudy.objects.get(id=id)
    b=ClassStudy.objects.all()
    return render(req,'Admin/EditClass.html',{"data":a,"data2":b})
def EditClass_post(req):
    cl=req.POST['class']
    cid=req.POST['cid']
    data=ClassStudy.objects.get(id=cid)
    data.ClassName=cl
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
    return HttpResponse("""<script>alert("subject added successfully");window.location='/tushionapp/AddSubjects/#bodyname' </script>""")
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
    # req.session.flush()
    return HttpResponse("""<script>alert("logout successfully done");window.location='/tushionapp/login/';window.reload=''</script>""")

# def Logout(req):
#     # Clear the session
#     req.session.flush()
#
#     # Optionally, add a success message (if you have message framework set up)
#     # messages.success(req, "Logout successfully done")
#
#     # Redirect to the login page
#     return redirect('/tushionapp/login/')


                    # ------------------------------------------------------------------------
                    # --------------------         TUTOR        ------------------------------
                    # ------------------------------------------------------------------------


def TutorHome(req):
    return render(req,'Tutor/TutorIndex.html')

def TutorHome_post(req):
    return render(req,'Tutor/TutorHome.html')

def SignupTutor(req):
    return render(req,'Tutor/TutorSignupindex.html')

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
    # eml = req.POST['email']
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
    # r.email = eml
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
    # print(eid,subject)

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
def AddAttendence(req,id):
    sd=Student.objects.get(id=id)
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
    return HttpResponse("""<script>window.alert("attendence added ");window.location='/tushionapp/ViewAttendence/#bodyname'</script>""")

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

def AddTestResult(req,id):
    student=Student.objects.get(id=id)
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

def StudentHome(req):
    return render(req,'Student/StudentIndex.html')

def StudentSignup(req):
    cls=ClassStudy.objects.all()
    return render(req,'Student/StudentSignupindex.html',{"class":cls})

def StudentSignup_post(req):
    name = req.POST['sname']
    gender = req.POST['gender']
    # q = req.POST['qulaification']
    dob1 = req.POST['dob']
    pht = req.FILES['photo']
    eml = req.POST['email']
    phn = req.POST['phn']
    cls = req.POST['class']
    plc = req.POST['place']
    idp = req.FILES['idprf']
    pswd = req.POST['pswd']
    cpswd = req.POST['cpswd']

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

            r = Student()
            r.Login = logindata
            r.name = name
            r.dob = dob1
            r.email = eml
            r.place = plc
            r.gender = gender
            r.password = pswd
            r.phone = phn
            # r.qualification = q
            r.Class_id = cls
            r.id_proof = idppath
            r.photo = photopath
            r.LOGIN = logindata
            r.status = 'pending'
            r.save()
            return HttpResponse("""<script>alert(" student signup successfull");window.location='/tushionapp/login/'</script>""")
    else:
        return HttpResponse("""<script>alert("password and confirm password not match ");window.location='/tushionapp/StudentSignup/'</script>""")

def ViewStudentProfile(req):
    data=Student.objects.get(Login_id=req.session['lid'])
    cls = ClassStudy.objects.all()
    return render(req,'Student/ViewStudentProfile.html',{"data":data,"class":cls})

def ViewStudentProfile_post(req):
    return render(req,'Student/ViewStudentProfile.html')

def EditStudentProfile_post(req):
    name = req.POST['sname']
    gender = req.POST['gender']
    # q = req.POST['qulaification']
    dob1 = req.POST['dob']
    phn = req.POST['phn']
    # cls = req.POST['class']
    plc = req.POST['place']

    r=Student.objects.get(Login_id=req.session['lid'])

    if 'phto' in req.FILES:
        pht = req.FILES['phto']
        date = datetime.now().strftime('%Y%m%d-%H%M%S') + ".jpg"
        fs = FileSystemStorage()
        fs.save(date, pht)
        photopath = fs.url(date)
        r.photo = photopath
        r.save()

    if 'idprf' in req.FILES:
        idp = req.FILES['idprf']

        date = datetime.now().strftime('%Y%m%d-%H%M%S') + ".jpg"
        fs12 = FileSystemStorage()
        fs12.save(date, idp)
        idppath = fs12.url(date)
        r.id_proof = idppath
        r.save()

    r.name = name
    r.dob = dob1
    r.place = plc
    r.gender = gender
    # r.password = pswd
    r.phone = phn
    # r.Class_id = cls
    r.save()
    # return HttpResponse("""<script>alert("edited");window.location='/tushionapp/ViewStudentProfile/'</sctipt>""")
    return HttpResponse("""<script>alert(" student edited successfull");window.location='/tushionapp/StudentHome/'</script>""")

def ViewStudentNotification(req):
    cls_id=Student.objects.get(Login_id=req.session['lid']).Class_id
    data=Notification.objects.filter(mysubject__Subject__Class_id=cls_id)
    print(data)
    return render(req,'Student/ViewStudentNotification.html',{"data":data})

def ViewStudentNotification_post(req):
    frmdate=req.POST['fromdate']
    todate=req.POST['to']
    cls_id=Student.objects.get(Login_id=req.session['lid']).Class_id
    data=Notification.objects.filter(mysubject__Subject__Class_id=cls_id,Date__range=[frmdate,todate])
    return render(req,'Student/ViewStudentNotification.html',{"data":data})

def ViewStudentTest(req):
    cls_id=Student.objects.get(Login_id=req.session['lid']).Class_id
    data=TestDetails.objects.filter(Subject__Class_id=cls_id)
    return render(req,'Student/ViewStudentTestDetails.html',{"data":data})

def ViewStudentTest_post(req):
    frmdate = req.POST['fromdate']
    todate = req.POST['to']
    cls_id=Student.objects.get(Login_id=req.session['lid']).Class_id
    data=TestDetails.objects.filter(Subject__Class_id=cls_id,Date__range=[frmdate,todate])
    return render(req,'Student/ViewStudentTestDetails.html',{"data":data})

def ViewStudentAttendence(req):
    id=Student.objects.get(Login_id=req.session['lid']).id
    data=Attendence.objects.filter(Student_id=id)
    return render(req,'Student/ViewStudentAttendence.html',{"data":data})

def ViewStudentAttendence_post(req):
    frmdate = req.POST['fromdate']
    todate = req.POST['to']
    id=Student.objects.get(Login_id=req.session['lid']).id
    data=Attendence.objects.filter(Student_id=id,Date__range=[frmdate,todate])
    return render(req,'Student/ViewStudentAttendence.html',{"data":data})

def ViewStudentResult(req):
    id = Student.objects.get(Login_id=req.session['lid']).id
    data=Result.objects.filter(Student_id=id)
    return render(req,'Student/ViewTestResult.html',{"data":data})

def ViewStudentresult_post(req):
    subject = req.POST['subject']
    id = Student.objects.get(Login_id=req.session['lid']).id
    data = Result.objects.filter(Student_id=id,TestDetails__Subject__SubjectName=subject)
    return render(req,'Student/ViewTestResult.html',{"data":data})


def ViewSubject(req):
    cls_id = Student.objects.get(Login_id=req.session['lid']).Class_id
    data=Subjects.objects.filter(Class_id=cls_id)
    return render(req,'Student/ViewStudentSubject.html',{"data":data})

def ViewStudentTimeTable(req):
    cls_id=Student.objects.get(Login_id=req.session['lid']).Class_id
    data=Timetable.objects.filter(Subject__Class_id=cls_id)
    return render(req,'Student/ViewStudentTimetable.html',{"data":data})

def ViewStudentTimeTable_post(req):
    subject=req.POST['subject']
    cls_id=Student.objects.get(Login_id=req.session['lid']).Class_id
    data=Timetable.objects.filter(Subject__Class_id=cls_id,Subject__SubjectName=subject)
    return render(req,'Student/ViewStudentTimetable.html',{"data":data})

def AddStudentComplaint(req):
    return render(req,'Student/AddComplaint.html')

def AddStudentComplaint_post(req):
    complaint = req.POST['complaint']
    id=Student.objects.get(Login_id=req.session['lid']).id
    c=Complaints()
    c.complaint=complaint
    c.Student_id=id
    c.Date=datetime.now().today()
    c.replay='pending'
    c.status='pending'
    c.save()
    return HttpResponse("""<script>alert("complaint send");window.location='/tushionapp/StudentHome/'</script>""")

def ViewStudentreply(req):
    id=Student.objects.get(Login_id=req.session['lid']).id
    data=Complaints.objects.filter(Student_id=id)
    return render(req,'Student/ViewReply.html',{"data":data})

def StudentChangePassword(req):
    return render(req,'Student/StudentChangepassword.html')

def StudentChangePassword_post(req):
    crnt = req.POST['Cpass']
    new = req.POST['newpass']
    cnfm = req.POST['cfrmpasswd']

    check = Login.objects.filter(id=req.session['lid'], password=crnt)
    if check.exists():
        get = Login.objects.get(id=req.session['lid'], password=crnt)
        if new == cnfm:
            update = Login.objects.filter(id=req.session['lid']).update(password=cnfm)
        else:
            return HttpResponse("""<script>window.alert("newpassword and confirm password not equal");window.location='/tushionapp/StudentChangePassword/'</script>""")
    else:
        return HttpResponse("""<script>window.alert("no password found");window.location='/tushionapp/StudentChangePassword/'</script>""")

    return HttpResponse("""<script>window.alert("password Changed");window.location='/tushionapp/StudentChangePassword/'</script>""")


def StudentFeedback(req):
    cls_id=Student.objects.get(Login_id=req.session['lid']).Class_id
    data=Mysubject.objects.filter(Subject__Class_id=cls_id)
    return render(req,'Student/SendStudentFeedback.html',{"data":data})

def StudentFeedback_post(req):
    tutor=req.POST['tutor']
    fdbk=req.POST['feedback']
    id=Student.objects.get(Login_id=req.session['lid']).id
    f=Feedback()
    f.Student_id=id
    f.Tutor_id=tutor
    f.feedback=fdbk
    f.Date=datetime.now().today()
    f.save()
    return HttpResponse("""<script>alert("feedback Send");window.location='/tushionapp/StudentHome/'</script>""")
def StudentLogout(req):
    req.session['lid']=''
    return render(req,'Login.html')

#--------------------------------   Public

def ViewPublic(req):
    return render(req,'Public/publicHome.html')

def PublicViewTutor(req):
    data=Mysubject.objects.all()
    return render(req,'Public/publicViewtutor.html',{"data":data})

def PublicViewSubject(req):
    data=Subjects.objects.all()
    return render(req,'Public/publicViewsubject.html',{"data":data})

def PublicViewtimetable(req):
    data=Timetable.objects.all()
    return render(req,'Public/publicViewtimetable.html',{"data":data})

# -------------------------flutter student

def viewflutStudentSignup(req):
    cls=ClassStudy.objects.all()
    l=[]
    for i in cls:
        l.append({'id':i.id,'classname':i.ClassName})
    print(l,"llllll")
    return JsonResponse({"status":"ok","data":l})


def flutStudentSignup(req):
    name=req.POST["uname"]
    dob=req.POST["dob"]
    gender=req.POST["gender"]
    email=req.POST["em"]
    phone=req.POST["phn"]
    place=req.POST["plc"]
    pwd=req.POST["pwd"]
    cpwd=req.POST["cpwd"]
    photo=req.POST["photo"]
    idprd=req.POST["idproof"]
    cls=req.POST["class"]

    import base64
    date = datetime.now().strftime("%y%m%d-%H%M%S")
    a = base64.b64decode(photo)
    fh= open("C:\\Users\\kashy\\PycharmProjects\\TushionClass\\media\\Student\\"+date+".jpg","wb")
    phpath = '/media/Student/' + date + '.jpg'
    fh.write(a)
    fh.close()

    date1 = datetime.now().strftime("%y%m%d-%H%M%S")
    a1 = base64.b64decode(idprd)
    fh= open("C:\\Users\\kashy\\PycharmProjects\\TushionClass\\media\\Student\\"+date1+"-1.jpg","wb")
    idpath = '/media/Student/' + date1 + '-1.jpg'
    fh.write(a1)
    fh.close()

    if pwd == cpwd:
        if Login.objects.filter(username=email).exists():
            return JsonResponse({"status":"No"})
        login=Login()
        login.username=email
        login.password=cpwd
        login.type="student"
        login.save()

        st=Student()
        st.name=name
        st.dob=dob
        st.email=email
        st.phone=phone
        st.place=place
        st.photo=phpath
        st.id_proof=idpath
        st.gender=gender
        st.status="pending"
        st.Class_id=cls
        st.Login=login
        st.save()
        return JsonResponse({"status":"ok"})
    else:
        return JsonResponse({"status":"no"})



def flutStudentLogin(req):
    uname=req.POST["uname"]
    upassword=req.POST["password"]
    print(uname,upassword)
    lg1=Login.objects.filter(username=uname,password=upassword)
    if lg1.exists():
        lg2=Login.objects.get(username=uname,password=upassword)
        lid=lg2.id
        if lg2.type == "student":
            print('ok')
            return JsonResponse({"status":"ok","lid":str(lid)})
        else:
            return JsonResponse({"status":"no"})
    else:
        return JsonResponse({"status":"no"})


def ViewFlutStudentProfile(req):
    lid=req.POST['lid']
    stu=Student.objects.get(Login_id=lid)
    print(stu.place)
    return JsonResponse({"status":"ok",
                         "name":stu.name,
                         "dob":stu.dob,
                         "photo":stu.photo,
                         "gender":stu.gender,
                         "email":stu.email,
                         "phone":stu.phone,
                         "place":stu.place,
                         "idproof":stu.id_proof,
                         "class":stu.Class.ClassName
                         })



def EditProfileFlut(req):
    name = req.POST["uname"]
    dob = req.POST["dob"]
    gender = req.POST["gender"]
    email = req.POST["em"]
    phone = req.POST["phn"]
    place = req.POST["plc"]
    photo = req.POST["photo"]
    idprd = req.POST["idproof"]
    cls = req.POST["class"]
    uid=req.POST['uid']
    print(name,dob,gender,email,phone,place,photo,idprd,cls,)
    print(uid)
    return