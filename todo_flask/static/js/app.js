document.addEventListener("DOMContentLoaded", loadTasks);

async function loadTasks(url='/api/tasks') {
    const res = await fetch(url);
    const tasks = await res.json();

    renderTasks(tasks);
    updateCounter(tasks);
}

function renderTasks(tasks) {
    const list = document.getElementById("task-list");
    list.innerHTML = "";

    if(tasks.length === 0){
        list.innerHTML = "<p>No tasks yet 🚀</p>";
        return;
    }

    tasks.forEach(t => {
        list.innerHTML += `
        <div class="task ${t.completed ? 'done' : ''}">
            <div>
                <input type="checkbox" ${t.completed ? 'checked' : ''} 
                onclick="toggleTask(${t.id})">

                <span>${t.title}</span>
                <small>${t.description}</small>
            </div>

            <div>
                <span class="badge ${t.priority}">${t.priority}</span>
                <button onclick="deleteTask(${t.id})">❌</button>
            </div>
        </div>`;
    });
}

async function addTask() {
    const title = document.getElementById("title").value;
    const desc = document.getElementById("desc").value;
    const priority = document.getElementById("priority").value;

    if (!title) {
        alert("Title required!");
        return;
    }

    await fetch('/api/tasks', {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({title, description: desc, priority})
    });

    loadTasks();
}

async function deleteTask(id) {
    await fetch(`/api/tasks/${id}`, {method: "DELETE"});
    loadTasks();
}

async function toggleTask(id) {
    await fetch(`/api/tasks/${id}/toggle`, {method: "PATCH"});
    loadTasks();
}

function filterTasks(type){
    loadTasks(`/api/tasks?status=${type}`);
}

function updateCounter(tasks){
    let total = tasks.length;
    let completed = tasks.filter(t=>t.completed).length;
    let active = total - completed;

    document.getElementById("counter").innerHTML =
        `Total: ${total} | Active: ${active} | Completed: ${completed}`;
}
