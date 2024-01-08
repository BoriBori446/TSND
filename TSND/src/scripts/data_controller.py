"""
データロガー2個分のファイルを操作する
＊フォーマットはSensorControllerV4利用を想定

ここで処理するために、記録時の設定が必要です。
データロガーを、PS12,PS34としておく。　*圧力センサー1番2番、3番4番の意。

"""

# =========================
# config
# =========================
dst = "src/data/merged"

# ============================
# import
# ============================
import pandas as pd
import glob
import os


# =========================
# define
# =========================
def merge_data(root, target):
    """

    :param root:
    :param target:
    :return:
    """
    # ベースパス設定
    path = os.path.join(root, target)
    files = glob.glob(path + "/*.csv")

    # データ読み込み
    src1 = [file for file in files if os.path.basename(file).startswith("PS12")][0]
    src2 = [file for file in files if os.path.basename(file).startswith("PS34")][0]
    # カラムが無名なのでデフォルトのカラムNoで処理
    data1 = pd.read_csv(src1, usecols=[1, 6, 7])
    data2 = pd.read_csv(src2, usecols=[1, 6, 7])
    # カラム名をリネーム
    data1.columns = ["ts", "p1", "p2"]
    data2.columns = ["ts", "p3", "p4"]
    # データマージ、targetをファイル名にして保存
    data = pd.merge(data1, data2, on="ts")
    data["ts"] = data["ts"] - data["ts"].min()
    data["sum"] = data["p1"] + data["p2"] + data["p3"] + data["p4"]
    data.to_csv(os.path.join(dst, target + ".csv"), index=False)
