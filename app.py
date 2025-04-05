from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'supersecretmre'


@app.route('/')
def index():
    flash('Welcome to the Flask App', 'info')
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/form', methods=['GET','POST'])
def forminput():
    return render_template('form.html')

@app.route('/results', methods=['GET','POST'])
def result():
    return render_template('results.html')

@app.route("/register",methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # Here you would typically save the user to a database
        flash(f"User {username} registered successfully!", "success")
        return redirect(url_for("index"))
    return render_template("register.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/home")
def home():
    return render_template("home.html")
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

    