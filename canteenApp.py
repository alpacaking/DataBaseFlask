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

# 查看活跃度
@app.route("/user/watch_activity")
def watch_activity():
    status = request.cookies.get('status')
    if status != "user":
        return redirect(url_for("index"))
    if "user_name" not in session:
        return redirect(url_for("index"))
    user_id = request.cookies.get('user_id')
    datas = db.analyze_user_activity(user_id=user_id)
    return render_template("watch_activity.html", datas=datas)

# 查看订单详情
@app.route("/user/watch_order/<order_id>")
def watch_order(order_id):
    status = request.cookies.get('status')
    if status != "user":
        return redirect(url_for("index"))
    if "user_name" not in session:
        return redirect(url_for("index"))
    userorder = db.get_userorder_info(Entity_id=order_id)
    havedonefood=db.check_user_rating_food(order_id=order_id)
    havedonemer=db.check_user_rating_merchant(order_id=order_id)
    print(userorder)
    return render_template("watch_order.html", userorder=userorder[0],havedonefood=havedonefood,havedonemer=havedonemer)

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


# 选择时间段,收藏的各个菜品在一段时间内的销量
@app.route("/user/show_user_count_sales")
def show_user_count_sales():
    status = request.cookies.get('status')
    if status != "user":
        return redirect(url_for("index"))
    if "user_name" not in session:
        return redirect(url_for("index"))
    return render_template("show_user_count_sales.html")


# 选择时间段
@app.route("/user/do_user_count_sales", methods=["POST"])
def do_user_count_sales():
    status = request.cookies.get('status')
    if status != "user":
        return redirect(url_for("index"))
    if "user_name" not in session:
        return redirect(url_for("index"))
    print(request.form)
    start_date = request.form.get("start_date")
    end_date = request.form.get("end_date")
    user_id = request.cookies.get('user_id')
    datas = db.analyze_favorite_food_sales(user_id=user_id, start_date=start_date, end_date=end_date)
    return render_template("do_user_count_sales.html", datas=datas)


# 收藏菜
@app.route("/user/do_like_dishes/<food_id>")
def do_like_dishes(food_id):
    status = request.cookies.get('status')
    if status != "user":
        return redirect(url_for("index"))
    if "user_name" not in session:
        return redirect(url_for("index"))
    user_id = request.cookies.get('user_id')
    datas = db.favorite_food(user_id, food_id)
    return render_template("do_order_dishes.html", datas=datas["success"])


# 收藏商家
@app.route("/user/do_like_mer/<mer_id>")
def do_like_mer(mer_id):
    status = request.cookies.get('status')
    if status != "user":
        return redirect(url_for("index"))
    if "user_name" not in session:
        return redirect(url_for("index"))
    user_id = request.cookies.get('user_id')
    print(user_id,mer_id)
    datas = db.favorite_merchant(user_id, merchant_id=mer_id)
    return render_template("do_order_dishes.html", datas=datas["success"])


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
    user_id = request.cookies.get('user_id')
    havedonemer=db.check_user_favorite_merchant(user_id, merchantId=merchant_id)
    return render_template("watch_merchantDetail.html", merchant=datas[0],havedonemer=havedonemer)


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
    user_id = request.cookies.get('user_id')
    classification = db.get_food_classification_name(classificationId)
    havedonefood=db.check_user_favorite_food(user_id=user_id, food_id=food_id)
    return render_template("watch_dishes.html", food=data, classification=classification,havedonefood=havedonefood)

# 点餐
@app.route("/user/order_dishes/<food_id>")
def show_order_dishes(food_id):
    status = request.cookies.get('status')
    if status != "user":
        return redirect(url_for("index"))
    if "user_name" not in session:
        return redirect(url_for("index"))
    return render_template("show_order_dishes.html", food_id=food_id)

# 点餐
@app.route("/user/do_order_dishes/<food_id>", methods=["POST"])
def do_order_dishes(food_id):
    status = request.cookies.get('status')
    if status != "user":
        return redirect(url_for("index"))
    if "user_name" not in session:
        return redirect(url_for("index"))
    print(request.form)
    user_id=request.cookies.get('user_id')
    details = request.form.get("detail")
    print(details)
    datas = db.place_order(food_id=food_id,user_id=user_id,details=details,is_paid="是")
    return render_template("do_order_dishes.html", datas=datas["success"])

# 根据订单评价打分菜
@app.route("/user/show_score_dishes/<order_id>")
def show_score_dishes(order_id):
    status = request.cookies.get('status')
    if status != "user":
        return redirect(url_for("index"))
    if "user_name" not in session:
        return redirect(url_for("index"))
    return render_template("show_score_dishes.html", order_id=order_id)

# 根据订单评价打分菜
@app.route("/user/do_score_dishes/<order_id>", methods=["POST"])
def do_score_dishes(order_id):
    status = request.cookies.get('status')
    if status != "user":
        return redirect(url_for("index"))
    if "user_name" not in session:
        return redirect(url_for("index"))
    print(request.form)
    user_id=request.cookies.get('user_id')
    score = request.form.get("score")
    content = request.form.get("content")
    print(score,content)
    print(user_id,order_id)
    datas = db.rate_food(user_id=user_id, order_id=order_id, score=score, content=content)
    return render_template("do_order_dishes.html", datas=datas["success"])


# 根据订单评价打分商户
@app.route("/user/show_score_merchant/<order_id>")
def show_score_merchant(order_id):
    status = request.cookies.get('status')
    if status != "user":
        return redirect(url_for("index"))
    if "user_name" not in session:
        return redirect(url_for("index"))
    return render_template("show_score_merchant.html", order_id=order_id)

# 根据订单评价打分商户
@app.route("/user/do_score_merchant/<order_id>", methods=["POST"])
def do_score_merchant(order_id):
    status = request.cookies.get('status')
    if status != "user":
        return redirect(url_for("index"))
    if "user_name" not in session:
        return redirect(url_for("index"))
    user_id = request.cookies.get('user_id')
    score = request.form.get("score")
    content = request.form.get("content")
    print(score, content)
    datas = db.rate_merchant(user_id, order_id, score, content)
    return render_template("do_order_dishes.html", datas=datas["success"])


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
    ana_datas=db.analyze_food_data(merchant_id=user_id)
    return render_template("mer_watch_detail.html", merchant=datas[0],ana_datas=ana_datas[0])
    # return render_template("mer_watch_detail.html", merchant=datas[0])

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

# 选择时间段,一段时间内某个忠实粉丝在该商户的消费分布
@app.route("/mer/show_mer_count_sales")
def show_mer_count_sales():
    status = request.cookies.get('status')
    if status != "merchant":
        return redirect(url_for("index"))
    if "user_name" not in session:
        return redirect(url_for("index"))
    return render_template("show_mer_count_sales.html")


# 选择时间段
@app.route("/mer/do_mer_count_sales", methods=["POST"])
def do_mer_count_sales():
    status = request.cookies.get('status')
    if status != "merchant":
        return redirect(url_for("index"))
    if "user_name" not in session:
        return redirect(url_for("index"))
    print(request.form)
    start_date = request.form.get("start_date")
    end_date = request.form.get("end_date")
    threshold = request.form.get("threshold")
    user_id = request.cookies.get('user_id')
    datas = db.analyze_merchant_loyal_customers(merchant_id=user_id, start_date=start_date, end_date=end_date,threshold=threshold)
    return render_template("do_mer_count_sales.html", datas=datas)





# 商户查看全部未完成订单
@app.route("/mer/mer_watch_unfinished_orders")
def mer_watch_unfinished_orders():
    status = request.cookies.get('status')
    if status != "merchant":
        return redirect(url_for("index"))
    if "user_name" not in session:
        return redirect(url_for("index"))
    user_id = request.cookies.get('user_id')
    datas = db.get_merchant_pending_orders(merchant_id=user_id)
    return render_template("mer_watch_unfinished_orders.html", datas=datas)

# 商户完成订单
@app.route("/mer/mer_do_finished_orders/<order_id>")
def mer_do_finished_orders(order_id):
    status = request.cookies.get('status')
    if status != "merchant":
        return redirect(url_for("index"))
    if "user_name" not in session:
        return redirect(url_for("index"))
    datas = db.add_message(order_id=order_id, message_content="已完成")
    datas = db.update_order_status(order_id=order_id, new_status="已完成")
    result = datas["success"]
    print(result)
    return render_template("do_mer_add_dishes.html", result=result)


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
    result = datas["success"]
    print(result)
    return render_template("do_mer_add_dishes.html", result=result)




# 管理员查看全部用户并删除用户
@app.route("/man/man_watch_users_or_delete")
def man_watch_users_or_delete():
    status = request.cookies.get('status')
    if status != "admin":
        return redirect(url_for("index"))
    if "user_name" not in session:
        return redirect(url_for("index"))
    datas = db.get_all_users()
    return render_template("man_watch_users_or_delete.html", datas=datas)


# 管理员删除用户
@app.route("/man/man_do_users_or_delete/<user_id>")
def man_do_users_or_delete(user_id):
    status = request.cookies.get('status')
    if status != "admin":
        return redirect(url_for("index"))
    if "user_name" not in session:
        return redirect(url_for("index"))
    print(request.form)
    datas = db.delete_user(user_id=user_id)
    result = datas["success"]
    print(result)
    return render_template("man_do_dishes_or_delete.html", result=result)


# 管理员添加用户
@app.route("/man/show_man_add_users")
def show_man_add_users():
    status = request.cookies.get('status')
    if status != "admin":
        return redirect(url_for("index"))
    if "user_name" not in session:
        return redirect(url_for("index"))
    return render_template("show_man_add_users.html")


# 管理员添加拥护
@app.route("/man/do_man_add_users", methods=["POST"])
def do_man_add_users():
    status = request.cookies.get('status')
    if status != "admin":
        return redirect(url_for("index"))
    if "user_name" not in session:
        return redirect(url_for("index"))
    print(request.form)
    name = request.form.get("name")
    identity=request.form.get("identity")
    student_number = request.form.get("student_number")
    pwd = request.form.get("pwd")
    sex = request.form.get("sex")
    BirthDate = request.form.get("BirthDate")
    datas = db.register_user(student_number=student_number, pwd=pwd, name=name, sex=sex, birthdate=BirthDate,identity=identity)
    result = datas["success"]
    print(result)
    return render_template("man_do_dishes_or_delete.html", result=result)


# 管理员查看全部商户并删除商户
@app.route("/man/man_watch_mers_or_delete")
def man_watch_mers_or_delete():
    status = request.cookies.get('status')
    if status != "admin":
        return redirect(url_for("index"))
    if "user_name" not in session:
        return redirect(url_for("index"))
    datas = db.get_all_merchants()
    return render_template("man_watch_mers_or_delete.html", datas=datas)


# 管理员删除商户
@app.route("/man/man_do_mers_or_delete/<mer_id>")
def man_do_mers_or_delete(mer_id):
    status = request.cookies.get('status')
    if status != "admin":
        return redirect(url_for("index"))
    if "user_name" not in session:
        return redirect(url_for("index"))
    print(request.form)
    datas = db.delete_merchant(merchant_id=mer_id)
    result = datas["success"]
    print(result)
    return render_template("man_do_dishes_or_delete.html", result=result)


# 管理员添加商户
@app.route("/man/show_man_add_mers")
def show_man_add_mers():
    status = request.cookies.get('status')
    if status != "admin":
        return redirect(url_for("index"))
    if "user_name" not in session:
        return redirect(url_for("index"))
    return render_template("show_man_add_mers.html")


# 管理员添加商户
@app.route("/man/do_man_add_mers", methods=["POST"])
def do_man_add_mers():
    status = request.cookies.get('status')
    if status != "admin":
        return redirect(url_for("index"))
    if "user_name" not in session:
        return redirect(url_for("index"))
    print(request.form)
    name = request.form.get("name")
    account = request.form.get("account")
    pwd = request.form.get("pwd")
    address = request.form.get("address")
    datas = db.add_merchant(account=account, pwd=pwd, name=name, address=address)
    result = datas["success"]
    print(result)
    return render_template("man_do_dishes_or_delete.html", result=result)







# 管理员查看全部菜品并删除菜品
@app.route("/man/man_watch_dishes_or_delete")
def man_watch_dishes_or_delete():
    status = request.cookies.get('status')
    if status != "admin":
        return redirect(url_for("index"))
    if "user_name" not in session:
        return redirect(url_for("index"))
    datas = db.get_all_foods()
    return render_template("man_watch_dishes_or_delete.html", datas=datas)

# 管理员查看菜品详细信息
@app.route("/man/man_watch_dishes/<food_id>")
def man_watch_dishes(food_id):
    if "user_name" not in session:
        return redirect(url_for("index"))
    datas = db.get_food_info(food_id=food_id)
    data = datas[0]
    classificationId = int(data["classificationId"])
    classification = db.get_food_classification_name(classificationId)
    return render_template("man_watch_dishes.html", food=data, classification=classification)


# 管理员删除菜品
@app.route("/man/man_do_dishes_or_delete/<food_id>")
def man_do_dishes_or_delete(food_id):
    status = request.cookies.get('status')
    if status != "admin":
        return redirect(url_for("index"))
    if "user_name" not in session:
        return redirect(url_for("index"))
    print(request.form)
    datas = db.delete_food(food_id=food_id)
    result = datas["success"]
    print("success" + str(result))
    if result != None:
        return render_template("man_do_dishes_or_delete.html", result=result)

# 管理员查看用户群体特征分析
@app.route("/man/man_watch_analysis")
def man_watch_analysis():
    status = request.cookies.get('status')
    if status != "admin":
        return redirect(url_for("index"))
    if "user_name" not in session:
        return redirect(url_for("index"))
    # e1. 根据年龄段进行点餐习惯分析
    datas1 = db.analyze_order_habits_by_age()

    # e2. 根据角色进行点餐习惯分析
    datas2 = db.analyze_order_habits_by_role()

    # e3. 根据性别进行点餐习惯分析
    datas3 = db.analyze_order_habits_by_gender()

    # e4.根据年龄段进行评价习惯分析
    datas4 = db.analyze_review_habits_by_age()

    # e5. 根据角色进行评价习惯分析
    datas5 = db.analyze_review_habits_by_role()

    # e6.根据性别进行评价习惯分析
    datas6 = db.analyze_review_habits_by_gender()
    return render_template("man_watch_analysis.html", datas1=datas1,datas2=datas2,datas3=datas3,datas4=datas4,datas5=datas5,datas6=datas6)



# # 增加用户页面
# @app.route("/show_add_user")
# def show_add_user():
#     if "user_name" not in session:
#         return redirect(url_for("index"))
#     return render_template("show_add_user.html")
#
#
# # 增加用户操作
# @app.route("/do_add_user", methods=["POST"])
# def do_add_user():
#     if "user_name" not in session:
#         return redirect(url_for("index"))
#     print(request.form)
#     name = request.form.get("name")
#     sex = request.form.get("sex")
#     age = request.form.get("age")
#     email = request.form.get("email")
#     sql = f"""
#         insert into user(name,sex,age,email)
#         values ('{name}','{sex}',{age},'{email}')
#     """
#     print(sql)
#     db.insert_or_update_data(sql)
#     return "success"
#
#
# # 展示用户列表
# @app.route("/show_users")
# def show_users():
#     if "user_name" not in session:
#         return redirect(url_for("index"))
#     sql = "select id,name from user"
#     datas = db.query_data(sql)
#     return render_template("show_users.html", datas=datas)
#
#
# # <tr>...</tr> 定义一行标签，一组行标签内可以建立多组由<td>或<th>标签所定义的单元格
# # <th>...</th>定义表头单元格。表格中的文字将以粗体显示
# # <td>...</td> 定义单元格标签
#
# # 查看单个用户
# @app.route("/show_user/<user_id>")
# def show_user(user_id):
#     if "user_name" not in session:
#         return redirect(url_for("index"))
#     sql = "select * from user where id=" + user_id
#     datas = db.query_data(sql)
#     # print(datas)
#     user = datas[0]
#     # print(user)
#     return render_template("show_user.html", user=user)


if __name__ == '__main__':
    app.run()
