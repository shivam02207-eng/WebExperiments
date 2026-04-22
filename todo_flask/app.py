from flask import Flask, render_template, request, jsonify, abort
from datetime import datetime

app = Flask(__name__)

tasks = []

next_id = 1
# Home Page
@app.route('/')
def index():
    return render_template('index.html')

# Get all tasks
@app.route('/api/tasks')
def get_tasks():
    status = request.args.get('status')
    if status == 'active':
        return jsonify([t for t in tasks if not t['completed']])
    elif status == 'completed':
        return jsonify([t for t in tasks if t['completed']])
    return jsonify(tasks)

# Add task
@app.route('/api/tasks', methods=['POST'])
def add_task():
    global next_id
    data = request.json

    if not data.get('title'):
        abort(400)

    task = {
        "id": next_id,
        "title": data['title'],
        "description": data.get('description', ''),
        "priority": data.get('priority', 'medium'),
        "completed": False,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    tasks.append(task)
    next_id += 1
    return jsonify(task), 201

# Update task
@app.route('/api/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    data = request.json
    for task in tasks:
        if task['id'] == id:
            task.update(data)
            return jsonify(task)
    abort(404)

# Toggle task
@app.route('/api/tasks/<int:id>/toggle', methods=['PATCH'])
def toggle_task(id):
    for task in tasks:
        if task['id'] == id:
            task['completed'] = not task['completed']
            return jsonify(task)
    abort(404)

# Delete task
@app.route('/api/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    global tasks
    tasks = [t for t in tasks if t['id'] != id]
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
