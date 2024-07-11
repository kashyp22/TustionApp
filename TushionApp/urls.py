from django.urls import path

from TushionApp import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    # admin get
    path('login/', views.login),
    path('HomeAdmin/', views.HomeAdmin),
    path('verifyTutor/', views.verifyTutor),
    path('verifyTutor_post/', views.verifyTutor_post),
    path('approvedTutor/', views.approvedTutor),
    path('approveTutor/<id>', views.approveTutor),
    path('approveTutor_post/', views.approvedTutor_post),
    path('rejectTutor/<id>', views.rejectTutor),
    path('rejectedTutor/', views.rejectedTutor),
    path('rejectedTutor_post/', views.rejectedTutor_post),
    path('studentVerify/', views.studentVerify),
    path('studentApproved/', views.studentApproved),
    path('studentApprove/<id>', views.studentApprove),
    path('studentReject/<id>', views.studentReject),
    path('studentRejected/', views.studentRejected),
    path('StudentComplaint/', views.StudentComplaint),
    path('StudentComplaint_post/', views.StudentComplaint_post),
    path('ReplyStudentComplaint/<id>', views.ReplyStudentComplaint),
    path('ReplyStudentComplaint_post/', views.ReplyStudentComplaint_post),
    path('ViewFeedback/', views.ViewFeedback),
    path('ViewFeedback_post/', views.ViewFeedback_post),
    path('ViewClass/', views.ViewClass),
    path('ViewClass_post/', views.ViewClass_post),
    path('AddClass/', views.AddClass),
    path('AddClass_post/', views.AddClass_post),
    path('EditClass/<id>', views.EditClass),
    path('deleteClass/<id>', views.deleteClass),
    path('EditClass_post/', views.EditClass_post),
    path('ViewSubjects/', views.ViewSubjects),
    path('ViewSubjects_post/', views.ViewSubjects_post),
    path('AddSubjects/', views.AddSubjects),
    path('EditSubjects/<id>', views.EditSubjects),
    path('EditSubjects_post/', views.EditSubjects_post),
    path('DeleteSubjects/<id>', views.DeleteSubjects),
    path('ViewTimeTable/', views.ViewTimeTable),
    path('ViewTimeTable_post/', views.ViewTimeTable_post),
    path('AddTimeTable/', views.AddTimeTable),
    path('AddTimeTable_post/', views.AddTimeTable_post),
    path('EditTimeTable/<id>', views.EditTimeTable),
    path('EditTimeTable_post/', views.EditTimeTable_post),
    path('DeleteTimeTable/<id>', views.DeleteTimeTable),
    path('SubjectAllocate/', views.SubjectAllocate),
    path('SubjectAllocate_post/', views.SubjectAllocate_post),
    path('ViewAllocateTeacher/', views.ViewAllocateTeacher),
    path('ViewAllocateTeacher_post/', views.ViewAllocateTeacher_post),
    path('EditAllocateTeacher/<id>', views.EditAllocateTeacher),
    path('EditAllocateTeacher_post/', views.EditAllocateTeacher_post),
    path('DeleteAllocateTeacher/<id>', views.DeleteAllocateTeacher),
    path('Logout/',views.Logout),
    path('ajax/get_class_students/<int:class_id>/', views.get_class_students),
    path('ajax/StudentApproved_search/<int:classId>/', views.StudentApproved_search),
    path('ajax/StudentReject_search/<int:class_id>/', views.StudentReject_search),
    path('login_post/', views.login_post),
    path('verifyTutor_post/', views.verifyTutor_post),
    path('approvedTutor_post/', views.approvedTutor_post),
    path('rejectedTutor_post/', views.rejectedTutor_post),
    path('studentVerify_post/', views.studentVerify_post),
    path('studentApproved_post/', views.studentApproved_post),
    path('studentRejected_post/', views.studentRejected_post),
    path('AddSubjects_post/', views.AddSubjects_post),

#  ----------------------------tutor

    path('TutorHome/',views.TutorHome),
    path('TutorHome_post/',views.TutorHome_post),
    path('SignupTutor/',views.SignupTutor),
    path('SignupTutor_post/',views.SignupTutor_post),
    path('ViewProfile/',views.ViewProfile),
    path('EditProfile/',views.EditProfile),
    path('EditProfile_post/',views.EditProfile_post),
    path('ViewMySubject/',views.ViewMySubject),
    path('ViewMySubject_post/',views.ViewMySubject_post),
    path('ViewTimeTabelTutor/',views.ViewTimeTabelTutor),
    path('ViewTimeTabel_post/',views.ViewTimeTabel_post),
    path('SendNotification/',views.SendNotification),
    path('SendNotification_post/',views.SendNotification_post),
    path('ViewNotification/',views.ViewNotification),
    path('ViewNotification_post/',views.ViewNotification_post),
    path('EditNotification/<id>',views.EditNotification),
    path('EditNotification_post/',views.EditNotification_post),
    path('DeleteNotification/<id>',views.DeleteNotification),
    path('AddAttendence/',views.AddAttendence),
    path('AddAttendence_post/',views.AddAttendence_post),
    path('ViewAttendence/',views.ViewAttendence),
    path('ViewAttendence_post/',views.ViewAttendence_post),
    path('EditAttendence/<id>',views.EditAttendence),
    path('EditAttendence_post/',views.EditAttendence_post),
    path('deleteAttendence/<id>', views.deleteAttendence),
    path('AddTests/',views.AddTests),
    path('AddTests_post/',views.AddTests_post),
    path('ViewTest/',views.ViewTest),
    path('ViewTest_post/',views.ViewTest_post),
    path('EditTest/<id>',views.EditTest),
    path('EditTest_post/',views.EditTest_post),
    path('DeleteTest/<id>',views.DeleteTest),
    path('AddTestResult/',views.AddTestResult),
    path('AddTestResult_post/',views.AddTestResult_post),
    path('ViewTestResult/',views.ViewTestResult),
    path('ViewTestResult_post/',views.ViewTestResult_post),
    path('EditTestResult/<id>',views.EditTestResult),
    path('EditTestResult_post/',views.EditTestResult_post),
    path('DeleteTestResult/<id>',views.DeleteTestResult),
    path('ViewStudent/',views.ViewStudent),
    path('ViewStudent_post/',views.ViewStudent_post),
    path('ViewFeedbackTutor/',views.ViewFeedbackTutor),
    path('ViewFeedbackTutor_post/',views.ViewFeedbackTutor_post),
    path('ChangePassword/',views.ChangePassword),
    path('ChangePassword_post/',views.ChangePassword_post),
    path('logout/',views.Logout_tutor),

#     Student
    path('StudentHome/',views.StudentHome),
    path('StudentSignup/',views.StudentSignup),
    path('StudentSignup_post/',views.StudentSignup_post),
    path('ViewStudentProfile/',views.ViewStudentProfile),
    path('EditStudentProfile_post/',views.EditStudentProfile_post),
    path('ViewStudentNotification/',views.ViewStudentNotification),
    path('ViewStudentNotification_post/',views.ViewStudentNotification_post),
    path('ViewStudentTest/',views.ViewStudentTest),
    path('ViewStudentTest_post/',views.ViewStudentTest_post),
    path('ViewStudentAttendence/',views.ViewStudentAttendence),
    path('ViewStudentAttendence_post/',views.ViewStudentAttendence_post),
    path('ViewStudentResult/',views.ViewStudentResult),
    path('ViewStudentresult_post/',views.ViewStudentresult_post),
    path('ViewSubject/',views.ViewSubject),
    path('ViewStudentTimeTable/',views.ViewStudentTimeTable),
    path('ViewStudentTimeTable_post/',views.ViewStudentTimeTable_post),
    path('AddStudentComplaint/',views.AddStudentComplaint),
    path('AddStudentComplaint_post/',views.AddStudentComplaint_post),
    path('ViewStudentreply/',views.ViewStudentreply),
    path('StudentChangePassword/',views.StudentChangePassword),
    path('StudentChangePassword_post/',views.StudentChangePassword_post),
    path('StudentFeedback/',views.StudentFeedback),
    path('StudentFeedback_post/',views.StudentFeedback_post),
    path('StudentLogout/',views.StudentLogout),

]
