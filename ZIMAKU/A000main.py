
import tkinter
from tkinter import messagebox
from tkinter import filedialog #　ファイル参照
import re
import shutil #　コピー
import os
import glob
import unicodedata

import datetime

from ZIMAKU import A001Audio_cut
from ZIMAKU import A002Zimaku
from ZIMAKU import A003honyaku
from ZIMAKU import A004AviutilTEXT
from ZIMAKU import A006Setting


from ZIMAKU import A010Parts

MY_DIRECTRY = A010Parts.DIRECTRY_F()


onsei = MY_DIRECTRY + 'ONSEI.wav'
wavfile = MY_DIRECTRY + 'testwav'
textfile = MY_DIRECTRY + 'text_folder'
text_path = textfile + '/HONYAKU.txt'
text_GENKOU = textfile + '/MOTOtext.txt'
text_setting = MY_DIRECTRY + 'text_folder' + '/setting'



#　－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－



# -----------------------　メイン画面　---------------------------------
# メイン画面の表示・処理
def main_A000():

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


        if check_bool == False: # ファイルの名前に全角、日本語が含まれているか
            messagebox.showinfo('確認', 'ファイルパスに全角、あるいは日本語が含まれています。\n半角英数字の名前に変更してみてください。')

        elif check_bool_2 == True: # ファイルがwavかどうか
            onsei_label["text"] = file_path # 絶対パスにある音声を、コピーする。
            shutil.copyfile(file_path, onsei)

        elif check_bool_3 == True:# ファイルが動画かどうか
            onsei_label["text"] = file_path  # 動画から音声へ変換処理
            A010Parts.Movie_convert(file_path, onsei)
        else:
            messagebox.showinfo('確認', 'mp4 または wavファイルではありません')
            return

        # settingファイルにファイル名を記述
        A006Setting.settin_Write_filename_F(file_path, "")


    #　textファイルの絶対パスを入手 バックアップ作成
    def btn_genko_F():
        print("原稿")
        idir = './' #　参照の際、最初の画面
        GENfile_path = tkinter.filedialog.askopenfilename(initialdir = idir) #　ファイルの参照

        pattern = re.compile(r'.txt$')
        check_bool = bool(pattern.search(GENfile_path))

        if check_bool == True:
            genko_label["text"] = GENfile_path
            print("原稿コピー")
            shutil.copyfile(GENfile_path, text_GENKOU)
        else:
            messagebox.showinfo('確認', 'textファイルではありません')
            return

        # settingファイルにファイル名を記述
        A006Setting.settin_Write_filename_F("", GENfile_path)



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

    A006Setting.create_settingtxt_F() # 初期のセッティングtxtを作成


    main_frame = tkinter.Tk()
    main_frame.minsize(width=600, height=600)# 画面サイズの設定
    main_frame.maxsize(width=600, height=600)

    main_frame.title('メイン画面') # 画面タイトルの設定



    # すでにファイルを読み込んでいれば、その名前を表示
    honyaku_lb, genko_lb = A006Setting.read_setting_falename_F()
    hon_time, gen_time = A006Setting.file_creation_time_f()

 


    #　音声の絶対パスラベル

    label = tkinter.Label(text = "wavファイル - " + hon_time) #ラベルWidgetを生成
    label.place(relx = 0.15, rely = 0.05) #ラベルを配置

    if honyaku_lb == "\n" or honyaku_lb == "":
        onsei_label = tkinter.Label(text = "音声の絶対パス") #ラベルWidgetを生成
    else:
        onsei_label = tkinter.Label(text = honyaku_lb) #ラベルWidgetを生成
    onsei_label.place(relx = 0.15, rely = 0.1) #ラベルを配置



    #　テキストパスラベル

    label2 = tkinter.Label(text = "原稿テキスト - " + gen_time) #ラベルWidgetを生成
    label2.place(relx = 0.15, rely = 0.35) #ラベルを配置

    if genko_lb == "":
        genko_label = tkinter.Label(text = "原稿の絶対パス")
    else:
        genko_label = tkinter.Label(text = genko_lb)
    genko_label.place(relx = 0.15, rely = 0.4)

    #　設定ラベル
    setting_label = tkinter.Label(text = "音声の分割タイミングを調整") #ラベルWidgetを生成
    setting_label.place(relx = 0.64, rely = 0.1) #ラベルを配置




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

    # 設定btn
    setting_btn = tkinter.Button(main_frame, text='設定', command = lambda: setting_F(main_frame) , width=13, height=2,
                            background="#ffff00" ,font=("MSゴシック", "10", "bold"))
    setting_btn.place(relx = 0.64, rely = 0.15)

    # 入れ替えボタン
    irekae_btn = tkinter.Button(main_frame, text='入れ替え',  command = btn_irekae_F  , width=20, height=5, background="#faf0e6")
    irekae_btn.place(relx = 0.15, rely = 0.7)

    # 字幕生成ボタン
    zimaku_btn = tkinter.Button(main_frame, text='字幕生成',  command = btn_zimaku_F  , width=20, height=5, background="#faf0e6")
    zimaku_btn.place(relx = 0.6, rely = 0.7)



    main_frame.mainloop() # msgbox 表示


# -----------------------　メイン画面　終わり　---------------------------------

# 〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇


# -----------------------　設定画面　---------------------------------



# 設定画面　表示・処理
    # 音声の分割に関する設定を変更する。
def setting_F(main_frame):
    main_frame.destroy()

    # 完了ボタン
    def setting_btn_kanryo_F():
        # すべてのテキストボックスで数字だけか
        #       （2番目だけ、マイナス記号OK）

        muonbox = textbox_muon.get()# Entryの中身を、0文字目から最後の文字まで削除
        volumebox = textbox_volume.get()
        keepbox = textbox_keep.get()
        FPSbox = textbox_FPS.get()

        test_T = muonbox + volumebox + keepbox + FPSbox

        if " " in test_T or "　" in test_T:
            messagebox.showerror("エラー", "いずれかのメッセージボックスに空白が含まれています！")
            return

        try:
            int_muonbox = int(muonbox)
            int_volumebox = int(volumebox)
            int_keepbox = int(keepbox)
            int_FPS = int(FPSbox)
        except:
            messagebox.showerror("エラー","テキストボックスが正しく入力されていない可能性があります！")
            return

            #  テキストボックスの一番上が空白なら、エラーを返す。
        if muonbox == "" or volumebox == "" or keepbox == "" or FPSbox == "":
            messagebox.showwarning("エラー", "すべてのテキストボックスに入力してください。")
        else: # 問題なければ確認msgで、書き換え処理
            ret = messagebox.askyesno('確認', 'この内容に書き換えますか？')
            if ret == True:
                # すべて大丈夫なら、セッティングtxtに書き込む
                A006Setting.setting_Write_F(int_muonbox, int_volumebox, int_keepbox, int_FPS)
                tki.destroy()
                main_A000()

    # キャンセルボタン
    def setting_btn_Cancel_F():
        tki.destroy()
        main_A000()

    # テキストボックスの入力制限
    def limit_char(string):
        return len(string) <= 5



   # 画面作成  ――――――――――――――――――――――――――――――――――――――――――――――
    tki = tkinter.Tk() # Toplevel サブの画面
    # def MSG_tkinter():
    tki.title('設定') # 画面タイトルの設定
    tki.minsize(width=400, height=680)
    tki.maxsize(width=400, height=680)

    #　ラベル
    label = tkinter.Label(text = "") #ラベルWidgetを生成
    label.pack() #ラベルを配置

    label1 = tkinter.Label(text = "数値を変えることで音声の分割を調整することができます。") #ラベルWidgetを生成
    label1.pack() #ラベルを配置
    label2 = tkinter.Label(text = "分割された１つが、１つの字幕表示になります。") #ラベルWidgetを生成
    label2.pack() #ラベルを配置
    label3 = tkinter.Label(text = "うまくいかない場合は、音声の中の雑音を処理してみてください。",foreground='#ff4500') #ラベルWidgetを生成
    label3.pack() #ラベルを配置
    label_null = tkinter.Label(text="")
    label_null.pack(ipady=2)

    # 単位のラベル
    label_ms1 = tkinter.Label(text = "ms")
    label_ms1.place(x=264, y=160)

    label_ms2 = tkinter.Label(text = "dBFS")
    label_ms2.place(x=264, y=277)

    label_ms3 = tkinter.Label(text = "ms")
    label_ms3.place(x=264, y=394)


    # 入力制限
    vc = tki.register(limit_char)



    # 無音時間
    label_muon = tkinter.Label(text = "無音時間がどれくらい続いたらカットするか", font=("MSゴシック",10,"bold")) #ラベルWidgetを生成
    label_muon.pack(ipady = 10) #ラベルを配置
    textbox_muon = tkinter.Entry(validate="key", validatecommand=(vc, "%P"))
    textbox_muon.pack()

    label_bikou1 = tkinter.Label(text = "〇〇ms以上無音なら分割")
    label_bikou1.pack()
    label_bikou2 = tkinter.Label(text = "（初期値：100）")
    label_bikou2.pack()
    label_null2 = tkinter.Label(text="")
    label_null2.pack(ipady=1)


    # 無音にするボリューム
    label_volume = tkinter.Label(text = "どれくらいの音量から無音扱いするか", font=("MSゴシック",10,"bold")) #ラベルWidgetを生成
    label_volume.pack(ipady = 10) #ラベルを配置
    textbox_volume = tkinter.Entry(validate="key", validatecommand=(vc, "%P"))
    textbox_volume.pack()

    label_bikou3 = tkinter.Label(text = "-〇〇dBFS以下で無音と判定（ここの調整で結構かわる？）")
    label_bikou3.pack()
    label_bikou4 = tkinter.Label(text = "（初期値：-70）")
    label_bikou4.pack()
    label_null3 = tkinter.Label(text="")
    label_null3.pack(ipady=1)


    # カット後の無音時間
    label_keep = tkinter.Label(text = "カットした後の音声に残す、無音時間", font=("MSゴシック",10,"bold")) #ラベルWidgetを生成
    label_keep.pack(ipady = 10) #ラベルを配置
    textbox_keep = tkinter.Entry(validate="key", validatecommand=(vc, "%P"))
    textbox_keep.pack()

    label_bikou5 = tkinter.Label(text = "分割後、〇〇msは無音を残す")
    label_bikou5.pack()
    label_bikou6 = tkinter.Label(text = "（初期値：500）")
    label_bikou6.pack()
    label_null3 = tkinter.Label(text="")
    label_null3.pack(ipady=1)

    # 動画のFPS
    label_FPS = tkinter.Label(text = "動画のFPS設定", font=("MSゴシック",10,"bold")) #ラベルWidgetを生成
    label_FPS.pack(ipady = 10) #ラベルを配置
    textbox_FPS = tkinter.Entry(validate="key", validatecommand=(vc, "%P"))
    textbox_FPS.pack()

    label_bikou7 = tkinter.Label(text = "（初期値：30）")
    label_bikou7.pack()
    label_null4 = tkinter.Label(text="")
    label_null4.pack(ipady=1)





    # 完了ボタン　（再度確認を行う）
    OK_btn = tkinter.Button(tki, text='完了', command = lambda: setting_btn_kanryo_F() , width=10, height=2,
                            background="#cd5c5c" ,font=("MSゴシック", "10", "bold"))
    OK_btn.place(relx = 0.2, rely = 0.9)

    # キャンセルボタン
    reset_btn = tkinter.Button(tki, text='キャンセル',  command = lambda: setting_btn_Cancel_F(),
                                width=10, height=2  ,font=("MSゴシック", "10", "bold"))
    reset_btn.place(relx = 0.6, rely = 0.9)


    #　――――――――――――――　画面制作


    # settingファイルがなければ、初期値で作成。
    A006Setting.create_settingtxt_F()

    # settingtxtから、値を取得
    min_silence_len, silence_thresh, keep_silence, fps = A006Setting.read_settingtxt_F()

    # 画面の初期化
    def setting_initial_value_F():
        textbox_muon.delete(0, tkinter.END) # Entryの中身を、0文字目から最後の文字まで削除
        textbox_volume.delete(0, tkinter.END)
        textbox_keep.delete(0, tkinter.END)
        textbox_muon.insert(tkinter.END, min_silence_len)
        textbox_volume.insert(tkinter.END, silence_thresh)
        textbox_keep.insert(tkinter.END, keep_silence)
        textbox_FPS.insert(tkinter.END, fps)

    setting_initial_value_F()

    tki.mainloop() # msgbox 表示


# -----------------------　設定画面　終わり　---------------------------------



main_A000()