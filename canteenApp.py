import flask
from flask import Flask, render_template, request, session, redirect, url_for
import db
app = Flask(__name__)
app.config["SECRET_KEY"] = "uuuunnnnnnhh"
# 主页面
@app.route("/")
def index():
    return render_template("index.html")

# 登陆
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user_name = request.form.get("user_name")
        password = request.form.get("password")
        button = request.form.get("button")  # 获取用户点击的按钮标识符
        if (button == "user" and user_name == "wht" and password == "8") or (button == "admin" and user_name == "abc" and password == "6"):
            flask.session["user_name"] = user_name
            return flask.redirect(flask.url_for("index"))

    return render_template(("login.html"))

# 登陆
@app.route("/login_user", methods=["POST", "GET"])
def login_user():
    if request.method == "POST":
        user_name = request.form.get("user_name")
        password = request.form.get("password")
        button = request.form.get()
        if (user_name == "wht" and password == "8") or (user_name == "abc" and password == "6"):
            flask.session["user_name"] = user_name
            return flask.redirect(flask.url_for("index"))

    return render_template(("login.html"))

@app.route("/login_merchant", methods=["POST", "GET"])
def login_merchant():
    if request.method == "POST":
        user_name = request.form.get("user_name")
        password = request.form.get("password")
        button = request.form.get()
        if (user_name == "wht" and password == "8") or (user_name == "abc" and password == "6"):
            flask.session["user_name"] = user_name
            return flask.redirect(flask.url_for("index"))

    return render_template(("login.html"))

@app.route("/login_admin", methods=["POST", "GET"])
def login_admin():
    if request.method == "POST":
        user_name = request.form.get("user_name")
        password = request.form.get("password")
        button = request.form.get()
        if (user_name == "wht" and password == "8") or (user_name == "abc" and password == "6"):
            flask.session["user_name"] = user_name
            return flask.redirect(flask.url_for("index"))

    return render_template(("login.html"))

# 选择登陆身份
@app.route("/login_choose")
def login_choose():
    return render_template(("login_choose.html"))




# 登出
@app.route("/logout")
def logout():
    session.pop("user_name")
    return redirect(url_for("index"))

#增加用户页面
@app.route("/show_add_user")
def show_add_user():
    if "user_name" not in session:
        return redirect(url_for("index"))
    return render_template("show_add_user.html")

#增加用户操作
@app.route("/do_add_user",methods = ["POST"])
def do_add_user():
    if "user_name" not in session:
        return redirect(url_for("index"))
    print(request.form)
    name = request.form.get("name")
    sex = request.form.get("sex")
    age = request.form.get("age")
    email = request.form.get("email")
    sql = f"""
        insert into user(name,sex,age,email) 
        values ('{name}','{sex}',{age},'{email}')
    """
    print(sql)
    db.insert_or_update_data(sql)
    return "success"

#展示用户列表
@app.route("/show_users")
def show_users():
    if "user_name" not in session:
        return redirect(url_for("index"))
    sql = "select id,name from user"
    datas = db.query_data(sql)
    return render_template("show_users.html",datas = datas)

#<tr>...</tr> 定义一行标签，一组行标签内可以建立多组由<td>或<th>标签所定义的单元格
#<th>...</th>定义表头单元格。表格中的文字将以粗体显示
#<td>...</td> 定义单元格标签

# 查看单个用户
@app.route("/show_user/<user_id>")
def show_user(user_id):
    if "user_name" not in session:
        return redirect(url_for("index"))
    sql ="select * from user where id=" +user_id
    datas = db.query_data(sql)
    # print(datas)
    user = datas[0]
    # print(user)
    return render_template("show_user.html",user=user)




if __name__ == '__main__':
    app.run()