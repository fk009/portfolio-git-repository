

# Aviutil　に利用できるexoファイルを作成する処理
    #すべてが完了したら、この処理を使って、字幕を作成していく処理

# ここはshift-jisでないとうまくいかない。

# 注意！　設定したフォントが存在しない場合、文字化けしてしまう！

"""
Aviutil用のexoファイルには、記述の決まりがあるので、
その必要な記述の一部を書き換えることで、１つの字幕を作成していく。
"""


import os
import time
import math
import re # 区切るときに、区切り文字を消さない

from tkinter import messagebox

FONT_type = "MS UI Gothic" # 字幕フォントの種類

from ZIMAKU.A010Parts import DIRECTRY_F
MY_DIRECTRY = DIRECTRY_F()

#　出力するテキストのパス
zimaku_text_path = MY_DIRECTRY + 'text_folder/Aviutil_ZIMAKU.txt'
zimaku_text_path_2 = MY_DIRECTRY + 'text_folder/Aviutil_ZIMAKU.exo'


text_honyaku = MY_DIRECTRY + 'text_folder/HONYAKU.txt'
Timingtext_path = MY_DIRECTRY + 'text_folder/timing.txt'




def ZIMAKU_creation_F():
    #　文字列コンバーター
        #文字列をUnicodeでエンコードして、それをBitConverterで16 進数文字列形式に変換し、
        #かつ"-"を取り除き、4096バイトとなるように後ろに"0"を付加。
    def ConvertExoText_F(text):
        result = text.encode('utf-16-le',"replace").hex() #　１，Unicodeでエンコード そして１６進数表記へ
        result = result.ljust(4096, '0')                  #4096バイトとなるように後ろに"0"を付加する
        return result

    #　exo字幕ファイル　作成ファンクション
    def Template_text_F(No,start,end,text):
        tmptext = ""
        tmptext = "[" + str(No) + "]\n" + "start=" + str(start) + "\nend=" + str(end) + "\nlayer=2\noverlay=1\ncamera=0\n[" + str(No) + ".0]\n_name=テキスト\nサイズ=50\n表示速度=0.0\n文字毎に個別オブジェクト=0\n移動座標上に表示する=0\n自動スクロール=0\nB=1\nI=0\ntype=0\nautoadjust=0\nsoft=1\nmonospace=0\nalign=4\nspacing_x=5\nspacing_y=0\nprecision=1\ncolor=000000\ncolor2=000000\nfont=" + FONT_type + "\n"
        tmptext = tmptext + "text=" + text + "\n[" + str(No) + ".1]\n_name=フェード\nイン=0.07\nアウト=0.07\n[" + str(No) + ".2]\n_name=標準描画\nX=0.0\nY=444.0\nZ=0.0\n拡大率=89.00\n透明度=0.0\n回転=0.00\nblend=0\n"
        #出力した内容を、末尾に追加でテキストに記述
        f = open(zimaku_text_path, 'a', encoding = "shift-jis")
        f.write(tmptext)
        f.close()
        print("---字幕　記述完了")

    #　字幕テキストファイル作成
    def Text_creat_F():
        f = open(zimaku_text_path, 'w', encoding = "shift-jis")
        f.write("[exedit]\nwidth=1920\nheight=1080\nrate=30\nscale=1\nlength=1030\naudio_rate=44100\naudio_ch=2\n")
        f.close()
        print("-text creation-")
    Text_creat_F()

    #　文章のタイミングを取得する。
    def timingtxt_F():
        count = 0
        data = []
        with open(Timingtext_path,"r",encoding='UTF-8') as f:
            for line in f:
                NAMAE = line.split("-") #（例） 999,1039-testwav/output25.wav （←この1行を分割）
                st_ed = NAMAE[0]
                data.append(st_ed)
                count += 1
        print("Fold count --- " + str(count) + " ----" + Timingtext_path)
        print(data)

        return data, count

    #　テキストの行数と、文をリストに取得する
    def text_reading_F(text_bun):
        count = 0
        data = []
        with open(text_bun,"r",encoding='UTF-8') as f:
            for line in f:
                line = line.lstrip("★")
                data.append(line)
                count += 1
        print("Fold count --- " + str(count) + " ----" + text_bun)
        print(data)

        return data, count


    # TODO ここで、半角空白もできるようにする？
    #　送られてきたテキスト１文を、イイ感じに２行にする処理
    def splittext_F(text):
        #文を『、』と『。』ごとに区切る処理
        textsplit = re.split("(?<=、)",text)
        textcountlist = []
        for A in range(len(textsplit)):
            sptext = re.split("(?<=。)",textsplit[A])
            for i in range(len(sptext)):
                textcountlist.append(sptext[i])
        print(textcountlist)

        #区切りができたので、区切った文をそれぞれ足していって、その文字数を計算する。　一番０に近い物が、改行として最適と考える
        wordls = [] # 計算した文字数を入れるlist
        CountA = 0
        for W in textcountlist:
            if W == textcountlist[0]:
                Word = W
            else:
                Word = Word + textcountlist[CountA]

            W_con = len(text)//2 - len(Word) # 文から、結合文を引いた数字
            if W_con < 0: #　数字がマイナスになったら、それ以上は無意味なので＋に変えた後にbreak
                W_con = W_con*-1
                wordls.append(W_con)
                break
            else:
                wordls.append(W_con)
            CountA+=1


       # 改行を入れる処理-------
        min_con = min(wordls) # 一番最小
        min_index = wordls.index(min_con) # 最小は何番目か
        print("インデックス確認　　" + str(min_index))
        CountB = 0
        for txt in textcountlist:
            if txt == textcountlist[0]:
                BUN = txt
            else:
                BUN += txt
            if CountB == min_index: # 中間として改行を入れる
                BUN += "\n"
            CountB+=1
        BUN2 = BUN.rstrip("\n") # 一行だった場合、字幕の位置が真ん中になるようにするため
        return BUN2
       #-----------------------
    # ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー

    # すでに字幕ファイルがあれば削除
    if os.path.exists(zimaku_text_path_2) == True:
        os.remove(zimaku_text_path_2)


    honyaku_data,count = text_reading_F(text_honyaku) #　文をリストに入れ、テキストの行数を取得する
    timedata, timecount = timingtxt_F()               #　文章のスタート、エンドをとってくる。


    #テキストを1行ずつAviutil用字幕へと変換していく。
    for i in range(count):
        print("テキスト　" + str(i+1) + "　行目")

       # ここで、２０文字以上なら、イイ感じに改行する処理--------------
        BUN = honyaku_data[i]
        if len(BUN) > 20:
            BUN = splittext_F(BUN)
       #-----------------------------------------------------------
        textAVI_16 = ConvertExoText_F(BUN) #文章を１６進数変換
        timing = timedata[i].split(",")
        start = timing[0]
        end   = timing[1]

        # 字幕を作成
        Template_text_F(i,start,end,textAVI_16)


    #　拡張子をexoに変更
    os.rename(zimaku_text_path, zimaku_text_path_2)




