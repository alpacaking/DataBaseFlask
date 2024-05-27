#引入模块
from flask import Flask, render_template,request
import json
import requests
import db
import datetime
import os
import flask
import xlwt

#初始化flask对象
app = Flask(__name__)

@app.route('/')  # 路由，指定访问的url路径
def hello_world():
    return 'Hello World!'

#可以添加多个路由
@app.route("/hello")
def hello_world2():
    data = "hello xingshi "  # 给html文件中输入数据
    return render_template("hello.html", data=data) #调用HTML模板


@app.route("/user/<username>", methods=["POST"])  # < >用于传递参数，methods设置访问方法
def get_user(username):
    return f"hello {username}"

# 获取数据 比如：http://127.0.0.1:5000/data?a=233&b=345
# @app.route('/data', methods=["POST", "GET"])
# def test_data():
#     print(request.args)  # 接收url后面有问号的形式
#     print(request.args.get("a"), request.args.get("b"))
#     return "success"

# http://127.0.0.1:5000/static/form_test.html
@app.route('/data', methods=["POST", "GET"])
def test_data():
    print(request.form)  # 获取表单
    print(request.form.get("username"), request.form.get("password"))
    return "success"

# request对象并返回
# http://127.0.0.1:5000/static/form_test.html
@app.route('/index', methods=["POST", "GET"])
def index():
    if request.method =='GET':
        return render_template('form_test.html')
    if request.method == 'POST':
        username=request.form.get('username')
        password=request.form.get('password')
        print(username,password)
        return "this is post"

# 使用模板展示数据
@app.route("/use_template")
def use_template():
    datas = [(1, "name1"), (2, "name2"), (3, "name3")]
    title = "学生信息"
    return render_template("use_template.html", datas=datas, title=title)

# 读取文件数据并返回网页表格
def read_pvuv_data():
    # 读取文件
    data = []
    with open("./static/shili") as f:
        next(f)
        for line in f:
            line = line[:-1]
            bio1, bio2, bio3 = line.split(" ")
            data.append((bio1, bio2, bio3))
    return data

@app.route("/pvuv")
def pvuv():
    # 读取文件
    data = read_pvuv_data()
    #返回html:
    return render_template("pvuv.html",data = data)





@app.route("/show_add_user")
def show_add_user():
    return render_template("show_add_user.html")

@app.route("/do_add_user",methods = ["POST"])
def do_add_user():
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
    sql = "select id,name from user"
    datas = db.query_data(sql)
    return render_template("show_users.html",datas = datas)

#<tr>...</tr> 定义一行标签，一组行标签内可以建立多组由<td>或<th>标签所定义的单元格
#<th>...</th>定义表头单元格。表格中的文字将以粗体显示
#<td>...</td> 定义单元格标签

@app.route("/show_user/<user_id>")
def show_user(user_id):
    sql ="select * from user where id=" +user_id
    datas = db.query_data(sql)
    # print(datas)
    user = datas[0]
    # print(user)
    return render_template("show_user.html",user=user)




#运行
if __name__ == '__main__':
    app.run()

