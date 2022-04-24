import glob
import cv2
import os
import subprocess
import sys
import time
import math



# 処理用カメラ映像の保存先
f_camera_path = "カメラ動画の保存先"
f_temp_fold = f_camera_path + "/tmp_f"

# 結合後の映像保存先
f_KAN_path ="結合後の映像保存先"

#nasにある、 mntの映像保存場所
mnt_path = "NASにある映像の保存先"

# エラー動画　格納フォルダ作成
err_dir = f_KAN_path  + "/ERROR_DIR"

# ディレクトリがない場合、作成する
if not os.path.exists(err_dir):
    print("ディレクトリを作成します")
    os.makedirs(err_dir)

if not os.path.exists(f_camera_path):
    print("ディレクトリを作成します")
    os.makedirs(f_camera_path)

if not os.path.exists(f_KAN_path):
    print("ディレクトリを作成します")
    os.makedirs(f_KAN_path)




print("---------------------")
print("カメラ　結合　 作成プログラム")
print("---------------------")
print("動画処理　開始")
time_S = time.time()
time.sleep(2)

#----------------
# 処理スタート
#----------------

# 以前のmp4データを削除させる処理
def rm_glob(rm_path, recursive=True):
    print("削除処理開始")
    count=0
    f_del_num = len(glob.glob(rm_path)) # ログの母数

    #動画移動処理
    for p in glob.glob(rm_path, recursive=recursive):
        count+=1
        #ここで、pの削除処理を行う。
        sys.stdout.write("\r{}/{} 件目のデータを削除しています".format(count, f_del_num))
        subprocess.check_call(["sudo", "rm", p])

    print("削除が完了しました")

rm_glob(f_camera_path+"/*")




#複数のフォルダを作成し、そこに移動させたあとで、一つにまとめるようにしてみた。
# nasからPCへとmp4を移動させる処理

f_num = len(glob.glob(mnt_path+"/*.mp4")) # ログの母数

def move_glob(dst_path, pathname, recursive=True):
    print("移動処理開始")

    # tempフォルダに入れたあと、全データを移動させる
    count=0
    T_num = 500
    # NASからデータを複数のフォルダに入れる
    tmp_n = math.ceil(f_num/T_num) # 一定数ごとにフォルダに入れていく
    for i in range(tmp_n):
        f_tmp_num = f_temp_fold + "/" + str(i)
        if not os.path.exists(f_tmp_num):  # 一時フォルダ作成
            print("ディレクトリを作成します")
            os.makedirs(f_tmp_num)
        #NASから動画移動処理
        for p in glob.glob(mnt_path+"/*.mp4", recursive=recursive):
            #ここで、pの移動処理を行う。
            sys.stdout.write("\r{}/{} 件目のデータを移動しています".format(count, f_num))
            subprocess.check_call(["sudo", "mv", p, f_tmp_num])
            count+=1
            if 0 == count%T_num: # 一定数をすぎるとブレイク
                break

    # 複数フォルダから、１つの場所へあつめる。
    for n in range(len(f_temp_fold)):
        print( "\n データ集合　"  + str(n) + "  フォルダ目")
        f_tmp_num = f_temp_fold + "/" + str(n)
        count = 0
        for g in glob.glob(f_tmp_num+"/*.mp4", recursive=recursive):
            count+=1
            sys.stdout.write("\r{}/{} 件目のデータを移動しています".format(count, f_num))
            subprocess.check_call(["sudo", "mv", g, f_camera_path])

    subprocess.check_call(["sudo", "rm", "-rf", f_temp_fold])    # temp_foldを削除
    print("移動が完了しました")

move_glob(f_camera_path, mnt_path+"/*")



# フォルダの中にある動画ファイルを、識別nameごとにわけて結合
def move_list_Separation():
    files = glob.glob(mnt_path + "/*.mp4")
    files = sorted(files) # 動画名をソートする
    filecount = len(files)
    print(f"総動画ファイル数   {filecount}")

    mov_list = [[]] # 識別名ごとに分けてファイル名を入れる
    mov_name = files[0].split('/')
    sikibetu_name = mov_name[4][0:5]  # 先頭５文字の識別

    listnum=0 # リストのぶん別

    # 識別名　振り分けループ : [came1]  [came2]  [came3] ..........
        # mov_list[]    に格納
    for R in files:
        R_split=R.split('/')
        SIKIBETU = R_split[4][0:5]
        # 同じ識別nameごとに、フォルダをわける
        if sikibetu_name==SIKIBETU:
            # 同じなら、ループ格納
            mov_list[listnum].append(R)
        else:
            mov_list.append([R])
            sikibetu_name=SIKIBETU
            listnum+=1


    MOV_LIST_2 = [[]]
    listnum=0 # MOV_LIST_2 リストのぶん別


    # 次は、識別名+日付ごとにフォルダ分け :  [came1-2021_1_1]   [came1-2021_1_2]  [came2-2021_1_1] ........
    # mov_list[] ->  MOV_LIST_2[]

    # 識別名+年月日 "came1-2020_1_1"
    mov_list[0] = sorted(mov_list[0]) # ファイル名をソートする
    mov_name = mov_list[0][0].split('/')
    sikibetu_name = mov_name[4]
    sikibetu_name_2 = sikibetu_name.split('-')[-4] +"-"+ sikibetu_name.split('-')[1]
    #---------------------
    for A in range(len(mov_list)):
        mov_list[A] = sorted(mov_list[A]) # ファイル名をソートする

        # 振り分けループ
        for R in mov_list[A] :
            R_split=R.split('/')
            SIKIBETU = R_split[4]
            SIKIBETU_2 = SIKIBETU.split('-')[-4] +"-"+  SIKIBETU.split('-')[1]  # 2021_08_19


            # 日付ごとに分ける
            # 同じ識別NAME + 同じ日付の場合、結合
            if sikibetu_name_2==SIKIBETU_2:
                # 同じなら、ループ格納
                MOV_LIST_2[listnum].append(R)
            else:
                MOV_LIST_2.append([R])
                sikibetu_name_2=SIKIBETU_2
                listnum+=1



    print("結合予定　動画数")
    print(len(MOV_LIST_2))


    # 複数のmp4ファイルを一つにまとめる処理
    def combine_movie(FILES, kanseimp4):

        #　確認用
        print("\n")
        print(FILES[0])


        # 【 FPS の速度を決める 】
        # fps = movie.get(cv2.CAP_PROP_FPS)
        fps = 18

        SPLIT = FILES[0].split('/')[4]
        SPLIT_2 = SPLIT.split('-')[0]

        if SPLIT_2 == "came1":
            fps = 18
        elif SPLIT_2 == "came2":
            fps = 12
        else:
            fps = 15


        print("mp4 結合処理")
        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')

        movie = cv2.VideoCapture(FILES[0])


        # 高さと横幅を動画に合わせる
        height = movie.get(cv2.CAP_PROP_FRAME_HEIGHT)
        width = movie.get(cv2.CAP_PROP_FRAME_WIDTH)

        # 動画の形式を決める（動画名. ?. FPS. (横, 縦)）
        output = cv2.VideoWriter(kanseimp4, int(fourcc), fps, (int(width), int(height)))

        frame = None

        count=0
        goukei = len(FILES)
        for i in FILES:
            count+=1
            sys.stdout.write("\r{}/{} 件目のデータを結合しています".format(count, goukei))


            # エラーチェック　問題があれば、動画を移動させる。
            try:
                vid = cv2.VideoCapture(i)
                if not vid.isOpened():
                    print(i)
                    subprocess.check_call(["sudo", "mv", i, err_dir])
                    raise NameError('Just a Dummy Exception, write your own')
            except cv2.error as e:
                print(i)
                print("cv2.error:", e)
                subprocess.check_call(["sudo", "mv", i, err_dir])
            except Exception as e:
                print(i)
                print("Exception:", e)

            else:
                #print("no problem reported　問題なし")
                # 普通の処理を行う
                movie = cv2.VideoCapture(i)
                if movie.isOpened():
                    ret, frame = movie.read()
                else:
                    ret = False
                while ret:
                    output.write(frame)
                    ret, frame = movie.read()

    # 振り分けたデータを実際に結合させていくループ --- 保存先フォルダも作成
    for B in range(len(MOV_LIST_2)):
        MOV_LIST_2[B] = sorted(MOV_LIST_2[B]) # ファイル名をソートする
        # 識別名と年月日を割り出す。
        MOV_split=MOV_LIST_2[B][0].split('/')
        tstr = MOV_split[4]
        # １．月フォルダの作成　もし存在していれば、流す　２．そのフォルダに、３．動画を保存する

        hozon_DIR =  tstr.split('-')[1]  # ここに年月日を入れる
        hozon_DIR_2 = f_KAN_path  + "/" + hozon_DIR
        hozon_DIR_2 = f_KAN_path  + "/" + hozon_DIR.split('_')[0] + "_" +  hozon_DIR.split('_')[1]

        # ディレクトリがない場合、作成する
        if not os.path.exists(hozon_DIR_2):
            print("ディレクトリを作成します")
            os.makedirs(hozon_DIR_2)

        # 完成ファイルの名前と保存先
        tstr_2 = tstr.split('-')[1] +"-"+ tstr.split('-')[2]   +"-"+tstr.split('-')[-4]
        kanseimp4  = hozon_DIR_2 + "/KETUGO-" + tstr_2 + ".mp4"

        # 動画結合処理ファンクション
        combine_movie(MOV_LIST_2[B], kanseimp4)

move_list_Separation()




# -------　処理終了　-------

print("\n結合完了")

print("処理　終了")


# 経過時間を表示する
time_E = time.time()
tim = time_E- time_S
tim_2 = math.floor(tim)

hun = math.floor(tim_2/60)
byou = tim_2%60

print(f"経過時間は {hun}分 {byou}秒 です。")











