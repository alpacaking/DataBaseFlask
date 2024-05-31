-- User 表索引
CREATE INDEX idx_user_student_number ON User(student_number);
CREATE INDEX idx_user_identity ON User(identity);

-- Merchant 表索引
CREATE INDEX idx_merchant_account ON Merchant(account);
CREATE INDEX idx_merchant_name ON Merchant(name);

-- Food 表索引
CREATE INDEX idx_food_merchantId ON Food(merchantId);
CREATE INDEX idx_food_name ON Food(name);

-- UserOrder 表索引
CREATE INDEX idx_userorder_userId ON UserOrder(userId);
CREATE INDEX idx_userorder_merchantId ON UserOrder(merchantId);
CREATE INDEX idx_userorder_status ON UserOrder(status);
CREATE INDEX idx_userorder_foodId ON UserOrder(foodId);

-- CommentFood 表索引
CREATE INDEX idx_commentfood_foodId ON CommentFood(foodId);

-- ScoreFood 表索引
CREATE INDEX idx_scorefood_foodId ON ScoreFood(foodId);

-- CommentMerchant 表索引
CREATE INDEX idx_commentmerchant_merchantId ON CommentMerchant(merchantId);

-- ScoreMerchant 表索引
CREATE INDEX idx_scoremerchant_merchantId ON ScoreMerchant(merchantId);
