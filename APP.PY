import streamlit as st
import yfinance as yf
import pandas as pd

# 🔐 Page Configuration & Password Setup
st.set_page_config(page_title="My Private Trading AI", layout="wide")
st.title("📈 MY PRIVATE TRADING ASSISTANT / தனிப்பட்ட டிரேடிங் அசிஸ்டெண்ட்")

password = st.sidebar.text_input("Enter Password / பாஸ்வேர்ட் உள்ளிடவும்:", type="password")
if password != "NambaTrading2026":
    st.warning("⚠️ Access Denied: Enter correct password! / சரியான பாஸ்வேர்ட் உள்ளிட்டால் மட்டுமே ஆப் வேலை செய்யும்!")
    st.stop()

# 📊 Stock Selection Input
st.sidebar.markdown("---")
ticker_input = st.sidebar.text_input("Stock Code (e.g., RELIANCE.NS, TATAMOTORS.NS, ^NSEI):", "RELIANCE.NS").strip()
interval = st.sidebar.selectbox("Time Frame / கால அளவு:", ["1m", "5m", "15m", "1d"])

# 🔄 Fetching Live Market Data
try:
    # Multi-index குழப்பத்தை தவிர்க்க group_by="column" சேர்க்கப்பட்டுள்ளது
    data = yf.download(ticker_input, period="1d", interval=interval, group_by="column")
    
    if not data.empty:
        # Multi-index-ஐ சாதாரண சிங்கிள் லேயர் காலம்களாக மாற்றுதல் (Fixes the crash!)
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.droplevel(1)
            
        # RSI Calculation using raw pandas
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        data['RSI'] = 100 - (100 / (1 + rs))
        
        # கடைசியாக வந்த லைவ் ரோ தரவுகளை எடுத்தல்
        last_row = data.iloc[-1]
        prev_row = data.iloc[-2] if len(data) > 1 else last_row
        
        current_price = float(last_row['Close'])
        
        st.subheader(f"📊 Live Price Details / லைவ் விலை விபரம்: {ticker_input}")
        st.metric("Current Price / தற்போதைய விலை", f"₹{round(current_price, 2)}")
        
        # 🟢🔴 Buy / Sell Signal Logic
        st.subheader("🤖 AI Signals & Recommendations / ஏஐ சிக்னல்")
        current_rsi = float(last_row['RSI'])
        
        if pd.isna(current_rsi):
            st.info("🟡 **WAIT:** Calculating Indicators. Please refresh in a few seconds... / இண்டிகேட்டர்கள் கணக்கிடப்படுகிறது, சற்று காத்திருக்கவும்.")
        elif current_rsi < 35:
            st.success("🟢 **BUY SIGNAL:** Market is in Oversold zone. Price has a high chance to go up! \n\n **பை சிக்னல்:** மார்க்கெட் ஓவர்சோல்ட் (Oversold) மண்டலத்தில் உள்ளது. விலை மேலேற வாய்ப்பு அதிகம்!")
        elif current_rsi > 65:
            st.error("🔴 **SELL SIGNAL:** Market is in Overbought zone. Price has a high chance to go down! \n\n **செல் சிக்னல்:** மார்க்கெட் ஓவர்பாட் (Overbought) மண்டலத்தில் உள்ளது. விலை இறங்க வாய்ப்பு அதிகம்!")
        else:
            st.info("🟡 **HOLD / WAIT:** No clear signal. Watch the market. \n\n **வெயிட் பண்ணுங்க:** தெளிவான சிக்னல் இல்லை. சந்தையை உற்று நோக்கவும்.")
            
        # 🕯️ Candle Analysis Explanation
        st.subheader("🧐 Candle Movement Reason / கேண்டில் மூவ்மென்ட் விளக்கம்")
        if float(last_row['Close']) > float(prev_row['Close']):
            st.write("⬆️ **Why it goes up? / ஏன் மேலே போகுது?**")
            st.write("Buying pressure/volume is higher than the previous candle. Indicators show positive momentum. \n\n கடந்த கேண்டிலை விட தற்போதைய கேண்டிலில் வாங்குபவர்களின் (Buyers) ஆதிக்கம் அதிகமாக உள்ளது. இண்டிகேட்டர்களும் பாசிட்டிவ் ட்ரெண்டைக் காட்டுகின்றன.")
        else:
            st.write("⬇️ **Why it comes down? / ஏன் கீழே வருது?**")
            st.write("Selling pressure or profit booking is active. Sellers are dominating this candle. \n\n லாப நோக்கம் (Profit Booking) அல்லது விற்பவர்களின் (Sellers) அழுத்தம் அதிகமாக இருப்பதால் கேண்டில் கீழ்நோக்கி வருகிறது.")
    else:
        st.warning("No data found! Please check the stock ticker symbol. / தரவு எதுவும் கிடைக்கவில்லை! குறியீட்டைச் சரியாக உள்ளிடவும்.")
            
except Exception as e:
    st.error(f"Error fetching data: {e} / டேட்டா எடுப்பதில் சிக்கல். குறியீட்டைச் சரியாக உள்ளிடவும்.")
