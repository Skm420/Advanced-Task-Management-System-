from flask import Flask, render_template, request, redirect, url_for
import datetime

app = Flask(__name__)

def write_user_information(username, password, name, address, age):
    user_info_file = f"{username}_info.txt"
    with open(user_info_file, 'w') as f:
        f.write(f"Password: {password}\n")
        f.write(f"Name: {name}\n")
        f.write(f"Address: {address}\n")
        f.write(f"Age: {age}\n")

def read_user_information(username):
    user_info_file = f"{username}_info.txt"
    try:
        with open(user_info_file, 'r') as f:
            return f.readlines()
    except FileNotFoundError:
        return []

def write_task_information(username, tasks):
    task_file = f"{username}_tasks.txt"
    with open(task_file, 'a') as f:
        f.writelines(tasks)

def write_task_update(username, completed_task, ongoing_task, not_started_task):
    task_update_file = f"{username}_task_update.txt"
    with open(task_update_file, 'a') as f:
        f.write(f"{datetime.datetime.now()}\n")
        f.write("COMPLETED TASK\n")
        f.write(f"{completed_task}\n")
        f.write("ONGOING TASK\n")
        f.write(f"{ongoing_task}\n")
        f.write("NOT YET STARTED\n")
        f.write(f"{not_started_task}\n")

def process_signup_form():
    name = request.form['name']
    password = request.form['password']
    email_phone = request.form['email_phone']
    write_user_information(name, password, name, email_phone)
    return redirect(url_for('task_manager', username=name, message="Successfully signed up!"))

	
def process_login_form():
    username = request.form['username']
    password = request.form['password'] + '\n'
    stored_password = read_user_information(username)
    
    if stored_password and password == stored_password[0]:
        return render_template('task_manager.html', username=username)
    else:
        return render_template('login.html', message="Incorrect username or password")

def process_create_task_form():
    username = request.form['username']
    num_tasks = int(request.form['num_tasks'])
    
    tasks = []
    for i in range(1, num_tasks + 1):
        task_name = request.form[f'task_name_{i}']
        target_time = request.form[f'target_time_{i}']
        tasks.append(f"TASK {i}: {task_name}\nTARGET {i}: {target_time}\n")
    
    write_task_information(username, tasks)
    return render_template('task_manager.html', username=username, message="Tasks created successfully!")

def process_update_task_form():
    username = request.form['username']
    completed_task = request.form['completed_task']
    ongoing_task = request.form['ongoing_task']
    not_started_task = request.form['not_started_task']
    
    write_task_update(username, completed_task, ongoing_task, not_started_task)
    return render_template('task_manager.html', username=username, message="Task updates recorded!")

@app.route('/')
def home():
    return render_template('all_functions.html')

@app.route('/all_functions', methods=['GET', 'POST'])
def all_functions():
    if request.method == 'POST':
        if 'signup' in request.form:
            return process_signup_form()
        elif 'login' in request.form:
            return process_login_form()
        elif 'create_task' in request.form:
            return process_create_task_form()
        elif 'update_task' in request.form:
            return process_update_task_form()

    return render_template('all_functions.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup_page():
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    return render_template('login.html')

@app.route('/create_task', methods=['GET', 'POST'])
def create_task_page():
    return render_template('create_task.html')

@app.route('/update_task', methods=['GET', 'POST'])
def update_task_page():
    return render_template('update_task.html')
	
@app.route('/task_manager/<username>', methods=['GET', 'POST'])
def task_manager(username):
    return render_template('task_manager.html', username=username)

if __name__ == '__main__':
    app.run(debug=True)
