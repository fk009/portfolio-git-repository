

#　手作業で修正するときに使用するメッセージボックスUI



import tkinter
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText # 複数行の入力のテキストボックス作成
from playsound import playsound #　音声を流すライブラリ(※エラーが出るため、1.2.2のバージョンを利用する！)

from ZIMAKU.A010Parts import DIRECTRY_F
MY_DIRECTRY = DIRECTRY_F()



Timingtext_path = MY_DIRECTRY + 'text_folder/timing.txt'

# グローバル変数
Honyaku_list = []
Genko_list = []
A_num = 0
G_num = 0
timing_list = []
end_flg = 0



# ――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――



# ほかから呼び出し
def Tenaosi_msg(honyaku_data, genko_data, A, Genko_num):



  global Honyaku_list, Genko_list, A_num, timing_list, G_num, check_hosi

  Honyaku_list = honyaku_data
  Genko_list = genko_data
  A_num = A
  G_num = Genko_num
  check_hosi = True #原稿テキスト行から★が削除されたかどうかを確認

#　関数　――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――

  #初期値を入れる処理　リセットボタンにも反映させる
  def initial_value_F(Honyaku_list, Genko_list, A_num, G_num):
    print("初期値入れる処理")

    #　初期化　

    Honyaku_txtbox_S.delete(0, tkinter.END)
    Honyaku_txtbox0.delete(0, tkinter.END) # Entryの中身を、0文字目から最後の文字まで削除
    Honyaku_txtbox1.delete(0, tkinter.END)
    Honyaku_txtbox2.delete(0, tkinter.END)


    Genko_txtbox_S.delete(0, tkinter.END)
    Genko_txtbox0.delete(0, tkinter.END)
    Genko_txtbox1.delete(0, tkinter.END)
    Genko_txtbox2.delete(0, tkinter.END)


    if 1 <= A_num:
      Honyaku_txtbox_S.insert(tkinter.END,Honyaku_list[A_num-1].replace('\n', ''))

    try:
      Honyaku_txtbox0.insert(tkinter.END,Honyaku_list[A_num].replace('\n', ''))
      Honyaku_txtbox1.insert(tkinter.END,Honyaku_list[A_num+1].replace('\n', ''))
      Honyaku_txtbox2.insert(tkinter.END,Honyaku_list[A_num+2].replace('\n', ''))
    except:
      print("翻訳リストの最後か、リストが存在していない")

    if 1 <= G_num:
      Genko_txtbox_S.insert(tkinter.END,"★" + Genko_list[G_num-1].replace('\n', ''))

    try:
      Genko_txtbox0.insert(tkinter.END,Genko_list[G_num].replace('\n', ''))
      Genko_txtbox1.insert(tkinter.END,Genko_list[G_num+1].replace('\n', ''))
      Genko_txtbox2.insert(tkinter.END,Genko_list[G_num+2].replace('\n', ''))
    except:
      print("原稿リストの最後か、リストが存在していない")


  # 完了ボタン　リスト入れ替え処理
  def btn_kanryo_F():
    print("完了btn")

    # リスト入れ替え処理
    def Irekaesyori_F():
      #問題なければ処理を続行
      global Honyaku_list, Genko_list

      if 1 <= A_num:
        Honyaku_list[A_num-1] = textS + "\n"
        if not "★" in textS: #　星を削除した場合、いったん処理を終わらせる。
          global end_flg
          end_flg = 1
          messagebox.showinfo('確認', '翻訳テキストの★を削除しました')


      try:
        Honyaku_list[A_num] = text + "\n"
        Honyaku_list[A_num+1] = text2 + "\n"
        Honyaku_list[A_num+2] = text3 + "\n"
      except:
        print("翻訳リスト最後")



      if 1 <= G_num:
        gtextS = Genko_txtbox_S.get()
        gtextS = gtextS.replace(" ","")
        gtextS = gtextS.replace("　","")

        Genko_list[G_num-1] = gtextS + "\n"
        if not "★" in gtextS:
          global check_hosi
          check_hosi = False

      try:
          gtext2 = Genko_txtbox1.get()
          gtext2 = gtext2.replace(" ","")
          gtext2 = gtext2.replace("　","")

          gtext3 = Genko_txtbox2.get()
          gtext3 = gtext3.replace(" ","")
          gtext3 = gtext3.replace("　","")

          Genko_list[G_num] = gtext + "\n"
          Genko_list[G_num+1] = gtext2 + "\n"
          Genko_list[G_num+2] = gtext3 + "\n"
      except:
        print("原稿リスト最後")

      # 原稿行が空白だった場合、削除する
      for i in range(1,3):
        if Genko_list[G_num+i] == "\n":
          del Genko_list[G_num+i]



    # テキストボックスの内容を入れる
    textS = Honyaku_txtbox_S.get()
    textS = textS.replace(" ","")
    textS = textS.replace("　","")

    text = Honyaku_txtbox0.get()
    text = text.replace(" ","")
    text = text.replace("　","")

    text2 = Honyaku_txtbox1.get()
    text2 = text2.replace(" ","")
    text2 = text2.replace("　","")

    text3 = Honyaku_txtbox2.get()
    text3 = text3.replace(" ","")
    text3 = text3.replace("　","")

    gtext = Genko_txtbox0.get()
    gtext = gtext.replace(" ","")
    gtext = gtext.replace("　","")



      #  テキストボックスの一番上が空白なら、エラーを返す。
    if text == "" or text2 == "" or text3 == "" or gtext == "" :
      messagebox.showwarning("エラー", "翻訳・原稿 テキスト　1行目が空白です")
    else: # 問題なければ確認msgで、書き換え処理
      ret = messagebox.askyesno('確認', 'この内容に書き換えますか？')
      if ret == True:
        Irekaesyori_F() #　入れ替え処理
        tki.destroy()



    # 再度確認を促すメッセージボックス


  #閉じる　キャンセルボタン
  def btn_Cancel_F():
    print("キャンセル　ボタン")
    global end_flg
    end_flg = 1
    tki.destroy()

  # 音声を流す方法　流す処理
  def btn_Onsei_F(Onseinum):
    try:
      onsei = timing_list[Onseinum].split(",")
      for i in range(len(onsei)):
        playsound(onsei[i]) #   音声を流す処理
    except Exception as e:
      print("音声が存在していない可能性")
      print(e)


  # タイミングtxtからデータ取得--------
  def Timingtext_reading_F():
      timingdata = []
      with open(Timingtext_path,"r",encoding='UTF-8') as f:
          count = 0
          for line in f:
              timingdata.append(line)
              count += 1
      print("Fold count --- " + str(count) + " ----" + Timingtext_path)


      # タイミングtxtの、音声の絶対パスだけを取得する
      timinglist = []

      if 1 <= A_num:
        split = timingdata[A_num-1].split("-")
        timinglist.append(split[1].strip("\n"))

      try:
        split = timingdata[A_num].split("-")
        timinglist.append(split[1].strip("\n"))
        split = timingdata[A_num+1].split("-")
        timinglist.append(split[1].strip("\n"))
        split = timingdata[A_num+2].split("-")
        timinglist.append(split[1].strip("\n"))
      except:
        print("リストの最後に到達　あるいは存在していないリスト")

      return timinglist
  # タイミングtxtからデータ取得--------

#――――――――――――――――――――――――――　　関数


# 画面作成  ――――――――――――――――――――――――――――――――――――――――――――――
  tki = tkinter.Tk() # Toplevel サブの画面
  # def MSG_tkinter():
  tki.geometry('1200x600') # 画面サイズの設定
  tki.title('入れ替え') # 画面タイトルの設定
  #　ラベル
  label = tkinter.Label(text = "音声") #ラベルWidgetを生成
  label.place(relx = 0.04, rely = 0.1) #ラベルを配置

  Honyaku_label = tkinter.Label(text = "翻訳　テキスト",background="#f08080", foreground="#000000") #ラベルWidgetを生成
  Honyaku_label.place(relx = 0.1, rely = 0.1) #ラベルを配置

  Genko_label = tkinter.Label(text = "原稿　テキスト",background="#87ceeb", foreground="#000000") #ラベルWidgetを生成
  Genko_label.place(relx = 0.1, rely = 0.4) #ラベルを配置

  # テキストボックスの作成 翻訳

  Honyaku_txtbox_S = tkinter.Entry(width=120,background="#b22222")
  Honyaku_txtbox_S.place(relx = 0.1, rely = 0.15)
  Honyaku_txtbox_S.configure(font=("System", 17))


  Honyaku_txtbox0 = tkinter.Entry(width=120,background="#ffe4e1")
  Honyaku_txtbox0.place(relx = 0.1, rely = 0.2)
  Honyaku_txtbox0.configure(font=("System", 17))

  Honyaku_txtbox1 = tkinter.Entry(width=120,background="#ffe4e1")
  Honyaku_txtbox1.place(relx = 0.1, rely = 0.25)
  Honyaku_txtbox1.configure(font=("System", 17))

  Honyaku_txtbox2 = tkinter.Entry(width=120,background="#ffe4e1")
  Honyaku_txtbox2.place(relx = 0.1, rely = 0.3)
  Honyaku_txtbox2.configure(font=("System", 17))

  # テキストボックスの作成 原稿

  Genko_txtbox_S = tkinter.Entry(width=120,background="#87ceeb")
  Genko_txtbox_S.place(relx = 0.1, rely = 0.45)
  Genko_txtbox_S.configure(font=("System", 17))


  Genko_txtbox0 = tkinter.Entry(width=120,background="#e0ffff")
  Genko_txtbox0.place(relx = 0.1, rely = 0.5)
  Genko_txtbox0.configure(font=("System", 17))

  Genko_txtbox1 = tkinter.Entry(width=120,background="#e0ffff")
  Genko_txtbox1.place(relx = 0.1, rely = 0.55)
  Genko_txtbox1.configure(font=("System", 17))

  Genko_txtbox2 = tkinter.Entry(width=120,background="#e0ffff")
  Genko_txtbox2.place(relx = 0.1, rely = 0.6)
  Genko_txtbox2.configure(font=("System", 17))

  # 音声ボタンの作成

  onsei_btn0 = tkinter.Button(tki, text='音声０',background="#dda0dd", command = lambda: btn_Onsei_F(0)) # ボタンの設定(text=ボタンに表示するテキスト)
  onsei_btn0.place(relx = 0.034, rely = 0.15)

  onsei_btn0 = tkinter.Button(tki, text='音声１',background="#dda0dd", command = lambda: btn_Onsei_F(1)) # ボタンの設定(text=ボタンに表示するテキスト)
  onsei_btn0.place(relx = 0.034, rely = 0.2)

  onsei_btn1 = tkinter.Button(tki, text='音声２',background="#dda0dd", command = lambda: btn_Onsei_F(2)) # ボタンの設定(text=ボタンに表示するテキスト)
  onsei_btn1.place(relx = 0.034, rely = 0.25)

  onsei_btn2 = tkinter.Button(tki, text='音声３',background="#dda0dd", command = lambda: btn_Onsei_F(3))  # ボタンの設定(text=ボタンに表示するテキスト)
  onsei_btn2.place(relx = 0.034, rely = 0.3)




  # 完了ボタン　（再度確認を行う）
  OK_btn = tkinter.Button(tki, text='完了', command = lambda: btn_kanryo_F() , width=20, height=5,
                          background="#cd5c5c" ,font=("MSゴシック", "10", "bold"))
  OK_btn.place(relx = 0.2, rely = 0.8)

  # セーブボタン
  Cancel_btn = tkinter.Button(tki, text='セーブ', command = btn_Cancel_F , width=20, height=5 ,
                          background="#00bfff" ,font=("MSゴシック", "10", "bold"))
  Cancel_btn.place(relx = 0.5, rely = 0.8)


  # リセットボタン
  reset_btn = tkinter.Button(tki, text='やり直し',  command = lambda: initial_value_F(Honyaku_list, Genko_list, A_num, G_num)  , width=13, height=5,background="#228b22")
  reset_btn.place(relx = 0.8, rely = 0.8)


#　――――――――――――――　画面制作

  timing_list = Timingtext_reading_F() # 音声の絶対パスを取得

  # テキストボックスに入れる処理
  initial_value_F(Honyaku_list, Genko_list, A_num, G_num)

  tki.mainloop() # msgbox 表示

  return Honyaku_list, Genko_list, end_flg , check_hosi # この返却の前に、１．空白改行のみ行を削除と、２．改行文字（\n）を入れる

