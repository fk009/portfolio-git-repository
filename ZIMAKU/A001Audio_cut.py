#　音声wavファイルを無音で区切って分割し、その始まり終わり時間をテキストに保存する処理


from pydub import AudioSegment
from pydub.silence import split_on_silence
import os
import shutil
import sys
import math

from ZIMAKU import A006Setting

from ZIMAKU.A010Parts import DIRECTRY_F
MY_DIRECTRY = DIRECTRY_F()


# 分割するwavファイル
cutwav = MY_DIRECTRY + 'ONSEI.wav'

#　カットした音楽を保存する場所と名前
wav_name = MY_DIRECTRY + 'testwav/output'
wav_fold = MY_DIRECTRY + 'testwav'

#　字幕のタイミングを記述したファイル
Timingtext_path = MY_DIRECTRY + 'text_folder/timing.txt'


#-----------------------------------------------------

# TODO
# セッティングtxtファイルから、設定を受け継ぐ。
def Audio_setting_F():
    # セッティングtxtがない場合、エラーを返す。

    # あった場合、その値を引き継ぐ。

    pass


def Audio_cut_F():


    #wav音声データを無音があるごとに分割していき、testwavフォルダに保存する処理
    print("分割 開始")

    # wavファイルのデータ取得
    try:
        sound = AudioSegment.from_file(cutwav, format="wav")
    except FileNotFoundError:
        print(cutwav + "フォルダかファイルが見当たらない可能性あり")
        sys.exit()


    # wavフォルダを空にして作成する。
    if os.path.exists(wav_fold) == True:
        shutil.rmtree(wav_fold)
        os.makedirs(wav_fold)


    # wavデータの分割（無音部分で区切る）処理
        # ※このパラメータを変更することにより、分割される間隔が変わる。

    # min_silence_len=100  #  100 〇〇ms以上無音なら分割
    # silence_thresh=-70   #  -（マイナス）-70dBFS以下で無音と判定（ここの調整で結構かわる？）
    # keep_silence= 500      #　 分割後3000msは無音を残す　
    # FPS = 30   # FPS設定　# 注意！　Aviutil編集 側のFPSと、プログラムのFPSを一緒にすること！

    # TODO settingファイルから、分割に関連する値を取得してくる。
    min_silence_len, silence_thresh, keep_silence, FPS = A006Setting.read_settingtxt_F()

    chunks = split_on_silence(sound, min_silence_len, silence_thresh, keep_silence)


    #　タイミングを記録するためのテキストファイルの作成
    f = open(Timingtext_path, 'w', encoding = "utf_8")
    f.write("")
    f.close()
    print("-Timingtext creation-")


    # timingテキストに音声のstart,end時間を書く。さらに、どの音声を使ったかを保存
    # スタート,エンド-音声の番号
    def time_txt_F(outputAudio):
        timingtxt = str(start) + "," + str(end) + "-" + outputAudio + "\n"
        f = open(Timingtext_path, 'a', encoding = "utf_8")
        f.write(timingtxt)  # 記述する内容
        f.close()
        print("---start,end time　記述完了" + str(i))


    # 分割したデータ毎にファイルに出力し、さらにタイミングをテキストに記録
    I = 0
    Audiosec_list = []
    for i, chunk in enumerate(chunks):
        # 音声を保存していく
        chunk.export(wav_name + str(i) +".wav", format="wav")

        # 保存された音声の時間を測る
        outputAudio = wav_name + str(i) + ".wav"
        print(outputAudio)
        sourceAudio = AudioSegment.from_wav(outputAudio)
        Audiosec = sourceAudio.duration_seconds

        #小数点以下が多いので、小数点以下２つまでを残す
        Audiosec_2 = round(Audiosec , 4)
        Audiosec_list.append(Audiosec_2)
        print(Audiosec_2)

        #　時間が立つごとに、小数点以下の時間の合計で、字幕のずれが激しくなってしまう。
            # そこで、音声時間を足して、それを割る感じにしてみた。

        #　テキストに、スタート、エンド時間を保存していく。
        if i == 0: #最初のときだけ、start = o end = 動画時間(変数FPSに依存した換算)
            start = 1
            end = math.floor(Audiosec_2 * FPS) - 1   # (重ならないようにしている)
            time_txt_F(outputAudio) #テキストに記述
        else:
            start = end + 1 #　１を足さないと、字幕時にバグる (重ならないようにしている)
            end = math.floor(Audiosec_2 * FPS)
            end = start + end - 1


            # ５回に1回、時間調整の計算を行う
            if i % 5 == 0:
                gousei = Audiosec_list[i-4]
                for A in range(4):
                    gousei += Audiosec_list[i-A]
                if i == 5:
                    # i%5なので、初回だけは０から５の６個を足す必要があった。
                    gousei_2 = gousei + Audiosec_list[0]
                else:
                    gousei_2 += gousei

                end = math.floor(gousei_2 * FPS)


            time_txt_F(outputAudio) #テキストに記述
        I += 1


    print("enddd")







