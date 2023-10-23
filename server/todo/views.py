from django.shortcuts import render, redirect
from .models import TodoModel

# Create your views here.


def TodosView(request):
    todos = TodoModel.objects.all().order_by('-status', '-date_created')

    if request.method == 'POST' and 'submit_todo' in request.POST:
        addTodo = TodoModel()
        addTodo.title = request.POST.get('Title')
        addTodo.todo = request.POST.get('todo')
        dueDate = request.POST.get('dueDate')
        if dueDate:
            addTodo.dueDate = dueDate
        addTodo.save()
        return redirect('todos')

    if request.method == 'POST' and 'edit_todo' in request.POST:
        todoID = request.POST.get('todoID')
        editTodo = TodoModel.objects.get(id=todoID)
        editTodo.title = request.POST.get('Title')
        editTodo.todo = request.POST.get('todo')
        dueDate = request.POST.get('dueDate')
        if dueDate:
            editTodo.dueDate = dueDate
        editTodo.save()
        return redirect('todos')

    if request.method == 'POST' and 'complete_todo' in request.POST:
        todoID = request.POST.get('todoID')
        complete_todo = TodoModel.objects.get(id=todoID)
        complete_todo.status = 'Complete'
        complete_todo.save()
        return redirect('todos')

    if request.method == 'POST' and 'delete_todo' in request.POST:
        todoID = request.POST.get('todoID')
        delete_todo = TodoModel.objects.get(id=todoID)
        delete_todo.delete()
        return redirect('todos')

    context = {
        "todos": todos
    }

    return render(request, 'todo/todos.html', context)
