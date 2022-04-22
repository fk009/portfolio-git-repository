# テキストフォルダに書き込んでいく処理。

from re import match

from ZIMAKU.A010Parts import DIRECTRY_F
MY_DIRECTRY = DIRECTRY_F()

text_TEST = MY_DIRECTRY + 'text_folder/TEST_log.txt'

# 文章の確認ファンクション（入れ替え内容 確認用）
    # TEST_log.txt を作成し、その中に、どの文章とどの文章を比較して入れ替えたのかを記述する。
def TEST_PG_1(moto_text, genko_txt):
    with open(text_TEST, "a", encoding = "utf_8") as f:
        # 必要なもの
        num_hon = len(moto_text)
        num_gen = len(genko_txt)
        num = num_hon - num_gen

        f.write("\n")
        numline = str(num_hon) +" - "+ str(num_gen)+" - "+str(num)
        f.write(numline)
        f.write("\n")
        line = moto_text + "  --  " + genko_txt
        f.write(line)
        f.write("\n")




# 一致率が高くても、文字数がかけ離れている場合はチェック
def sentence_ward_count(genko_data,h_data, sentence_list_HOKAN, MAXrateloop, MAXrate, MAXrate2, MAXrate3, A,Genko_txt_line,honyakuren_exist):

        if MAXrateloop == 0:
            print("連結原稿行　処理")
            genko_txt = sentence_list_HOKAN[0][1 + MAXrate].replace('\u3000', ' ')
            num_hon = len(h_data[A])

        # ★１行どうし　だった場合
        elif MAXrateloop == 1:
            print("1行原稿　処理")
            genko_txt =  sentence_list_HOKAN[1][1 + MAXrate2].replace('\u3000', ' ') # 書き換え処理
            num_hon = len(h_data[A])

        # ★翻訳txtの連結だった場合
        elif MAXrateloop == 2:
            print("連結翻訳行　処理")
            honyaku =  sentence_list_HOKAN[2][MAXrate3].replace('\u3000', ' ') #　1行ずつ　足しながら結合していくので
            num_hon = len(honyaku)
            genko_txt = genko_data[Genko_txt_line]

        num_gen = len(genko_txt)
        num = num_hon - num_gen
        if num < 0:
            num = num*-1

        # 文字数の差が ６以上なら、チェックを促す
        if num > 5:
            A = False
            print("\n文字数に問題あり\n")
            return A
        else:
            A = True
            return A







