# 銅期貨價格趨勢圖 (Databento)

資料來源：[Databento](https://databento.com/) GLBX.MDP3 資料集，symbol `HG.c.0`（CME 銅期貨連續合約，美分/磅）。

## 內容
- `fetch_and_build.py`：抓取最近一個月日線 OHLCV 資料，輸出 `copper_hg_daily.csv`
- `copper_hg_daily.csv`：已抓取的日線資料（範例快照）
- `index.html`：K 線趨勢圖，支援拖曳區間拉桿與快捷按鈕（近1週/2週/1個月/全部）

## 使用方式
1. 設定 API Key（擇一）：
   - 環境變數：`set DATABENTO_API_KEY=你的key`（Windows）或 `export DATABENTO_API_KEY=你的key`（macOS/Linux）
   - 或複製 `databento_config.example.json` 為 `databento_config.json` 並填入 key（此檔已加入 .gitignore，不會被提交）
2. 執行 `python fetch_and_build.py` 產生最新的 `copper_hg_daily.csv`
3. 直接用瀏覽器開啟 `index.html` 即可查看趨勢圖

## 注意事項
- HG 是 CME 美系期貨報價（美分/磅），與 LME 銅現貨或上海期交所報價單位、基礎不同，僅供趨勢參考，不可直接對標。
- Databento 免費帳號有一次性測試額度，超過需自行付費。
