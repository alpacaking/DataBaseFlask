DELIMITER //

-- 更新食物评分
CREATE TRIGGER update_food_score
AFTER INSERT ON ScoreFood
FOR EACH ROW
BEGIN
    DECLARE avg_score DECIMAL(5, 2);
    -- 计算新平均分
    SELECT AVG(score) INTO avg_score FROM ScoreFood WHERE foodId = NEW.foodId;
    -- 更新食物评分
    UPDATE Food SET score = avg_score WHERE id = NEW.foodId;
END//


-- 更新食物销量
CREATE TRIGGER update_food_sales
AFTER INSERT ON UserOrder
FOR EACH ROW
BEGIN
    -- 更新食物的销量
    UPDATE Food SET sales_volume = sales_volume + 1 WHERE id = NEW.foodId;
END//

DELIMITER ;
