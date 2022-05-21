


# ーーーーーーーーーーーーーーーーーーーーーーーーーーーーー

import cv2
import numpy as np

# ーーーーーーーーーーーーーーーーーーーーーーーーーーーーー

#　キャラ画像から、使用されたサポートカードを割り出す処理
#　　6枚のサポカを、1枚ずつ、レア度、練習属性、3か所の色の平均を調べ、DBと付け合わせる。
class C_irohantei:

    # 初期にロードされるもの
    def __init__(self):

        # ↓プロフィール画像の中にあるカードの位置を示している
        self.e_top = 524 # 1枚目のサポートカード Y軸
        self.e_left = 29 # 1枚目のサポートカード X軸
        self.e_tasi = 87 # 2枚目以降のサポートに足す X軸

        self.RGB_list = np.empty((6, 4)) # ６舞のカードと、４つの箇所
        self.RGB_list = np.array(self.RGB_list,dtype = object) # 配列の型を、文字列の型に変換

        self.CardNum = 4

        # print("色の初期位置")
        # print(self.iropos)
        # print("ーーーーーーーーーーー")

    # 指定された範囲の色の平均を調べる処理
    def iro_F(self,boxFromY, boxToY, boxFromX, boxToX, GAZOU):
        #   （self,Y初     , Y終　  , X初　   , X終　 , 画像情報）
        # 対象画像読み込み
        img = cv2.imread(GAZOU,cv2.IMREAD_COLOR)

        # 対象範囲を切り出し
        #boxFromY = 対象範囲 開始位置 Y座標  #boxToY =   対象範囲 終了位置 Y座標
        #boxFromX = 対象範囲 開始位置 X座標  #boxToX =   対象範囲 終了位置 X座標

        # y:y+h, x:x+w　の順で設定
        imgBox = img[boxFromY: boxToY, boxFromX: boxToX]

        # RGB平均値を出力
        # flattenで一次元化しmeanで平均を取得
        b = imgBox.T[0].flatten().mean()
        g = imgBox.T[1].flatten().mean()
        r = imgBox.T[2].flatten().mean()

        # 小数点以下切り捨て
        r = round(r)
        g = round(g)
        b = round(b)
        print("R: " + str(r))
        print("G: " + str(g))
        print("B: " + str(b))


        # 取得した色情報を、配列に入れて、後でDBと照合する処理
        d_RGB = str(r) + "-" + str(g) + "-" + str(b)
        print("-------------------------------")
        return d_RGB

    # 実際に処理する部分
    def looptest(self,UMApng):

        gazou = UMApng # UMApng　プロフィール画像png

        reado = [0,4,9,20]     # レア度の位置　左上
        rensyu = [4,8,58,73]    # 練習属性の位置　右上
        zentai_1 = [25,35,10,25] # 画像判別するための位置１つめ
        zentai_2 = [55,65,45,60]  # 画像判別するための位置２つめ
        # zentai_3 = [25,35,50,65]

        # 色の平均を取得したい場所
        IROposition = [reado, rensyu, zentai_1, zentai_2]
        self.iropos = IROposition

        # 色を調べる、1枚目の初期位置を設定する
        for count in range(self.CardNum):
            self.iropos[count][0]+=self.e_top
            self.iropos[count][1]+=self.e_top
            self.iropos[count][2]+=self.e_left
            self.iropos[count][3]+=self.e_left





        # ↓ ループ　６枚分取得する
        for i in range(6):
            # １．レア度 (SSR-SR-R)3種
            #　出てきた数字からレア度を出し、DBと付け合わせる
            print("【ーーー カード ---" + str(i+1) + " 枚目 ーーー】")

            #　確認する位置の個数の分　回す。　#  IROposition = [reado, rensyu, zentai_1, zentai_2]
            for count,A in enumerate(self.iropos):
                print("色情報　" + str(count+1) + "　箇所目　1:Rare 2:Trai 3:RGB 4:R2G2B2")
                # レア度　練習　全体から2か所の色平均をとってくる。
                self.RGB_list[i][count] = self.iro_F(self.iropos[count][0], self.iropos[count][1], self.iropos[count][2], self.iropos[count][3], gazou)

                # 次のカードの位置を入れる
                self.iropos[count][2]+=self.e_tasi
                self.iropos[count][3]+=self.e_tasi
            print("【ーーー　" + str(i+1) + " 枚目　終わり ーーー】")

        return self.RGB_list
                # ３．全体画像
                #2か所ぐらいでok


# ーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
# ーーーーーーーーーーーーーーーーーーーーーーーーーーーーー



# # SS = "SYASIN/testyou.png"
# SS = "SYASIN/sp6.png"
# # テスト
# IRO = C_irohantei()

# # reado, rensyu, zentai_1, zentai_2
# SPcadelist = IRO.looptest(SS) # 6枚分の[レア,練習,絵1,絵2]　の RGB をリストにして返却

# print("end")
# print(SS)
# print(SPcadelist)

