from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = os.urandom(24) 

def get_tasks():
    if 'tasks' not in session:
        session['tasks'] = []
    return session['tasks']

def save_tasks(tasks):
    session['tasks'] = tasks

@app.route('/')
def index():
    filter_type = request.args.get('filter', 'all')
    tasks = get_tasks()

    total_task_count = len(tasks)
    active_task_count = len([task for task in tasks if not task['completed']])
    completed_task_count = len([task for task in tasks if task['completed']])

    if filter_type == 'completed':
        filtered_tasks = [task for task in tasks if task['completed']]
        task_count = completed_task_count
    elif filter_type == 'active':
        filtered_tasks = [task for task in tasks if not task['completed']]
        task_count = active_task_count
    else:
        filtered_tasks = tasks
        task_count = total_task_count

    return render_template('index.html', tasks=filtered_tasks, task_count=task_count, 
                           total_task_count=total_task_count, active_task_count=active_task_count,
                           completed_task_count=completed_task_count, filter_type=filter_type)


@app.route('/add', methods=['POST'])
def add_task():
    new_task = request.form.get('newTask')
    if new_task:
        tasks = get_tasks()
        tasks.append({'name': new_task, 'completed': False})
        save_tasks(tasks)
    return redirect(url_for('index'))

@app.route('/toggle/<int:task_index>', methods=['POST'])
def toggle_task(task_index):
    tasks = get_tasks()
    if 0 <= task_index < len(tasks):
        tasks[task_index]['completed'] = not tasks[task_index]['completed']
        save_tasks(tasks)
    return redirect(url_for('index'))

@app.route('/delete_task/<int:task_index>', methods=['POST'])
def delete_task(task_index):
    tasks = get_tasks()
    if 0 <= task_index < len(tasks):
        tasks.pop(task_index)
        save_tasks(tasks)
    return redirect(url_for('index'))

def delete_completed_tasks():
    global tasks
    tasks = [task for task in tasks if not task['completed']]

@app.route('/clear_completed', methods=['GET'])
def clear_completed():
    tasks = get_tasks()
    tasks = [task for task in tasks if not task['completed']]
    save_tasks(tasks)
    return redirect(url_for('index', filter=request.args.get('filter', 'all')))

if __name__ == '__main__':
    app.run(debug=True)