from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "secret123"

users = {}
votes = {"A":0,"B":0,"C":0}
voted = set()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        users[request.form['username']] = request.form['password']
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']
        if u in users and users[u] == p:
            session['user'] = u
            return redirect('/vote')
    return render_template('login.html')

@app.route('/vote', methods=['GET','POST'])
def vote():
    if 'user' not in session:
        return redirect('/login')

    if session['user'] in voted:
        return redirect('/result')

    if request.method == 'POST':
        choice = request.form.get('candidate')
        if not choice:
            return redirect('/vote')
        votes[choice] += 1
        voted.add(session['user'])
        return redirect('/result')

    return render_template('vote.html', candidates=votes)

@app.route('/result')
def result():
    total = sum(votes.values())
    return render_template('result.html', votes=votes, total=total)

@app.route('/admin')
def admin():
    return render_template('admin.html', votes=votes, users=users)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
