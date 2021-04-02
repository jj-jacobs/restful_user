from flask import Flask, render_template, request, redirect
from my_sql_connect import connectToMySQL
app = Flask(__name__)

# http://localhost:5000/users/new

@app.route('/users/new')
def new():
    db = connectToMySQL("friends_thingy")
    users = db.query_db('SELECT * FROM users;')
    return render_template("create_user.html", all_users = users)

@app.route('/users/create', methods = ["POST"])
def create_user():
    query = "INSERT INTO users (first_name, last_name, email, created_at, updated_at) VALUES (%(fn)s, %(ln)s, %(em)s, NOW(), NOW());"
    data = {
        'fn' : request.form["first_name"],
        'ln' : request.form["last_name"],
        'em' : request.form["email"]
    }
    db = connectToMySQL("friends_thingy")
    user_id = db.query_db(query, data)
    return redirect(f'/users/{user_id}')

@app.route('/users/<id>')
def user_id_show(id):
    db = connectToMySQL("friends_thingy")
    user_info = db.query_db(f'SELECT * FROM users where id = {id};')
    print(user_info)
    return render_template("show_user.html", user = user_info[0])

@app.route('/users')
def show_all_users():
    db = connectToMySQL("friends_thingy")
    user_profile = db.query_db('SELECT * FROM users as people;')
    return render_template("show_all_users.html", user_prof = user_profile)

@app.route('/users/<id>/edit')
def edit_user(id):
    db = connectToMySQL("friends_thingy")
    user_info = db.query_db(f'SELECT * FROM users where id = {id};')
    return render_template("edit_user.html")

@app.route('/users/<id>/update', methods = ["POST"])
def update(id): 
    db = connectToMySQL("friends_thingy")
    user_id = db.query_db(f'UPDATE users SET first_name = {request.form["first_name"]}, last_name = {request.form["last_name"]}, email = {request.form["email"]} where id = {id};')
    return redirect(f'/users/{user_id}')

@app.route('/users/<id>/delete')
def delete(id):
    db = connectToMySQL("friends_thingy")
    delete_info = db.query_db(f'DELETE FROM users where id = {id};')
    return redirect("/users")


if __name__ == "__main__":
    app.run(debug=True)