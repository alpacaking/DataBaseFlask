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
def check_user_login(student_number, pwd):
    sql = f"SELECT * FROM User WHERE student_number = '{student_number}' AND pwd = '{pwd}'"
    result = query_data(sql)
    if result:
        return result[0]  # 返回用户信息
    return None  # 用户名或密码错误

# 0.1验证商家登录
def check_merchant_login(account, pwd):
    sql = f"SELECT * FROM Merchant WHERE account = '{account}' AND pwd = '{pwd}'"
    result = query_data(sql)
    if result:
        return result[0]  # 返回商家信息
    return None  # 账号或密码错误

# 0.2验证管理员登录
def check_admin_login(username, pwd):
    sql = f"SELECT * FROM Admins WHERE username = '{username}' AND pwd = '{pwd}'"
    result = query_data(sql)
    if result:
        return result[0]  # 返回管理员信息
    return None  # 账号或密码错误

def get_commentfood_info(Entity_id):
    sql = f"SELECT * FROM commentfood WHERE id = {Entity_id}"
    return query_data(sql)

def get_commentmerchant_info(Entity_id):
    sql = f"SELECT * FROM commentmerchant WHERE id = {Entity_id}"
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
    WHERE MerchantId = {merchant_id} AND is_deleted = 0 AND name LIKE '%{keyword}% '
    """
    return query_data(sql)

# 7.1 查看商户的所有餐品
def get_merchant_foods(merchant_id):
    sql = f"""
    SELECT * FROM Food 
    WHERE MerchantId = {merchant_id} AND is_deleted = 0
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
    sql = f"SELECT * FROM Food WHERE id = {food_id} AND is_deleted = 0"
    return query_data(sql)

# 9. 用户收藏商户
def favorite_merchant(user_id, merchant_id):
    sql = f"INSERT INTO UserFavoriteMerchant (userId, merchantId) VALUES ({user_id}, {merchant_id})"
    return insert_or_update_data(sql)

# 10. 用户收藏菜品
def favorite_food(user_id, food_id):
    sql = f"INSERT INTO UserFavoriteDish (userId, foodId) VALUES ({user_id}, {food_id})"
    return insert_or_update_data(sql)

# 11. 用户根据订单评价商户
def rate_merchant(user_id, order_id, score, content):
    order_info = get_userorder_info(order_id)
    order = order_info[0]
    merchant_id = order["merchantId"]
    sql1 = f"""
    INSERT INTO CommentMerchant (merchantId, content, commenterId, orderId) 
    VALUES ({merchant_id}, '{content}', {user_id}, {order_id});
    """
    sql2 = f"""
    INSERT INTO ScoreMerchant (merchantId, score, commenterId, orderId) 
    VALUES ({merchant_id}, {score}, {user_id}, {order_id});
    """
    print(sql1,sql2)
    conn = conn_mysql()
    try:
        cursor = conn.cursor()
        cursor.execute(sql1)
        cursor.execute(sql2)
        conn.commit()  # 提交
    except Exception as e:
        print(f"插入/更新数据失败: {e}")
        conn.rollback()
        return {"success": False}
    finally:
        cursor.close()
        conn.close()
    return {"success": True}

# 12. 用户根据订单评价菜品
def rate_food(user_id, order_id, score, content):
    order_info = get_userorder_info(Entity_id=order_id)
    order = order_info[0]
    food_id = order["foodId"]
    sql1 = f"""
    INSERT INTO CommentFood (foodId, content, commenterId, orderId) 
    VALUES ({food_id}, '{content}', {user_id}, {order_id});
    """
    sql2 = f"""
    INSERT INTO ScoreFood (foodId, score, commenterId, orderId) 
    VALUES ({food_id}, {score}, {user_id}, {order_id});
    """
    print(sql1, sql2)
    conn = conn_mysql()
    try:
        cursor = conn.cursor()
        cursor.execute(sql1)
        cursor.execute(sql2)
        conn.commit()  # 提交
    except Exception as e:
        print(f"插入/更新数据失败: {e}")
        conn.rollback()
        return {"success": False}
    finally:
        cursor.close()
        conn.close()
    return {"success": True}

# 13. 商户查看信息
def get_merchant_self_info(merchant_id):
    sql = f"SELECT * FROM Merchant WHERE id = {merchant_id}"
    return query_data(sql)

# 14. 商户管理菜单
def get_merchant_foods(merchant_id):
    sql = f"SELECT * FROM Food WHERE MerchantId = {merchant_id} AND is_deleted = 0"
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
    sql = f"SELECT * FROM Food WHERE is_deleted = 0"
    return query_data(sql)

# 18. 用户注册 & 管理员添加用户
def register_user(identity, student_number, pwd, name, sex, birthdate):
    # 检查 student_number 是否已存在
    check_sql = f"SELECT * FROM User WHERE student_number = '{student_number}'"
    check_result = query_data(check_sql)
    if check_result:
        # 更新已存在用户信息
        update_sql = f"""
        UPDATE User 
        SET identity = '{identity}', pwd = '{pwd}', name = '{name}', sex = '{sex}', BirthDate = '{birthdate}'
        WHERE student_number = '{student_number}'
        """
        print("更新已存在用户信息")
        return insert_or_update_data(update_sql)
    else:
        # 插入新用户
        insert_sql = f"""
        INSERT INTO User (identity, student_number, pwd, name, sex, BirthDate) 
        VALUES ('{identity}', '{student_number}', '{pwd}', '{name}', '{sex}', '{birthdate}')
        """
        return insert_or_update_data(insert_sql)


# 19. 用户点餐
def place_order(food_id, user_id, details, is_paid):
    food_info = get_food_info(food_id)
    food=food_info[0]
    price_amount = food["price"]
    merchant_id = food["MerchantId"]

    sql = f"""
    INSERT INTO UserOrder (FoodId, detail, price_amount, userId, merchantId, status, is_paid) 
    VALUES ({food_id}, '{details}', {price_amount}, {user_id}, {merchant_id}, '待处理', '{is_paid}')
    """
    return insert_or_update_data(sql)

# 20. 商户添加菜品
def add_food(merchant_id, name, classification_id, picture, price, description, nutrition, ingredient, allergy):
    score=4
    sales_volume=0
    is_deleted=0
    sql = f"""
    INSERT INTO Food (name, classificationId, picture, score, price, sales_volume, description, nutrition, ingredient, allergy, MerchantId, is_deleted) 
    VALUES ('{name}', {classification_id}, '{picture}', {score}, {price}, {sales_volume}, '{description}', '{nutrition}', '{ingredient}', '{allergy}', {merchant_id}, {is_deleted})
    """
    return insert_or_update_data(sql)

# 21. 商户删除菜品
def delete_food(food_id):
    sql = f"DELETE FROM Food WHERE id = {food_id} AND is_deleted = 0"
    return delete_data(sql)

# 22. 管理员添加/更新商户
def add_merchant(account, pwd, name, address):
    # 检查 account 是否已存在
    check_sql = f"SELECT * FROM Merchant WHERE account = '{account}'"
    check_result = query_data(check_sql)
    if check_result:
        # 更新已存在商户信息
        update_sql = f"""
        UPDATE Merchant 
        SET pwd = '{pwd}', name = '{name}', address = '{address}'
        WHERE account = '{account}'
        """
        print("更新已存在商户信息")
        return insert_or_update_data(update_sql)
    else:
        # 插入新商户
        insert_sql = f"""
        INSERT INTO Merchant (account, pwd, name, address) 
        VALUES ('{account}', '{pwd}', '{name}', '{address}')
        """
        return insert_or_update_data(insert_sql)

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
    sql = f"DELETE FROM Food WHERE id = {food_id} AND is_deleted = 0"
    return delete_data(sql)

# 26. 根据分类ID查找分类名称
def get_food_classification_name(classification_id):
    sql = f"SELECT name FROM FoodClassification WHERE id = {classification_id}"
    result = query_data(sql)
    if result:
        return result[0]['name']
    else:
        return None

# 27.商家查询自己所有未完成的订单
def get_merchant_pending_orders(merchant_id):
    sql = f"""
    SELECT * FROM UserOrder 
    WHERE merchantId = {merchant_id} AND status != '已完成'
    """
    return query_data(sql)

# 28.1 更新订单状态
def update_order_status(order_id, new_status):
    update_order_sql = f"""
    UPDATE UserOrder 
    SET status = '{new_status}' 
    WHERE id = {order_id}
    """
    return insert_or_update_data(update_order_sql)


# 28.2 添加消息
def add_message(order_id, message_content):
    order_info = get_userorder_info(order_id)
    order = order_info[0]
    user_id = order['userId']
    merchant_id = order['merchantId']
    add_message_sql = f"""
    INSERT INTO Message (orderId, content, userId, status, merchantId) 
    VALUES ({order_id}, '{message_content}', {user_id}, '未读', {merchant_id})
    """
    return insert_or_update_data(add_message_sql)

# 29. 根据用户ID和食品ID查询有没有收藏
def check_user_favorite_food(user_id, food_id):
    sql = f"""
    SELECT * FROM UserFavoriteDish 
    WHERE userId = {user_id} AND foodId = {food_id}
    """
    return query_data(sql)

# 29.1 根据用户ID和商家ID查询有没有收藏
def check_user_favorite_merchant(user_id, merchantId):
    sql = f"""
    SELECT * FROM UserFavoriteMerchant 
    WHERE userId = {user_id} AND merchantId = {merchantId}
    """
    return query_data(sql)

# 30. # 根据用户ID和商家ID查询有没有评价、打分
def check_user_rating_merchant(order_id):
    order_info = get_userorder_info(order_id)
    order = order_info[0]
    merchant_id = order['merchantId']
    check_comment_sql = f"""
    SELECT * FROM CommentMerchant 
    WHERE orderId = {order_id} AND merchantId = {merchant_id}
    """
    return query_data(check_comment_sql)

# 31. # 根据订单ID查询该订单有没有评价、打分
def check_user_rating_food(order_id):
    order_info = get_userorder_info(order_id)
    order = order_info[0]
    food_id = order['foodId']
    check_comment_sql = f"""
    SELECT * FROM commentfood
    WHERE orderId = {order_id} AND foodId = {food_id}
    """
    return query_data(check_comment_sql)

# -----------------------------------以下为进阶需求
# a:菜品数据分析：某个商户所有菜品的评分、销量以及购买该菜品次数最多的人
def analyze_food_data(merchant_id):
    sql = f"""
    SELECT 
        f.id AS food_id,
        f.name AS food_name, 
        f.score AS food_score, 
        f.sales_volume AS food_sales_volume,
        (
            SELECT u.name 
            FROM User u
            JOIN UserOrder uo ON u.id = uo.userId
            WHERE uo.foodId = f.id
            GROUP BY u.id
            ORDER BY COUNT(uo.id) DESC
            LIMIT 1
        ) AS top_buyer
    FROM 
        Food f
    WHERE 
        f.MerchantId = {merchant_id}
    """
    print(sql)
    return query_data(sql)


# b: 用户收藏的各个菜品在一段时间内的销量
def analyze_favorite_food_sales(user_id, start_date, end_date):
    sql = f"""
    SELECT f.name AS food_name, COUNT(uo.id) AS sales_count
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
    SELECT u.name AS user_name, f.name AS food_name, COUNT(uo.id) AS purchase_count
    FROM UserOrder uo
    JOIN User u ON uo.userId = u.id
    JOIN Food f ON uo.FoodId = f.id
    WHERE uo.merchantId = {merchant_id} AND uo.add_time BETWEEN '{start_date}' AND '{end_date}'
    GROUP BY u.id, f.id
    HAVING COUNT(uo.id) > {threshold}
    """
    return query_data(sql)

# e: 用户群体特征分析：根据用户的角色、年龄 和性别等信息，对用户群体进行特征分析。

# e1. 根据年龄段进行点餐习惯分析
def analyze_order_habits_by_age():
    sql = """
    SELECT 
        CASE
            WHEN TIMESTAMPDIFF(YEAR, u.BirthDate, CURDATE()) < 18 THEN 'Under 18'
            WHEN TIMESTAMPDIFF(YEAR, u.BirthDate, CURDATE()) BETWEEN 18 AND 24 THEN '18-24'
            WHEN TIMESTAMPDIFF(YEAR, u.BirthDate, CURDATE()) BETWEEN 25 AND 34 THEN '25-34'
            WHEN TIMESTAMPDIFF(YEAR, u.BirthDate, CURDATE()) BETWEEN 35 AND 44 THEN '35-44'
            ELSE '45+'
        END AS age_group,
        m.name AS merchant_name,
        COUNT(uo.id) AS order_count
    FROM UserOrder uo
    JOIN User u ON uo.userId = u.id
    JOIN Merchant m ON uo.merchantId = m.id
    GROUP BY age_group, m.id
    ORDER BY age_group, order_count DESC
    """
    return query_data(sql)

# e2. 根据角色进行点餐习惯分析
def analyze_order_habits_by_role():
    sql = """
    SELECT 
        u.identity AS user_role,
        m.name AS merchant_name,
        COUNT(uo.id) AS order_count
    FROM UserOrder uo
    JOIN User u ON uo.userId = u.id
    JOIN Merchant m ON uo.merchantId = m.id
    GROUP BY u.identity, m.id
    ORDER BY u.identity, order_count DESC
    """
    return query_data(sql)

# e3. 根据性别进行点餐习惯分析
def analyze_order_habits_by_gender():
    sql = """
    SELECT 
        u.sex AS user_gender,
        m.name AS merchant_name,
        COUNT(uo.id) AS order_count
    FROM UserOrder uo
    JOIN User u ON uo.userId = u.id
    JOIN Merchant m ON uo.merchantId = m.id
    GROUP BY u.sex, m.id
    ORDER BY u.sex, order_count DESC
    """
    return query_data(sql)

# e4.根据年龄段进行评价习惯分析
def analyze_review_habits_by_age():
    sql = """
    SELECT 
        CASE
            WHEN TIMESTAMPDIFF(YEAR, u.BirthDate, CURDATE()) < 18 THEN 'Under 18'
            WHEN TIMESTAMPDIFF(YEAR, u.BirthDate, CURDATE()) BETWEEN 18 AND 24 THEN '18-24'
            WHEN TIMESTAMPDIFF(YEAR, u.BirthDate, CURDATE()) BETWEEN 25 AND 34 THEN '25-34'
            WHEN TIMESTAMPDIFF(YEAR, u.BirthDate, CURDATE()) BETWEEN 35 AND 44 THEN '35-44'
            ELSE '45+'
        END AS age_group,
        COUNT(c.id) AS review_count,
        AVG(s.score) AS average_score
    FROM CommentMerchant c
    JOIN User u ON c.commenterId = u.id
    JOIN ScoreMerchant s ON s.commenterId = u.id
    GROUP BY age_group
    ORDER BY age_group
    """
    return query_data(sql)

# e5. 根据角色进行评价习惯分析
def analyze_review_habits_by_role():
    sql = """
    SELECT 
        u.identity AS user_role,
        COUNT(c.id) AS review_count,
        AVG(s.score) AS average_score
    FROM CommentMerchant c
    JOIN User u ON c.commenterId = u.id
    JOIN ScoreMerchant s ON s.commenterId = u.id
    GROUP BY u.identity
    ORDER BY u.identity
    """
    return query_data(sql)

# e6.根据性别进行评价习惯分析
def analyze_review_habits_by_gender():
    sql = """
    SELECT 
        u.sex AS user_gender,
        COUNT(c.id) AS review_count,
        AVG(s.score) AS average_score
    FROM CommentMerchant c
    JOIN User u ON c.commenterId = u.id
    JOIN ScoreMerchant s ON s.commenterId = u.id
    GROUP BY u.sex
    ORDER BY u.sex
    """
    return query_data(sql)

# 未完待续 。。。。。。。。。。