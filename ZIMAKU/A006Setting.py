
import os
import datetime


from ZIMAKU import A010Parts
MY_DIRECTRY = A010Parts.DIRECTRY_F()

textfile = MY_DIRECTRY + 'text_folder'
text_path = textfile + '/HONYAKU.txt'
text_GENKOU = textfile + '/MOTOtext.txt'
text_setting = MY_DIRECTRY + 'text_folder' + '/setting'




# 原稿と翻訳のファイルを検索し、その作成日時を表示する。
def file_creation_time_f():

        HONYAKU_time = ""
        GENKO_time = ""

        # text_GENKOU  # text_path
        try:
            t_honyaku = os.path.getmtime(text_path)
            d_honyaku = datetime.datetime.fromtimestamp(t_honyaku)
            HONYAKU_time = d_honyaku.strftime('%Y年%m月%d日 %H時%M分%S秒')
        except:
            print("err A006 HONYAKU")
        try:
            t_genko = os.path.getmtime(text_GENKOU)
            d_genko = datetime.datetime.fromtimestamp(t_genko)
            GENKO_time = d_genko.strftime('%Y年%m月%d日 %H時%M分%S秒')
        except:
            print("err A006 GENKO")
        return HONYAKU_time, GENKO_time

# 初期のセッティングtxtを作成する処理。 text_setting
def create_settingtxt_F():
    if not os.path.isfile(text_setting):

        with open(text_setting, 'w',encoding='UTF-8') as f:
            f.write("100,-70,500,30")
            f.write("\n")
            f.write("\n")
        print("setting_txt　作成完了")

# settingtxtから、音声分割の設定値を取得する処理
def read_settingtxt_F():
    # 初期値
    min_silence_len = 100  #  100 〇〇ms以上無音なら分割
    silence_thresh =  -70   #  -（マイナス）-70dBFS以下で無音と判定（ここの調整で結構かわる？）
    keep_silence= 500      #　 分割後3000msは無音を残す　
    FPS = 30

    try:
        with open(text_setting, 'r', encoding='UTF-8') as f:
            text = f.readlines()
            min_silence_len = int(text[0].split(",")[0])
            silence_thresh = int(text[0].split(",")[1])
            keep_silence = int(text[0].split(",")[2])
            FPS = int(text[0].split(",")[3])
    except :
        import traceback
        traceback.print_exc()
        print("settingファイルに問題あり。初期値を読み込みます")
        if os.path.isfile(text_setting):
            os.remove(text_setting)
        create_settingtxt_F()


    return min_silence_len, silence_thresh, keep_silence, FPS

# settingtxtから、ファイル名を取得する処理
def read_setting_falename_F():
    honyakuparh = ""
    genkopath = ""
    text = ""
    # ファイルからすでに入力されている情報を取得
    try:
        with open(text_setting, 'r', encoding='UTF-8') as f:
            text = f.readlines()
    except :
        import traceback
        traceback.print_exc()
        print("名前が読み込めません")
    try:
        if os.path.exists(text_path):
            honyakuparh = text[1]
    except:
        print("翻訳ファイルなし")
    try:
        if os.path.exists(text_GENKOU):
            genkopath = text[2]
    except:
        print("原稿ファイルなし")


    return honyakuparh, genkopath

# settingtxtに保存する処理
def setting_Write_F(min, volume, keep, fps):

    honyakuparh, genkopath = read_setting_falename_F()
    honyakuparh = honyakuparh.replace( '\n' , '' )
    genkopath = genkopath.replace( '\n' , '' )


    # テキストファイルに書き込み
    with open(text_setting, 'w',encoding='UTF-8') as f:
        setting_text = str(min) + "," + str(volume) + "," + str(keep) + "," + str(fps)
        f.write(setting_text)
        f.write("\n" + honyakuparh)
        f.write("\n" + genkopath)   # TODO ここが増えたり消えたり
        print("書き込み完了")

# settingtxtにファイル名を保存する処理
def settin_Write_filename_F(honyakuname, genkoname):

    hon_name, gen_name = read_setting_falename_F()
    min_silence_len, silence_thresh, keep_silence, FPS = read_settingtxt_F()

    if not honyakuname == "":
        hon_name = honyakuname
    if not genkoname == "":
        gen_name = genkoname

    hon_name = hon_name.replace( '\n' , '' )
    gen_name = gen_name.replace( '\n' , '' )

    # テキストファイルに書き込み
    with open(text_setting, 'w',encoding='UTF-8') as f:
        setting_text = str(min_silence_len) + "," + str(silence_thresh) + "," + str(keep_silence) + "," + str(FPS)
        f.write(setting_text)
        f.write("\n" + hon_name)
        f.write("\n" + gen_name)
        print("書き込み完了")


