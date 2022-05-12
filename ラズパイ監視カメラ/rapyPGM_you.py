
import cv2
import matplotlib.pyplot as plt




# 加工する画像
gazou = './Raspi/kakou.png'

# -----------------------------------

YOKO = 944
TATE = 720

# XとYが３の倍数のときはスキップ（continue）する
warizan = 38 # 点を打つ間隔(数字が大きいほど枠が少なくなる)
amari = 9 # 四角の大きさ（数字が小さいほど大きくなる）
yosumi = 4 # 隅っこの幅


from PIL import Image
import matplotlib.pyplot as plt


#画像の読み込み
beautiful_view = Image.open(gazou)

#画像のリサイズ
small_beautiful_view = beautiful_view.resize((YOKO, TATE)) #横　縦


# 加工後の画像
hensyugo = './Raspi/kanryo.png'


#リサイズした画像を名前をつけて保存
small_beautiful_view.save(hensyugo)

print("endddd")


# -----------------------------------

img = cv2.imread(hensyugo)
print(img.shape) # 画像の大きさと色の種類？（RGBだから３）

HEIGHT = img.shape[0]
WIDTH = img.shape[1]

img = cv2.imread(hensyugo)
print(img[15, 30]) # これでその位置の色ア分かる


count=0
sousu=HEIGHT*WIDTH


for x in range(HEIGHT):
    Xamari = x%warizan
    if x < yosumi:
        continue
    if TATE-yosumi < x:
        continue
    if 0 < Xamari < amari:
        continue
    else:
        for y in range(WIDTH):
            Yamari = y%warizan

            if y < yosumi:
                continue
            if YOKO-yosumi < y:
                continue


            if 0 < Yamari < amari:
                continue
            else:
                b, g, r = img[x, y]
                if (b, g, r) == (0, 0, 0): # このいろの場合は変更なし
                    continue
                img[x, y] = 0, 0, 0 # この色に変更する
                count+=1



# 加工後の画像
kanryo = './Raspi/kanryo222.png'


cv2.imwrite(kanryo, img)

print("黒化数　:" + str(count))
print(sousu)

A=count/sousu

print(A)

#pgmこっちのpgmは上手く反応しない　GIMPからがいい
pgmyou = './Raspi/mask.pgm'

img_bgr = cv2.imread(kanryo)
img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)  # RGB2〜 でなく BGR2〜 を指定
cv2.imwrite(pgmyou, img_gray)

print("mask END")

