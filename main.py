import os
import re
import csv

############################################
# ここだけ設定せよ！！！！
# output.csvに出力されるよ！！！！
ABSOLUTE_SRC_PATH = "C:/Users/duck5/Desktop/src"
############################################


def extract_public_methods_from_php(file_path):
    """指定されたPHPファイルからpublicメソッドを抽出します。"""
    public_methods = []
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
        # 正規表現でpublic functionを抽出
        matches = re.finditer(r"\bpublic function (\w+)\(", content)
        for match in matches:
            public_methods.append(match.group(1))
    return public_methods


def analyze_cakephp_source(source_folder, output_csv):
    """CakePHPのソースコードを解析し、結果をCSVに出力します。"""
    csv_data = [["prefix", "controller", "action"]]

    for root, dirs, files in os.walk(source_folder):
        for file in files:
            if file.endswith(".php"):
                # ファイルパスからプリフィックスとコントローラー名を抽出
                relative_path = os.path.relpath(root, source_folder)
                parts = relative_path.split(os.sep) + [file[:-4]]  # '.php'を除去
                if len(parts) >= 3 and parts[0] == "Controller":
                    prefix = parts[1]
                    controller = parts[2]
                    # 末尾のControllerを除去
                    if controller.endswith("Controller"):
                        controller = controller[:-10]
                    actions = extract_public_methods_from_php(os.path.join(root, file))
                    for action in actions:
                        csv_data.append([prefix, controller, action])

    # CSVファイルに書き込み
    with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(csv_data)


if __name__ == "__main__":
    output_csv = "output.csv"
    analyze_cakephp_source(ABSOLUTE_SRC_PATH, output_csv)
