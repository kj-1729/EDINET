# EDINET
EDINETから有価証券データをダウンロードし、データセットを作るプログラム

# 使い方
## 日別リストの取得
```
python get_list.py ymd_from ymd_to output_dir output_fname subscription_key
```
- ymd_from: リスト取得する最初の日付
- ymd_to: リスト取得する最後の日付
- output_dir: 出力先のディレクトリ
- output_fname: 出力ファイル（output_fname)_(yyyy-mm-dd).jsonという名前のファイルで保存される
- subscription_key: EDINETから発行されたAPI Key 

## レポートの取得
取得した日別リストから、レポート名を取得して、EDINETのサイトからDLする
```
python get_report.py ymd_from ymd_to bank_master_path list_dir list_fname output_dir subscription_key > report_list_path
```
- ymd_from: レポートをDLする最初の日付
- ymd_to: レポートをDLする最後の日付
- bank_master_path: 銀行のedinetCodeのリスト（今回は銀行のみデータ取得している）
- list_dir: 日別リストのあるディレクトリ
- list_fname: 日別リストのファイル名（（output_fname)_(yyyy-mm-dd).jsonという名前で保存されている）
- output_dir: レポート出力するディレクトリ（DocID).zipという名前で保存される
- subscription_key: EDINETから発行されたAPI Key
- report_list_path: ここにDocIDなど、レポートのメタ情報を出力する

## CSVのマージ
各レポートは、zipファイルの中のcsvファイル。BS/PLと関係ない情報も含まれる
ここから更に、csvファイルを読み込み、ファイルのマージ処理を行う
```
python mege_csv.py element_id_master_path report_list_path docs_dir > csv_path
```
- element_id_master_path: 集計対象のelement_idを治めているファイル
- report_list_path: レポートのリストが書かれているファイル
- docs_dir: 実際のレポートがあるディレクトリ
- csv_path: 結果ファイル

