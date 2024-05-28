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

#查询数据
def query_data(sql):
    conn = conn_mysql()
    try:
        cursor = conn.cursor(pymysql.cursors.DictCursor) #返回数据是字典形式，而不是数组
        cursor.execute(sql)
        return cursor.fetchall()
    finally:
        conn.close()

#更新数据:
def insert_or_update_data(sql):
    conn = conn_mysql()
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit() #提交
    finally:
        conn.close()

# 删除数据
def delete_data(sql):
    conn = conn_mysql()
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()  # 提交
    finally:
        conn.close()

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

# 8. 查看餐品详细信息
def get_food_info(food_id):
    sql = f"SELECT * FROM Food WHERE id = {food_id}"
    return query_data(sql)

# 9. 用户收藏商户
def favorite_merchant(user_id, merchant_id):
    sql = f"INSERT INTO UserFavoriteMerchant (userId, merchantId) VALUES ({user_id}, {merchant_id})"
    insert_or_update_data(sql)

# 10. 用户收藏菜品
def favorite_food(user_id, food_id):
    sql = f"INSERT INTO UserFavoriteDish (userId, foodId) VALUES ({user_id}, {food_id})"
    insert_or_update_data(sql)

# 11. 用户评价商户
def rate_merchant(user_id, merchant_id, order_id, score, content):
    sql = f"""
    INSERT INTO CommentMerchant (merchantId, content, commenterId, orderId) 
    VALUES ({merchant_id}, '{content}', {user_id}, {order_id});
    INSERT INTO ScoreMerchant (merchantId, score, commenterId, orderId) 
    VALUES ({merchant_id}, {score}, {user_id}, {order_id});
    """
    insert_or_update_data(sql)

# 12. 用户评价菜品
def rate_food(user_id, food_id, order_id, score, content):
    sql = f"""
    INSERT INTO CommentFood (foodId, content, commenterId, orderId) 
    VALUES ({food_id}, '{content}', {user_id}, {order_id});
    INSERT INTO ScoreFood (foodId, score, commenterId, orderId) 
    VALUES ({food_id}, {score}, {user_id}, {order_id});
    """
    insert_or_update_data(sql)

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

# 18. 用户注册
def register_user(student_number, pwd, name, sex, birthdate):
    sql = f"""
    INSERT INTO User (student_number, pwd, name, sex, BirthDate) 
    VALUES ('{student_number}', '{pwd}', '{name}', '{sex}', '{birthdate}')
    """
    insert_or_update_data(sql)

# 19. 用户点餐
def place_order(user_id, merchant_id, details, price_amount):
    sql = f"""
    INSERT INTO UserOrder (detail, price_amount, userId, merchantId, status) 
    VALUES ('{details}', {price_amount}, {user_id}, {merchant_id}, '待处理')
    """
    insert_or_update_data(sql)

# 20. 商户添加菜品
def add_food(merchant_id, name, classification_id, picture, score, price, sales_volume, description, nutrition, ingredient, allergy):
    sql = f"""
    INSERT INTO Food (name, classificationId, picture, score, price, sales_volume, description, nutrition, ingredient, allergy, MerchantId) 
    VALUES ('{name}', {classification_id}, '{picture}', {score}, {price}, {sales_volume}, '{description}', '{nutrition}', '{ingredient}', '{allergy}', {merchant_id})
    """
    insert_or_update_data(sql)

# 21. 商户删除菜品
def delete_food(food_id):
    sql = f"DELETE FROM Food WHERE id = {food_id}"
    delete_data(sql)

# 22. 管理员添加商户
def add_merchant(account, pwd, name, address):
    sql = f"""
    INSERT INTO Merchant (account, pwd, name, address) 
    VALUES ('{account}', '{pwd}', '{name}', '{address}')
    """
    insert_or_update_data(sql)

# 23. 管理员删除商户
def delete_merchant(merchant_id):
    sql = f"DELETE FROM Merchant WHERE id = {merchant_id}"
    delete_data(sql)

# 24. 管理员删除用户
def delete_user(user_id):
    sql = f"DELETE FROM User WHERE id = {user_id}"
    delete_data(sql)

# 25. 管理员删除菜品
def admin_delete_food(food_id):
    sql = f"DELETE FROM Food WHERE id = {food_id}"
    delete_data(sql)

