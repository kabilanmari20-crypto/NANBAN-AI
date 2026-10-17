import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta

# 🔐 Page Configuration & Password Setup
st.set_page_config(page_title="My Private Trading AI", layout="wide")
st.title("📈 MY PRIVATE TRADING ASSISTANT / தனிப்பட்ட டிரேடிங் அசிஸ்டெண்ட்")

password = st.sidebar.text_input("Enter Password / பாஸ்வேர்ட் உள்ளிடவும்:", type="password")
if password != "NambaTrading2026": # 👈 உங்களுக்கு பிடித்த பாஸ்வேர்டை இங்கே மாற்றிக் கொள்ளலாம்
    st.warning("⚠️ Access Denied: Enter correct password! / சரியான பாஸ்வேர்ட் உள்ளிட்டால் மட்டுமே ஆப் வேலை செய்யும்!")
    st.stop()

# 📊 Stock Selection Input
st.sidebar.markdown("---")
ticker = st.sidebar.text_input("Stock Code (e.g., RELIANCE.NS, TATAMOTORS.NS, ^NSEI):", "RELIANCE.NS")
interval = st.sidebar.selectbox("Time Frame / கால அளவு:", ["1m", "5m", "15m", "1d"])

# 🔄 Fetching Live Market Data
try:
    data = yf.download(ticker, period="1d", interval=interval)
    
    if not data.empty:
        # Technical Indicators Calculation
        data['RSI'] = ta.rsi(data['Close'])
        macd = ta.macd(data['Close'])
        data = pd.concat([data, macd], axis=1)
        
        last_row = data.iloc[-1]
        prev_row = data.iloc[-2]
        
        st.subheader(f"📊 Live Price Details / லைவ் விலை விபரம்: {ticker}")
        st.metric("Current Price / தற்போதைய விலை", f"₹{round(last_row['Close'], 2)}")
        
        # 🟢🔴 Buy / Sell Signal Logic
        st.subheader("🤖 AI Signals & Recommendations / ஏஐ சிக்னல்")
        if last_row['RSI'] < 35:
            st.success("🟢 **BUY SIGNAL:** Market is in Oversold zone. Price has a high chance to go up! \n\n **பை சிக்னல்:** மார்க்கெட் ஓவர்சோல்ட் (Oversold) மண்டலத்தில் உள்ளது. விலை மேலேற வாய்ப்பு அதிகம்!")
        elif last_row['RSI'] > 65:
            st.error("🔴 **SELL SIGNAL:** Market is in Overbought zone. Price has a high chance to go down! \n\n **செல் சிக்னல்:** மார்க்கெட் ஓவர்பாட் (Overbought) மண்டலத்தில் உள்ளது. விலை இறங்க வாய்ப்பு அதிகம்!")
        else:
            st.info("🟡 **HOLD / WAIT:** No clear signal. Watch the market. \n\n **வெயிட் பண்ணுங்க:** தெளிவான சிக்னல் இல்லை. சந்தையை உற்று நோக்கவும்.")
            
        # 🕯️ Candle Analysis Explanation
        st.subheader("🧐 Candle Movement Reason / கேண்டில் மூவ்மென்ட் விளக்கம்")
        if last_row['Close'] > prev_row['Close']:
            st.write("⬆️ **Why it goes up? / ஏன் மேலே போகுது?**")
            st.write("Buying pressure/volume is higher than the previous candle. Indicators show positive momentum. \n\n கடந்த கேண்டிலை விட தற்போதைய கேண்டிலில் வாங்குபவர்களின் (Buyers) ஆதிக்கம் அதிகமாக உள்ளது. இண்டிகேட்டர்களும் பாசிட்டிவ் ட்ரெண்டைக் காட்டுகின்றன.")
        else:
            st.write("⬇️ **Why it comes down? / ஏன் கீழே வருது?**")
            st.write("Selling pressure or profit booking is active. Sellers are dominating this candle. \n\n லாப நோக்கம் (Profit Booking) அல்லது விற்பவர்களின் (Sellers) அழுத்தம் அதிகமாக இருப்பதால் கேண்டில் கீழ்நோக்கி வருகிறது.")
            
except Exception as e:
    st.error("Error fetching data. Please check the stock symbol (Add .NS for Indian stocks). / டேட்டா எடுப்பதில் சிக்கல். குறியீட்டைச் சரியாக உள்ளிடவும்.")
