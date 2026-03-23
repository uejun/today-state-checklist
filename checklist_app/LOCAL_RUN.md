# 当日状態確認チェックシート ローカル起動手順

## 前提

- Python 3.10 以上がインストール済み

---

## 1. 仮想環境の作成と有効化

```bash
cd checklist_app
python -m venv .venv
```

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**Mac / Linux:**
```bash
source .venv/bin/activate
```

---

## 2. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

---

## 3. アプリの起動

プロジェクトルートから実行する場合:

```bash
streamlit run checklist_app/streamlit_app.py
```

`checklist_app` ディレクトリ内から実行する場合:

```bash
cd checklist_app
streamlit run streamlit_app.py
```

起動後、ブラウザで `http://localhost:8501` が自動的に開く。

---

## 4. 回答データの保存先

回答データは `checklist_app/results/responses.csv` にCSV形式で保存される。
Excelで開く場合も文字化けしない（BOM付きUTF-8）。

---

## オプション: ポート番号の変更

デフォルトのポート `8501` を変更したい場合:

```bash
streamlit run streamlit_app.py --server.port 8080
```
