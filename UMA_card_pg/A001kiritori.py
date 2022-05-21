
#画像の一部分を切り取るプログラム

######################

#ちゃんとした位置から色の取得ができれば、切り取りは必要ないかも

######################


import cv2


# 指定されたプロフィールから、SPカードを1枚切り抜く
class Kiritori:
    def __init__(self):

        #　６枚分の写真を取る。
        # img[top : bottom, left : right]
        # img[524 : 624, 29: 106] からスタート

        # 画像読み込み  （例）img = cv2.imread("SYASIN/testyou.png")

        self.top = 524 # 高さ
        self.bottom = 624 # 下
        self.left = 29 # 左
        self.right = 106 #右

        self.e_tasi = 87 # 2枚目以降のカードの位置

    # 切り取りする処理
    def photo(self, sspimg, card_No, path, cardNo):


        self.img = cv2.imread(sspimg) # プロフィール画像のpath

        # 切り取りたいカードは何枚目なのかを調べる。
        if card_No == 0:
            print("テスト１")
            p_left = self.left
            p_right = self.right
        else:
            print("テスト２")
            p_left = self.left + self.e_tasi*card_No
            p_right = self.right + self.e_tasi*card_No

        # 切り取った画像の名前　TODO　ここでは、登録したサポートカードのIDを入れるようにする。
        supportname =path + "/" + str(cardNo) + ".png"

        # 切り取り処理
        trim_img = self.img[self.top : self.bottom, p_left: p_right]
        cv2.imwrite(supportname, trim_img)

        #  なぜか、DBにデータが存在していない最初の一回目は、エラーが起きてしまう。
                # カードが101001のとき、つまり、一番最初のときだけエラーが起きてしまう。
                # DBから101001を削除して、実行すると、やはりエラー
                # 変数）trim_imgにデータが上手く入っていない。なぜ？



# AAA = './SYASIN/sp2.png'
# BBB= 0
# CCC='./UMA_card_pg/UMA_SS_folder'
# DDD="101001"

# ASD = Kiritori()
# ASD.photo(AAA,BBB,CCC,DDD)




