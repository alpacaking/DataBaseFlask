CREATE TABLE `Admins` (
                          `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
                          `username` varchar(50) NOT NULL COMMENT '帐号',
                          `pwd` varchar(50) NOT NULL COMMENT '密码',
                          `add_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '添加时间',
                          PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

CREATE TABLE `User` (
                        `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
                        `student_number` varchar(50) NOT NULL COMMENT '学号/工号',
                        `pwd` varchar(50) NOT NULL COMMENT '密码',
                        `name` varchar(50) NOT NULL COMMENT '姓名',
                        `sex ` varchar(255) NOT NULL COMMENT '性别',
                        `BirthDate` date NOT NULL COMMENT '年龄',
                        `add_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '添加时间',
                        PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

CREATE TABLE `Merchant` (
                            `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
                            `account` varchar(50) NOT NULL COMMENT '账号',
                            `pwd` varchar(50) NOT NULL COMMENT '密码',
                            `name` varchar(255) NOT NULL COMMENT '店家名称',
                            `address` varchar(50) NOT NULL COMMENT '地址',
                            `add_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '添加时间',
                            PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

CREATE TABLE `FoodClassification` (
                                      `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
                                      `name` varchar(255) NOT NULL COMMENT '分类名称',
                                      PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

CREATE TABLE `Food` (
                        `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
                        `name` varchar(255) NOT NULL COMMENT '菜品名称',
                        `classificationId` int(10) unsigned NOT NULL COMMENT '分类编号',
                        `picture` varchar(255) NOT NULL COMMENT '菜品图片',
                        `score` decimal(18,2) NOT NULL COMMENT '评分',
                        `price` decimal(18,2) NOT NULL COMMENT '价格',
                        `sales_volume` int(11) NOT NULL COMMENT '销量',
                        `description` longtext NOT NULL COMMENT '菜品描述',
                        `nutrition` longtext NOT NULL COMMENT '菜品营养',
                        `ingredient` longtext NOT NULL COMMENT '菜品成分',
                        `allergy` longtext NOT NULL COMMENT '菜品过敏源',
                        `MerchantId` int(10) unsigned NOT NULL COMMENT '发布商户编号',
                        `add_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '添加时间',
                        PRIMARY KEY (`id`),
                        FOREIGN KEY (classificationId) REFERENCES FoodClassification(id),
                        FOREIGN KEY (MerchantId) REFERENCES Merchant(id)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;



CREATE TABLE `UserOrder` (
                             `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
                             `detail` text NOT NULL COMMENT '订单信息',
                             `price_amount` decimal(18,2) NOT NULL COMMENT '订单金额',
                             `userId` int(10) unsigned NOT NULL COMMENT '下单人',
                             `merchantId` int(10) unsigned NOT NULL COMMENT '下单商户',
                             `status` varchar(50) NOT NULL COMMENT '状态',
                             `is_paid` varchar(10) NOT NULL DEFAULT '否' COMMENT '是否支付',
                             `add_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '添加时间',
                             PRIMARY KEY (`id`),
                             FOREIGN KEY (userId) REFERENCES User(id),
                             FOREIGN KEY (merchantId) REFERENCES Merchant(id)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;

CREATE TABLE `OrderFood` (
                             `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
                             `orderId` int(10) unsigned NOT NULL COMMENT '订单ID',
                             `foodId` int(10) unsigned NOT NULL COMMENT '菜品信息ID',
                             `number` int(11) NOT NULL COMMENT '购买数量',
                             `add_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '添加时间',
                             PRIMARY KEY (`id`),
                             FOREIGN KEY (orderId) REFERENCES UserOrder(id),
                             FOREIGN KEY (foodId) REFERENCES Food(id)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;

CREATE TABLE `UserFavoriteMerchant` (
                                        `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
                                        `merchantId` int(10) unsigned NOT NULL COMMENT '商户id',
                                        `userId` int(10) unsigned NOT NULL COMMENT '收藏人id',
                                        `add_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '添加时间',
                                        PRIMARY KEY (`id`),
                                        FOREIGN KEY (merchantId) REFERENCES Merchant(id),
                                        FOREIGN KEY (userId) REFERENCES User(id)
) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=utf8;

CREATE TABLE `UserFavoriteDish` (
                                    `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
                                    `foodId` int(10) unsigned NOT NULL COMMENT '菜品id',
                                    `userId` int(10) unsigned NOT NULL COMMENT '收藏人id',
                                    `add_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '添加时间',
                                    PRIMARY KEY (`id`),
                                    FOREIGN KEY (foodId) REFERENCES Food(id),
                                    FOREIGN KEY (userId) REFERENCES User(id)
) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=utf8;

CREATE TABLE `Message` (
                           `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
                           `orderId` int(10) unsigned NOT NULL COMMENT '订单ID',
                           `content` text NOT NULL COMMENT '消息信息',
                           `userId` int(10) unsigned NOT NULL COMMENT '下单人',
                           `status` varchar(50) NOT NULL COMMENT '状态',
                           `merchantId` varchar(50) NOT NULL COMMENT '店家',
                           `add_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '添加时间',
                           PRIMARY KEY (`id`),
                           FOREIGN KEY (orderId) REFERENCES UserOrder(id),
                           FOREIGN KEY (userId) REFERENCES User(id),
                           FOREIGN KEY (merchantId) REFERENCES Merchant(id)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;

CREATE TABLE `CommentMerchant` (
                                   `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
                                   `merchantId` int(10) unsigned NOT NULL COMMENT '商户id',
                                   `content` text NOT NULL COMMENT '评论内容',
                                   `commenterId` int(10) unsigned NOT NULL COMMENT '评论人id',
                                   `orderId` int(10) unsigned NOT NULL COMMENT '订单id',
                                   `add_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '添加时间',
                                   PRIMARY KEY (`id`),
                                   FOREIGN KEY (orderId) REFERENCES UserOrder(id),
                                   FOREIGN KEY (merchantId) REFERENCES Merchant(id),
                                   FOREIGN KEY (commenterId) REFERENCES User(id)
) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=utf8;

CREATE TABLE `CommentFood` (
                               `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
                               `foodId` int(10) unsigned NOT NULL COMMENT '菜品id',
                               `content` text NOT NULL COMMENT '评论内容',
                               `commenterId` int(10) unsigned NOT NULL COMMENT '评论人id',
                               `orderId` int(10) unsigned NOT NULL COMMENT '订单id',
                               `add_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '添加时间',
                               PRIMARY KEY (`id`),
                               FOREIGN KEY (orderId) REFERENCES UserOrder(id),
                               FOREIGN KEY (foodId) REFERENCES Food(id),
                               FOREIGN KEY (commenterId) REFERENCES User(id)
) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=utf8;

CREATE TABLE `ScoreMerchant` (
                                 `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
                                 `merchantId` int(10) unsigned NOT NULL COMMENT '商户id',
                                 `score` decimal(18,2) NOT NULL COMMENT '评分',
                                 `commenterId` int(10) unsigned NOT NULL COMMENT '评论人id',
                                 `orderId` int(10) unsigned NOT NULL COMMENT '订单id',
                                 `add_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '添加时间',
                                 PRIMARY KEY (`id`),
                                 FOREIGN KEY (orderId) REFERENCES UserOrder(id),
                                 FOREIGN KEY (merchantId) REFERENCES Merchant(id),
                                 FOREIGN KEY (commenterId) REFERENCES User(id)
) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=utf8;

CREATE TABLE `ScoreFood` (
                             `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
                             `foodId` int(10) unsigned NOT NULL COMMENT '菜品id',
                             `score` decimal(18,2) NOT NULL COMMENT '评分',
                             `commenterId` int(10) unsigned NOT NULL COMMENT '评论人id',
                             `orderId` int(10) unsigned NOT NULL COMMENT '订单id',
                             `add_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '添加时间',
                             PRIMARY KEY (`id`),
                             FOREIGN KEY (orderId) REFERENCES UserOrder(id),
                             FOREIGN KEY (foodId) REFERENCES Food(id),
                             FOREIGN KEY (commenterId) REFERENCES User(id)
) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=utf8;

DELIMITER //
CREATE TRIGGER check_order_merchant_before_insert
    BEFORE INSERT ON OrderFood
    FOR EACH ROW
BEGIN
    DECLARE order_merchant_id INT;
    DECLARE food_merchant_id INT;

    SELECT merchantId INTO order_merchant_id
    FROM UserOrder
    WHERE id = NEW.orderId;

    SELECT merchantId INTO food_merchant_id
    FROM Food
    WHERE id = NEW.foodId;

    IF order_merchant_id != food_merchant_id THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Food merchant does not match with UserOrder merchant.';
    END IF;
END;//
DELIMITER ;

