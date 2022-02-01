from flask import render_template, redirect, request, session, flash
from users_cr_app import app
from users_cr_app.models.users_model import User

@app.route('/', methods=["GET"])
def home():
    return redirect('/users')

@app.route('/users', methods=["GET", "POST"])
def usersListDisplay():
    usersList = User.getUsers()
    return render_template("read.html", users=usersList)

@app.route('/user/new', methods=["GET"])
def newUserForm():
    return render_template("create.html")

@app.route('/user/add', methods=["POST"])
def addUserNew():
    newUser = {
        "first_name" : request.form["firstname"],
        "last_name" : request.form["lastname"],
        "email" : request.form["email"]
    }
    result = User.addUser(newUser)
    if type(result) is int:
        return redirect('/user/show/' + str(result))
    else:
        flash("There was a problem registering the new user, please try again", "addusernew")
        return redirect('/user/new')

@app.route('/user/show/<id>', methods=["GET", "POST"])
def showUser(id):
    id = int(id)
    if request.method == "GET":
        userInfo = session["userInfo"]
        if userInfo["id"] != id:
            user = {
                "id" : id
            }
            userInfo = User.getUser(user)
        userInfo["created_at"] = userInfo["created_at"].strftime("%B %d, %Y")
        userInfo["updated_at"] = userInfo["updated_at"].strftime("%B %d, %Y") + " at " + userInfo["updated_at"].strftime("%-I:%-M %p")
        return render_template("user.html", user=userInfo)
    elif request.method == "POST":
        user = {
            "id" : id
        }
        userInfo = User.getUser(user)
        # print("Esto es lo que viene de la base de datos:", userInfo)
        # print("Su tipo es:", type(userInfo))
        session["userInfo"] = userInfo        
        return redirect('/user/show/' + str(id))

@app.route('/user/edit/<id>', methods=["GET", "POST"])
def editUser(id):
    id = int(id)
    if request.method == "GET":
        userInfo = session["userInfo"]
        if userInfo["id"] != id:
            user = {
                "id" : id
            }
            userInfo = User.getUser(user)
        return render_template("edit.html", user=userInfo)
    elif request.method == "POST":
        user = {
            "id" : id,
            "first_name" : request.form["firstname"],
            "last_name" : request.form["lastname"],
            "email" : request.form["email"]
        }
        userInfo = User.updateUser(user)
        return redirect('/user/show/' + str(id))

@app.route('/user/delete/<id>', methods=["POST"])
def deleteUser(id):
    id = int(id)
    user = {
        "id" : id
    }
    userInfo = User.removeUser(user)
    return redirect("/users")