
# 画像データから使用されているカードを切り出し、DBに存在しているかをチェック。
    # 存在していなければ、カードを切り抜いて保存、DBに番号と色データを新規保存


# スタートするファイル

#指定したフォルダから、ファイル（png）の名前を取り出し、その分ループする

#ＳＱＬの登録、あるいは使用率加算処理プログラム
    #その際、5桁の数字で、１２０１１みたいにする。
        #万の位で、レア度　百～千の位で、練習、残りの2桁で、カードのＩＤを入れる。

import os
import sys
import datetime
import time
import cv2


import A001kiritori  # A = A001kiritori.Kiritori()
import A002iroai
import A003DBConnect


# ---------------------------------------------------

C_KIRI = A001kiritori.Kiritori() # spカードを切り取る
    # def photo(self, sspimg, card_No)

C_IRO = A002iroai.C_irohantei() # １．プロフィール画像から、6枚のspカードの色を調べる。
    # def looptest(self,UMApng):

C_DB = A003DBConnect.DB_Connection() # ２．6枚分の色データから、spカードを特定する。
    # def RGBsearch(self, SPcadelist):


# プロフィール画像が入ってるフォルダー　ここから、カード使用を調べる
SSdir = './UMA_card_pg/SYASIN'

# カード候補が複数あって、特定できなかった場合（888888）、errorテキストに内容を保存する。（まだちゃんと記録されるかテストしてない？）
new_dir_path = './UMA_card_pg/error_folder'

# 未登録のカード.pngを保存するフォルダ―
new_SSdir_path = './UMA_card_pg/UMA_SS_folder'




#フォルダの中身を取ってくる処理
class folder_Allpick():
    def __init__(self):
        # プロフィールのSSがあるフォルダの中身を一括で取ってくる
        self.ss_list = os.listdir(SSdir)
        print(self.ss_list)


    # プロフィールの数だけループしてspカードを調べる。
    def profile_roop(self):
        print("プロフィール画像処理　開始")

       # フォルダ + エラー用のテキストログを作成する処理------------------------------------
        try:
            print("エラーフォルダ作成")
            os.makedirs(new_dir_path)
        except:
            print("")

        try:
            print("SPcard　新規SS保存フォルダ作成")
            os.makedirs(new_SSdir_path)
        except:
            print("")


        dt_now = datetime.datetime.now()
        self.txttime = dt_now.strftime('%Y年%m月%d日 %H_%M_%S')

        error_text_path =  "./UMA_card_pg/error_folder/"
        error_text_path += "%s" %(self.txttime)
        error_text_path += 'UMAerror.txt'

        #　記録するためのテキストファイルの作成
        f = open(error_text_path, 'w', encoding = "utf_8")
        f.write("")
        f.close()
        print("-error_text creation-")

        def UMA_error(nam, Uname):
            # テキストファイルに追加記述
            UMAtxt = "%s___%s\n" %(nam, Uname)

            #出力した内容を、末尾に追加でテキストに記述
            f = open(error_text_path, 'a', encoding = "utf_8")
            f.write(UMAtxt)  # 記述する内容
            f.close()
            print("---start,end time　記述完了" )
       # ---------------------------------------------------------------------

        if len(self.ss_list) < 1:
            print("画像が存在しません！！")
            sys.exit()

        # ループ　ランキング上位のサポートカード使用を調べる。
        countABC = 0
        for L in self.ss_list:
            PF = "./SYASIN/" + L # プロフィールのpass(sp1.pngなど)
            print("")
            print("")
            print("=======================")
            print(PF)
            print("=======================")
            print("=======================")
            #色を、[['214-191-239' '113-205-255' '149-99-117' '217-163-174'][~~][~~]~~[~~]]
            # の形式でもってくる
            iro_list = C_IRO.looptest(PF)

            # 数値のリストから、ｓｐカードの特定
            sp_list, SPCADE_list = C_DB.RGBsearch(iro_list)


            print("")
            print("")
            print("【----- SPcardリスト and IDリスト -----】")
            print(sp_list)   # [101001, 102001, 201011, 101021, 888888, 999999]のような形
            print(SPCADE_list) #[['SSR' 'speed' '149-99-117' '217-163-174'],[~~],[~~],[~~],[~~]]
            print("")


            # もしDBに存在していないカードがあれば、DBに追加する
            for A in range(6):
                # DBにカードが存在していなかった場合、Support__CardとUse_rateのDBにデータを追加する
                if sp_list[A] == 999999:
                    sp_list[A] = C_DB.SPinsert(SPCADE_list[A])
                    # 登録されていなかったカードの写真を切り取る処理
                    C_KIRI.photo(PF, int(A), new_SSdir_path, sp_list[A])




            try:   # listの中に888888がなければ、タイプエラーが起こるので、expeptの方に流れる（つまり、SPcadeはすべて特定済み）
                num888 = sp_list.index(888888)
                print("!!問題発生!! 使用しているSPカードを特定できませんでした")
                UMA_error(PF, num888)   # 問題のあったSSと、その中のSPカードの位置をエラーとしてテキストに記述する。
            except ValueError:
                print("")   # 問題ないので、ランキングDBに登録処理
                C_DB.rankinginsert(sp_list)


            countABC+=1
            print("###############")
            print(str(countABC)+" 回目終わり")
            print("###############")




    # もしエラーがなければ、エラーテキストを削除
    def errortxtcheck(self):

        error_text_path =  "./UMA_card_pg/error_folder/"
        error_text_path += "%s" %(self.txttime)
        error_text_path += 'UMAerror.txt'

        f = open(error_text_path, 'r', encoding='UTF-8')
        data = f.read()
        f.close()
        if data=="":
            os.remove(error_text_path)


A=folder_Allpick()
A.profile_roop()
A.errortxtcheck()

print("ーーー終了ーーー")


