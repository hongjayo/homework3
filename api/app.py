import os
import streamlit as st
from flask import Flask, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv
import argparse
import threading

# 載入環境變數
load_dotenv()

# 設定 Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyBlYVDEjAo7k5cZhtoRso63Ww4HIsaRanc")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(GEMINI_MODEL)

# 初始化 Flask 應用
app = Flask(__name__)

# Flask 路由
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    
    try:
        response = model.generate_content(user_message)
        return jsonify({'response': response.text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Streamlit 介面
def main():
    st.set_page_config(
        page_title="AI 智慧問答機器人",
        page_icon="🤖",
        layout="centered"
    )
    
    st.title("AI 智慧問答機器人")
    
    # 初始化聊天歷史
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # 顯示聊天歷史
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # 使用者輸入
    if prompt := st.chat_input("請輸入您的問題"):
        # 添加使用者訊息到聊天歷史
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # 獲取 AI 回應
        with st.chat_message("assistant"):
            try:
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"發生錯誤: {str(e)}")

# CLI 介面
def cli_interface():
    print("歡迎使用 AI 智慧問答機器人 CLI 版本")
    print("輸入 'quit' 或 'exit' 結束對話")
    
    while True:
        user_input = input("\n請輸入您的問題: ")
        if user_input.lower() in ['quit', 'exit']:
            break
            
        try:
            response = model.generate_content(user_input)
            print("\nAI 回應:", response.text)
        except Exception as e:
            print(f"\n發生錯誤: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='AI 智慧問答機器人')
    parser.add_argument('--mode', choices=['web', 'cli'], default='web',
                      help='選擇運行模式: web (Streamlit) 或 cli (命令列)')
    args = parser.parse_args()
    
    if args.mode == 'web':
        # 在背景執行 Flask
        flask_thread = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=5000))
        flask_thread.daemon = True
        flask_thread.start()
        
        # 執行 Streamlit
        main()
    else:
        cli_interface() 