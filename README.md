実行の仕方
```
pip install fpdf2
python -m src.main --input data\unit3.csv
python -m src.main --input data
```

## CSVファイルの形式

1行目に `# key=value; ...` の形式でメタデータを記述できます。
- `type`: 問題タイプ (`rearrange`, `selection`, `translation`)。省略時は `rearrange`。
- `title`: PDFのタイトル。
- `instruction`: 問題の指示文。省略時はタイプごとのデフォルト文が使用されます。

### 1. 並べ替え問題（デフォルト）（１ページ８問）
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

### 3. 英文和訳問題（１ページ１１問）
`# type=translation` をヘッダーに指定してください。

```csv
# type=translation; title=英文和訳テスト
This is a pen.,これはペンです。
...
```
- 列1: 英文
- 列2: 和訳
- 問題用紙には英文のみが表示され、解答用紙に和訳が表示されます。
