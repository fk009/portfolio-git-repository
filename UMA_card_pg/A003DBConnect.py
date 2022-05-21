

# データとDBを比較する処理



from os import name
import sqlite3
import sys
import csv #csvファイルをpythonで扱うためのモジュール
import datetime


umamusumeDB_path = 'UMA_card_pg/SQLite_UMA/umamusume.db'

# --------------------------------------------------------------------------------------------------

# データベース接続
class DB_Connection:

    # DBと接続
    def __init__(self):
        self.conn = sqlite3.connect(umamusumeDB_path)
        self.CON = self.conn.cursor()
        #print("DBと接続")

    # インサート+Use_rateDBにも追加
    def SPinsert(self, SP_list):
        print("インサート")
        self.CON = self.conn.cursor()


        inSPnum=0
        rare = 100000
        trai = 1000

        # listで必要なものは？
        # レア・練習・RGB/RGB2

        if SP_list[0] == "SSR":
            rare = rare*1
        elif SP_list[0] == "SR":
            rare = rare*2
        elif SP_list[0] =="R":
            rare = rare*3
        else:
            print("不正な値 「レア」　DB_Connection.SPinsert")

        # トレーニング
        if SP_list[1] == "speed":
            trai = trai*1
        elif SP_list[1] == "stamina":
            trai = trai*2
        elif SP_list[1] =="power":
            trai = trai*3
        elif SP_list[1] =="wise":
            trai = trai*4
        elif SP_list[1] =="guts":
            trai = trai*5
        elif SP_list[1] =="Partner":
            trai = trai*6
        else:
            print("不正な値 「トレーニング」　DB_Connection.SPinsert")

        inSPnum = rare + trai

        # 登録されてるidの数を調べる。
        sqlsearch = "SELECT %s FROM %s WHERE " %("id", "Support_Card")
        sqlsearch += "%d<id AND id<%d" %(inSPnum, inSPnum+1000)
        self.CON.execute(sqlsearch)
        result = self.CON.fetchall()

        print(result)

        if len(result) == 0:
            print("データが存在していません")
            inSPnum += 1
        elif 1<result[0][0]:
            # DBに存在する同じレア・練習のカードIDを調べた後、それに1を足したものをこのカードのIDにする
            result2=[]
            for name in result:
                result2.append(name[0])
            MAX = max(result2)
            inSPnum = MAX + 1

        # RGB と R2G2B2 の値がstr型の[-]で入ってるので、それをsplitしたあと、int型へと変換。
        rgb = SP_list[2].split("-")      # 例）"214-191-239"
        INTrgb =  list(map(int, rgb))       # 例）[214,191,239]
        rgb = SP_list[3].split("-")      # 例）"214-191-239"
        INTrgb2 =  list(map(int, rgb))      # 例）[214,191,239]


        # Use_rateにも新規カードを追加する
        print("Use_rateDBにデータを追加")
        retuname = "R_"+str(inSPnum)
        gyouname = "G_"+str(inSPnum)
        SQL = "ALTER TABLE Use_rate ADD '%s' int NOT NULL DEFAULT 0" %(retuname)
        self.CON.execute(SQL)
        SQL = "INSERT INTO Use_rate (name) VALUES ('%s')" %(gyouname)
        self.CON.execute(SQL)
        self.conn.commit()

        # データベースに追加する。
        sqlinsert = "INSERT INTO Support_Card (id, name, grade, type, R,G,B,R2,G2,B2) "
        sqlinsert += "VALUES (%d, '%s', '%s', '%s',%d,%d,%d,%d,%d,%d)" %(inSPnum, "", SP_list[0], SP_list[1], INTrgb[0],INTrgb[1],INTrgb[2],INTrgb2[0],INTrgb2[1],INTrgb2[2])
        self.CON.execute(sqlinsert)
        self.conn.commit() # コミットする
        self.CON.close()
        return inSPnum # これを使って、切り取った画像に名前をつける

    #ランキングのデータをDBに入れる。
    def rankinginsert(self, splist):
        print("ランキングにデータ挿入")

        self.CON = self.conn.cursor()

        # データベースに追加する。
        ranksql = "INSERT INTO Ranking_Data (rank, position, character_name, SP_Card_1, SP_Card_2, SP_Card_3, SP_Card_4, SP_Card_5, SP_Card_6) "
        ranksql += "VALUES ('%s','%s','%s', %d,%d,%d,%d,%d,%d)" %("", "", "", splist[0], splist[1], splist[2], splist[3], splist[4], splist[5])
        self.CON.execute(ranksql)
        self.conn.commit() # コミットする
        self.CON.close()

    # RGBの値から　レア度とトレーニングを調べる処理
    def RareTradb(self, RGBdate):

        SPlist = RGBdate # 書き換え用のリスト

        # レア度と練習属性の２つ
        for n in range(2):
            if n == 0:
                RETUname = "grade"
                tablename = "Rarity"
            else:
                RETUname = "type"
                tablename = "Training"

            # 6枚のカード
            for i in range(6):
                # RGB が[-]で入ってるので、それをsplitしたあと、int型へと変換。
                rgb = RGBdate[i][n].split("-")      # "214-191-239"
                INTrgb =  list(map(int, rgb)) # [214,191,239]
                # RGBの値から、DBの該当する値を調べる処理
                #       RGBは、-6<x<6までの数字で検索
                # TODO　ここで、あとで、条件にidを加えて、5桁の数字で範囲を指定する。

                sqlsearch = "SELECT %s FROM %s WHERE " %(RETUname, tablename)
                sqlsearch += "%d<R AND R<%d" %(INTrgb[0]-6, INTrgb[0]+6)
                sqlsearch += " AND %d<G AND G<%d" %(INTrgb[1]-6, INTrgb[1]+6)
                sqlsearch += " AND %d<B AND B<%d" %(INTrgb[2]-6, INTrgb[2]+6)
                self.CON.execute(sqlsearch)

                result = self.CON.fetchall() # DBからデータを取得


                # TODO DBでなにもなかった場合エラー
                        # 大きさが違ってもできるかどうかをやってみる！　数値の幅を変えたりして
                if result == []:
                    print("SSの大きさが違う可能性あり。分類できず")
                    sys.exit()


                SPlist[i][n] = result[0][0]

        return SPlist

    # サポートカードを特定する処理
    def SPcarddb(self, RGBdate):

        tablename = "Support_Card"
        SPcardID = []

        # カード６枚分回す
        for i in range(6):
            print("")
            print("●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●")
            print("")
            print("カード　"+ str(i+1) + "　回目")
            print("SPデータベースと照合")
            print(RGBdate[i])

            sqlsearch = "" # これにSQL文を入れる
            SPgrade = RGBdate[i][0] # レア度
            SPtype = RGBdate[i][1]  # 練習属性
            print(SPgrade, SPtype)

            # RGB と R2G2B2 の値がstr型の[-]で入ってるので、それをsplitしたあと、int型へと変換。
            rgb = RGBdate[i][2].split("-")      # 例）"214-191-239"
            INTrgb =  list(map(int, rgb))       # 例）[214,191,239]
            rgb = RGBdate[i][3].split("-")      # 例）"214-191-239"
            INTrgb2 =  list(map(int, rgb))      # 例）[214,191,239]

            # レア度と練習属性で絞り、新しいテーブル(tmp_sptb)を作成する
            sqlsearch = "CREATE TEMPORARY TABLE tmp_sptb AS SELECT * "
            sqlsearch += "FROM %s " %(tablename)
            sqlsearch += "WHERE grade='%s' AND type='%s'" %(SPgrade, SPtype)
            self.CON.execute(sqlsearch)
            # tmp_sptbデータの中身を取ってくる-------------
            sqlsearch = "SELECT * FROM tmp_sptb"
            self.CON.execute(sqlsearch)
            result = self.CON.fetchall() # DBからデータを取得
                #[tmp_sptb]
                # 例）'test1', 'SSR', 'speed', 11, 21, 31, 12, 32, 37)
                #     'test5', 'SSR', 'speed', 11, 21, 31, 12, 222, 111)
            print("")
            print("▽ テーブル１ 絞り込み [grade]　[type]")
            for i in range(len(result)):
                print(result[i])

            # ----------------------------------

            # (tmp_sptb)からカード絵のR,G,Bでサーチをかけて、１回目のサポートカードを特定を試みる
            sqlsearch = "CREATE TEMPORARY TABLE tmp_rgb_tb AS SELECT * FROM tmp_sptb "
            sqlsearch += "WHERE %d<R AND R<%d" %(INTrgb[0]-6, INTrgb[0]+6)
            sqlsearch += " AND %d<G AND G<%d" %(INTrgb[1]-6, INTrgb[1]+6)
            sqlsearch += " AND %d<B AND B<%d" %(INTrgb[2]-6, INTrgb[2]+6)
            self.CON.execute(sqlsearch)
            # ----------------------------------
            # tmp_rgb_tb データの中身を取ってくる--------------
            sqlsearch = "SELECT * FROM tmp_rgb_tb"
            self.CON.execute(sqlsearch)
            RGBresult = self.CON.fetchall() # DBからデータを取得
                #[tmp_rgb_tb]
            print("")
            print("▽ テーブル２ 絞り込み　RGB Card_Serch")
            for i in range(len(RGBresult)):
                print(RGBresult[i])

            # ----------------------------------
            print("データの件数  " + str(len(RGBresult))+"件")
            print("")



            # もしまだ複数のカード候補がある場合、さらなる特定を試みる。
            if 1 < len(RGBresult):
                print("▽ さらに  R2,G2,B2  による絞り込み")
                print("")
                # (tmp_rgb_tb)からカード絵のR2,G2,B2でサーチをかけて、サポートカードを特定を試みる
                sqlsearch = "SELECT id FROM tmp_rgb_tb "
                sqlsearch += "WHERE %d<R2 AND R2<%d" %(INTrgb2[0]-6, INTrgb2[0]+6)
                sqlsearch += " AND %d<G2 AND G2<%d" %(INTrgb2[1]-6, INTrgb2[1]+6)
                sqlsearch += " AND %d<B2 AND B2<%d" %(INTrgb2[2]-6, INTrgb2[2]+6)
                self.CON.execute(sqlsearch)
                R2G2B2result = self.CON.fetchall()
                print("-----------------------------------")
                print("")

                # データがあった場合
                if len(R2G2B2result) == 1:
                    print("---カードの特定！---")
                    print(R2G2B2result[0][0])
                    SPcardID.append(R2G2B2result[0][0])
                # miss or データが複数あった場合は、id=88888にする
                else:
                    print("！！！特定失敗！！！　複数のデータがヒットしました！")
                    print(R2G2B2result)
                    SPcardID.append(888888)
            # 1回でカードが特定できた場合
            elif len(RGBresult) == 1:
                print("---特定---")
                SPcardID.append(RGBresult[0][0])
            # カード発見できず
            else:
                print("！！！カードが存在していません！！！")
                SPcardID.append(999999)

            # 仮テーブルの削除
            sqlsearch = "DROP TABLE tmp_sptb"
            self.CON.execute(sqlsearch)
            sqlsearch = "DROP TABLE tmp_rgb_tb"
            self.CON.execute(sqlsearch)
            print("-------")
            print("TMP_table × 2   DELEAT!")


        #テスト用------
        self.CON.close() # データベースを閉じる
        #テスト用------

        return SPcardID, RGBdate

    # 送られてきたRGBのデータから、def(RareTradb)　と　def(SPcarddb)　でカードを特定する処理
    def RGBsearch(self, SPcadelist):


        # ループで６回×３回（レア、練習、絵と絵２）する
        # まずは、RGBから、レア度と練習を調べ、配列に入れる。
        DB = DB_Connection()

        # ----------------------------------------------------------------------------
        sp_list = [] # 中には　レア度,練習,SP番号　を入れる

        # レア度と練習属性を特定する
        sp_list = DB.RareTradb(SPcadelist)

        # 絵からとった2か所の色平均を調べ、サポートカードを特定する。
        sp_IDlist = DB.SPcarddb(sp_list)

        self.CON.close()
        return sp_IDlist
        # ----------------------------------------------------------------------------


# CSV の処理をするクラス
class DB_csv:
    # DBと接続
    def __init__(self):
        self.conn = sqlite3.connect(umamusumeDB_path)
        self.CON = self.conn.cursor()
        #print("DBと接続")

    # ランキングの全データ取得
    def Rankingserth(self):
        print("ランキングデータ取得中")

        self.CON = self.conn.cursor()

        sql = ("SELECT position,character_name,SP_Card_1,SP_Card_2,SP_Card_3,SP_Card_4,SP_Card_5,SP_Card_6 FROM Ranking_Data")
        self.CON.execute(sql)
        result = self.CON.fetchall()
        print(result)
        return result

    # ランキングデータから、カードの使用率を調べる処理　１を足していく
    def userateupdate(self,rankinglist):
        print("更新処理")
        print("ランキングデータ 総数　" + str(len(rankinglist)) + " 個")

        # 使用率に足していく処理
        def rankpuls(templist):
            # ランキングのデータが1件くる
            def R_puls(useRETU,useGYOU):

                    # この列と行に該当する使用回数を取ってきて、それに１を足す処理
                    self.CON = self.conn.cursor()
                    usesql = ("SELECT %s FROM Use_rate WHERE name ='%s'" %(useRETU, useGYOU))
                    self.CON.execute(usesql)
                    useresult = self.CON.fetchall()
                    print("使用回数 " + str(useresult[0][0]))
                    num = useresult[0][0] + 1
                    # updateで検索したもののレコードを更新する
                    # データベースに追加する。
                    usesql = "UPDATE Use_rate SET %s = %d WHERE name = '%s'" %(useRETU, num, useGYOU)
                    self.CON.execute(usesql)
                    self.conn.commit() # コミットする
                    self.CON.close()

            for B in range(6):
                print("\n\n-----------")
                print(str(B+1) + "枚目")
                print("-----------\n")

                useR = "R_" + str(templist[B+2])
                # ここから、カードを総当たりで
                count = B
                while count < 6:
                    print("\n//count  " + str(count+1)+"//")
                    useG = "G_" + str(templist[count+2])
                    print(useR+" - "+useG)
                    R_puls(useR,useG)

                    # 自分自身に登録するとき　B == count のときは、反転は処理させない。
                    if B == count:
                        count+=1
                        continue

                    else:
                        useR2 = "R_" + str(templist[count+2])
                        useG2 = "G_" + str(templist[B+2])
                        print("(--反転--)　"+useR2+" - "+useG2)
                        R_puls(useR2,useG2)
                        count+=1

        # 全データの総数 ランキングを1件ずつ
        for A in range(len(rankinglist)):
            print("\n\n\n" + str(A+1) +" 件目のデータ --- ranking")
            # カード6枚分
            rankpuls(rankinglist[A])

        print("use_rate count end")

    # Use_rate のデータをCSVで出力
    def useratecsv(self):
        print("userate csv出力")

        dt_now = datetime.datetime.now()
        cstxttime = dt_now.strftime('%Y年%m月%d日 %H_%M_%S')

        csvname =  "./UMA_card_pg/csv_date/"
        csvname += "%s" %(cstxttime)
        csvname += 'UMA.csv'

        self.CON = self.conn.cursor()

        # use_rateのデータをもってくる。
        sql = ("SELECT * FROM Use_rate")
        self.CON.execute(sql)
        use_result = self.CON.fetchall()


        # このままだと、列名が記録されないので、列名を取ってくる。
        names = list(map(lambda x: x[0], self.CON.description))

        # csv 記述
        with open(csvname, "w", newline="", encoding="utf-16") as f: #csvファイルを書き込みモードで開く
            writer = csv.writer(f, dialect="excel-tab") #書き込み設定
            writer.writerow(names)
            writer.writerows(use_result) #listに記録した時間をcsvに出力 #time_listは多次元配列になっているのでwriterows。1次元であればwriterowで十分

    # use_rateを０で初期化
    def useratezero(self):
        print("userate ０で初期化")

        # use_rateの列名をもってくる。
        sql = ("SELECT * FROM Use_rate")
        self.CON.execute(sql)
        names = list(map(lambda x: x[0], self.CON.description))
        # use_rateの列名を使って、行と列名を、リストに入れる
        R_list=[]
        G_list=[]
        for i in names:
            if i == "name":
                continue
            R_list.append(i)
            name_G = "G_"+i.lstrip("R_")
            G_list.append(name_G)
        # 繰り返しで、use_rateの全データを０に書き換える。
        self.CON = self.conn.cursor()
        for A in R_list:
            for B in G_list:
                usesql = "UPDATE Use_rate SET %s = %d WHERE name = '%s'" %(A, 0, B)
                self.CON.execute(usesql)
        self.conn.commit() # コミットする
        self.CON.close()




# ランキングから、使用率処理をした後、csv出力して、０で初期化
    #　(！) ランキングデータにはデータが残っているので、必要なくなった場合はテーブルの中身を削除する。（大体1ヵ月ごと？）
def csv_syri():
    clas_csv = DB_csv()
    resurt = clas_csv.Rankingserth()
    clas_csv.userateupdate(resurt)
    clas_csv.useratecsv()
    clas_csv.useratezero()

csv_syri()






# clas_DB = DB_Connection()
# resurt = clas_DB.Rankingserth()

# clas_DB.userateupdate(resurt)



# # ーーーーーーーーーーーーーーーーーーーーーーーーーーーーー

# # テスト用


# print("")
# print("")
# print("")
# print("")


# clas_DB = DB_Connection() # DBプログラムのクラス
# SPcadelist = [] # 写真から分析した色の平均データを入れる変数

# SPcadelist=[['214-191-239','113-205-255','11-21-31','12-32-37'],['255-226-146','255-190-81','213-213-207','225-190-186'],['255-226-146','113-205-255','157-124-101','184-71-96'],['213-191-241','112-205-255','222-124-88','195-118-153'],['212-191-241','255-183-174','165-145-141','203-177-172'],['212-191-241','113-205-255','72-96-129','129-116-155']]

# test_list = ['SSR','guts','164-165-167','181-76-100']

# A = clas_DB.SPinsert(test_list)

# print(A)

# # DBlist = clas_DB.RareTradb(SPcadelist) # テスト用
# # DBlist = clas_DB.SPcarddb(SPcadelist) # テスト用

# sp_IDlist = clas_DB.RGBsearch(SPcadelist)


# print("-----【結果】-----")
# print(sp_IDlist)

