# AI 智慧問答機器人

這是一個使用 Google Gemini AI 模型的智慧問答機器人，提供 Web 介面和 CLI 介面兩種使用方式。

## 功能特點

- 使用 Google Gemini AI 模型進行對話
- 提供 Streamlit Web 介面
- 提供 CLI 命令列介面
- 使用環境變數管理設定

## 安裝需求

1. Python 3.7 或更高版本
2. 安裝所需套件：
   ```bash
   pip install -r requirements.txt
   ```

## 環境設定

1. 複製 `.env.example` 為 `.env`
2. 在 `.env` 檔案中設定您的 Gemini API Key 和模型名稱

## 使用方法

### Web 介面

執行以下命令啟動 Web 介面：
```bash
python app.py --mode web
```

### CLI 介面

執行以下命令啟動 CLI 介面：
```bash
python app.py --mode cli
```

## 注意事項

- 請確保您有有效的 Google Gemini API Key
- Web 介面預設在 http://localhost:8501
- Flask 後端預設在 http://localhost:5000 