--CUSTOMER
INSERT INTO Customer (customer_id, customer_name, password, address, mail_address, phone_number) VALUES
(1, 'Ahmet Yılmaz', 'parola', 'Istanbul, Turkey', 'ahmet.yilmaz@example.com', '555-123-4567'),
(2, 'Ayşe Demir', 'parola', 'Ankara, Turkey', 'ayse.demir@example.com', '555-987-6543'),
(3, 'Mehmet Öz', 'parola', 'Izmir, Turkey', 'mehmet.oz@example.com', '555-543-2198'),
(4, 'Ahmet Kaya', 'mypassword123', 'Bursa, Turkey', 'ahmet.kaya@example.com', '555-888-4321'),
(5, 'Ali Can', 'pass987654', 'Antalya, Turkey', 'ali.can@example.com', '555-222-8765'),
(6, 'Veli Aydın', 'mypassword654', 'Konya, Turkey', 'veli.aydin@example.com', '555-333-1234'),
(7, 'Zeynep Kılıç', 'zey12345', 'Adana, Turkey', 'zeynep.kilic@example.com', '555-444-5678'),
(8, 'Fatma Gül', 'securepass123', 'Trabzon, Turkey', 'fatma.gul@example.com', '555-555-9012'),
(9, 'Mehmet Ali', 'alipass890', 'Eskişehir, Turkey', 'mehmet.ali@example.com', '555-666-2345'),
(10, 'Seda Yılmaz', 'seda0987', 'Mersin, Turkey', 'seda.yilmaz@example.com', '555-777-3456');

--SELLER 
INSERT INTO Seller (seller_ssn, seller_name, password, address, mail_address, phone_number) VALUES
('123-45-6789', 'Elif Kaya', 'parola', 'Istanbul, Turkey', 'elif.kaya@example.com', '555-345-6789'),
('987-65-4321', 'Ali Çelik', 'parola', 'Bursa, Turkey', 'ali.celik@example.com', '555-678-1234'),
('456-78-9012', 'Zeynep Aydın', 'parola', 'Antalya, Turkey', 'zeynep.aydin@example.com', '555-789-3456'),
('234-56-7890', 'Fatma Arslan', 'fatmapass456', 'Izmir, Turkey', 'fatma.arslan@example.com', '555-234-5678'),
('345-67-8901', 'Veli Kılıç', 'velipassword321', 'Konya, Turkey', 'veli.kilic@example.com', '555-345-6789'),
('567-89-0123', 'Mehmet Can', 'mehmetpass654', 'Antalya, Turkey', 'mehmet.can@example.com', '555-456-7890'),
('678-90-1234', 'Seda Gül', 'sedapass890', 'Adana, Turkey', 'seda.gul@example.com', '555-567-8901'),
('789-01-2345', 'Ahmet Yılmaz', 'ahmetpass234', 'Bursa, Turkey', 'ahmet.yilmaz@example.com', '555-678-9012'),
('890-12-3456', 'Ayşe Demir', 'aysepassword987', 'Mersin, Turkey', 'ayse.demir@example.com', '555-789-0123'),
('901-23-4567', 'Zeynep Öz', 'zeynep123secure', 'Eskişehir, Turkey', 'zeynep.oz@example.com', '555-890-1234');

-- CATEGORY
-- Insert main categories
INSERT INTO Category (category_id, category_name, parent_category_id) VALUES (1, 'Ev Dekorasyonu', NULL);
INSERT INTO Category (category_id, category_name, parent_category_id) VALUES (2, 'Takılar ve Aksesuarlar', NULL);
INSERT INTO Category (category_id, category_name, parent_category_id) VALUES (3, 'Kıyafetler ve Tekstil Ürünleri', NULL);
INSERT INTO Category (category_id, category_name, parent_category_id) VALUES (4, 'Oyuncaklar ve Bebek Ürünleri', NULL);
INSERT INTO Category (category_id, category_name, parent_category_id) VALUES (5, 'Mutfak Gereçleri', NULL);
INSERT INTO Category (category_id, category_name, parent_category_id) VALUES (6, 'Sanatsal Ürünler', NULL);
INSERT INTO Category (category_id, category_name, parent_category_id) VALUES (7, 'Doğal ve Organik Ürünler', NULL);
INSERT INTO Category (category_id, category_name, parent_category_id) VALUES (8, 'Hediyelik Eşyalar', NULL);
INSERT INTO Category (category_id, category_name, parent_category_id) VALUES (9, 'Kâğıt ve Kitap Sanatları', NULL);

-- Insert subcategories for 'Ev Dekorasyonu'
INSERT INTO Category (category_id, category_name, parent_category_id) VALUES (10, 'Ahşap Oymacılık', 1);
INSERT INTO Category (category_id, category_name, parent_category_id) VALUES (11, 'El Dokuması Kilimler', 1);
INSERT INTO Category (category_id, category_name, parent_category_id) VALUES (12, 'Seramik Vazolar', 1);

-- Insert subcategories for 'Takılar ve Aksesuarlar'
INSERT INTO Category (category_id, category_name, parent_category_id) VALUES (13, 'Kolye ve Küpeler', 2);
INSERT INTO Category (category_id, category_name, parent_category_id) VALUES (14, 'Doğal Taş Aksesuarlar', 2);

-- Insert subcategories for 'Kıyafetler ve Tekstil Ürünleri'
INSERT INTO Category (category_id, category_name, parent_category_id) VALUES (15, 'El Dokuması Şallar', 3);
INSERT INTO Category (category_id, category_name, parent_category_id) VALUES (16, 'El İşlemesi Masa Örtüleri', 3);

-- Insert subcategories for 'Oyuncaklar ve Bebek Ürünleri'
INSERT INTO Category (category_id, category_name, parent_category_id) VALUES (17, 'Ahşap Oyuncaklar', 4);
INSERT INTO Category (category_id, category_name, parent_category_id) VALUES (18, 'Keçe Bebekler', 4);

-- Insert subcategories for 'Doğal ve Organik Ürünler'
INSERT INTO Category (category_id, category_name, parent_category_id) VALUES (19, 'Sabunlar ve Mumlar', 7);
INSERT INTO Category (category_id, category_name, parent_category_id) VALUES (20, 'El Yapımı Kozmetik Ürünleri', 7);

-- Insert subcategories for 'Kâğıt ve Kitap Sanatları'
INSERT INTO Category (category_id, category_name, parent_category_id) VALUES (21, 'El Yapımı Defterler', 9);
INSERT INTO Category (category_id, category_name, parent_category_id) VALUES (22, 'Kağıt Kesme Sanatı Ürünleri', 9);

--PRODUCT
INSERT INTO Product (product_id, product_description, product_amount, price, category_id) VALUES 
(1, 'El yapımı ahşap tablo', 10, 250.00, 1),
(2, 'Modern dekoratif lambader', 15, 320.00, 1),
(3, 'Oyma işlemeli sandık', 5, 400.00, 10),
(4, 'Ahşap kuş evi', 8, 150.00, 10),
(5, 'Kırmızı el dokuması kilim', 12, 600.00, 11),
(6, 'Mavi el dokuması kilim', 10, 650.00, 11),
(7, 'Çiçek desenli seramik vazo', 20, 180.00, 12),
(8, 'Minimalist seramik vazo', 15, 200.00, 12),
(9, 'Altın kaplama kolye', 25, 120.00, 2),
(10, 'Gümüş küpe', 30, 80.00, 2),
(11, 'Doğal taşlı kolye', 15, 100.00, 13),
(12, 'Kehribar taşlı küpe', 10, 140.00, 13),
(13, 'Akik taşlı yüzük', 20, 90.00, 14),
(14, 'Turkuaz taşlı kolye', 18, 110.00, 14),
(15, 'Pamuklu el yapımı şal', 20, 70.00, 3),
(16, 'El örgüsü atkı', 25, 90.00, 3),
(17, 'Doğal kumaş şal', 15, 75.00, 15),
(18, 'Yün şal', 10, 85.00, 15),
(19, 'Beyaz işlemeli masa örtüsü', 8, 200.00, 16),
(20, 'Çiçek desenli masa örtüsü', 10, 220.00, 16),
(21, 'Ahşap tren seti', 12, 150.00, 4),
(22, 'Peluş oyuncak ayı', 20, 100.00, 4),
(23, 'Ahşap yapboz', 15, 120.00, 17),
(24, 'Ahşap blok seti', 10, 130.00, 17),
(25, 'Kız keçe bebek', 18, 60.00, 18),
(26, 'Erkek keçe bebek', 18, 60.00, 18),
(27, 'Lavanta sabunu', 40, 30.00, 7),
(28, 'Balmumu mum', 25, 50.00, 7),
(29, 'Gül sabunu', 30, 35.00, 19),
(30, 'Vanilya kokulu mum', 20, 45.00, 19),
(31, 'Doğal dudak balmı', 50, 25.00, 20),
(32, 'Doğal el kremi', 30, 40.00, 20),
(33, 'Deri kapaklı defter', 15, 100.00, 9),
(34, 'Kaligrafi başlangıç seti', 10, 150.00, 9),
(35, 'Doğal kağıt defter', 20, 80.00, 21),
(36, 'Kişiye özel defter', 12, 90.00, 21),
(37, 'Çiçekli kağıt kesme motifi', 25, 50.00, 22),
(38, 'Hayvan figürlü kağıt kesme', 20, 60.00, 22);

--ORDER
INSERT INTO Order_ (order_id, order_time, customer_id) VALUES
(1, '2024-12-08 14:30:00', 1),
(2, '2024-12-08 15:00:00', 2),
(3, '2024-12-09 16:00:00', 3),
(4, '2024-12-10 10:00:00', 4),
(5, '2024-12-11 11:30:00', 5),
(6, '2024-12-12 12:00:00', 6),
(7, '2024-12-13 13:00:00', 7),
(8, '2024-12-14 14:30:00', 8),
(9, '2024-12-15 15:00:00', 9),
(10, '2024-12-16 16:00:00', 10);

--ORDER_PRODUCT
INSERT INTO Order_Product (order_id, product_id, order_amount) VALUES
(1, 1, 2),
(1, 3, 1),
(2, 2, 1),
(2, 4, 3),
(3, 5, 2),
(4, 4, 1),
(5, 5, 2),
(6, 6, 1),
(7, 7, 3),
(8, 8, 1),
(9, 9, 2),
(10, 10, 3);

--REVIEW
INSERT INTO Review (customer_id, product_id, review_body, review_rating) VALUES
(1, 1, 'Harika kalite, tekrar alırım!', 5),
(2, 2, 'Güzel ürün, fakat biraz pahalı.', 3),
(3, 3, 'Fiyatına göre iyi kalite.', 4),
(4, 4, 'Harika kuş evi, bahçemde çok güzel duruyor.', 5),
(5, 5, 'Çok güzel el dokuması kilim, çok memnun kaldım!', 4),
(6, 6, 'Tasarımı güzel, ama renkler resimdekilerden biraz farklı.', 3),
(7, 7, 'Çok güzel vazo, çok şık.', 5),
(8, 8, 'Minimalist bir vazo, oturma odamda çok güzel duruyor.', 4),
(9, 9, 'Kolye güzel, ancak biraz hassas hissettiriyor.', 3),
(10, 10, 'Küpe çok güzel ve hafif, bayıldım!', 4);

--sells
INSERT INTO Product_Seller (product_id, seller_ssn) VALUES
(1, '123-45-6789'),
(2, '987-65-4321'),
(3, '456-78-9012'),
(4, '123-45-6789'),
(5, '987-65-4321');


