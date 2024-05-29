import flask
from flask import Flask, render_template, request, session, redirect, url_for, flash, Response
import db

app = Flask(__name__)
app.config["SECRET_KEY"] = "uuuunnnnnnhh"

# 主页面
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/index_user")
def index_user():
    return render_template("index_user.html")


@app.route("/index_merchant")
def index_merchant():
    return render_template("index_merchant.html")


@app.route("/index_admin")
def index_admin():
    return render_template("index_admin.html")


# 登陆
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        student_number = request.form.get("user_name")
        password = request.form.get("password")
        button = request.form.get("button")  # 获取用户点击的按钮标识符
        user = db.check_user_login(student_number, password)
        mer = db.check_merchant_login(student_number, password)
        admin = db.check_admin_login(student_number, password)
        if (button == "user" and user != None):
            flask.session["user_name"] = student_number
            login_in_id = user["id"]
            print(login_in_id)
            return flask.redirect(flask.url_for("create_cookie_user", user_id=login_in_id))
        if (button == "merchant" and mer != None):
            flask.session["user_name"] = student_number
            login_in_id = mer["id"]
            print(login_in_id)
            return flask.redirect(flask.url_for("create_cookie_mer", user_id=login_in_id))
        if (button == "admin" and admin != None):
            flask.session["user_name"] = student_number
            login_in_id = admin["id"]
            print(login_in_id)
            return flask.redirect(flask.url_for("create_cookie_admin", user_id=login_in_id))
        flash('用户名或密码不正确,请检查!')
    return render_template(("login.html"))


# 设置用户cookie
@app.route('/create_cookie/user/<user_id>')
def create_cookie_user(user_id):
    resp = Response(render_template("index_user.html"))
    print("cookie set success! user_id=" + user_id)
    resp.set_cookie('user_id', user_id)
    resp.set_cookie('status', 'user')
    return resp


# 设置商家cookie
@app.route('/create_cookie/mer/<user_id>')
def create_cookie_mer(user_id):
    resp = Response(render_template("index_merchant.html"))
    print("cookie set success! user_id=" + user_id)
    resp.set_cookie('user_id', user_id)
    resp.set_cookie('status', 'merchant')
    return resp


# 设置管理员cookie
@app.route('/create_cookie/admin/<user_id>')
def create_cookie_admin(user_id):
    resp = Response(render_template("index_admin.html"))
    print("cookie set success! user_id=" + user_id)
    resp.set_cookie('user_id', user_id)
    resp.set_cookie('status', 'admin')
    return resp


@app.route('/del/')
def del_cookie():
    resp = Response(render_template("index.html"))
    resp.delete_cookie('user_id')
    resp.delete_cookie('status')
    return resp


# 登出
@app.route("/logout")
def logout():
    session.pop("user_name")
    return redirect(url_for("del_cookie"))


# 用户查看账户
@app.route("/user/watch_accountMessage")
def watch_accountMessage():
    status = request.cookies.get('status')
    if status != "user":
        return redirect(url_for("index"))
    if "user_name" not in session:
        return redirect(url_for("index"))
    user_id = request.cookies.get('user_id')
    datas = db.get_user_info(user_id=user_id)
    user = datas[0]
    return render_template("watch_accountMessage.html", user=user)


# 查看订单历史
@app.route("/user/watch_orderHistory")
def watch_orderHistory():
    status = request.cookies.get('status')
    if status != "user":
        return redirect(url_for("index"))
    if "user_name" not in session:
        return redirect(url_for("index"))
    user_id = request.cookies.get('user_id')
    datas = db.get_user_orders(user_id=user_id)
    return render_template("watch_orderHistory.html", datas=datas)


# 查看收藏菜品
@app.route("/user/watch_favouriteDishes")
def watch_favouriteDishes():
    status = request.cookies.get('status')
    if status != "user":
        return redirect(url_for("index"))
    if "user_name" not in session:
        return redirect(url_for("index"))
    user_id = request.cookies.get('user_id')
    datas = db.get_user_favorite_dishes(user_id=user_id)
    return render_template("watch_favouriteDishes.html", datas=datas)


# 消息列表
@app.route("/user/watch_messageBox")
def watch_messageBox():
    status = request.cookies.get('status')
    if status != "user":
        return redirect(url_for("index"))
    if "user_name" not in session:
        return redirect(url_for("index"))
    user_id = request.cookies.get('user_id')
    datas = db.get_user_messages(user_id=user_id)
    return render_template("watch_messageBox.html", datas=datas)


# 搜索商户页面
@app.route("/user/show_search_merchant")
def show_search_merchant():
    status = request.cookies.get('status')
    if status != "user":
        return redirect(url_for("index"))
    if "user_name" not in session:
        return redirect(url_for("index"))
    return render_template("show_search_merchant.html")


# 搜索商户
@app.route("/user/do_search_merchant", methods=["POST"])
def do_search_merchant():
    status = request.cookies.get('status')
    if status != "user":
        return redirect(url_for("index"))
    if "user_name" not in session:
        return redirect(url_for("index"))
    print(request.form)
    name = request.form.get("name")
    datas = db.search_merchants(keyword=name)
    return render_template("do_search_merchant.html", datas=datas)


# 查看商户详细信息
@app.route("/user/watch_merchantDetail/<merchant_id>")
def watch_merchantDetail(merchant_id):
    if "user_name" not in session:
        return redirect(url_for("index"))
    datas = db.get_merchant_info(merchant_id=merchant_id)
    return render_template("watch_merchantDetail.html", merchant=datas[0])


# 查看商户菜品
@app.route("/user/watch_merchant_dishes/<merchant_id>")
def watch_merchant_dishes(merchant_id):
    if "user_name" not in session:
        return redirect(url_for("index"))
    datas = db.get_merchant_foods(merchant_id=merchant_id)
    return render_template("watch_merchant_dishes.html", datas=datas)


# 查看菜品详细信息
@app.route("/user/watch_dishes/<food_id>")
def watch_dishes(food_id):
    if "user_name" not in session:
        return redirect(url_for("index"))
    datas = db.get_food_info(food_id=food_id)
    data = datas[0]
    classificationId = int(data["classificationId"])
    classification = db.get_food_classification_name(classificationId)
    return render_template("watch_dishes.html", food=data, classification=classification)


# 评价商户或菜品
@app.route("/user/add_comment")
def add_comment():
    session.pop("user_name")
    return redirect(url_for("index"))


# 商户查看自己信息
@app.route("/mer/mer_watch_detail")
def mer_watch_detail():
    status = request.cookies.get('status')
    if status != "merchant":
        return redirect(url_for("index"))
    if "user_name" not in session:
        return redirect(url_for("index"))
    user_id = request.cookies.get('user_id')
    datas = db.get_merchant_self_info(merchant_id=user_id)
    return render_template("mer_watch_detail.html", merchant=datas[0])


# 商户查看菜品详细信息
@app.route("/mer/mer_watch_dishes/<food_id>")
def mer_watch_dishes(food_id):
    if "user_name" not in session:
        return redirect(url_for("index"))
    datas = db.get_food_info(food_id=food_id)
    data = datas[0]
    classificationId = int(data["classificationId"])
    classification = db.get_food_classification_name(classificationId)
    return render_template("mer_watch_dishes.html", food=data, classification=classification)


# 商户查看全部菜品并删除菜品
@app.route("/mer/mer_watch_dishes_or_delete")
def mer_watch_dishes_or_delete():
    status = request.cookies.get('status')
    if status != "merchant":
        return redirect(url_for("index"))
    if "user_name" not in session:
        return redirect(url_for("index"))
    user_id = request.cookies.get('user_id')
    datas = db.get_merchant_foods(merchant_id=user_id)
    return render_template("mer_watch_dishes_or_delete.html", datas=datas)


# 商户删除菜品
@app.route("/mer/mer_do_dishes_or_delete/<food_id>")
def mer_do_dishes_or_delete(food_id):
    status = request.cookies.get('status')
    if status != "merchant":
        return redirect(url_for("index"))
    if "user_name" not in session:
        return redirect(url_for("index"))
    print(request.form)
    datas = db.delete_food(food_id=food_id)
    result = datas["success"]
    print("success" + str(result))
    if result != None:
        return render_template("mer_do_dishes_or_delete.html", result=result)


# 商户添加菜单
@app.route("/mer/show_mer_add_dishes")
def show_mer_add_dishes():
    status = request.cookies.get('status')
    if status != "merchant":
        return redirect(url_for("index"))
    if "user_name" not in session:
        return redirect(url_for("index"))
    classDatas = db.get_all_foodClassification()
    return render_template("show_mer_add_dishes.html", classDatas=classDatas)


# 商户添加菜单
@app.route("/mer/do_mer_add_dishes", methods=["POST"])
def do_mer_add_dishes():
    status = request.cookies.get('status')
    if status != "merchant":
        return redirect(url_for("index"))
    if "user_name" not in session:
        return redirect(url_for("index"))
    print(request.form)
    merchant_id = request.cookies.get('user_id')
    name = request.form.get("name")
    classification_id = request.form.get("option")
    picture = request.form.get("picture")
    price = request.form.get("price")
    description = request.form.get("description")
    nutrition = request.form.get("nutrition")
    ingredient = request.form.get("ingredient")
    allergy = request.form.get("allergy")
    datas = db.add_food(merchant_id=merchant_id, name=name, classification_id=classification_id, picture=picture,
                        price=price,
                        description=description, nutrition=nutrition, ingredient=ingredient, allergy=allergy)
    return render_template("do_mer_add_dishes.html", datas=datas)

# 管理员管理用户
@app.route("/man/manage_all_users")
def manage_all_users():
    if "user_name" not in session:
        return redirect(url_for("index"))
    return render_template("show_add_user.html")


# 管理员管理商户
@app.route("/man/manage_all_merchant")
def manage_all_merchant():
    if "user_name" not in session:
        return redirect(url_for("index"))
    return render_template("show_add_user.html")


# 管理员管理菜品
@app.route("/man/manage_all_dishes")
def manage_all_dishes():
    if "user_name" not in session:
        return redirect(url_for("index"))
    return render_template("show_add_user.html")


# 增加用户页面
@app.route("/show_add_user")
def show_add_user():
    if "user_name" not in session:
        return redirect(url_for("index"))
    return render_template("show_add_user.html")


# 增加用户操作
@app.route("/do_add_user", methods=["POST"])
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


# 展示用户列表
@app.route("/show_users")
def show_users():
    if "user_name" not in session:
        return redirect(url_for("index"))
    sql = "select id,name from user"
    datas = db.query_data(sql)
    return render_template("show_users.html", datas=datas)


# <tr>...</tr> 定义一行标签，一组行标签内可以建立多组由<td>或<th>标签所定义的单元格
# <th>...</th>定义表头单元格。表格中的文字将以粗体显示
# <td>...</td> 定义单元格标签

# 查看单个用户
@app.route("/show_user/<user_id>")
def show_user(user_id):
    if "user_name" not in session:
        return redirect(url_for("index"))
    sql = "select * from user where id=" + user_id
    datas = db.query_data(sql)
    # print(datas)
    user = datas[0]
    # print(user)
    return render_template("show_user.html", user=user)


if __name__ == '__main__':
    app.run()
