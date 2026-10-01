from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from .forms import StudentForm



def student_list(request):
    students = Student.objects.all().order_by('-id')

    search = request.GET.get('search')

    if search:
        students = students.filter(
            name__icontains=search
        ) | students.filter(
            email__icontains=search
        ) | students.filter(
            course__icontains=search
        )

    context = {
        'students': students,
        'search': search or '',
    }

    return render(request, 'students/student_list.html', context)


def student_detail(request, id):
    student = get_object_or_404(Student, id=id)

    return render(
        request,
        'students/student_detail.html',
        {'student': student}
    )


def student_create(request):

    if request.method == 'POST':
        form = StudentForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('student_list')

    else:
        form = StudentForm()

    return render(
        request,
        'students/student_form.html',
        {
            'form': form,
            'title': 'Add Student',
            'button': 'Save Student',
        }
    )


def student_update(request, id):

    student = get_object_or_404(Student, id=id)

    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)

        if form.is_valid():
            form.save()
            return redirect('student_list')

    else:
        form = StudentForm(instance=student)

    return render(
        request,
        'students/student_form.html',
        {
            'form': form,
            'title': 'Edit Student',
            'button': 'Update Student',
        }
    )


def student_delete(request, id):

    student = get_object_or_404(Student, id=id)

    if request.method == 'POST':
        student.delete()
        return redirect('student_list')

    return render(
        request,
        'students/student_confirm_delete.html',
        {'student': student}
    )