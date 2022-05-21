-- SQLite



-- SQLite


-- データの形は
--


-- データベースの種類
--１．レア度　色（参照）　
--２．練習属性（参照）
--３．サポカ（参照）
--４．DB　キャラ（ランキングからほぼ毎日記録していく）１５×？　ランキングなので、最大１５００　毎日削除（or　出力）
--５．DB　カード関連性（それぞれのカードで、別のカードがどれくらい使われているかを見る）
--６．DB　カード関連性２　（４のやつを、1枚ごとに、当日-3日-1週間-1ヵ月　の4種類作って、集計する）SSRとSRの数×４


--　ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
--１．レア度　色（参照）

-- CREATE TABLE Rarity(
-- 	grade varchar,
-- 	R integer,G integer,B integer
-- );

-- INSERT INTO Rarity (grade, R,G,B) VALUES ("SSR",213,191,240);
-- INSERT INTO Rarity (grade, R,G,B) VALUES ("SR",255,226,146);

-- DELETE FROM Rarity WHERE grade = "SR";

--　ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
--２．練習属性（参照）

-- CREATE TABLE Training(
-- 	type varchar,
-- 	R integer,G integer,B integer
-- );

-- INSERT INTO Training (type, R,G,B) VALUES ("speed",113,205,255);
-- INSERT INTO Training (type, R,G,B) VALUES ("wise",156,234,209);
-- INSERT INTO Training (type, R,G,B) VALUES ("stamina",255,183,173);
-- INSERT INTO Training (type, R,G,B) VALUES ("Partner",255,214,114);
-- INSERT INTO Training (type, R,G,B) VALUES ("guts",255,155,190);
-- INSERT INTO Training (type, R,G,B) VALUES ("power",255,190,81);



--　ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
--３．サポカ（参照）

-- CREATE TABLE Support_Card(
-- 	id INTEGER PRIMARY KEY AUTOINCREMENT,
-- 	name varchar,
-- 	grade varchar,
-- 	type varchar,
-- 	R integer,G integer,B integer,
-- 	R2 integer,G2 integer,B2 integer
-- );




-- INSERT INTO Support_Card (name, grade, type, R,G,B,R2,G2,B2) VALUES ("test1", "SSR", "speed",11,21,31,12,32,37);
-- INSERT INTO Support_Card (name, grade, type, R,G,B,R2,G2,B2) VALUES ("test22", "SR", "stamina",41,51,61,12,32,36);
-- INSERT INTO Support_Card (name, grade, type, R,G,B,R2,G2,B2) VALUES ("test333", "SSR", "speed",71,81,91,11,24,53);
-- INSERT INTO Support_Card (name, grade, type, R,G,B,R2,G2,B2) VALUES ("test4444", "SR", "power",99,81,94,22,34,43);

-- INSERT INTO Support_Card (name, grade, type, R,G,B,R2,G2,B2) VALUES ("test5", "SSR", "speed",11,21,31,12,222,111);
-- INSERT INTO Support_Card (name, grade, type, R,G,B,R2,G2,B2) VALUES ("test6", "SR", "power",213,213,207,225,190,186);
-- INSERT INTO Support_Card (name, grade, type, R,G,B,R2,G2,B2) VALUES ("test7", "SR", "speed",157,124,101,184,71,96);
-- INSERT INTO Support_Card (name, grade, type, R,G,B,R2,G2,B2) VALUES ("test8", "SSR", "speed",222,124,88,195,118,153);


--テーブルの中身をすべて削除（ただし、データが多いと重い）
--DELETE FROM Support_Card;

--　ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
--４．DB　キャラ（ランキングからほぼ毎日記録していく）１５×？　ランキングなので、最大１５００　毎日削除（or　出力）

-- ①番号ー②ランクー
-- ③ポジションー
-- ④育成キャラ名ー
-- ⑤サポートカード番号１ー⑥２－⑦３－⑧４－⑨５－⑩フレンド
-- ⑪登録日付
--　ランクとポジションは、絶対ではない。

-- CREATE TABLE Ranking_Data(
-- 	Num INTEGER PRIMARY KEY AUTOINCREMENT,
-- 	rank varcher,
-- 	position varcher,
-- 	character_name varchar,
-- 	SP_Card_1 integer,
-- 	SP_Card_2 integer,
-- 	SP_Card_3 integer,
-- 	SP_Card_4 integer,
-- 	SP_Card_5 integer,
-- 	SP_Card_6 integer,
-- 	Date_Day default CURRENT_TIMESTAMP
-- );


-- DELETE FROM Ranking_Data;


--　ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
--５．DB　カード利用率（それぞれのカードで、別のカードがどれくらい使われているかを見る）

-- 列と行が増えていく
-- 列と行には、IDが入る。
--　列と同じ数の行は何も入らないようにする（自分なので）

--テーブル削除
--DROP TABLE Use_rate;

-- CREATE TABLE Use_rate(
--     name varcher
-- );


--　ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
--６．DB　カード利用率２　（４のやつを、1枚ごとに、当日-3日-1週間-1ヵ月　の4種類作って、集計する）SSRとSRの数×４



--　ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー

--練習
--INSERT INTO Training (type, C_value) VALUES ("power","255-190-81");



--インサート
--INSERT INTO Training (type, C_value) VALUES ("testttt","111-222-333");

--INSERT INTO Support_Card (name, C_value) VALUES ("aaaa111","333-222-333");

--INSERT INTO Support_Card (name, C_value) VALUES ("test3","111-232-333/444-555-666");


--削除
-- DELETE FROM Support_Card WHERE id=4;

--テーブル削除
--DROP TABLE テーブル名;

-- DROP TABLE tmp_sptb;



--SELECT * FROM Rarity;
--SELECT * FROM Use_rate;





--insert into Support_Card (name) VALUES('test')



-- UPDATE テーブル名
--    SET 列名 = 変更内容, ...
--  WHERE 条件式;

--レコード更新処理

--SELECT 101001 FROM Use_rate WHERE name ='101004';
        --行                      --列

--SELECT R FROM Rarity WHERE grade='SSR';

--SELECT '103002' FROM Use_rate WHERE name = 101003;

--列名に数字を使用することはできない！！！！
-- SELECT R_103002 FROM Use_rate WHERE name = 'G_101003';

--SELECT position,character_name,SP_Card_1,SP_Card_2,SP_Card_3,SP_Card_4,SP_Card_5,SP_Card_6 FROM Ranking_Data;

--SELECT 'R_101001' FROM Use_rate WHERE name ='G_101001';

--SELECT R_101002 FROM Use_rate WHERE name ='G_101001';



--UPDATE Use_rate SET '103002' = 1 WHERE name = 101003;
                        --列　　　　　　　　　行














-----------------------------------------------------------------------------------------------------------


-- -- ///////////////////　↓　初期化処///////////////////

-- --テーブル削除
-- DROP TABLE Use_rate;

-- CREATE TABLE Use_rate(
--     name varcher
-- );

-- --テーブルの中身をすべて削除（ただし、データが覆いと重い）
-- DELETE FROM Support_Card;
-- DELETE FROM Ranking_Data;


-- -- ///////////////////　↑　初期化処///////////////////



-- INSERT INTO Support_Card (name, grade, type, R,G,B,R2,G2,B2) VALUES ("101001", "SSR", "speed",11,21,31,12,32,37);
-- ALTER TABLE Use_rate ADD '101001' int NOT NULL DEFAULT 0;
-- INSERT INTO Use_rate (name) VALUES ('101001');
-- DELETE FROM Support_Card WHERE id=101001;



