from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
    notices=Notice.objects.all().order_by('-id')

    return render(request, 'index.html',locals())

def admin_login(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard')  
    error=None
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user=authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            error="Invalid username or password"
    return render(request, 'admin_login.html', locals())    

def admin_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    total_students=Student.objects.count()
    total_subjects=Subject.objects.count()
    total_classes=Class.objects.count()
    total_results=Result.objects.values('student').distinct().count()
    

    return render(request, 'admin_dashboard.html',locals())

def admin_logout(request):
    logout(request)
    return redirect('admin_login')
    
@login_required
def create_class(request):
    if request.method == "POST":
        try:
            class_name = request.POST.get('classname')
            class_numeric = request.POST.get('classnamenumeric')
            section = request.POST.get('section')

            Class.objects.create(
                name=class_name,
                numeric=class_numeric,
                section=section
            )

            messages.success(request, "Class Created Successfully")
            return redirect('create_class')

        except Exception as e:
            messages.error(request, f"Something went wrong: {str(e)}")
            return redirect('create_class')

    return render(request, 'create_class.html')

@login_required
def manage_classes(request):
    classes=Class.objects.all()

    if request.GET.get('delete'):
        try:
            class_id=request.GET.get('delete')
            class_obj=get_object_or_404(Class,id=class_id)
            class_obj.delete()
            messages.success(request,"Class deleted successfully")
            return redirect('manage_classes')
        except Exception as e:
            messages.error(request,f"Something Went Wrong: {str(e)}")
            return redirect('manage_classes')


    return render(request,'manage_classes.html',locals())

@login_required
def edit_class(request, class_id):
    class_obj = get_object_or_404(Class, id=class_id)

    if request.method == "POST":
        class_name = request.POST.get('classname')
        class_numeric = request.POST.get('classnamenumeric')
        section = request.POST.get('section')

        try:
            class_obj.name = class_name
            class_obj.numeric = class_numeric
            class_obj.section = section

            class_obj.save()
            messages.success(request, "Class updated successfully")
            return redirect('manage_classes')

        except Exception as e:
            messages.error(request, f"Something went wrong: {str(e)}")
            return redirect('manage_classes')

    return render(request, 'edit_class.html', locals())


@login_required
def create_subject(request):
    if request.method == "POST":
        try:
            subject_name = request.POST.get('subjectname')
            subject_code= request.POST.get('subjectcode')
            Subject.objects.create(
                name=subject_name,
                code=subject_code,
            )
            messages.success(request, "Subject Created Successfully")
        except Exception as e:
            messages.error(request, f"Something went wrong: {str(e)}")
        return redirect('create_subject')
    return render(request, 'create_subject.html')
@login_required
def manage_subject(request):
    subject=Subject.objects.all()

    if request.GET.get('delete'):
        try:
            subject_id=request.GET.get('delete')
            subject_obj=get_object_or_404(Subject,id=subject_id)
            subject_obj.delete()
            messages.success(request,"Class deleted successfully")
        except Exception as e:
            messages.error(request,f"Something Went Wrong: {str(e)}")
        return redirect('manage_subject')
    return render(request,'manage_subject.html',locals())

@login_required
def edit_subject(request, subject_id):
    subject_obj = get_object_or_404(Subject, id=subject_id)

    if request.method == "POST":
        subject_name = request.POST.get('subjectname')
        subject_code = request.POST.get('subjectcode')
        try:
            subject_obj.name = subject_name
            subject_obj.code = subject_code
            subject_obj.save()
            messages.success(request, "Class updated successfully")
      
        except Exception as e:
            messages.error(request, f"Something went wrong: {str(e)}")
        return redirect('manage_subject')

    return render(request, 'edit_subject.html', locals())

@login_required
def add_subject_combination(request):
    classes=Class.objects.all()
    subjects=Subject.objects.all()

    if request.method == "POST":
        try:
            class_id = request.POST.get('class')
            subject_id= request.POST.get('subject')
            SubjectCombination.objects.create(
                student_class_id=class_id,
                subject_id=subject_id,
                status=1
            )
            messages.success(request, "Subject combination added Successfully")
        except Exception as e:
            messages.error(request, f"Something went wrong: {str(e)}")
        return redirect('add_subject_combination')
    return render(request, 'add_subject_combination.html',locals())


@login_required
def manage_subject_combination(request):
    combination=SubjectCombination.objects.all()
    aid=request.GET.get('aid')

    if request.GET.get('aid'):
        try:
            SubjectCombination.objects.filter(id=aid).update(status=1)
            messages.success(request,"Subject Combination Successfully Activated")
        except Exception as e:
            messages.error(request,f"Something Went Wrong: {str(e)}")
        return redirect('manage_subject_combination')
    
    did=request.GET.get('did')

    if request.GET.get('did'):
        try:
            SubjectCombination.objects.filter(id=did).update(status=0)
            messages.success(request,"Subject Combination Successfully Deactivated")
        except Exception as e:
            messages.error(request,f"Something Went Wrong: {str(e)}")
        return redirect('manage_subject_combination')
    return render(request,'manage_subject_combination.html',locals())


@login_required
def add_student(request):
    classes = Class.objects.all()
    subjects = Subject.objects.all()

    if request.method == "POST":
        try:
            name = request.POST.get('name')
            roll_id = request.POST.get('roll_id')
            email = request.POST.get('email')
            gender = request.POST.get('gender')
            dob = request.POST.get('dob')
            class_id = request.POST.get('class')

            # Validate fields
            if not name:
                raise ValueError("Name field is empty")
            if not class_id:
                raise ValueError("Class not selected")

            student_class = Class.objects.get(id=class_id)

            Student.objects.create(
                name=name,
                roll_id=roll_id,
                email=email,
                gender=gender,
                dob=dob,
                student_class=student_class,
            )

            messages.success(request, "Student Info Added Successfully")

        except Exception as e:
            messages.error(request, f"Something went wrong: {str(e)}")

        return redirect('add_student')

    return render(request, 'add_student.html', locals())


@login_required
def manage_student(request):
    student=Student.objects.all()
    
    return render(request,'manage_student.html',locals())


@login_required
def edit_student(request, student_id):
    student_obj = get_object_or_404(Student, id=student_id)

    if request.method == "POST":
        try:
            student_obj.name = request.POST.get('name')
            student_obj.roll_id = request.POST.get('roll_id')
            student_obj.email = request.POST.get('email')
            student_obj.gender = request.POST.get('gender')
            student_obj.dob = request.POST.get('dob')
            student_obj.status = int(request.POST.get('status'))

            student_obj.save()
            messages.success(request, "Student info updated successfully")

        except Exception as e:
            messages.error(request, f"Something went wrong: {str(e)}")
        
        return redirect('manage_student')

    return render(request, 'edit_student.html', {"student_obj": student_obj})



from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Notice

@login_required
def add_notice(request):
    if request.method == "POST":
        title = request.POST.get('title', '').strip()
        details = request.POST.get('details', '').strip()

        if not title or not details:
            messages.error(request, "Title and Details are required.")
            return redirect('add_notice')

        try:
            Notice.objects.create(title=title, detail=details)
            messages.success(request, "Notice added successfully.")
        except Exception as e:
            messages.error(request, f"Something went wrong: {str(e)}")

        return redirect('add_notice')

    return render(request, 'add_notice.html', {})

@login_required
def manage_notice(request):
    notices = Notice.objects.all()  # plural naming is clearer

    if request.GET.get('delete'):
        try:
            notice_id = request.GET.get('delete')
            notice_obj = get_object_or_404(Notice, id=notice_id)
            notice_obj.delete()
            messages.success(request, "Notice deleted successfully")
        except Exception as e:
            messages.error(request, f"Something Went Wrong: {str(e)}")
        return redirect('manage_notice')

    return render(request, 'manage_notice.html', {'notices': notices})


@login_required
def edit_notice(request, notice_id):
    notice_obj = get_object_or_404(Notice, id=notice_id)

    if request.method == "POST":
        try:
            notice_obj.title = request.POST.get('title')
            notice_obj.detail = request.POST.get('detail')   # FIXED
            notice_obj.save()
            messages.success(request, "Notice updated successfully")

        except Exception as e:
            messages.error(request, f"Something went wrong: {str(e)}")

        return redirect('manage_notice')

    return render(request, "edit_notice.html", {"notice_obj": notice_obj})


@login_required
def add_result(request):
    classes = Class.objects.all()

    if request.method == "POST":
        try:
            class_id = request.POST.get("class")
            student_id = request.POST.get("studentid")

            if not class_id or not student_id:
                raise ValueError("Class and Student are required")

            student = Student.objects.get(id=student_id)
            student_class = Class.objects.get(id=class_id)

            subject_combinations = SubjectCombination.objects.filter(
                student_class=student_class,
                status=1
            ).select_related("subject")

            for sc in subject_combinations:
                marks = request.POST.get(f"subject_{sc.subject.id}")

                if marks is None:
                    continue

                Result.objects.update_or_create(
                    student=student,
                    student_class=student_class,
                    subject=sc.subject,
                    defaults={"marks": marks}
                )

            messages.success(request, "Result declared successfully")
            return redirect("add_result")

        except Exception as e:
            messages.error(request, f"Error: {str(e)}")

    return render(request, "add_result.html", {
        "classes": classes
    })

from django.http import JsonResponse
def get_student_subjects(request):
    class_id = request.GET.get("class_id")

    if class_id:
        students = list(
            Student.objects.filter(student_class_id=class_id)
            .values("id", "name", "roll_id")
        )

        subject_combinations = SubjectCombination.objects.filter(
            student_class_id=class_id, status=1
        ).select_related("subject")

        subjects = [
            {"id": sc.subject.id, "name": sc.subject.name}
            for sc in subject_combinations
        ]

        return JsonResponse({
            "students": students,
            "subjects": subjects
        })

    return JsonResponse({"students": [], "subjects": []})


@login_required
def manage_result(request):
    # get unique students who have results
    students = (
        Student.objects
        .filter(result__isnull=False)
        .select_related('student_class')
        .distinct()
    )

    if request.GET.get('delete'):
        student_id = request.GET.get('delete')
        Result.objects.filter(student_id=student_id).delete()
        messages.success(request, "Student result deleted successfully")
        return redirect('manage_result')

    return render(request, 'manage_result.html', {
        'students': students
    })

@login_required
def edit_result(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    results = Result.objects.filter(student=student).select_related("subject")

    if request.method == "POST":
        for r in results:
            marks = request.POST.get(f"subject_{r.subject.id}")
            if marks is not None:
                r.marks = marks
                r.save()

        messages.success(request, "Result updated successfully")
        return redirect("manage_result")

    return render(request, "edit_result.html", {
        "student": student,
        "results": results
    })
from django.contrib.auth import update_session_auth_hash
@login_required
def change_password(request):

    if request.method == "POST":
        old=request.POST['oldpassword']
        new=request.POST['newpassword']
        confirm=request.POST['confpassword']

        if new!= confirm:
            messages.error(request,"New Password and Confirm Password do not same")
            return redirect("change_password")
        user=authenticate(username=request.user.username,password=old)
        if user:
            user.set_password(new)
            user.save()
            update_session_auth_hash(request,user)
            messages.success(request, "Password updated successfully")
            return redirect("change_password")
        else:
            messages.success(request, "old password is incorrect")
            return redirect("change_password")

    return render(request, "change_password.html")


def search_result(request):
    classes=Class.objects.all()

    return render(request,'search_result.html',locals())

def check_result(request):

    if request.method=='POST':
        rollid=request.POST['rollid']
        class_id =request .POST['class']
        print(rollid)
        print(class_id)
        try:
            student=Student.objects.get(roll_id= rollid, student_class_id=class_id)
            results=Result.objects.filter(student=student)

            total_marks=sum([r.marks for r in results ])
            subject_count=results.count()
            max_total=subject_count*100
            percentage=(total_marks/max_total)*100 if max_total>0 else 0
            percentage=round(percentage,2)
            return render(request,'check_result.html',locals())
        except Exception as e:
            messages.error(request, "No Result for given Roll ID and class")
            return redirect('search_result')


    return render(request,'check_result.html',locals())

def notice_detail(request, notice_id):
    notice = get_object_or_404(Notice, id=notice_id)
    context = {
        'notice': notice
    }
    return render(request, 'notice_detail.html', context)