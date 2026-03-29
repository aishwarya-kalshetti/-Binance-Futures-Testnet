import streamlit as st
import pandas as pd
import json
import os
from pathlib import Path
from bot.orders import place_order
from bot.exceptions import TradingBotException
from bot.logging_config import setup_logger

logger = setup_logger()

# Configure page UI settings
st.set_page_config(
    page_title="Binance Testnet Trading Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Modern Custom CSS specifically built for an immersive feel
st.markdown("""
<style>
    .main-header {
        font-family: 'Inter', sans-serif;
        color: #F0B90B; /* Binance Brand Color */
        font-weight: 800;
        letter-spacing: -0.5px;
        margin-bottom: 0px;
        padding-bottom: 0px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .sub-header {
        font-family: 'Inter', sans-serif;
        color: #A0AEC0;
        margin-top: 5px;
        font-size: 1.1rem;
    }
    /* Output result cards */
    .success-card {
        padding: 24px;
        border-radius: 12px;
        background-color: rgba(46, 204, 113, 0.08);
        border: 1px solid rgba(46, 204, 113, 0.5);
        color: #2ECC71;
        margin-top: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .success-card h4 { color: #2ECC71; margin-top: 0; }
    
    .error-card {
        padding: 24px;
        border-radius: 12px;
        background-color: rgba(231, 76, 60, 0.08);
        border: 1px solid rgba(231, 76, 60, 0.5);
        color: #E74C3C;
        margin-top: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .error-card h4 { color: #E74C3C; margin-top: 0; }
    
    /* Animation Keyframes */
    @keyframes fadeInSlide {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .animated-content {
        animation: fadeInSlide 0.5s ease-out forwards;
    }
</style>
""", unsafe_allow_html=True)


# --- HEADER SECTION ---
st.markdown('<h1 class="main-header">⚡ Binance Futures Terminal</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Execute trades instantly, visually, and efficiently.</p>', unsafe_allow_html=True)
st.divider()

# --- SIDEBAR CONFIGURATION ---
with st.sidebar:
    st.markdown("### 🟡 Terminal Settings")
    st.caption("Settings will fall back to your backend `.env` file if left blank.")
    
    api_key_override = st.text_input("Override API Key", type="password")
    api_secret_override = st.text_input("Override API Secret", type="password")
    
    if api_key_override and api_secret_override:
        os.environ["BINANCE_API_KEY"] = api_key_override
        os.environ["BINANCE_API_SECRET"] = api_secret_override
        st.success("Testnet Keys Overridden", icon="✅")

# --- MAIN DASHBOARD AREA ---
col_form, col_display = st.columns([1.2, 1], gap="large")

with col_form:
    st.subheader("Place New Order")
    with st.container(border=True):
        # We removed the st.form wrapper so that inputs are live and reactive to the dropdown!
        symbol = st.text_input("Symbol", value="BTCUSDT").upper()
        
        rc1, rc2 = st.columns(2)
        side = rc1.selectbox("Order Side", ["BUY", "SELL"])
        order_type = rc2.selectbox("Order Type", ["MARKET", "LIMIT", "STOP", "STOP_MARKET"])
        
        quantity = st.number_input("Quantity", min_value=0.001, value=0.01, step=0.01, format="%.3f")
        
        # Contextual Fields
        price, stop_price = None, None
        
        if order_type in ["LIMIT", "STOP"]:
            price = st.number_input("Limit Price", min_value=0.1, value=65000.0, step=100.0)
            
        if order_type in ["STOP", "STOP_MARKET"]:
            stop_price = st.number_input("Stop Price", min_value=0.1, value=60000.0, step=100.0)

        submitted = st.button("Launch Order")

if submitted:
    with col_display:
        st.subheader("Execution Status")
        with st.spinner("Connecting to Binance Testnet..."):
            try:
                response = place_order(
                    symbol=symbol,
                    side=side,
                    order_type=order_type,
                    quantity=quantity,
                    price=price if order_type in ["LIMIT", "STOP"] else None,
                    stopPrice=stop_price if order_type in ["STOP", "STOP_MARKET"] else None
                )
                
                st.markdown(f"""
                <div class="animated-content success-card">
                    <h4>✅ Order Succeeded</h4>
                    <ul style="list-style-type: none; padding-left: 0;">
                        <li><strong>Order ID</strong>: {response.get('orderId')}</li>
                        <li><strong>Status</strong>: {response.get('status')}</li>
                        <li><strong>Allocated Qty</strong>: {response.get('executedQty')}</li>
                        <li><strong>Average Fill Price</strong>: {response.get('avgPrice')}</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
                
                with st.expander("Show Detailed Payload"):
                    st.json(response)
                    
            except TradingBotException as e:
                st.markdown(f"""
                <div class="animated-content error-card">
                    <h4>❌ Execution Rejected</h4>
                    <p style="font-family: monospace;">{str(e)}</p>
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f"""
                <div class="animated-content error-card">
                    <h4>⚠️ Native System Error</h4>
                    <p>{str(e)}</p>
                </div>
                """, unsafe_allow_html=True)

# --- SYSTEM LOGS ---
st.divider()
st.markdown("### 📝 System Background Logs")

log_path = Path("logs/trading_bot.log")
if log_path.exists():
    try:
        with open(log_path, "r") as log_file:
            logs = log_file.readlines()
            # Show last 15 log operations
            recent_logs = "".join(logs[-15:])
        
        st.code(recent_logs, language="bash")
    except Exception as e:
        st.error("Failed to parse local log files.")
else:
    st.info("System operational. Waiting for first execution payload to log.")
