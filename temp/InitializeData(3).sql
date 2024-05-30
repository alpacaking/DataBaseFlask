-- 插入 Admins 数据
INSERT INTO Admins (username, pwd) VALUES
('admin', 'adminpwd');

-- 插入 User 数据
INSERT INTO User (identity, student_number, pwd, name, sex, BirthDate) VALUES
('学生', '2021001', 'userpwd1', '张三', '男', '2000-01-01'),
('教职工', '2021002', 'userpwd2', '李四', '女', '1999-02-02'),
('学生', '2021003', 'userpwd3', '王五', '男', '2001-03-03');

-- 插入 Merchant 数据
INSERT INTO Merchant (account, pwd, name, address) VALUES
('merchant1', 'pwd123', '川味馆', '北京市海淀区'),
('merchant2', 'pwd123', '美食坊', '上海市浦东新区'),
('merchant3', 'pwd123', '湘菜馆', '湖南省长沙市');

-- 插入 FoodClassification 数据
INSERT INTO FoodClassification (name) VALUES
('川菜'), ('粤菜'), ('鲁菜'), ('苏菜'), ('湘菜'), ('闽菜'), ('浙菜'), ('徽菜');

-- 插入 Food 数据
INSERT INTO Food (name, classificationId, picture, score, price, sales_volume, description, nutrition, ingredient, allergy, MerchantId, is_deleted) VALUES
('宫保鸡丁', 1, 'gongbao.jpg', 4.5, 38.00, 120, '经典川菜，口感鲜香', '高蛋白质', '鸡肉, 花生', '花生过敏者慎食', 1, 0),
('麻婆豆腐', 1, 'mapo.jpg', 4.2, 28.00, 150, '麻辣鲜香', '植物蛋白', '豆腐, 辣椒', '无', 1, 0),
('水煮鱼', 1, 'shuizhu.jpg', 4.8, 58.00, 100, '香辣可口', '高蛋白质', '鱼, 辣椒', '鱼类过敏者慎食', 1, 0),
('清蒸鲈鱼', 2, 'luyu.jpg', 4.8, 68.00, 80, '清淡健康，肉质鲜美', '高蛋白质', '鲈鱼', '鱼类过敏者慎食', 2, 0),
('广式烧鹅', 2, 'shaoge.jpg', 4.6, 88.00, 70, '外皮酥脆，肉质鲜嫩', '高蛋白质', '鹅肉', '无', 2, 0),
('糖醋排骨', 3, 'tangcu.jpg', 4.5, 48.00, 90, '酸甜可口', '高蛋白质', '猪排骨', '无', 3, 0),
('红烧狮子头', 3, 'shizitou.jpg', 4.7, 38.00, 85, '软糯鲜香', '高蛋白质', '猪肉', '无', 3, 0),
('剁椒鱼头', 5, 'duojiao.jpg', 4.7, 68.00, 95, '鲜辣入味', '高蛋白质', '鱼头', '鱼类过敏者慎食', 3, 0),
('东坡肉', 6, 'dongpo.jpg', 4.8, 58.00, 110, '肥而不腻', '高蛋白质', '猪肉', '无', 3, 0),
('叫花鸡', 7, 'jiaohua.jpg', 4.9, 78.00, 65, '香嫩多汁', '高蛋白质', '鸡肉', '无', 2, 0);

-- 插入 UserOrder 数据
INSERT INTO UserOrder (detail, foodid,price_amount, userId, merchantId, status, is_paid) VALUES
('宫保鸡丁, 微辣, 少盐', 1, 38.00, 1, 1, '已完成', '是'),
('清蒸鲈鱼, 加姜丝', 4, 68.00, 2, 2, '已完成', '是'),
('宫保鸡丁, 多放花生', 1, 38.00, 2, 1, '已完成', '否'),
('麻婆豆腐, 多加辣', 2, 28.00, 3, 1, '已完成', '是'),
('剁椒鱼头, 少辣', 8, 68.00, 3, 3, '已完成', '否'),
('东坡肉, 少油', 9, 58.00, 1, 3, '已完成', '是'),
('红烧狮子头, 正常', 7, 38.00, 2, 3, '已完成', '是'),
('糖醋排骨, 多糖', 6, 48.00, 1, 3, '已完成', '否');

-- 插入 UserFavoriteMerchant 数据
INSERT INTO UserFavoriteMerchant (merchantId, userId) VALUES
(1, 1), (2, 1), (2, 2), (3, 3);

-- 插入 UserFavoriteDish 数据
INSERT INTO UserFavoriteDish (foodId, userId) VALUES
(1, 1), (2, 1), (2, 2), (3, 3), (4, 1), (5, 2), (6, 3);

-- 插入 Message 数据
INSERT INTO Message (orderId, content, userId, status, merchantId) VALUES
(1, '请尽快送达', 1, '已读', 1),
(2, '请提供发票', 2, '未读', 2),
(3, '请多放些花生', 2, '已读', 1),
(4, '多加辣椒', 3, '未读', 1);

-- 插入 CommentMerchant 数据
INSERT INTO CommentMerchant (merchantId, content, commenterId, orderId) VALUES
(1, '味道很好，服务周到', 1, 1),
(2, '环境干净整洁', 2, 2),
(3, '菜品丰富多样', 3, 3);

-- 插入 CommentFood 数据
INSERT INTO CommentFood (foodId, content, commenterId, orderId) VALUES
(1, '味道不错，但有点咸', 1, 1),
(2, '鱼很新鲜，值得推荐', 2, 2),
(3, '麻婆豆腐特别入味', 3, 4);

-- 插入 ScoreMerchant 数据
INSERT INTO ScoreMerchant (merchantId, score, commenterId, orderId) VALUES
(1, 4.5, 1, 1),
(2, 4.8, 2, 2),
(3, 4.7, 3, 3);

-- 插入 ScoreFood 数据
INSERT INTO ScoreFood (foodId, score, commenterId, orderId) VALUES
(1, 4.0, 1, 1),
(2, 5.0, 2, 2),
(3, 4.2, 3, 4),
(4, 4.7, 2, 3),
(5, 4.8, 1, 5),
(6, 4.5, 3, 6),
(7, 4.6, 2, 7),
(8, 4.7, 1, 8);
