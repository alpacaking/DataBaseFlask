import pprint
import pymysql
from pymysql import cursors
#引入模块
from flask import Flask, render_template,request
import json
import requests

#连接mysql数据库
def conn_mysql():
    return pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password="123456",# 密码
        database="flask_db",
        charset="utf8"
    )

def query_data(sql):
    conn = conn_mysql()
    try:
        cursor = conn.cursor(pymysql.cursors.DictCursor) #返回数据是字典形式，而不是数组
        cursor.execute(sql)
        result = cursor.fetchall()
        if not result:
            return None  # 返回空值
        return result
    finally:
        conn.close()


#更新数据:
# 更新数据
def insert_or_update_data(sql):
    conn = conn_mysql()
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()  # 提交
    except Exception as e:
        print(f"插入/更新数据失败: {e}")
        return {"success": False}
    finally:
        conn.close()
    return {"success": True}

# 删除数据
def delete_data(sql):
    conn = conn_mysql()
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()  # 提交
    except Exception as e:
        print(f"删除数据失败: {e}")
        return {"success": False}
    finally:
        conn.close()
    return {"success": True}


# 0.0 验证用户登录
def check_user_login(student_number, pwd):
    sql = f"SELECT * FROM User WHERE student_number = '{student_number}' AND pwd = '{pwd}'"
    result = query_data(sql)
    if "error" not in result and result:
        return result[0]  # 返回用户信息
    return {"error": "Invalid username or password"}  # 用户名或密码错误

# 0.1 验证商家登录
def check_merchant_login(account, pwd):
    sql = f"SELECT * FROM Merchant WHERE account = '{account}' AND pwd = '{pwd}'"
    result = query_data(sql)
    if "error" not in result and result:
        return result[0]  # 返回商家信息
    return {"error": "Invalid account or password"}  # 账号或密码错误

# 0.2 验证管理员登录
def check_admin_login(username, pwd):
    sql = f"SELECT * FROM Admins WHERE username = '{username}' AND pwd = '{pwd}'"
    result = query_data(sql)
    if "error" not in result and result:
        return result[0]  # 返回管理员信息
    return {"error": "Invalid username or password"}  # 账号或密码错误

# 0.3 所有表根据id返回对应元组值
def get_admins_info(Entity_id):
    sql = f"SELECT * FROM admins WHERE id = {Entity_id}"
    return query_data(sql)

def get_commentfood_info(Entity_id):
    sql = f"SELECT * FROM commentfood WHERE id = {Entity_id}"
    return query_data(sql)

def get_commentmerchant_info(Entity_id):
    sql = f"SELECT * FROM commentmerchant WHERE id = {Entity_id}"
    return query_data(sql)

def get_food_info(Entity_id):
    sql = f"SELECT * FROM food WHERE id = {Entity_id}"
    return query_data(sql)

def get_foodclassification_info(Entity_id):
    sql = f"SELECT * FROM foodclassification WHERE id = {Entity_id}"
    return query_data(sql)

def get_message_info(Entity_id):
    sql = f"SELECT * FROM message WHERE id = {Entity_id}"
    return query_data(sql)

def get_scorefood_info(Entity_id):
    sql = f"SELECT * FROM scorefood WHERE id = {Entity_id}"
    return query_data(sql)

def get_scoremerchant_info(Entity_id):
    sql = f"SELECT * FROM scoremerchant WHERE id = {Entity_id}"
    return query_data(sql)

def get_userfavoritedish_info(Entity_id):
    sql = f"SELECT * FROM userfavoritedish WHERE id = {Entity_id}"
    return query_data(sql)

def get_userfavoritemerchant_info(Entity_id):
    sql = f"SELECT * FROM userfavoritemerchant WHERE id = {Entity_id}"
    return query_data(sql)

def get_userorder_info(Entity_id):
    sql = f"SELECT * FROM userorder WHERE id = {Entity_id}"
    return query_data(sql)


# 1. 用户查看账户信息
def get_user_info(user_id):
    sql = f"SELECT * FROM User WHERE id = {user_id}"
    return query_data(sql)

# 2. 用户查看订单历史
def get_user_orders(user_id):
    sql = f"SELECT * FROM UserOrder WHERE userId = {user_id}"
    return query_data(sql)

# 3. 用户查看收藏菜品
def get_user_favorite_dishes(user_id):
    sql = f"""
    SELECT Food.* FROM UserFavoriteDish 
    JOIN Food ON UserFavoriteDish.foodId = Food.id 
    WHERE UserFavoriteDish.userId = {user_id}
    """
    return query_data(sql)

# 4. 用户查看消息列表
def get_user_messages(user_id):
    sql = f"SELECT * FROM Message WHERE userId = {user_id}"
    return query_data(sql)

# 5. 搜索商户
def search_merchants(keyword):
    sql = f"SELECT * FROM Merchant WHERE name LIKE '%{keyword}%'"
    return query_data(sql)

# 6. 查看商户详细信息
def get_merchant_info(merchant_id):
    sql = f"SELECT * FROM Merchant WHERE id = {merchant_id}"
    return query_data(sql)

# 7. 搜索商户的餐品
def search_merchant_foods(merchant_id, keyword):
    sql = f"""
    SELECT * FROM Food 
    WHERE MerchantId = {merchant_id} AND name LIKE '%{keyword}%'
    """
    return query_data(sql)

# 7.1 查看商户的所有餐品
def get_merchant_foods(merchant_id):
    sql = f"""
    SELECT * FROM Food 
    WHERE MerchantId = {merchant_id}
    """
    return query_data(sql)

# 7.2 查看商户的所有餐品分类
def get_all_foodClassification():
    sql = f"""
    SELECT * FROM FoodClassification 
    """
    return query_data(sql)

# 8. 查看餐品详细信息
def get_food_info(food_id):
    sql = f"SELECT * FROM Food WHERE id = {food_id}"
    return query_data(sql)

# 9. 用户收藏商户
def favorite_merchant(user_id, merchant_id):
    sql = f"INSERT INTO UserFavoriteMerchant (userId, merchantId) VALUES ({user_id}, {merchant_id})"
    return insert_or_update_data(sql)

# 10. 用户收藏菜品
def favorite_food(user_id, food_id):
    sql = f"INSERT INTO UserFavoriteDish (userId, foodId) VALUES ({user_id}, {food_id})"
    return insert_or_update_data(sql)

# 11. 用户评价商户
def rate_merchant(user_id, merchant_id, order_id, score, content):
    sql = f"""
    INSERT INTO CommentMerchant (merchantId, content, commenterId, orderId) 
    VALUES ({merchant_id}, '{content}', {user_id}, {order_id});
    INSERT INTO ScoreMerchant (merchantId, score, commenterId, orderId) 
    VALUES ({merchant_id}, {score}, {user_id}, {order_id});
    """
    return insert_or_update_data(sql)

# 12. 用户评价菜品
def rate_food(user_id, food_id, order_id, score, content):
    sql = f"""
    INSERT INTO CommentFood (foodId, content, commenterId, orderId) 
    VALUES ({food_id}, '{content}', {user_id}, {order_id});
    INSERT INTO ScoreFood (foodId, score, commenterId, orderId) 
    VALUES ({food_id}, {score}, {user_id}, {order_id});
    """
    return  insert_or_update_data(sql)

# 13. 商户查看信息
def get_merchant_self_info(merchant_id):
    sql = f"SELECT * FROM Merchant WHERE id = {merchant_id}"
    return query_data(sql)

# 14. 商户管理菜单
def get_merchant_foods(merchant_id):
    sql = f"SELECT * FROM Food WHERE MerchantId = {merchant_id}"
    return query_data(sql)

# 15. 管理员管理用户
def get_all_users():
    sql = "SELECT * FROM User"
    return query_data(sql)

# 16. 管理员管理商户
def get_all_merchants():
    sql = "SELECT * FROM Merchant"
    return query_data(sql)

# 17. 管理员管理菜品
def get_all_foods():
    sql = "SELECT * FROM Food"
    return query_data(sql)

# 18. 用户注册 & 管理员添加用户
def register_user(student_number, pwd, name, sex, birthdate):
    # 检查 student_number 是否已存在
    check_sql = f"SELECT * FROM User WHERE student_number = '{student_number}'"
    check_result = query_data(check_sql)
    if "error" not in check_result and check_result:
        return {"success": "Student number already exists"}
    # 插入新用户
    insert_sql = f"""
    INSERT INTO User (student_number, pwd, name, sex, BirthDate) 
    VALUES ('{student_number}', '{pwd}', '{name}', '{sex}', '{birthdate}')
    """
    return insert_or_update_data(insert_sql)

# 19. 用户点餐
def place_order(user_id, merchant_id, details, price_amount):
    sql = f"""
    INSERT INTO UserOrder (detail, price_amount, userId, merchantId, status) 
    VALUES ('{details}', {price_amount}, {user_id}, {merchant_id}, '待处理')
    """
    return insert_or_update_data(sql)

# 20. 商户添加菜品
def add_food(merchant_id, name, classification_id, picture, price, description, nutrition, ingredient, allergy):
    score=4
    sales_volume=0
    sql = f"""
    INSERT INTO Food (name, classificationId, picture, score, price, sales_volume, description, nutrition, ingredient, allergy, MerchantId) 
    VALUES ('{name}', {classification_id}, '{picture}', {score}, {price}, {sales_volume}, '{description}', '{nutrition}', '{ingredient}', '{allergy}', {merchant_id})
    """
    return insert_or_update_data(sql)

# 21. 商户删除菜品
def delete_food(food_id):
    sql = f"DELETE FROM Food WHERE id = {food_id}"
    return delete_data(sql)

# 22. 管理员添加商户
def add_merchant(account, pwd, name, address):
    sql = f"""
    INSERT INTO Merchant (account, pwd, name, address) 
    VALUES ('{account}', '{pwd}', '{name}', '{address}')
    """
    return insert_or_update_data(sql)

# 23. 管理员删除商户
def delete_merchant(merchant_id):
    sql = f"DELETE FROM Merchant WHERE id = {merchant_id}"
    return delete_data(sql)

# 24.2 管理员删除用户
def delete_user(user_id):
    sql = f"DELETE FROM User WHERE id = {user_id}"
    return delete_data(sql)

# 25. 管理员删除菜品
def admin_delete_food(food_id):
    sql = f"DELETE FROM Food WHERE id = {food_id}"
    return delete_data(sql)

# 26. 根据分类ID查找分类名称
def get_food_classification_name(classification_id):
    sql = f"SELECT name FROM FoodClassification WHERE id = {classification_id}"
    result = query_data(sql)
    if result:
        return result[0]['name']
    else:
        return None


# -----------------------------------以下为进阶需求
# a:菜品数据分析：某个商户所有菜品的评分、销量以及购买该菜品次数最多的人
def analyze_food_data(merchant_id):
    sql = f"""
    SELECT f.name, f.score, f.sales_volume, u.name AS top_buyer
    FROM Food f, User u
    LEFT JOIN (
        SELECT uo.FoodId, u.name, COUNT(uo.id) AS purchase_count
        FROM UserOrder uo
        JOIN u ON uo.userId = u.id
        WHERE uo.merchantId = {merchant_id}
        GROUP BY uo.FoodId, u.id
        ORDER BY purchase_count DESC
        LIMIT 1
    ) AS top ON f.id = top.FoodId
    WHERE f.MerchantId = {merchant_id}
    """
    return query_data(sql)


# b: 用户收藏的各个菜品在一段时间内的销量
def analyze_favorite_food_sales(user_id, start_date, end_date):
    sql = f"""
    SELECT f.name, COUNT(uo.id) AS sales_count
    FROM UserFavoriteDish ufd
    JOIN Food f ON ufd.foodId = f.id
    JOIN UserOrder uo ON uo.FoodId = f.id
    WHERE ufd.userId = {user_id} AND uo.add_time BETWEEN '{start_date}' AND '{end_date}'
    GROUP BY f.name
    """
    return query_data(sql)

# c: 用户活跃度分析
def analyze_user_activity(user_id):
    sql = f"""
    SELECT 
        DATE_FORMAT(add_time, '%Y-%m-%d') AS day, 
        COUNT(id) AS order_count
    FROM UserOrder
    WHERE userId = {user_id}
    GROUP BY day
    ORDER BY day
    """
    return query_data(sql)

# d: 一段时间内某个忠实粉丝在该商户的消费分布
def analyze_merchant_loyal_customers(merchant_id, start_date, end_date, threshold):
    sql = f"""
    SELECT u.name, f.name AS food_name, COUNT(uo.id) AS purchase_count
    FROM UserOrder uo
    JOIN User u ON uo.userId = u.id
    JOIN Food f ON uo.FoodId = f.id
    WHERE uo.merchantId = {merchant_id} AND uo.add_time BETWEEN '{start_date}' AND '{end_date}'
    GROUP BY u.id, f.id
    HAVING COUNT(uo.id) > {threshold}
    """
    return query_data(sql)

# 未完待续 。。。。。。。。。。