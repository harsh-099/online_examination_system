from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from exam import models as QMODEL
import base64
from django.core.files.base import ContentFile
from django.contrib import messages
from django.contrib.auth.models import User


def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'student/studentclick.html')
def student_signup_view(request):
    if request.method == 'POST':
        userForm = forms.StudentUserForm(request.POST)
        studentForm = forms.StudentForm(request.POST, request.FILES)

        if userForm.is_valid() and studentForm.is_valid():
            user = userForm.save(commit=False)
            user.set_password(userForm.cleaned_data['password'])
            user.save()

            student = studentForm.save(commit=False)
            student.user = user

            captured_data = request.POST.get("captured_image")
            if captured_data and captured_data.startswith("data:image"):
                format, imgstr = captured_data.split(';base64,')
                ext = format.split('/')[-1]
                student.profile_pic = ContentFile(base64.b64decode(imgstr), name=f"user_{user.id}.{ext}")

            student.save()

            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)

            return HttpResponseRedirect('studentlogin')
    else:
        userForm = forms.StudentUserForm()
        studentForm = forms.StudentForm()

    return render(request, 'student/studentsignup.html', {
        'userForm': userForm,
        'studentForm': studentForm
    })

def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_dashboard_view(request):
    dict={
    
    'total_course':QMODEL.Course.objects.all().count(),
    'total_question':QMODEL.Question.objects.all().count(),
    }
    return render(request,'student/student_dashboard.html',context=dict)

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_exam_view(request):
    courses=QMODEL.Course.objects.all()
    return render(request,'student/student_exam.html',{'courses':courses})

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def take_exam_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    total_questions=QMODEL.Question.objects.all().filter(course=course).count()
    questions=QMODEL.Question.objects.all().filter(course=course)
    total_marks=0
    for q in questions:
        total_marks=total_marks + q.marks
    
    return render(request,'student/take_exam.html',{'course':course,'total_questions':total_questions,'total_marks':total_marks})
@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def start_exam_view(request, pk):

    course = QMODEL.Course.objects.get(id=pk)

    questions = list(
        QMODEL.Question.objects.filter(course=course)
    )

    if not questions:
        return render(
            request,
            'student/start_exam.html',
            {
                'course': course,
                'questions': questions,
                'message': 'No questions available for this exam.'
            }
        )

    # Get current question from cookie
    current_question_id = request.COOKIES.get('current_question')

    current_question = None

    if current_question_id:
        try:
            current_question = QMODEL.Question.objects.get(
                id=current_question_id,
                course=course
            )
        except QMODEL.Question.DoesNotExist:
            current_question = None

    # First question
    if current_question is None:
        current_question = questions[0]

    # Current question number
    current_no = 1

    for index, question in enumerate(questions):
        if question.id == current_question.id:
            current_no = index + 1
            break

    # Saved answer
    saved_answer = request.COOKIES.get(
        str(current_question.id)
    )

    # Attempted questions
    attempted_cookie = request.COOKIES.get(
        'attempted_questions',
        ''
    )

    attempted_questions = []

    if attempted_cookie:
        attempted_questions = [
            int(x)
            for x in attempted_cookie.split(',')
            if x.isdigit()
        ]

    response = render(
        request,
        'student/start_exam.html',
        {
            'course': course,
            'questions': questions,
            'current_question': current_question,
            'current_no': current_no,
            'saved_answer': saved_answer,
            'attempted_questions': attempted_questions,
        }
    )

    response.set_cookie('course_id', course.id)

    return response
@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def calculate_marks_view(request):

    course_id = request.COOKIES.get('course_id')

    if course_id is not None:

        course = QMODEL.Course.objects.get(id=course_id)

        total_marks = 0

        questions = list(
            QMODEL.Question.objects.filter(course=course)
        )

        for question in questions:

            selected_ans = request.COOKIES.get(
                str(question.id)
            )

            actual_answer = question.answer

            if selected_ans == actual_answer:
                total_marks += question.marks

        student = models.Student.objects.get(
            user_id=request.user.id
        )

        result = QMODEL.Result()

        result.marks = total_marks
        result.exam = course
        result.student = student

        result.save()

        return HttpResponseRedirect(
            reverse('view-result')
        )

    return HttpResponseRedirect(
        reverse('student-exam')
    )

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def view_result_view(request):
    courses=QMODEL.Course.objects.all()
    return render(request,'student/view_result.html',{'courses':courses})
    

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def check_marks_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    student = models.Student.objects.get(user_id=request.user.id)
    results= QMODEL.Result.objects.all().filter(exam=course).filter(student=student)
    return render(request,'student/check_marks.html',{'results':results})

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_marks_view(request):
    courses=QMODEL.Course.objects.all()
    return render(request,'student/student_marks.html',{'courses':courses})
@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_save_next(request, course_id, question_id):

    course = QMODEL.Course.objects.get(id=course_id)

    questions = list(
        QMODEL.Question.objects.filter(course=course)
    )

    current_question = QMODEL.Question.objects.get(
        id=question_id,
        course=course
    )

    if request.method == 'POST':

        selected_answer = request.POST.get('answer')
        action = request.POST.get('action')

        # Find current question index
        current_index = 0

        for index, question in enumerate(questions):
            if question.id == current_question.id:
                current_index = index
                break

        # Save answer
        response = HttpResponseRedirect(
            reverse('start-exam', args=[course.id])
        )

        if selected_answer:
            response.set_cookie(
                str(current_question.id),
                selected_answer
            )

            # Attempted questions
            attempted_cookie = request.COOKIES.get(
                'attempted_questions',
                ''
            )

            attempted_list = (
                attempted_cookie.split(',')
                if attempted_cookie
                else []
            )

            if str(current_question.id) not in attempted_list:
                attempted_list.append(str(current_question.id))

            response.set_cookie(
                'attempted_questions',
                ','.join(attempted_list)
            )

        # Submit Answers
        if action == 'Submit Answers':
            response = HttpResponseRedirect(
                reverse('calculate-marks')
            )
            return response

        # Save & Next
        if action == 'Save & Next':

            if current_index + 1 < len(questions):

                next_question = questions[current_index + 1]

                response.set_cookie(
                    'current_question',
                    str(next_question.id)
                )

            else:
                response = HttpResponseRedirect(
                    reverse('calculate-marks')
                )

        return response

    return HttpResponseRedirect(
        reverse('start-exam', args=[course.id])
    )