from flask import Flask, request, redirect, render_template
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader
(template_dir), autoescape = True)

app = Flask(__name__)
app.config['DEBUG'] = True



@app.route("/")
def index():
    
    return render_template("signup.html")


def is_filled(val):
    if val != "":
        return True
    else:
        return False

def some_whitespace(val):
    whitespace = " "
    if whitespace not in val:
        return True
    else:
        return False

def email_validation(val):
    if val.count('@') == 1 and val.count('.') == 1:
        return True
    else:
        return False


@app.route("/validate-user", methods=['POST'])
def validate_user():
    user = request.form["user"]
    passwrd = request.form["passwrd"]
    verify = request.form["verify"]
    email = request.form["email"]

    user_error = ""
    passwrd_error = ""
    verify_error = ""
    email_error = ""

    user_len = len(user)
    password_len = len(passwrd)
    email_len = len(email)
    
    if not is_filled(user):
        user_error = "That's not a valid username"
        user = " "
    else:
        if user_len > 20 or user_len < 3:
            user_error = "username must be between 3 and 20 characters"
            user = " "
        else:
            if not some_whitespace(user):
                user_error = "No spaces allowed"
                user = " "

    if not is_filled(passwrd):
        passwrd_error = "That's not a valid password"
        passwrd = " "
    else:
        if password_len > 20 or password_len < 3:
            passwrd_error = "password must be between 3 and 20 characters"
            passwrd = " "
        else:
            if not some_whitespace(passwrd):
                passwrd_error = "No spaces allowed"
                passwrd = " "

    if not is_filled(verify):
        verify_error = "This field cannot be empty"
        verify = " "
    else:
        if verify != passwrd:
            verify_error = "Passwords must match"
            verify = " "
    
    if is_filled(email):
        if email_len > 20 or email_len < 3:
            email_error = "Email must be between 3 and 20 characters"
            email = " "
        else:
            if not email_validation(email):
                email_error = "Not a valid email"
                email = " "

    if not user_error and not passwrd_error and not verify_error and not email_error:
        user = user
        return redirect ("/welcome?user={0}".format(user))
        
    else:
        return render_template("signup.html", user=user, email=email, user_error=user_error, passwrd_error=passwrd_error,
        verify_error=verify_error, email_error=email_error)


@app.route("/welcome")
def welcome():
    user = request.args.get("user")
    return render_template("welcome.html", user=user)



app.run()

