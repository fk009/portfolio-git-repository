


# 自分のディレクトリを把握
def DIRECTRY_F():
    MY_DIR = __file__.split("\\")
    MY_DIRECTRY =  [MY_DIR[n] for n in range(len(MY_DIR) - 1)]
    MY_DIRECTRY = "/".join(MY_DIRECTRY) + "/"
    return MY_DIRECTRY



# 動画(mp4)から音声ファイル(wav)へ変換
def Movie_convert(MVpath,WAVpath):
    import os, sys
    import subprocess

    Input_file = MVpath
    Sampling_grate     = 44100
    Channnel    = 1
    Output_file = WAVpath

    cmd = "ffmpeg -y -i {} -ab {}k -ac {} {}".format(Input_file, Sampling_grate, Channnel, Output_file)
    resp = subprocess.check_output(cmd, shell=True)
    print("A010 wavファイル作成完了")





# 動画(mp4)から音声ファイル(wav)へ変換 (前の失敗)
def Movie_convert_2(MVpath,WAVpath):
    import ffmpeg
    # 入力
    stream = ffmpeg.input(MVpath)
    # 出力
    stream = ffmpeg.output(stream, WAVpath)
    # 実行
    ffmpeg.run(stream)


    # そのままだと64bitのwavファイルで読み取れない可能性があるので、32bitへと変換する処理を行う。
    # 変換するwavファイル拡張子を、mp3へとリネームした後、再びwavファイルへと変換処理
    mp3path = WAVpath.rstrip('wav') + "mp3"

    import os
    # 存在すれば、mp3ファイルを削除する
    if os.path.isdir(mp3path):
        os.remove(mp3path)


    import os
    os.rename(WAVpath, mp3path)

    import subprocess
    subprocess.call(['ffmpeg', '-i', mp3path, WAVpath])


    import pydub
    sound = pydub.AudioSegment.from_wav(WAVpath)
    sound = sound.set_channels(1)
    sound.export(WAVpath, format="wav")


    print("wav 完了")