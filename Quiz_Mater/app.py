from flask import Flask, render_template, request

app = Flask(__name__)

# Quiz Questions
quiz = [
    {
        "question": "What is the capital of India?",
        "options": ["Delhi", "Mumbai", "Chennai", "Kolkata"],
        "answer": "Delhi"
    },
    {
        "question": "Which language is used for web apps?",
        "options": ["Python", "JavaScript", "HTML", "All"],
        "answer": "All"
    },
    {
        "question": "2 + 2 = ?",
        "options": ["3", "4", "5", "6"],
        "answer": "4"
    },
    {
        "question": "Which is backend language?",
        "options": ["HTML", "CSS", "Python", "Bootstrap"],
        "answer": "Python"
    },
    {
        "question": "Flask is written in?",
        "options": ["Java", "Python", "C++", "PHP"],
        "answer": "Python"
    }
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/quiz')
def quiz_page():
    return render_template('quiz.html', quiz=quiz)

@app.route('/result', methods=['POST'])
def result():
    score = 0

    for i in range(len(quiz)):
        selected = request.form.get(f"q{i}")
        if selected == quiz[i]["answer"]:
            score += 1

    return render_template('result.html', score=score, total=len(quiz))

if __name__ == '__main__':
    app.run(debug=True)
