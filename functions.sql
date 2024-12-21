-- Seçilen kategoriden en az belirtilen puana sahip ürünleri getirir. 
CREATE OR REPLACE FUNCTION get_rated_product(
    min_rating_score real, 
    ctgry_id category.category_id%TYPE
)
RETURNS TABLE (
    product_id product.product_id%TYPE,
    product_description product.product_description%TYPE,
    price product.price%TYPE,
    category_name category.category_name%TYPE
) 
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        P.product_id, 
        P.product_description, 
        P.price, 
        C.category_name
    FROM Product P
    JOIN Category C ON P.category_id = C.category_id
    WHERE 
        C.category_id = ctgry_id
        AND (
            SELECT AVG(review_rating)
            FROM REVIEW
            WHERE REVIEW.product_id = P.product_id
        ) >= min_rating_score;
END;
$$ LANGUAGE plpgsql;

-- Son bir ayın en popüler ürünlerini döndürür
CREATE OR REPLACE FUNCTION get_most_popular_products()
RETURNS TABLE (prod_id INT, total_amount INT) AS $$
DECLARE
    rec RECORD; 
    cur CURSOR FOR
        SELECT product_id, COUNT(product_id) AS total_amount
        FROM Order_Product
        WHERE order_id IN (
        	SELECT order_id 
            FROM Order_
            WHERE order_time >= NOW() - INTERVAL '30 days'
			)
        GROUP BY product_id
        ORDER BY total_amount DESC
        LIMIT 5;
BEGIN
    OPEN cur;
    LOOP
        FETCH cur INTO rec;
        EXIT WHEN NOT FOUND;
        prod_id := rec.product_id;
        total_amount := rec.total_amount;
        RETURN NEXT; 
    END LOOP;
    CLOSE cur;
END $$ LANGUAGE plpgsql;
