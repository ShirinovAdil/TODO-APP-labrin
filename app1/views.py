from django.shortcuts import render
from .models import Task, Comment
#from .tasks import test_task
from .forms import AddNewTaskForm, ShareTask
from django.utils import timezone
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import LeaveComment


def homepage(request):
    todo_tasks = Task.objects.filter(by_who__exact=request.user)
    shared_todo_tasks = Task.objects.filter(viewable_by__username__exact=request.user)
    shared_todo_tasks_to_edit = Task.objects.filter(editable_by__username__exact=request.user)
    return render(request, 'app1/homepage.html', {'todo_tasks': todo_tasks,
                                                  'shared_todo_tasks': shared_todo_tasks,
                                                  'shared_todo_tasks_to_edit': shared_todo_tasks_to_edit})


@login_required(login_url="login")
def add_task(request):
    if request.method == "POST":
        form = AddNewTaskForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.by_who = request.user
            form.created_date = timezone.now()
            form.save()
            return redirect('homepage')
        else:
            form = AddNewTaskForm()
            return render(request, 'app1/add-task.html', {'form': form})
    else:
        form = AddNewTaskForm()
        return render(request, 'app1/add-task.html',  {'form': form})


@login_required(login_url="login")
def share_task(request, pk=None):
    """Share the task by its ID with other user by username"""
    if request.method == "POST":
        form = ShareTask(request.POST)
        if form.is_valid():
            username_to_share = form.cleaned_data['share_with']
            if User.objects.filter(username__exact=username_to_share):
                task = Task.objects.get(pk=pk)
                if form.cleaned_data['editable'] is True:
                    task.viewable_by.add(User.objects.get(username__exact=username_to_share))
                    task.editable_by.add(User.objects.get(username__exact=username_to_share))
                    return redirect('homepage')
                else:
                    task.viewable_by.add(User.objects.get(username__exact=username_to_share))
                    return redirect('homepage')
            else:
                form = ShareTask()
                return render(request, 'app1/share-task.html', {'form': form, 'error': "User doesnt exist"})
        return render(request, 'app1/share-task.html', {'form': form})
    else:
        form = ShareTask()
        return render(request, 'app1/share-task.html', {'form': form})


@login_required(login_url="login")
def edit_task(request, pk=None):
    """Edit task with id of pk"""
    task = get_object_or_404(Task, pk=pk)
    if str(request.user) == task.by_who:
        if request.method == "POST":
            form = AddNewTaskForm(request.POST, instance=task)
            if form.is_valid():
                form = form.save(commit=False)
                form.by_who = str(request.user)
                form.created_date = timezone.now()
                form.save()
                return redirect('homepage')
            else:
                form = AddNewTaskForm(instance=task)
                return render(request, 'app1/edit-task.html', {'form': form})
        else:
            form = AddNewTaskForm(instance=task)
            return render(request, 'app1/edit-task.html', {'form': form})
    else:
        return redirect('homepage')


@login_required(login_url='login')
def view_task(request, pk=None):
    """View task as a card, detailed form with comment section"""
    if request.method == "POST":
        form = LeaveComment(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.comment_sender = str(request.user)
            form.comment_date = timezone.now()
            form.comment_related_task = Task.objects.get(pk=pk)
            form.save()
            return redirect('view_task', pk=pk)
        else:
            form = LeaveComment()
            return render(request, 'app1/view-task.html', {'form': form})
    else:
        task = Task.objects.get(pk=pk)
        comments = Comment.objects.filter(comment_related_task_id=pk)
        form = LeaveComment()
        context = {
            'task': task,
            'comments': comments,
            'leave_comment_form': form
        }
    return render(request, 'app1/view-task.html', context)