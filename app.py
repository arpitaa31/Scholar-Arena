from flask import Flask, render_template, request, redirect, url_for, session
from database import db, User
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config['SECRET_KEY'] = 'scholar-arena-secret'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create tables automatically
with app.app_context():
    db.create_all()


# ---------------- HOME ----------------
@app.route("/")
def index():
    return render_template("index.html")


# ---------------- SIGNUP ----------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])

        # create user
        new_user = User(
            username=username,
            email=email,
            password=password,
            xp=0,
            level="Beginner"
        )

        db.session.add(new_user)
        db.session.commit()

        # auto-login (optional but nice UX)
        session["user_id"] = new_user.id

        return redirect("/dashboard")

    return render_template("signup.html")


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

                    
        if user and check_password_hash(user.password, password):
             session["user_id"] = user.id
             return redirect("/dashboard")

        return "Invalid credentials"

    return render_template("login.html")


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect("/")


# ---------------- VIEW DATABASE (VERY IMPORTANT) ----------------
@app.route("/users")
def users():
    all_users = User.query.all()

    if len(all_users) == 0:
        return "<h1>No users found!</h1>"

    output = ""

    for user in all_users:
        output += f"""
        <h2>{user.username}</h2>
        Email: {user.email}<br>
        XP: {user.xp}<br>
        Level: {user.level}<hr>
        """

    return output

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(session["user_id"])

    return render_template("dashboard.html", user=user)

if __name__ == "__main__":
    app.run(debug=True)