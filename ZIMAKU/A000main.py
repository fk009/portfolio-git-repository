
import tkinter
from tkinter import messagebox
from tkinter import filedialog #　ファイル参照
import re
import shutil #　コピー
import time
import os
import glob
import unicodedata



from ZIMAKU import A001Audio_cut
from ZIMAKU import A002Zimaku
from ZIMAKU import A003honyaku
from ZIMAKU import A004AviutilTEXT

from ZIMAKU import A010Parts

MY_DIRECTRY = A010Parts.DIRECTRY_F()


onsei = MY_DIRECTRY + 'ONSEI.wav'
wavfile = MY_DIRECTRY + 'testwav'
textfile = MY_DIRECTRY + 'text_folder'
text_path = textfile + '/HONYAKU.txt'
text_GENKOU = textfile + '/MOTOtext.txt'

textlog = ""

#　－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－





#　選択したファイルが動画or音声かをチェック、音声ファイル(wav)なら、そのコピーを作成する。
def btn_wav_F():
    print("動画、音声ファイルの選択")
    idir = './' #　参照の際、最初の画面
    file_path = tkinter.filedialog.askopenfilename(initialdir = idir) #　ファイルの参照

    # 以前のデータがあれば、それを削除
    if os.path.exists(onsei):
        os.remove(onsei)

    # ファイルの名前に全角、日本語が含まれているかをチェック
    check_bool = True
    for A in file_path:
        ret = unicodedata.east_asian_width(A)
        if ret == "F" or ret == "H" or ret == "W":
            check_bool = False
            break

    # ファイルがwavかどうかをチェック
    pattern = re.compile(r'.wav$')
    check_bool_2 = bool(pattern.search(file_path))
    # ファイルが動画かどうかをチェック
    pattern = re.compile(r'.mp4$')
    check_bool_3 = bool(pattern.search(file_path))


    if check_bool == False:
        messagebox.showinfo('確認', 'ファイルに全角、あるいは日本語が含まれています。\n半角英数字の名前に変更してみてください。')

    elif check_bool_2 == True:
        onsei_label["text"] = file_path # 絶対パスにある音声を、コピーする。
        shutil.copyfile(file_path, onsei)

    elif check_bool_3 == True:
        onsei_label["text"] = file_path  # 動画から音声へ変換処理
        A010Parts.Movie_convert(file_path, onsei)
    else:
        messagebox.showinfo('確認', 'mp4 または wavファイルではありません')


#　textファイルの絶対パスを入手 バックアップ作成
def btn_genko_F():
    print("原稿")
    idir = './' #　参照の際、最初の画面
    file_path = tkinter.filedialog.askopenfilename(initialdir = idir) #　ファイルの参照

    pattern = re.compile(r'.txt$')
    check_bool = bool(pattern.search(file_path))

    if check_bool == True:
        genko_label["text"] = file_path
        print("原稿コピー")
        shutil.copyfile(file_path, text_GENKOU)
    else:
        messagebox.showinfo('確認', 'textファイルではありません')


# 音声を分割・翻訳する関数
def btn_onsei_F():
    print("音声分割　翻訳 start")

    cp = onsei_label["text"]
    if not cp == "音声の絶対パス":

        # 前回の原稿txtと.exoファイルを削除する
        if os.path.isdir(text_GENKOU):
            os.remove(text_GENKOU)
        if os.path.isdir(A004AviutilTEXT.zimaku_text_path_2):
            os.remove(A004AviutilTEXT.zimaku_text_path_2)


        print("音声分割開始")
        A001Audio_cut.Audio_cut_F()
        print("音声分割終了")
        print("音声翻訳開始")
        A002Zimaku.translated_text_F()
        print("音声翻訳終了")
        messagebox.showinfo('確認','音声の翻訳が完了しました。')
    else:
        messagebox.showinfo('確認', 'wavファイルを選択してください')

# 入れ替え処理を始める
def btn_irekae_F():
    print("入れ替え")
    #フォルダの中に、HONYAKUとMOTOがあるかどうか
    file_H = glob.glob(text_path)
    file_G = glob.glob(text_GENKOU)
    if file_H == [] or file_G == []:
        print("存在しない")
        messagebox.showinfo('確認', '翻訳テキスト、原稿テキストの両方を用意してください。')
    else:
        main_frame.destroy()
        A003honyaku.TEXT_change_F()

# 字幕ファイル（exo）を作成する
def btn_zimaku_F():
    print("字幕生成")
    #フォルダの中に、HONYAKUとMOTOがあるかどうか
    file_H = glob.glob(text_path)
    if file_H == []:
        print("存在しない")
        messagebox.showinfo('確認', '翻訳されたテキストが存在しません。')
    else:
        A004AviutilTEXT.ZIMAKU_creation_F()
        messagebox.showinfo('確認', 'exoファイルの作成が完了しました。')


#　－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－


# ●●●●●●●●●　メイン処理　●●●●●●●●●

# フォルダがなければ作成する処理
    # testwav   #text_folder

if not os.path.isdir(wavfile):
    os.makedirs(wavfile)
if not os.path.isdir(textfile):
    os.makedirs(textfile)



main_frame = tkinter.Tk()
main_frame.geometry('600x600') # 画面サイズの設定
main_frame.title('メイン画面') # 画面タイトルの設定


#　ラベル
label = tkinter.Label(text = "wavファイル") #ラベルWidgetを生成
label.place(relx = 0.15, rely = 0.05) #ラベルを配置

label2 = tkinter.Label(text = "原稿テキスト") #ラベルWidgetを生成
label2.place(relx = 0.15, rely = 0.35) #ラベルを配置




#　音声の絶対パス
onsei_label = tkinter.Label(text = "音声の絶対パス") #ラベルWidgetを生成
onsei_label.place(relx = 0.15, rely = 0.1) #ラベルを配置

#　テキストパス
genko_label = tkinter.Label(text = "原稿の絶対パス")
genko_label.place(relx = 0.15, rely = 0.4)


#　－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－

# 音声参照btn
onsei_sansyo_btn = tkinter.Button(main_frame, text='参照', command = lambda: btn_wav_F() , width=6, height=1)
onsei_sansyo_btn.place(relx = 0.03, rely = 0.1)

# 原稿参照btn
genko_sansyo_btn = tkinter.Button(main_frame, text='参照', command = lambda: btn_genko_F() , width=6, height=1)
genko_sansyo_btn.place(relx = 0.03, rely = 0.4)


# 翻訳音声btn
onsei_btn = tkinter.Button(main_frame, text='音声翻訳', command = lambda: btn_onsei_F() , width=13, height=2,
                        background="#cd5c5c" ,font=("MSゴシック", "10", "bold"))
onsei_btn.place(relx = 0.15, rely = 0.15)


# 入れ替えボタン
irekae_btn = tkinter.Button(main_frame, text='入れ替え',  command = btn_irekae_F  , width=20, height=5, background="#faf0e6")
irekae_btn.place(relx = 0.2, rely = 0.7)


# 字幕生成ボタン
zimaku_btn = tkinter.Button(main_frame, text='字幕生成',  command = btn_zimaku_F  , width=20, height=5, background="#faf0e6")
zimaku_btn.place(relx = 0.6, rely = 0.7)




main_frame.mainloop() # msgbox 表示

