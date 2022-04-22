
#字幕生成
#音声ファイルから言葉を読み取り、文章を生成するプログラム


import speech_recognition as sr
import os
import glob
import time
#from tkinter import messagebox

from ZIMAKU.A010Parts import DIRECTRY_F
MY_DIRECTRY = DIRECTRY_F()


#　出力するテキストのパス
text_path = MY_DIRECTRY + 'text_folder/HONYAKU.txt'
# 音が保存されているフォルダ指定
DIR = MY_DIRECTRY + 'testwav/'
#　カットした音楽を保存する場所と名前
wav_name = MY_DIRECTRY + 'testwav/output'
#　字幕のタイミングを記述したファイル
Timingtext_path = MY_DIRECTRY + 'text_folder/timing.txt'

#---------------------------------------------------------------------------------------

def translated_text_F():

    # 翻訳テキストファイルの作成
    f = open(text_path, 'w', encoding = "utf_8")
    f.write("")
    f.close()
    print("-text creation-")

    #音声フォルダの中身の数を取得　（分割音声ファイルの個数）
    file_total = sum(os.path.isfile(os.path.join(DIR, name)) for name in os.listdir(DIR))
    print(file_total)


    # 音声を文字に変換して、テキストファイルに記述していくファンクション
        # ・聞き取れれば記述　できなければtimingテキストの行を削除（無音と判断）
    def oudio_text_F(MOTOoudio,mistime):

        #　オーディオ処理
        r = sr.Recognizer()
        with sr.AudioFile(MOTOoudio) as source:
            audio = r.record(source)

        #　グーグルの無料ライブラリを利用して、テキストに翻訳された文を記述
        try:
            wav_text = r.recognize_google(audio, language='ja-JP')
            print(wav_text)
            #出力した内容を、テキストに記述
            f = open(text_path, 'a', encoding = "utf_8")
            f.write(wav_text)
            f.write("\n")
            f.close()
            print("---記述完了")
        # 何を言っているのかわからなかった場合の処理（テキスト化不可時）
        except sr.UnknownValueError:
            print("✕✕✕✕✕✕✕✕✕　読み取れない。無音か雑音の可能性　✕✕✕✕✕✕✕")
            #問題のあった行を消すための参考を記録
            misstime_list.insert(0,mistime)
        # レスポンスが返ってこなかった場合の処理
        except sr.RequestError as e:
            print("レスポンスが返ってこなかった")


    #音声から文章を作成するプログラム
    misstime_list = []
    for i in range(file_total):
        #音声をテキストに変換
        MOTOoudio = wav_name + str(i) + ".wav"
        print(MOTOoudio)
        print("テキスト翻訳" + str(i))
        oudio_text_F(MOTOoudio,i) #　音声をテキストに翻訳していくファンクション

    print("-----ミスリスト　　" + str(misstime_list))

    mis_i = len(misstime_list)
    #timingテキストから、無音分を削除していく
    for i in range(mis_i):
        # 一度読み込んで、新しくテキスト作成
        with open(Timingtext_path, "r", encoding = "utf_8") as f:
            lines = f.readlines()
        linecount = 0
        with open(Timingtext_path, "w", encoding = "utf_8") as f:
            for line in lines:
                #ミスタイミングは飛ばして文章記述
                if linecount != misstime_list[i]:
                    f.write(line)
                linecount += 1





    print("-----　文章翻訳終了 -----")

