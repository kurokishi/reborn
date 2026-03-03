import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
import json
import os

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Reborn Rich | Analisis Saham AI",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Courier+Prime:wght@400;700&display=swap');

/* ─ Global ─ */
html, body, [data-testid="stAppViewContainer"] {
    background-color: #0a0705 !important;
    color: #c8a96e;
}
[data-testid="stAppViewContainer"] { background-color: #0a0705 !important; }
[data-testid="stHeader"] { background-color: #0a0705 !important; }
[data-testid="stSidebar"] { background-color: #0d0b07 !important; }
.block-container { max-width: 1400px !important; padding-top: 1rem !important; }

/* ─ Typography ─ */
h1, h2, h3 { font-family: 'Playfair Display', Georgia, serif !important; }
p, div, span, label { font-family: 'Courier Prime', monospace !important; }

/* ─ Header ─ */
.rr-header {
    text-align: center;
    padding: 1rem 0 1rem;
    border-bottom: 1px solid #2a2010;
    margin-bottom: 1.5rem;
}
.rr-eyebrow {
    font-family: 'Courier Prime', monospace !important;
    font-size: 0.65rem;
    letter-spacing: 0.4em;
    color: #5c4a2a;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}
.rr-title {
    font-family: 'Playfair Display', Georgia, serif !important;
    font-size: clamp(2rem, 4vw, 3rem);
    color: #d4af37;
    margin: 0;
    text-shadow: 0 0 30px #d4af3755;
    letter-spacing: 0.08em;
}
.rr-subtitle {
    font-size: 0.8rem;
    color: #5c4a2a;
    letter-spacing: 0.2em;
    font-style: italic;
    margin-top: 0.4rem;
}

/* ─ Cards ─ */
.rr-card {
    background: #0d0b07;
    border: 1px solid #1e1810;
    border-radius: 4px;
    padding: 1rem 1.2rem;
    margin-bottom: 1rem;
    transition: border-color 0.3s, box-shadow 0.3s;
}
.rr-card:hover {
    border-color: #d4af3744;
    box-shadow: 0 0 16px #d4af3715;
}
.rr-card-label {
    font-family: 'Courier Prime', monospace !important;
    font-size: 0.6rem;
    letter-spacing: 0.3em;
    color: #5c4a2a;
    text-transform: uppercase;
    margin-bottom: 0.6rem;
}
.rr-card-body {
    font-family: 'Playfair Display', serif !important;
    color: #c8a96e;
    font-size: 0.9rem;
    line-height: 1.6;
}

/* ─ Alert Banner ─ */
.rr-alert {
    background: linear-gradient(135deg, #d4af3710, #0d0b07);
    border-left: 3px solid #d4af37;
    padding: 0.8rem 1rem;
    margin-bottom: 0.5rem;
    border-radius: 0 4px 4px 0;
}
.rr-alert-beli { border-left-color: #4ade80; }
.rr-alert-jual { border-left-color: #f87171; }
.rr-alert-tahan { border-left-color: #fbbf24; }

/* ─ Comparison Table ─ */
.comparison-table {
    width: 100%;
    border-collapse: collapse;
}
.comparison-table th {
    color: #d4af37;
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    padding: 0.5rem;
    border-bottom: 1px solid #2a2010;
}
.comparison-table td {
    padding: 0.5rem;
    border-bottom: 1px solid #1e1810;
    color: #c8a96e;
}
.comparison-table tr:last-child td {
    border-bottom: none;
}
.score-high { color: #4ade80; }
.score-mid { color: #fbbf24; }
.score-low { color: #f87171; }

/* ─ Button ─ */
.stButton > button {
    background: linear-gradient(135deg, #d4af37, #a07d20) !important;
    color: #0a0705 !important;
    border: none !important;
    border-radius: 2px !important;
    font-family: 'Courier Prime', monospace !important;
    font-weight: 700 !important;
    letter-spacing: 0.2em !important;
    font-size: 0.7rem !important;
    padding: 0.4rem 1rem !important;
    text-transform: uppercase !important;
    box-shadow: 0 0 20px #d4af3733 !important;
    transition: all 0.3s !important;
}
.stButton > button:hover {
    box-shadow: 0 0 30px #d4af3766 !important;
    transform: translateY(-1px) !important;
}

/* ─ Score bar ─ */
.score-container { margin-bottom: 0.5rem; }
.score-label-row {
    display: flex;
    justify-content: space-between;
    margin-bottom: 2px;
}
.score-label {
    font-family: 'Courier Prime', monospace !important;
    font-size: 0.6rem;
    letter-spacing: 0.15em;
    color: #8b7355;
    text-transform: uppercase;
}
.score-value { font-weight: 700; font-family: 'Courier Prime', monospace !important; font-size: 0.7rem; }
.score-track {
    height: 3px;
    background: #1a1410;
    border-radius: 2px;
    overflow: hidden;
}
.score-fill {
    height: 100%;
    border-radius: 2px;
}

/* ─ Disclaimer ─ */
.rr-disclaimer {
    text-align: center;
    font-size: 0.6rem;
    color: #3d2e15;
    letter-spacing: 0.05em;
    line-height: 1.7;
    padding: 1rem 0;
    font-family: 'Courier Prime', monospace !important;
}

/* ─ Alert Settings ─ */
.alert-setting {
    background: #0d0b07;
    border: 1px solid #1e1810;
    border-radius: 4px;
    padding: 0.8rem;
    margin-bottom: 0.8rem;
}
</style>
""", unsafe_allow_html=True)

# ── Data Classes ─────────────────────────────────────────────────────────────

class AlertManager:
    """Manages price alerts for stocks"""
    
    def __init__(self):
        self.alerts_file = "alerts.json"
        self.load_alerts()
    
    def load_alerts(self):
        """Load alerts from file"""
        if os.path.exists(self.alerts_file):
            try:
                with open(self.alerts_file, 'r') as f:
                    self.alerts = json.load(f)
            except:
                self.alerts = {}
        else:
            self.alerts = {}
    
    def save_alerts(self):
        """Save alerts to file"""
        with open(self.alerts_file, 'w') as f:
            json.dump(self.alerts, f)
    
    def add_alert(self, symbol: str, alert_type: str, target_price: float, condition: str):
        """Add a new price alert"""
        if symbol not in self.alerts:
            self.alerts[symbol] = []
        
        alert = {
            'id': f"{symbol}_{len(self.alerts[symbol])}_{int(time.time())}",
            'type': alert_type,
            'target_price': target_price,
            'condition': condition,  # 'above' or 'below'
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'triggered': False
        }
        self.alerts[symbol].append(alert)
        self.save_alerts()
        return alert
    
    def remove_alert(self, symbol: str, alert_id: str):
        """Remove an alert"""
        if symbol in self.alerts:
            self.alerts[symbol] = [a for a in self.alerts[symbol] if a['id'] != alert_id]
            if not self.alerts[symbol]:
                del self.alerts[symbol]
            self.save_alerts()
    
    def check_alerts(self, current_prices: Dict[str, float]) -> List[Dict]:
        """Check which alerts have been triggered"""
        triggered = []
        
        for symbol, alerts in self.alerts.items():
            if symbol in current_prices:
                price = current_prices[symbol]
                for alert in alerts:
                    if not alert['triggered']:
                        condition_met = False
                        if alert['condition'] == 'above' and price >= alert['target_price']:
                            condition_met = True
                        elif alert['condition'] == 'below' and price <= alert['target_price']:
                            condition_met = True
                        
                        if condition_met:
                            alert['triggered'] = True
                            alert['triggered_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            alert['triggered_price'] = price
                            triggered.append(alert)
        
        if triggered:
            self.save_alerts()
        
        return triggered

# ── Helper Functions ──────────────────────────────────────────────────────────

def extract_symbol(query: str) -> str:
    """Extract stock symbol from user query."""
    query = query.upper().strip()
    
    # Common Indonesian stocks mapping
    id_stocks = {
        'BBCA': 'BBCA.JK', 'BBRI': 'BBRI.JK', 'BMRI': 'BMRI.JK', 
        'TLKM': 'TLKM.JK', 'ASII': 'ASII.JK', 'BREN': 'BREN.JK',
        'GOTO': 'GOTO.JK', 'BYAN': 'BYAN.JK', 'ADRO': 'ADRO.JK',
        'ANTM': 'ANTM.JK', 'INDF': 'INDF.JK', 'ICBP': 'ICBP.JK'
    }
    
    if query in id_stocks:
        return id_stocks[query]
    
    # US stocks
    us_stocks = {
        'TSLA': 'TSLA', 'AAPL': 'AAPL', 'MSFT': 'MSFT',
        'GOOGL': 'GOOGL', 'AMZN': 'AMZN', 'META': 'META',
        'NVDA': 'NVDA', 'JPM': 'JPM', 'V': 'V'
    }
    
    if query in us_stocks:
        return us_stocks[query]
    
    # Crypto
    crypto = {
        'BTC': 'BTC-USD', 'ETH': 'ETH-USD', 'BNB': 'BNB-USD',
        'SOL': 'SOL-USD', 'XRP': 'XRP-USD'
    }
    
    if query in crypto:
        return crypto[query]
    
    return query if '.' in query else f"{query}.JK"

@st.cache_data(ttl=300)  # Cache 5 menit
def get_stock_data(symbol: str, period: str = "3mo") -> Optional[pd.DataFrame]:
    """Get stock data from yfinance"""
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period=period)
        if hist.empty:
            return None
        return hist
    except:
        return None

@st.cache_data(ttl=300)
def get_stock_info(symbol: str) -> Dict:
    """Get stock info from yfinance"""
    try:
        stock = yf.Ticker(symbol)
        return stock.info
    except:
        return {}

def calculate_rsi(prices: pd.Series, periods: int = 14) -> float:
    """Calculate RSI indicator."""
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=periods).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=periods).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1] if not pd.isna(rsi.iloc[-1]) else 50

def analyze_stock(symbol: str) -> Optional[Dict[str, Any]]:
    """Analyze stock using yfinance data."""
    try:
        hist = get_stock_data(symbol, "6mo")
        info = get_stock_info(symbol)
        
        if hist is None or hist.empty:
            return None
        
        current_price = hist['Close'].iloc[-1]
        prev_price = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
        
        # Calculate indicators
        daily_change = ((current_price - prev_price) / prev_price) * 100
        ma20 = hist['Close'].rolling(window=20).mean().iloc[-1] if len(hist) >= 20 else current_price
        ma50 = hist['Close'].rolling(window=50).mean().iloc[-1] if len(hist) >= 50 else current_price
        rsi = calculate_rsi(hist['Close'])
        
        # Volume analysis
        avg_volume = hist['Volume'].rolling(window=20).mean().iloc[-1] if len(hist) >= 20 else hist['Volume'].mean()
        current_volume = hist['Volume'].iloc[-1]
        volume_ratio = current_volume / avg_volume if avg_volume > 0 else 1
        
        # Scoring
        pe = info.get('trailingPE', 15)
        pb = info.get('priceToBook', 1.5)
        
        # Fundamental score
        if pe < 15:
            fundamental_score = 8
        elif pe < 25:
            fundamental_score = 6
        elif pe < 35:
            fundamental_score = 4
        else:
            fundamental_score = 3
            
        # Momentum score
        if rsi < 30:
            momentum_score = 8
        elif rsi > 70:
            momentum_score = 4
        else:
            momentum_score = 6
            
        if current_price > ma50 and current_price > ma20:
            momentum_score += 1
        elif current_price < ma50 and current_price < ma20:
            momentum_score -= 1
            
        # Valuation score
        if pb < 1:
            valuation_score = 8
        elif pb < 2:
            valuation_score = 7
        elif pb < 3:
            valuation_score = 5
        else:
            valuation_score = 4
            
        # Catalyst score
        catalyst_score = 5
        if volume_ratio > 1.5:
            catalyst_score += 2
        elif volume_ratio > 1.2:
            catalyst_score += 1
            
        # Decision
        total_score = (fundamental_score + momentum_score + valuation_score + catalyst_score) / 4
        
        if total_score >= 7:
            decision = "BELI"
            conviction = min(10, int(total_score + 1))
        elif total_score <= 4:
            decision = "JUAL"
            conviction = min(10, int(10 - total_score))
        else:
            decision = "TAHAN"
            conviction = int(total_score)
        
        target_price = current_price * (1 + (total_score - 5) * 0.05)
        
        return {
            "symbol": symbol,
            "name": info.get('longName', symbol),
            "current_price": current_price,
            "daily_change": daily_change,
            "decision": decision,
            "conviction": conviction,
            "total_score": total_score,
            "scores": {
                "fundamental": min(10, max(1, int(fundamental_score))),
                "momentum": min(10, max(1, int(momentum_score))),
                "valuasi": min(10, max(1, int(valuation_score))),
                "katalis": min(10, max(1, int(catalyst_score)))
            },
            "rsi": rsi,
            "ma20": ma20,
            "ma50": ma50,
            "volume_ratio": volume_ratio,
            "target_price": target_price,
            "pe": pe,
            "pb": pb,
            "sector": info.get('sector', 'N/A')
        }
        
    except Exception as e:
        st.error(f"Error analyzing {symbol}: {str(e)}")
        return None

def create_comparison_chart(analyses: List[Dict]):
    """Create comparison chart for multiple stocks"""
    if not analyses:
        return None
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Skor Analisis', 'Konviction Level', 'RSI vs Target', 'Valuasi (PE/PB)'),
        specs=[[{'type': 'bar'}, {'type': 'bar'}],
               [{'type': 'scatter'}, {'type': 'bar'}]]
    )
    
    symbols = [a['symbol'] for a in analyses]
    
    # Skor analisis
    for score_type in ['fundamental', 'momentum', 'valuasi', 'katalis']:
        scores = [a['scores'][score_type] for a in analyses]
        fig.add_trace(
            go.Bar(name=score_type.capitalize(), x=symbols, y=scores, text=scores, textposition='auto'),
            row=1, col=1
        )
    
    # Conviction
    convictions = [a['conviction'] for a in analyses]
    colors = ['#4ade80' if a['decision'] == 'BELI' else '#f87171' if a['decision'] == 'JUAL' else '#fbbf24' for a in analyses]
    fig.add_trace(
        go.Bar(name='Conviction', x=symbols, y=convictions, text=convictions, textposition='auto',
               marker_color=colors),
        row=1, col=2
    )
    
    # RSI vs Target
    rsi_values = [a['rsi'] for a in analyses]
    target_pct = [((a['target_price']/a['current_price'])-1)*100 for a in analyses]
    
    fig.add_trace(
        go.Scatter(name='RSI', x=symbols, y=rsi_values, mode='lines+markers',
                  line=dict(color='#d4af37', width=2)),
        row=2, col=1
    )
    fig.add_trace(
        go.Scatter(name='Target %', x=symbols, y=target_pct, mode='lines+markers',
                  line=dict(color='#4ade80', width=2)),
        row=2, col=1
    )
    
    # Horizontal lines for RSI levels
    fig.add_hline(y=70, line_dash="dash", line_color="#f87171", opacity=0.5, row=2, col=1)
    fig.add_hline(y=30, line_dash="dash", line_color="#4ade80", opacity=0.5, row=2, col=1)
    
    # PE/PB comparison
    pe_values = [a['pe'] for a in analyses]
    pb_values = [a['pb'] for a in analyses]
    
    fig.add_trace(
        go.Bar(name='PE Ratio', x=symbols, y=pe_values, text=[f"{v:.1f}" for v in pe_values], textposition='auto'),
        row=2, col=2
    )
    fig.add_trace(
        go.Bar(name='PB Ratio', x=symbols, y=pb_values, text=[f"{v:.2f}" for v in pb_values], textposition='auto'),
        row=2, col=2
    )
    
    fig.update_layout(
        height=600,
        showlegend=True,
        paper_bgcolor='#0d0b07',
        plot_bgcolor='#0d0b07',
        font=dict(color='#c8a96e', family='Courier Prime'),
        legend=dict(font=dict(size=10))
    )
    
    fig.update_xaxes(gridcolor='#2a2010', gridwidth=1)
    fig.update_yaxes(gridcolor='#2a2010', gridwidth=1)
    
    return fig

def render_comparison_table(analyses: List[Dict]):
    """Render comparison table for multiple stocks"""
    if not analyses:
        return
    
    html = """
    <table class="comparison-table">
        <tr>
            <th>Saham</th>
            <th>Harga</th>
            <th>Change</th>
            <th>Keputusan</th>
            <th>Conviction</th>
            <th>RSI</th>
            <th>vs MA20</th>
            <th>vs MA50</th>
            <th>Target</th>
        </tr>
    """
    
    for a in analyses:
        decision_color = "#4ade80" if a['decision'] == 'BELI' else "#f87171" if a['decision'] == 'JUAL' else "#fbbf24"
        change_color = "#4ade80" if a['daily_change'] >= 0 else "#f87171"
        change_sign = "+" if a['daily_change'] >= 0 else ""
        
        ma20_status = "↑" if a['current_price'] > a['ma20'] else "↓"
        ma20_color = "#4ade80" if a['current_price'] > a['ma20'] else "#f87171"
        
        ma50_status = "↑" if a['current_price'] > a['ma50'] else "↓"
        ma50_color = "#4ade80" if a['current_price'] > a['ma50'] else "#f87171"
        
        rsi_color = "#4ade80" if a['rsi'] < 30 else "#f87171" if a['rsi'] > 70 else "#fbbf24"
        
        html += f"""
        <tr>
            <td><strong>{a['symbol']}</strong><br><span style="font-size:0.6rem;color:#5c4a2a;">{a['name'][:20]}</span></td>
            <td>Rp{a['current_price']:,.0f}</td>
            <td style="color:{change_color};">{change_sign}{a['daily_change']:.1f}%</td>
            <td style="color:{decision_color};font-weight:700;">{a['decision']}</td>
            <td>{a['conviction']}/10</td>
            <td style="color:{rsi_color};">{a['rsi']:.1f}</td>
            <td style="color:{ma20_color};">{ma20_status} Rp{a['ma20']:,.0f}</td>
            <td style="color:{ma50_color};">{ma50_status} Rp{a['ma50']:,.0f}</td>
            <td>Rp{a['target_price']:,.0f}</td>
        </tr>
        """
    
    html += "</table>"
    st.markdown(html, unsafe_allow_html=True)

def render_alert_ui(alert_manager: AlertManager, symbol: str, current_price: float):
    """Render alert creation UI"""
    with st.expander(f"🔔 Set Alert untuk {symbol}", expanded=False):
        col1, col2, col3 = st.columns([2,2,1])
        
        with col1:
            alert_type = st.selectbox(
                "Tipe Alert",
                ["Harga", "RSI", "Volume"],
                key=f"alert_type_{symbol}"
            )
        
        with col2:
            if alert_type == "Harga":
                condition = st.selectbox("Kondisi", ["Di atas", "Di bawah"], key=f"cond_{symbol}")
                target_price = st.number_input(
                    "Target Harga",
                    min_value=0.0,
                    value=float(current_price * 1.1),
                    step=100.0,
                    key=f"price_{symbol}"
                )
            elif alert_type == "RSI":
                condition = st.selectbox("Kondisi", ["Di atas", "Di bawah"], key=f"cond_{symbol}")
                target_price = st.number_input(
                    "Target RSI",
                    min_value=0.0,
                    max_value=100.0,
                    value=70.0,
                    step=5.0,
                    key=f"rsi_{symbol}"
                )
            else:  # Volume
                condition = "Di atas"
                target_price = st.number_input(
                    "Target Volume (x rata-rata)",
                    min_value=1.0,
                    value=2.0,
                    step=0.5,
                    key=f"vol_{symbol}"
                )
        
        with col3:
            st.write("")  # Spacer
            st.write("")  # Spacer
            if st.button("✅ Set", key=f"set_alert_{symbol}"):
                alert_manager.add_alert(
                    symbol=symbol,
                    alert_type=alert_type,
                    target_price=target_price,
                    condition='above' if condition == "Di atas" else 'below'
                )
                st.success(f"Alert untuk {symbol} telah diset!")
                time.sleep(1)
                st.rerun()
    
    # Show existing alerts for this symbol
    if symbol in alert_manager.alerts:
        st.markdown("**Alert Aktif:**")
        for alert in alert_manager.alerts[symbol]:
            if not alert['triggered']:
                col1, col2 = st.columns([4,1])
                with col1:
                    st.markdown(
                        f"<div class='rr-alert'>"
                        f"<span style='color:#d4af37;'>{alert['type']}</span>: "
                        f"{alert['condition']} {alert['target_price']:,.0f} "
                        f"<span style='color:#5c4a2a;font-size:0.6rem;'>({alert['created_at']})</span>"
                        f"</div>",
                        unsafe_allow_html=True
                    )
                with col2:
                    if st.button("❌", key=f"del_{alert['id']}"):
                        alert_manager.remove_alert(symbol, alert['id'])
                        st.rerun()

def render_alert_dashboard(alert_manager: AlertManager, current_prices: Dict[str, float]):
    """Render alert dashboard in sidebar"""
    st.sidebar.markdown("## 🔔 Dashboard Alert")
    
    # Check for triggered alerts
    triggered = alert_manager.check_alerts(current_prices)
    
    if triggered:
        st.sidebar.markdown("### ⚡ Alert Terpicu!")
        for alert in triggered:
            alert_class = "rr-alert-beli" if alert['condition'] == 'above' else "rr-alert-jual"
            st.sidebar.markdown(
                f"<div class='rr-alert {alert_class}'>"
                f"<strong>{alert['id'].split('_')[0]}</strong><br>"
                f"{alert['type']} {alert['condition']} {alert['target_price']:,.0f}<br>"
                f"Harga sekarang: {alert['triggered_price']:,.0f}<br>"
                f"<span style='font-size:0.6rem;'>{alert['triggered_at']}</span>"
                f"</div>",
                unsafe_allow_html=True
            )
        
        if st.sidebar.button("Bersihkan Alert", key="clear_alerts"):
            for symbol in list(alert_manager.alerts.keys()):
                alert_manager.alerts[symbol] = [a for a in alert_manager.alerts[symbol] if not a['triggered']]
                if not alert_manager.alerts[symbol]:
                    del alert_manager.alerts[symbol]
            alert_manager.save_alerts()
            st.rerun()
    
    # Show active alerts count
    active_count = sum(len([a for a in alerts if not a['triggered']]) 
                      for alerts in alert_manager.alerts.values())
    st.sidebar.markdown(f"**Alert Aktif:** {active_count}")

# ── UI Components ────────────────────────────────────────────────────────────

def render_header():
    st.markdown("""
    <div class="rr-header">
        <div class="rr-eyebrow">◆ SISTEM ANALISIS INVESTASI KELAS CHAEBOL ◆</div>
        <h1 class="rr-title">REBORN RICH</h1>
        <div class="rr-subtitle">"Lihat apa yang belum dilihat orang lain"</div>
    </div>
    """, unsafe_allow_html=True)

# ── Main App ─────────────────────────────────────────────────────────────────

def main():
    render_header()
    
    # Initialize alert manager
    if 'alert_manager' not in st.session_state:
        st.session_state.alert_manager = AlertManager()
    
    # Sidebar for alerts
    with st.sidebar:
        st.markdown("## 📊 Menu Utama")
        app_mode = st.radio(
            "Pilih Mode",
            ["🔍 Single Analysis", "📊 Multi Comparison", "🔔 Alert Manager"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
    
    if app_mode == "🔍 Single Analysis":
        render_single_analysis()
    elif app_mode == "📊 Multi Comparison":
        render_multi_comparison()
    else:
        render_alert_manager_view()

def render_single_analysis():
    """Render single stock analysis view"""
    col1, col2 = st.columns([3, 1])
    
    with col1:
        query = st.text_input(
            "Masukkan Kode Saham",
            placeholder="Contoh: BBCA, TSLA, BTC, BREN",
            key="single_query"
        )
    
    with col2:
        analyze_btn = st.button("🔍 Analisis", use_container_width=True)
    
    if analyze_btn and query:
        symbol = extract_symbol(query)
        
        with st.spinner(f"Menganalisis {symbol}..."):
            analysis = analyze_stock(symbol)
            
            if analysis:
                # Get current price for alerts
                current_prices = {symbol: analysis['current_price']}
                
                # Check alerts
                render_alert_dashboard(st.session_state.alert_manager, current_prices)
                
                # Render analysis
                col_left, col_right = st.columns([2, 1])
                
                with col_left:
                    # Decision card
                    decision_color = "#4ade80" if analysis['decision'] == 'BELI' else "#f87171" if analysis['decision'] == 'JUAL' else "#fbbf24"
                    st.markdown(f"""
                    <div class="rr-card" style="border-color:{decision_color}44;">
                        <div class="rr-card-label">KEPUTUSAN FINAL</div>
                        <div style="display:flex; align-items:center; gap:2rem;">
                            <div style="font-size:3rem; color:{decision_color};">{analysis['decision']}</div>
                            <div>
                                <div style="color:#d4af37;">{analysis['name']}</div>
                                <div style="font-size:1.5rem;">Rp{analysis['current_price']:,.0f}</div>
                                <div style="color:{'#4ade80' if analysis['daily_change']>=0 else '#f87171'};">
                                    {analysis['daily_change']:+.2f}%
                                </div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_right:
                    render_alert_ui(st.session_state.alert_manager, symbol, analysis['current_price'])
                
                # Metrics
                mcol1, mcol2, mcol3, mcol4 = st.columns(4)
                with mcol1:
                    st.metric("Conviction", f"{analysis['conviction']}/10")
                with mcol2:
                    st.metric("RSI", f"{analysis['rsi']:.1f}")
                with mcol3:
                    st.metric("Volume Ratio", f"{analysis['volume_ratio']:.2f}x")
                with mcol4:
                    st.metric("Target", f"Rp{analysis['target_price']:,.0f}")
                
                # Scores
                st.markdown("### 📊 Skor Analisis")
                for score_name, score_value in analysis['scores'].items():
                    score_pct = score_value * 10
                    score_color = "#4ade80" if score_value >= 7 else "#fbbf24" if score_value >= 5 else "#f87171"
                    st.markdown(f"""
                    <div class="score-container">
                        <div class="score-label-row">
                            <span class="score-label">{score_name.upper()}</span>
                            <span class="score-value" style="color:{score_color};">{score_value}/10</span>
                        </div>
                        <div class="score-track">
                            <div class="score-fill" style="width:{score_pct}%;background:{score_color};"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
            else:
                st.error(f"Tidak dapat menemukan data untuk {symbol}")
    
    else:
        # Show quick picks
        st.markdown("### 🔥 Pilihan Cepat")
        quick_picks = ["BBCA", "BBRI", "TSLA", "BTC", "BREN", "AAPL"]
        cols = st.columns(len(quick_picks))
        for i, pick in enumerate(quick_picks):
            with cols[i]:
                if st.button(pick, use_container_width=True):
                    st.session_state.single_query = pick
                    st.rerun()

def render_multi_comparison():
    """Render multi-stock comparison view"""
    st.markdown("## 📊 Perbandingan Multi-Saham")
    
    # Initialize comparison list
    if 'compare_symbols' not in st.session_state:
        st.session_state.compare_symbols = ['BBCA.JK', 'BBRI.JK', 'BMRI.JK']
    
    # Symbol input
    col1, col2 = st.columns([3, 1])
    with col1:
        new_symbol = st.text_input("Tambah Saham", placeholder="Contoh: TSLA, BBCA, BTC")
    with col2:
        if st.button("➕ Tambah", use_container_width=True) and new_symbol:
            symbol = extract_symbol(new_symbol)
            if symbol not in st.session_state.compare_symbols:
                st.session_state.compare_symbols.append(symbol)
                st.rerun()
    
    # Display current symbols
    st.markdown("**Saham yang dibandingkan:**")
    cols = st.columns(len(st.session_state.compare_symbols))
    for i, symbol in enumerate(st.session_state.compare_symbols):
        with cols[i]:
            st.markdown(f"• {symbol}")
            if st.button("❌", key=f"remove_{symbol}"):
                st.session_state.compare_symbols.remove(symbol)
                st.rerun()
    
    if st.button("🔄 Bandingkan Sekarang", use_container_width=True):
        with st.spinner("Menganalisis semua saham..."):
            analyses = []
            current_prices = {}
            
            for symbol in st.session_state.compare_symbols:
                analysis = analyze_stock(symbol)
                if analysis:
                    analyses.append(analysis)
                    current_prices[symbol] = analysis['current_price']
            
            if analyses:
                # Check alerts
                render_alert_dashboard(st.session_state.alert_manager, current_prices)
                
                # Comparison table
                st.markdown("### 📋 Tabel Perbandingan")
                render_comparison_table(analyses)
                
                # Comparison chart
                st.markdown("### 📈 Visualisasi Perbandingan")
                fig = create_comparison_chart(analyses)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                
                # Recommendation matrix
                st.markdown("### 🎯 Rekomendasi")
                cols = st.columns(len(analyses))
                for i, analysis in enumerate(analyses):
                    with cols[i]:
                        decision_color = "#4ade80" if analysis['decision'] == 'BELI' else "#f87171" if analysis['decision'] == 'JUAL' else "#fbbf24"
                        st.markdown(f"""
                        <div class="rr-card" style="text-align:center; border-color:{decision_color}44;">
                            <div style="font-size:1.2rem; color:{decision_color};">{analysis['symbol']}</div>
                            <div style="font-size:1.5rem; margin:0.5rem 0;">{analysis['decision']}</div>
                            <div>Conviction: {analysis['conviction']}/10</div>
                            <div style="font-size:0.8rem; color:#5c4a2a;">{analysis['name'][:30]}</div>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.error("Tidak dapat menganalisis saham-saham tersebut")

def render_alert_manager_view():
    """Render alert manager view"""
    st.markdown("## 🔔 Alert Manager")
    
    alert_manager = st.session_state.alert_manager
    
    # Show all active alerts
    st.markdown("### 📋 Semua Alert Aktif")
    
    has_alerts = False
    for symbol, alerts in alert_manager.alerts.items():
        active_alerts = [a for a in alerts if not a['triggered']]
        if active_alerts:
            has_alerts = True
            with st.expander(f"📊 {symbol} ({len(active_alerts)} alert)", expanded=True):
                for alert in active_alerts:
                    col1, col2, col3 = st.columns([2,2,1])
                    with col1:
                        st.markdown(f"**{alert['type']}**")
                    with col2:
                        st.markdown(f"{alert['condition']} {alert['target_price']:,.0f}")
                    with col3:
                        if st.button("Hapus", key=f"del_alert_{alert['id']}"):
                            alert_manager.remove_alert(symbol, alert['id'])
                            st.rerun()
    
    if not has_alerts:
        st.info("Belum ada alert aktif. Buat alert baru di halaman Single Analysis.")
    
    # Show alert history
    st.markdown("---")
    st.markdown("### 📜 Riwayat Alert Terpicu")
    
    triggered_alerts = []
    for symbol, alerts in alert_manager.alerts.items():
        triggered_alerts.extend([a for a in alerts if a.get('triggered', False)])
    
    if triggered_alerts:
        for alert in triggered_alerts[-10:]:  # Last 10
            st.markdown(f"""
            <div class="rr-alert">
                <strong>{alert['id'].split('_')[0]}</strong> - {alert['type']}<br>
                Target: {alert['target_price']:,.0f} | Terpicu: {alert.get('triggered_price', 0):,.0f}<br>
                <span style="font-size:0.6rem;">{alert.get('triggered_at', '')}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Belum ada alert yang terpicu.")

if __name__ == "__main__":
    main()
