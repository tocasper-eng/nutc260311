import streamlit as st
import yfinance as yf
import pandas as pd
import datetime

# 設定頁面標題
st.set_page_config(page_title="鴻海 (2317) 股價查詢工具")
st.title("📈 鴻海 (2317) 股價查詢系統")

# 側邊欄：輸入日期區間
st.sidebar.header("查詢參數")
today = datetime.date.today()
start_date = st.sidebar.date_input("開始日期", today - datetime.timedelta(days=365))
end_date = st.sidebar.date_input("結束日期", today)

if start_date < end_date:
    # 抓取資料
    with st.spinner('資料抓取中...'):
        df = yf.download("2317.TW", start=start_date, end=end_date)

    if not df.empty:
        # 顯示統計摘要
        st.subheader("📊 數據表格 (Grid)")
        st.dataframe(df.sort_index(ascending=False), use_container_width=True)

        # 顯示線形圖
        st.subheader("📉 股價走勢圖")
        st.line_chart(df['Close'])
        
        # 下載按鈕 (可供匯入您常用的 SQL Server)
        csv = df.to_csv().encode('utf-8')
        st.download_button("下載 CSV 檔案", csv, "foxconn_stock.csv", "text/csv")
    else:
        st.warning("該區間查無資料，請重新選擇。")
else:
    st.error("錯誤：開始日期必須早於結束日期。")
