#　文書を直していく処理
#　音声を翻訳したテキストと、読むときに使った原稿テキストを比較し、近いものを置換する

import ZIMAKU.A003_2count


import MeCab
import numpy as np # Pythonで数値計算を効率的に行うためのライブラリ
from tkinter import filedialog, Tk
from tkinter import messagebox


import ZIMAKU.A005Msgbox

from ZIMAKU.A010Parts import DIRECTRY_F
MY_DIRECTRY = DIRECTRY_F()


text_honyaku = MY_DIRECTRY + 'text_folder/HONYAKU.txt'
text_GENKOU = MY_DIRECTRY + 'text_folder/MOTOtext.txt'
Timingtext_path = MY_DIRECTRY + 'text_folder/timing.txt'
#---------------------------------------------------------------------------------------------------


def TEXT_change_F():



    #　txtファイルから、1.文 2.総行数 3.置換完了数（★） を取得するファンクション 1行ごとに配列に入れて返却
    def text_reading_F(text_bun):
        #　テキストの行数を調べる
        count = 0
        hoshi = 0
        with open(text_bun,"r",encoding='UTF-8') as f:
            for line in f:
                count += 1
        print("Fold count --- " + str(count) + " ----" + text_bun)

        # テキスト文を取り出す 変数dataに１行ずつ入れていく
        # そして文の中に、★がついているかどうかを確認し、数を数える
        data = []
        for i in range(count):
            with open(text_bun,"r",encoding='UTF-8') as f:
                Oneline = f.readlines()[i].replace('\u3000', ' ') # 大文字の空白を半角空白に治す
                check_hoshi = "★" in Oneline
                if check_hoshi == True:
                    hoshi += 1
                data.append(Oneline)
                #print(data[i])
        return data, count ,hoshi

    #　textファイルからすべての文を１行ずつ取得 fanction
        # 1行ずつ入れた本文, 行数 ,★の数
    honyaku_data, honcount, honhoshi = text_reading_F(text_honyaku)
    genko_data, genkocount, genhoshi = text_reading_F(text_GENKOU)


    #　Bag of Words 比較するための0-1のベクトルにする処理ーーーーーー
    def Bag_of_Words_F(sentence_wakati_list):
        word_to_index = {}  #　ワードごとに、何番目の数字かが付与される？
        index_to_word = {}  #  ０から順番に、ワードが入っていってる？
        for s in sentence_wakati_list: # sentence_wakati_listの1文目を、区切りごとに s に入れる。 ('そんな', 'パリ', 'の', ～～)(ヴィクトール', '・', 'ルースティヒ', 'に'～～～)
            for w in s:                # s から１ワードごとに処理を行っていく。　(そんな)（パリ）（の）～～～（でしょう）（か）
                if w not in word_to_index:  # ワードごとに、０から順番に数字を与えていく
                    new_index = len(word_to_index)
                    word_to_index[w] = new_index
                    index_to_word[new_index] = w

        # ワード数の個数分０をつける
        corpus = np.zeros((len(sentence_wakati_list), len(word_to_index)))

        # one hot vector ... 使われたワードがあれば、そのワードの番号を０から１にする。
        for i, s in enumerate(sentence_wakati_list):
            for w in s:
                corpus[i, word_to_index[w]] = 1

        return corpus
        #-----------------------------------------ベクトル終わり

    #　比較のための、ベクトルの角度を求める式
    def cos_sim_F(x, y):
        return np.dot(x, y) / (np.sqrt(np.sum(x**2)) * np.sqrt(np.sum(y**2)))

    # テキストを分割し、近似値の値を返す
    def BUNKATU_F(sentence_list, text_rate,syori_Type):
            #　文章を単語ごとに分割する処理---------------------------------------
            wakati = MeCab.Tagger("-Owakati")
            sentence_wakati_list = [wakati.parse(i).split() for i in sentence_list]
            print(sentence_wakati_list)
            #--------------------------------------------------------------------
            corpus = Bag_of_Words_F(sentence_wakati_list) #　Bag of Words 比較するための0-1のマトリクスにする処理
            per = cos_sim_F(corpus[0], corpus[1])  #　翻訳文（conrpus[0]） と　原稿文(corpus[1])のベクトルから、角度を出す
            text_rate[syori_Type].append((f"{per:.3}"))         #　４つまで近似値の結果を格納
            return text_rate


    #　すべての処理が終わったら、テキストを書き換える処理
    def Overwrite_text_F(Path, Otext):
        with open(Path, "w", encoding = "utf_8") as f:
            for line in Otext:
                f.write(line)

    #　ダイアログ表示
    def dialog_F(Mtitle, Mtext):
        # ダイアログ用のルートウィンドウの作成
        root = Tk()
        root.geometry("0x0")# ウィンドウサイズを0にする（Windows用の設定）
        root.overrideredirect(1)# ウィンドウのタイトルバーを消す（Windows用の設定）
        root.withdraw()# ウィンドウを非表示に
        messagebox.showinfo(Mtitle, Mtext)
        root.destroy()


    #〇（↑　ファンクション）
    #---------------------------------------------------------------------------------------------------
    #★'(↓　処理スタート)




    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@")


    check_hosiG = True
    end_flg = 0 # すべての処理が完了できたか、あるいは処理を中断した場合にループを抜け出すためのフラグ。
    countA = 0 #原稿の連結　による一致回数が何回実行されたかの確認用
    countB = 0 #1行        による一致回数が何回実行されたかの確認用
    countC = 0 #翻訳の連結　による一致回数が何回実行されたかの確認用

    sentence_list = [] # ここで比較する文章を入れる(１つ目は翻訳txt ２つめは原稿txt)
    Genko_txt_line = 0  # 原稿txtを比較するときの番号 どこまで進んだか
    #翻訳txt と　原稿txt　を比較

    # 比較処理ができた行には、★マークをつける。
    Genko_txt_line = genhoshi # 原稿txtで★がついているものは飛ばす
    startFOR = honhoshi       # 翻訳txtで★がついているものは飛ばす
    endFOR = len(honyaku_data) - 1  #　翻訳テキストの最後



    #ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
        # 翻訳が完了しない限り、ループ処理を行わせる。 for A の前に
        # そのとき、さきほど手直しさせた部分から再度始めさせる


    # 変換済みのマーク（★）が含まれている行は飛ばしてからスタートする。
    # Genko_txt_line =  これはしなくても大丈夫
    # startFOR       =  ループの始まり　さっき翻訳テキストのはじまりに使ったやつで
    # endFOR         =  len(honyaku_data) - 1  # 終わり　このまま

    endcount = 0

    # ////////////////手直し処理を繰り返し可能にするためのループ(画面を動的に変換できなかったので)////////////////////////
    while end_flg == 0:
        endcount += 1
        if endcount >= 50: #　無限ループ防止
            print("ループ防止作動")
            break

        if startFOR == endFOR+1:
            end_flg = 1
            dialog_F("入れ替え終了", "翻訳テキストの入れ替えが完了しました。")

       #ーーーーーーーーーーーーーーーーーーーーーーーーーー
       #　翻訳テキストの行数分ループ　翻訳テキストを1行ずつ原稿テキストと比較し、正しい文章へと置き換える。
       #ーーーーーーーーーーーーーーーーーーーーーーーーーー
        for A in range(startFOR,endFOR + 1):
            if not A < len(honyaku_data): # 翻訳結合などで、行が減っている場合があるので、endFORではない
                end_flg = 1
                dialog_F("入れ替え終了", "翻訳テキストの入れ替えが完了しました。")
                break

            print("ーーーーーーーーーー")
            print(str(A+1) + "回目　　")

            sentence_list = []
            sentence_list_HOKAN = [[""],[""],[""]] #　2次元配列にして、記録する
            sentence_list.append(honyaku_data[A]) #　翻訳文をリストの先頭[0]に入れる

            print("●●●●●●●●●●●●●●翻訳文●●●●●●●●●●●●●●●●●●●")
            print("★ー" + sentence_list[0])
            print("●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●")

            text_rate = [[],[],[]]#　３つあるうちのそれぞれに、比較用の近似値を４つまで入れる。
            ratelist = [] # １つの処理の中で、1番数値の高いものを格納。最終的に３つの処理の最大が入る



           #ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
           #　近似値を調べる処理　３つのループーーーーーー⇒
           #
           #  ・処理は３つ。１．原稿テキストを複数行連結して比較　２．個別に１行ずつ比較　３．翻訳行を複数行連結させて比較
           #ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー

            # 【１．★原】　原稿行を連結させて比較する処理　
            for B in range(3):
                Genko_num = B + Genko_txt_line

                if len(genko_data)-1 > Genko_num: #原稿txtに次の行が存在するなら、処理を続行
                    if B == 0:
                        sentence_list.append(genko_data[Genko_num]) #原稿文をリストの２番目に


                    #　原稿txt　の文を連結-------------------------------------
                    sentence_list[1] = sentence_list[1].replace('\n', ' ')
                    sentence_list[1] = sentence_list[1] + genko_data[Genko_num + 1]
                    sentence_list_HOKAN[0].append(sentence_list[1])
                    print("原連　" + sentence_list[1])
                    #----------------------------------------------------------
                else:
                    break
                #　文章を単語ごとに分割し、その近似値を調べる処理---------------------------------------
                syori_Type = 0
                text_rate = BUNKATU_F(sentence_list, text_rate, syori_Type)
                #　ーーーーーーーーーーーー文を入れる処理終わり
            # １番近い文章の組み合わせを調べる
            if text_rate[0] == []:
                text_rate[0] = "0"
            else:
                del sentence_list[1]

            MAXrate = [0,0,0] # 比較用の近似値の中で、それぞれの中で一番高いものを格納する。
            MAXrate[0] = text_rate[0].index(max(text_rate[0]))
            ratelist.append(text_rate[0][MAXrate[0]])
            print("(連結)　MAX   " + str(MAXrate[0]) + "-- " + str(ratelist[0]))
            print("--------")


            #//////////////////////

            # 【ー２．★行】　１行ずつ　翻訳と原稿を比較する処理
            for B in range(4):
                Genko_num = B + Genko_txt_line
                if len(genko_data)-1 >= Genko_num: #原稿txtに次の行が存在するなら、処理を続行
                    sentence_list.append(genko_data[Genko_num])#原稿文をリストの２番目に
                    sentence_list_HOKAN[1].append(sentence_list[1])
                    print("1行　" + sentence_list[1])
                    #　文章を単語ごとに分割し、その近似値を調べる処理
                    syori_Type = 1
                    text_rate = BUNKATU_F(sentence_list, text_rate, syori_Type)
                    del sentence_list[1]
                    #　ーーーーーーーーーーーー文を入れる処理終わり
            # １番近い文章の組み合わせを調べる
            MAXrate[1] = text_rate[1].index(max(text_rate[1]))
            ratelist.append(text_rate[1][MAXrate[1]])
            print("(１行)　MAX    " + str(MAXrate[1]) + "-- " + str(ratelist[1]))
            print("--------")

            #//////////////////////

            # 【ーー３．★翻】　翻訳行を連結させて比較する処理
            for B in range(4):
                honyaku_num = B + A
                honyakuren_exist = True
                if B == 0:
                    sentence_list.append(genko_data[Genko_txt_line]) #原稿文をリストの２番目に
                if B > 0:

                    if honcount > honyaku_num: #翻訳txtの次行が存在するなら、処理を続行

                        #　翻訳txt　の文を連結-------------------------------------
                        sentence_list[0] = sentence_list[0].replace('\n', ' ')
                        sentence_list[0] = sentence_list[0] + honyaku_data[honyaku_num]
                        sentence_list_HOKAN[2].append(sentence_list[0])
                        print("翻　" + sentence_list[0] + " 源 " + sentence_list[1])
                        #----------------------------------------------------------
                    else:
                        honyakuren_exist = False

                #　文章を単語ごとに分割し、その近似値を調べる処理
                syori_Type = 2
                text_rate = BUNKATU_F(sentence_list, text_rate, syori_Type)
                #　ーーーーーーーーーーーー文を入れる処理終わり
            # １番近い文章の組み合わせを調べる ※翻訳連結は、1行のみを飛ばして、2行以上連結させたもののみを判定する
            MAXrate[2] = text_rate[2].index(max(text_rate[2]))
            ratelist.append(text_rate[2][MAXrate[2]])
            print("(翻結)　MAX   " + str(MAXrate[2]) + "-- " + str(ratelist[2]))
            print("--------")

           # ーーーー  END 近似値を調べる処理　３つのループ END ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー


           #ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
           #　　判定処理
           #ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー


            #　３つの処理の中で、一番大きい値を出す処理を探す。それが、一番近い文章同士だということになる。
            MAXrateloop = ratelist.index(max(ratelist))
            print("最大r " + str(ratelist[MAXrateloop]))

            # もし、近似値が必要な値まで達していなかった場合は、手直しによる処理を行わせる。
            if float(ratelist[MAXrateloop]) < 0.7:
                print("該当なし")
                print(sentence_list[0])

                #  A005Msgbox.py のメッセージボックスに値を渡す。
                honyaku_data, genko_data, end_flg, check_hosiG = ZIMAKU.A005Msgbox.Tenaosi_msg(honyaku_data, genko_data, A, Genko_txt_line)
                startFOR = A
                break

            # 一番最後の行を処理するための判定（ないとエラーになるので）
            elif ratelist[2] <= ratelist[0]  and ratelist[0] == ratelist[1]:
                MAXrateloop = 1


            #　同じ近似値が複数存在するとき、翻訳結合と1行で文章の文字数が、より近い方を優先させるーー
                # （※ただし、文字数が離れすぎている場合、チェックを促す）
            def SEIMITUcheck_F(sentence_list_HOKAN):
                honyaku = len(honyaku_data[A]) #　翻訳行
                itigyou = len(sentence_list_HOKAN[1][1 + MAXrate[1]]) #　比較の1行

                if honyakuren_exist == True:
                    renketu = len(sentence_list_HOKAN[2][1 + MAXrate[1]]) #  比較の翻訳連結文
                else:
                    renketu = 0


                #　文字数を数えて、近い方を優先させる
                mozicount = [0,0]
                mozicount[0] = itigyou - honyaku
                if mozicount[0] < 0:
                    mozicount[0] *= -1
                mozicount[1] = renketu - itigyou
                if mozicount[1] < 0:
                    mozicount[1] *= -1
                MAX = mozicount.index(max(mozicount)) # mozicount　の　[0]が1行　[1]が翻連
                return MAX


            if ratelist[1] == ratelist[2]:
                #　最後の行でない場合
                if A <= len(honyaku_data):
                    MAX = SEIMITUcheck_F(sentence_list_HOKAN)
                    if MAX == 0: #　1行の方が翻連より文字数が多かった場合　翻連のほうが近いと判断する
                        MAXrateloop = 2


            # 一致率が高くても、文字数がかけ離れている場合は、念のためチェックを促す処理
            mozibool = ZIMAKU.A003_2count.sentence_ward_count(genko_data,honyaku_data, sentence_list_HOKAN, MAXrateloop, MAXrate[0], MAXrate[1], MAXrate[2],A,Genko_txt_line,honyakuren_exist)

            if mozibool == False:
                honyaku_data, genko_data, end_flg, check_hosiG = ZIMAKU.A005Msgbox.Tenaosi_msg(honyaku_data, genko_data, A, Genko_txt_line)
                startFOR = A
                break
                # ↑ここで、文字の再入力を促している

           # ーーーー  END 判定処理 END ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー




           #ーーーーーーーーーーーーーーーーーーーーーーーーーーーー
           #　文章入れ替え処理
           #ーーーーーーーーーーーーーーーーーーーーーーーーーーーー

            TEST_A = honyaku_data[A] #　テスト用

            # ★原稿txtの連結だった場合　
            #       翻訳txtを　連結させた文で書き換え、その後　利用した行はマークをつける
            if MAXrateloop == 0:
                print("連結原稿行　処理")
                honyaku_data[A] = "★" + sentence_list_HOKAN[0][1 + MAXrate[0]].replace('\u3000', ' ')
                Genko_txt_line += MAXrate[0] + 1 + 1
                countA += 1

            # ★１行どうし　だった場合
            elif MAXrateloop == 1:
                print("1行原稿　処理")
                honyaku_data[A] =  "★" + sentence_list_HOKAN[1][1 + MAXrate[1]].replace('\u3000', ' ') # 書き換え処理
                Genko_txt_line += + MAXrate[1] + 1 # Genko_txt_line = MAXrate[1](0~3の何行目？)　+ 1(次の行)
                countB += 1

            # ★翻訳txtの連結だった場合
            elif MAXrateloop == 2:
                print("連結翻訳行　処理")
                Genko_txt_line += 1
                honyaku_data[A] =   "★" + sentence_list_HOKAN[1][1].replace('\u3000', ' ') #　1行ずつ　足しながら結合していくので
                for delcount in range(MAXrate[2]): # 使用した行分繰り返す

                    TEST_A+=honyaku_data[A + 1]  # テスト用

                    del honyaku_data[A + 1] #文がダブらないように、結合に使用した行を削除する
                    honcount -= 1
                    timingdata = []
                    # タイミングtxtからデータ取得--------
                    def Timingtext_reading_F():
                        with open(Timingtext_path,"r",encoding='UTF-8') as f:
                            count = 0
                            for line in f:
                                timingdata.append(line)
                                count += 1
                        print("Fold count --- " + str(count) + " ----" + Timingtext_path)
                        return timingdata
                    timingdata = Timingtext_reading_F() 
                    # タイミングtxtからデータ取得--------

                    # タイミングのスタートとエンドを合体させ、余分を削除
                    def Taiming_Overwrite_F(ti_data):
                        ti_data[A] = ti_data[A].rstrip('\n')
                        NAMAE = ti_data[A].split("-")       #　1.タイミングから、音声をよける(一応、使ったやつは書いとく)
                        ATAMA = NAMAE[0].split(",")         #  2.コンマで分割　先頭と後方を合体して記録
                        NAMAE2 = ti_data[A+1].split("-")    #　1.タイミングから、音声をよける(一応、使ったやつは書いとく)
                        OSIRI = NAMAE2[0].split(",")        #  2.コンマで分割　先頭と後方を合体して記録
                        ti_data[A] = ATAMA[0] + "," + OSIRI[1] + "-" + NAMAE[1] + "," + NAMAE2[1]   # ライン書き換え
                        del timingdata[A+1] #　合体に使った行を消す
                        return ti_data
                    timingdata = Taiming_Overwrite_F(timingdata)
                    #----------------------------------------------
                    Overwrite_text_F(Timingtext_path,timingdata) # タイミングテキストを書き換え処理
                countC += 1

            TEST_A # テスト用
            TEST_B = honyaku_data[A] # テスト用 入れ替え後内容
            #TEST_C = MAXrateloop # テスト用

            # ここに文字数テストを入れる。
            ZIMAKU.A003_2count.TEST_PG_1(TEST_A,TEST_B)

           # ーーーー　 END 文章入れ替え処理 END ーーーーーーーーーーーーーーーーーーーーーーーーーーーー

            if Genko_txt_line > len(genko_data) - 1:
                dialog_F("入れ替え終了", '原稿テキストの最後まできました。')
                end_flg = 1




        Overwrite_text_F(text_honyaku,honyaku_data)   #　翻訳テキスト書き換え

        # 書き換えに使用した原稿データにマークをつける
        def HOSIsign(Genko_txt_line):
            with open(text_GENKOU, "w", encoding = "utf_8") as f:
                linenum = 0
                C = 0
                    #　msgボックスで原稿の★を消した場合の処理
                if check_hosiG == False and 0 < Genko_txt_line:
                    C = 1
                    Genko_txt_line -= 1

                for line in genko_data:
                    if linenum < Genko_txt_line-C:
                        if not "★" in line:
                            line = "★" + line
                            f.write(line)
                        else:
                            f.write(line)
                    else:
                        f.write(line)
                    linenum += 1

            print("原稿連結回数　--" + str(countA))
            print("1行　　 回数　--" + str(countB))
            print("翻訳連結回数　--" + str(countC))
            print("　　合計　数　---" + str(countA+countB+countC))
        HOSIsign(Genko_txt_line)

    print("ループ終了")


