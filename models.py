from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Admin(db.Model):
    __tablename__ = 'Admins'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, comment='帐号')
    pwd = db.Column(db.String(50), nullable=False, comment='密码')
    add_time = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False, comment='添加时间')

class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_number = db.Column(db.String(50), nullable=False, comment='学号/工号')
    pwd = db.Column(db.String(50), nullable=False, comment='密码')
    name = db.Column(db.String(50), nullable=False, comment='姓名')
    sex = db.Column(db.String(255), nullable=False, comment='性别')
    BirthDate = db.Column(db.Date, nullable=False, comment='年龄')
    add_time = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False, comment='添加时间')

class Merchant(db.Model):
    __tablename__ = 'Merchant'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account = db.Column(db.String(50), nullable=False, comment='账号')
    pwd = db.Column(db.String(50), nullable=False, comment='密码')
    name = db.Column(db.String(255), nullable=False, comment='店家名称')
    address = db.Column(db.String(50), nullable=False, comment='地址')
    add_time = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False, comment='添加时间')

class FoodClassification(db.Model):
    __tablename__ = 'FoodClassification'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False, comment='分类名称')

class Food(db.Model):
    __tablename__ = 'Food'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False, comment='菜品名称')
    classificationId = db.Column(db.Integer, db.ForeignKey('FoodClassification.id'), nullable=False, comment='分类编号')
    picture = db.Column(db.String(255), nullable=False, comment='菜品图片')
    score = db.Column(db.Numeric(18, 2), nullable=False, comment='评分')
    price = db.Column(db.Numeric(18, 2), nullable=False, comment='价格')
    sales_volume = db.Column(db.Integer, nullable=False, comment='销量')
    description = db.Column(db.Text, nullable=False, comment='菜品描述')
    nutrition = db.Column(db.Text, nullable=False, comment='菜品营养')
    ingredient = db.Column(db.Text, nullable=False, comment='菜品成分')
    allergy = db.Column(db.Text, nullable=False, comment='菜品过敏源')
    MerchantId = db.Column(db.Integer, db.ForeignKey('Merchant.id'), nullable=False, comment='发布商户编号')
    add_time = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False, comment='添加时间')

class UserOrder(db.Model):
    __tablename__ = 'UserOrder'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    detail = db.Column(db.Text, nullable=False, comment='订单信息')
    price_amount = db.Column(db.Numeric(18, 2), nullable=False, comment='订单金额')
    userId = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False, comment='下单人')
    merchantId = db.Column(db.Integer, db.ForeignKey('Merchant.id'), nullable=False, comment='下单商户')
    status = db.Column(db.String(50), nullable=False, comment='状态')
    is_paid = db.Column(db.String(10), nullable=False, default='否', comment='是否支付')
    add_time = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False, comment='添加时间')

class OrderFood(db.Model):
    __tablename__ = 'OrderFood'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    orderId = db.Column(db.Integer, db.ForeignKey('UserOrder.id'), nullable=False, comment='订单ID')
    foodId = db.Column(db.Integer, db.ForeignKey('Food.id'), nullable=False, comment='菜品信息ID')
    number = db.Column(db.Integer, nullable=False, comment='购买数量')
    add_time = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False, comment='添加时间')

class UserFavoriteMerchant(db.Model):
    __tablename__ = 'UserFavoriteMerchant'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    merchantId = db.Column(db.Integer, db.ForeignKey('Merchant.id'), nullable=False, comment='商户id')
    userId = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False, comment='收藏人id')
    add_time = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False, comment='添加时间')

class UserFavoriteDish(db.Model):
    __tablename__ = 'UserFavoriteDish'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    foodId = db.Column(db.Integer, db.ForeignKey('Food.id'), nullable=False, comment='菜品id')
    userId = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False, comment='收藏人id')
    add_time = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False, comment='添加时间')

class Message(db.Model):
    __tablename__ = 'Message'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    orderId = db.Column(db.Integer, db.ForeignKey('UserOrder.id'), nullable=False, comment='订单ID')
    content = db.Column(db.Text, nullable=False, comment='消息信息')
    userId = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False, comment='下单人')
    status = db.Column(db.String(50), nullable=False, comment='状态')
    merchantId = db.Column(db.Integer, db.ForeignKey('Merchant.id'), nullable=False, comment='店家')
    add_time = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False, comment='添加时间')

class CommentMerchant(db.Model):
    __tablename__ = 'CommentMerchant'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    merchantId = db.Column(db.Integer, db.ForeignKey('Merchant.id'), nullable=False, comment='商户id')
    content = db.Column(db.Text, nullable=False, comment='评论内容')
    commenterId = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False, comment='评论人id')
    orderId = db.Column(db.Integer, db.ForeignKey('UserOrder.id'), nullable=False, comment='订单id')
    add_time = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False, comment='添加时间')

class CommentFood(db.Model):
    __tablename__ = 'CommentFood'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    foodId = db.Column(db.Integer, db.ForeignKey('Food.id'), nullable=False, comment='菜品id')
    content = db.Column(db.Text, nullable=False, comment='评论内容')
    commenterId = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False, comment='评论人id')
    orderId = db.Column(db.Integer, db.ForeignKey('UserOrder.id'), nullable=False, comment='订单id')
    add_time = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False, comment='添加时间')

class ScoreMerchant(db.Model):
    __tablename__ = 'ScoreMerchant'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    merchantId = db.Column(db.Integer, db.ForeignKey('Merchant.id'), nullable=False, comment='商户id')
    score = db.Column(db.Numeric(18, 2), nullable=False, comment='评分')
    commenterId = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False, comment='评论人id')
    orderId = db.Column(db.Integer, db.ForeignKey('UserOrder.id'), nullable=False, comment='订单id')
    add_time = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False, comment='添加时间')

class ScoreFood(db.Model):
    __tablename__ = 'ScoreFood'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    foodId = db.Column(db.Integer, db.ForeignKey('Food.id'), nullable=False, comment='菜品id')
    score = db.Column(db.Numeric(18, 2), nullable=False, comment='评分')
    commenterId = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False, comment='评论人id')
    orderId = db.Column(db.Integer, db.ForeignKey('UserOrder.id'), nullable=False, comment='订单id')
    add_time = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False, comment='添加时间')
