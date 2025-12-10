実行の仕方
```
pip install fpdf2
python -m src.main --input data\unit3.csv
python -m src.main --input data
```

## CSVファイルの形式

### 1. 並べ替え問題（デフォルト）
`# type=rearrange`（省略可）

```csv
# title=Present Perfect Unit 3; instruction=次の語を正しい順に並べ替えなさい。
I have visited Kyoto three times.,私は京都に3回行ったことがあります。
...
```
- 列1: 英文
- 列2: 和訳
- 1ページ8問

### 2. 4択問題（選択問題）
`# type=selection` をヘッダーに指定してください。

```csv
# type=selection; title=Grammar Quiz; instruction=（　）に入る適切な語を選びなさい。
I (      ) a student.,私は学生です。,am,is,are,be,1
...
```
- 列1: 英文（穴埋め）
- 列2: 和訳
- 列3~6: 選択肢1~4
- 列7: 正解の番号 (1~4)
