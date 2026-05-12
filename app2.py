import streamlit as st
import yfinance as yf
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="Stock Price Prediction", layout="wide")

st.title("Real-Time Stock Price Prediction System")

stock_symbol = st.text_input("Enter Stock Symbol", "AAPL").upper()

if st.button("Predict"):


    ticker = yf.Ticker(stock_symbol)
    data = ticker.history(period="5y")

    if data.empty:
        st.error("No data found. Try symbols like AAPL, TSLA, MSFT, RELIANCE.NS")
    else:
        df = data[["Open", "High", "Low", "Volume", "Close"]].copy()

        df["Target"] = df["Close"].shift(-1)
        df.dropna(inplace=True)

        X = df[["Open", "High", "Low", "Volume", "Close"]]
        y = df["Target"]

        model = LinearRegression()
        model.fit(X, y)

        latest_data = X.tail(1)
        predicted_price = float(model.predict(latest_data)[0])
        current_price = float(latest_data["Close"].iloc[0])

        if predicted_price > current_price:
            signal = "BUY"
        elif predicted_price < current_price:
            signal = "SELL"
        else:
            signal = "HOLD"

        st.subheader("Prediction Result")
        st.write(f"Current Price: {round(current_price, 2)}")
        st.write(f"Predicted Price: {round(predicted_price, 2)}")
        st.write(f"Signal: {signal}")

        st.line_chart(df["Close"])