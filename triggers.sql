CREATE OR REPLACE FUNCTION price_change_warning()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.price <> OLD.price THEN
        RAISE NOTICE 'Price of product % has changed from % to %',
            OLD.product_id, OLD.price, NEW.price;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_price_change
AFTER UPDATE OF price
ON Product
FOR EACH ROW
EXECUTE FUNCTION price_change_warning();
