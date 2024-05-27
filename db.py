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
        database="python_mysql",
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


#尝试执行
if __name__ == "__main__":
    sql = "insert user (name,sex,age,email) values ('xishi','man',98,'xigshi@qq.com')"
    insert_or_update_data(sql)
    sql = "select * from user"
    datas = query_data(sql)
    pprint.pprint(datas)

