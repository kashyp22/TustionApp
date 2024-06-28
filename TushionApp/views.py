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
            return HttpResponse('''<script>alert("admin not found"); window.location='/tushionapp/login/'</script>''')
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

# -------------------- tutor --------------------------------------------

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
            logindata.type = 'tutor'
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
            r.save()
            return HttpResponse("""<script>alert(" signup successfull");window.location='/tushionapp/login/'</script>""")
    else:
      return  HttpResponse("""<script>alert("password and confirm password not math ");window.location='/tushionapp/SignupTutor/'</script>""")

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
    return render(req,'Tutor/ViewMySubjects.html',{"data":data})
def ViewMySubject_post(req):
    return render(req,'Tutor/ViewMySubjects.html')

def ViewTimeTabel(req):
    data=Timetable.objects.all()
    data1=Timetable.objects.get()
    return render(req,'Tutor/ViewMySubjects.html')
def ViewTimeTabel_post(req):
    return render(req,'Tutor/ViewMySubjects.html')

def SendNotification(req):
    return render(req,'Tutor/SendNotification.html')
def ViewNotification(req):
    return render(req,'Tutor/ViewNotification.html')
def EditNotification(req):
    return render(req,'Tutor/EditNotification.html')

def AddAttendence(req):
    return render(req,'Tutor/AddAttendence.html')
def AddAttendence_post(req):
    return render(req,'Tutor/AddAttendence.html')

def ViewAttendence(req):
    return render(req,'Tutor/ViewAttendence.html')
def ViewAttendence_post(req):
    return render(req,'Tutor/ViewAttendence.html')

def EditAttendence(req):
    return render(req,'Tutor/EditAttendence.html')
def EditAttendence_post(req):
    return render(req,'Tutor/EditAttendence.html')

def AddTests(req):
    return render(req,'Tutor/AddTestDetails.html')
def AddTests_post(req):
    return render(req,'Tutor/AddTestDetails.html')

def ViewTest(req):
    return render(req,'Tutor/ViewTests.html')
def EditTest(req):
    return render(req,'Tutor/EditTest.html')
def EditTest_post(req):
    return render(req,'Tutor/EditTest.html')

def DeleteTest(req):
    return render(req,'Tutor/ViewTests.html')

def AddTestResult(req):
    return render(req,'Tutor/UploadTestResult.html')
def ViewTestResult(req):
    return render(req,'Tutor/ViewTestResult.html')
def EditTestResult(req):
    return render(req,'Tutor/EditTestResult.html')

def ViewStudent(req):
    data=Student.objects.all()
    return render(req,'Tutor/ViewStudent.html',{"data":data})
def ViewStudent_post(req):
    return render(req,'Tutor/ViewStudent.html')

def ViewFeedbackTutor(req):
    return render(req,'Tutor/ViewFeedback.html')

def ChangePassword(req):
    return render(req,'Tutor/Changepassword.html')
def ChangePassword_post(req):
    return render(req,'Tutor/Changepassword.html')


def Logout_tutor(req):
    req.session['lid']=" "
    return HttpResponse("""<script>alert("logout tutor successfully done");window.location='/tushionapp/login/'</script>""")

