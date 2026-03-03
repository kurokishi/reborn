import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import re
import time
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Reborn Rich | Analisis Saham AI",
    page_icon="💰",
    layout="centered",
    initial_sidebar_state="collapsed",
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
.block-container { max-width: 860px !important; padding-top: 2rem !important; }

/* ─ Typography ─ */
h1, h2, h3 { font-family: 'Playfair Display', Georgia, serif !important; }
p, div, span, label { font-family: 'Courier Prime', monospace !important; }

/* ─ Header ─ */
.rr-header {
    text-align: center;
    padding: 2rem 0 1rem;
    border-bottom: 1px solid #2a2010;
    margin-bottom: 2rem;
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
    font-size: clamp(2rem, 6vw, 3.5rem);
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

/* ─ Input ─ */
.stTextArea textarea {
    background-color: #0d0b07 !important;
    color: #e8d5a0 !important;
    border: 1px solid #2a2010 !important;
    border-radius: 4px !important;
    font-family: 'Playfair Display', serif !important;
    font-size: 1rem !important;
    caret-color: #d4af37 !important;
}
.stTextArea textarea:focus {
    border-color: #d4af3766 !important;
    box-shadow: 0 0 12px #d4af3720 !important;
}

/* ─ Button ─ */
.stButton > button {
    background: linear-gradient(135deg, #d4af37, #a07d20) !important;
    color: #0a0705 !important;
    border: none !important;
    border-radius: 2px !important;
    font-family: 'Courier Prime', monospace !important;
    font-weight: 700 !important;
    letter-spacing: 0.2em !important;
    font-size: 0.8rem !important;
    padding: 0.6rem 2rem !important;
    text-transform: uppercase !important;
    box-shadow: 0 0 20px #d4af3733 !important;
    transition: all 0.3s !important;
    width: 100% !important;
}
.stButton > button:hover {
    box-shadow: 0 0 30px #d4af3766 !important;
    transform: translateY(-1px) !important;
}

/* ─ Cards ─ */
.rr-card {
    background: #0d0b07;
    border: 1px solid #1e1810;
    border-radius: 4px;
    padding: 1.25rem 1.5rem;
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
    font-size: 0.95rem;
    line-height: 1.75;
}

/* ─ Decision Banner ─ */
.rr-decision-beli {
    border-color: #4ade8044 !important;
    box-shadow: 0 0 40px #4ade8022 !important;
    background: radial-gradient(ellipse at 50% 0%, #4ade8010, #0d0b07 70%) !important;
}
.rr-decision-jual {
    border-color: #f8717144 !important;
    box-shadow: 0 0 40px #f8717122 !important;
    background: radial-gradient(ellipse at 50% 0%, #f8717110, #0d0b07 70%) !important;
}
.rr-decision-tahan {
    border-color: #fbbf2444 !important;
    box-shadow: 0 0 40px #fbbf2422 !important;
    background: radial-gradient(ellipse at 50% 0%, #fbbf2410, #0d0b07 70%) !important;
}
.decision-word-beli  { color: #4ade80; }
.decision-word-jual  { color: #f87171; }
.decision-word-tahan { color: #fbbf24; }

/* ─ Score bar ─ */
.score-container { margin-bottom: 0.75rem; }
.score-label-row {
    display: flex;
    justify-content: space-between;
    margin-bottom: 4px;
}
.score-label {
    font-family: 'Courier Prime', monospace !important;
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    color: #8b7355;
    text-transform: uppercase;
}
.score-value { font-weight: 700; font-family: 'Courier Prime', monospace !important; }
.score-track {
    height: 4px;
    background: #1a1410;
    border-radius: 2px;
    overflow: hidden;
}
.score-fill {
    height: 100%;
    border-radius: 2px;
}

/* ─ Quote ─ */
.rr-quote {
    border-left: 2px solid #d4af37;
    padding: 1.2rem 1.2rem 1.2rem 1.5rem;
    background: #0d0b0788;
    border-radius: 0 4px 4px 0;
    margin: 1rem 0;
}
.rr-quote-text {
    color: #d4af37;
    font-family: 'Playfair Display', serif !important;
    font-style: italic;
    font-size: 1rem;
    line-height: 1.8;
}

/* ─ Conviction bar ─ */
.conviction-bar {
    font-family: 'Courier Prime', monospace !important;
    color: #8b7355;
    letter-spacing: 0.15em;
    font-size: 0.8rem;
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

/* ─ Divider ─ */
hr { border-color: #2a2010 !important; }

/* ─ Hide Streamlit branding ─ */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ─ Selectbox & API input ─ */
.stTextInput input {
    background-color: #0d0b07 !important;
    color: #c8a96e !important;
    border: 1px solid #2a2010 !important;
    border-radius: 4px !important;
    font-family: 'Courier Prime', monospace !important;
}
.stTextInput input:focus {
    border-color: #d4af3766 !important;
}
[data-testid="stExpander"] {
    background: #0d0b07 !important;
    border: 1px solid #1e1810 !important;
    border-radius: 4px !important;
}
</style>
""", unsafe_allow_html=True)

# ── Helper Functions ──────────────────────────────────────────────────────────

def extract_symbol(query: str) -> str:
    """Extract stock symbol from user query."""
    # Common Indonesian stocks mapping
    id_stocks = {
        'BBCA': 'BBCA.JK', 'BBRI': 'BBRI.JK', 'BMRI': 'BMRI.JK', 
        'TLKM': 'TLKM.JK', 'ASII': 'ASII.JK', 'BREN': 'BREN.JK',
        'GOTO': 'GOTO.JK', 'BYAN': 'BYAN.JK', 'ADRO': 'ADRO.JK'
    }
    
    # Check for exact matches in Indonesian stocks
    query_upper = query.upper().strip()
    if query_upper in id_stocks:
        return id_stocks[query_upper]
    
    # Check for common US stocks
    us_stocks = {
        'TSLA': 'TSLA', 'AAPL': 'AAPL', 'MSFT': 'MSFT',
        'GOOGL': 'GOOGL', 'AMZN': 'AMZN', 'META': 'META',
        'BTC': 'BTC-USD', 'ETH': 'ETH-USD', 'GOLD': 'GC=F'
    }
    
    if query_upper in us_stocks:
        return us_stocks[query_upper]
    
    # Default: assume it's already a valid symbol or try with .JK for Indonesian stocks
    return query_upper if '.' in query_upper else f"{query_upper}.JK"

def calculate_rsi(prices: pd.Series, periods: int = 14) -> float:
    """Calculate RSI indicator."""
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=periods).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=periods).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1] if not pd.isna(rsi.iloc[-1]) else 50

def calculate_macd(prices: pd.Series) -> Dict[str, float]:
    """Calculate MACD indicator."""
    exp1 = prices.ewm(span=12, adjust=False).mean()
    exp2 = prices.ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2
    signal = macd.ewm(span=9, adjust=False).mean()
    return {
        'macd': macd.iloc[-1],
        'signal': signal.iloc[-1],
        'histogram': macd.iloc[-1] - signal.iloc[-1]
    }

def analyze_with_yfinance(symbol: str) -> Optional[Dict[str, Any]]:
    """Analyze stock using yfinance data."""
    try:
        # Download stock data
        stock = yf.Ticker(symbol)
        
        # Get info and historical data
        info = stock.info
        hist = stock.history(period="6mo")
        
        if hist.empty:
            return None
        
        # Calculate technical indicators
        current_price = hist['Close'].iloc[-1]
        prev_price = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
        
        # Price changes
        daily_change = ((current_price - prev_price) / prev_price) * 100
        weekly_change = ((current_price - hist['Close'].iloc[-5]) / hist['Close'].iloc[-5]) * 100 if len(hist) >= 5 else 0
        monthly_change = ((current_price - hist['Close'].iloc[-20]) / hist['Close'].iloc[-20]) * 100 if len(hist) >= 20 else 0
        
        # Moving averages
        ma20 = hist['Close'].rolling(window=20).mean().iloc[-1] if len(hist) >= 20 else current_price
        ma50 = hist['Close'].rolling(window=50).mean().iloc[-1] if len(hist) >= 50 else current_price
        
        # RSI
        rsi = calculate_rsi(hist['Close'])
        
        # MACD
        macd_data = calculate_macd(hist['Close'])
        
        # Volume analysis
        avg_volume = hist['Volume'].rolling(window=20).mean().iloc[-1] if len(hist) >= 20 else hist['Volume'].mean()
        current_volume = hist['Volume'].iloc[-1]
        volume_ratio = current_volume / avg_volume if avg_volume > 0 else 1
        
        # Scoring system (1-10 scale)
        # Fundamental score based on PE, PB, etc
        pe = info.get('trailingPE', 15)
        pb = info.get('priceToBook', 1.5)
        
        if pe < 15:
            fundamental_score = 8
        elif pe < 25:
            fundamental_score = 6
        elif pe < 35:
            fundamental_score = 4
        else:
            fundamental_score = 3
            
        # Momentum score based on price action and RSI
        if rsi < 30:  # Oversold
            momentum_score = 8
        elif rsi > 70:  # Overbought
            momentum_score = 4
        else:
            momentum_score = 6
            
        # Adjust for trend
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
            
        # Catalyst score based on volume and news (simplified)
        catalyst_score = 5
        if volume_ratio > 1.5:
            catalyst_score += 2
        elif volume_ratio > 1.2:
            catalyst_score += 1
            
        # Determine decision
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
            
        # Target price calculation
        target_price = current_price * (1 + (total_score - 5) * 0.05) if total_score > 5 else current_price * 0.95
        
        # Generate analysis text
        company_name = info.get('longName', symbol)
        sector = info.get('sector', 'N/A')
        
        kondisi_makro = f"Sektor {sector} saat ini menghadapi dinamika pasar yang kompleks. "
        if rsi > 70:
            kondisi_makro += "Tekanan jual mulai terlihat karena kondisi jenuh beli (overbought) di level RSI {:.1f}. ".format(rsi)
        elif rsi < 30:
            kondisi_makro += "Peluang akumulasi muncul karena kondisi jenuh jual (oversold) di level RSI {:.1f}. ".format(rsi)
        else:
            kondisi_makro += "Pasar berada dalam fase konsolidasi dengan momentum yang netral (RSI {:.1f}). ".format(rsi)
            
        kondisi_makro += f"Volume perdagangan {'meningkat' if volume_ratio > 1.2 else 'menurun'} {volume_ratio:.1f}x dari rata-rata."
        
        peluang_tersembunyi = f"Valuasi PB {pb:.2f}x tergolong {'murah' if pb < 1.5 else 'wajar' if pb < 3 else 'premium'}. "
        if pe < 20:
            peluang_tersembunyi += f"PER {pe:.1f}x masih menarik dibandingkan rata-rata historis. "
        if volume_ratio > 1.3:
            peluang_tersembunyi += "Ada peningkatan volume signifikan yang mengindikasikan minat institusional. "
            
        risiko_utama = f"Resistance teknikal di level Rp{ma50:.0f} (MA50) perlu ditembus untuk kelanjutan tren. "
        if rsi > 70:
            risiko_utama += "Koreksi jangka pendek sangat mungkin terjadi karena kondisi overbought. "
        elif rsi < 30:
            risiko_utama += "Pelemahan masih berpotensi berlanjut meski sudah oversold. "
            
        strategi_masuk = f"Entry ideal di kisaran Rp{current_price*0.97:.0f}-Rp{current_price:.0f} "
        if decision == "BELI":
            strategi_masuk += "dengan akumulasi bertahap (DCA). "
        elif decision == "JUAL":
            strategi_masuk += "untuk cut loss, exit di level Rp{current_price*0.95:.0f} jika breakdown. "
        else:
            strategi_masuk += "sambil wait and see hingga konfirmasi breakout/breakdown. "
            
        target_harga = f"Target harga 6-12 bulan: Rp{target_price:.0f}"
        if decision == "BELI":
            target_harga += f" (potensi upside {((target_price/current_price)-1)*100:.1f}%)"
            
        # Filosofi quotes
        filosofi_quotes = {
            "BELI": "Ketika ketakutan menguasai pasar, di sanalah harta karun tersembunyi. Jangan ikut arus, belilah saat darah mengalir di jalanan.",
            "JUAL": "Keserakahan adalah lawan terburuk investor. Ketika semua orang terbuai mimpi, saatnya mengambil keuntungan dan pergi.",
            "TAHAN": "Orang bijak tahu kapan harus diam. Dalam ketidakpastian, bertahan adalah strategi terbaik."
        }
        
        return {
            "keputusan": decision,
            "conviction": conviction,
            "ringkasan": f"{company_name} menunjukkan prospek {'positif' if decision == 'BELI' else 'negatif' if decision == 'JUAL' else 'netral'} dengan conviction {conviction}/10.",
            "kondisi_makro": kondisi_makro,
            "peluang_tersembunyi": peluang_tersembunyi,
            "risiko_utama": risiko_utama,
            "strategi_masuk": strategi_masuk,
            "target_harga": target_harga,
            "filosofi": filosofi_quotes.get(decision, filosofi_quotes["TAHAN"]),
            "skor": {
                "fundamental": min(10, max(1, int(fundamental_score))),
                "momentum": min(10, max(1, int(momentum_score))),
                "valuasi": min(10, max(1, int(valuation_score))),
                "katalis": min(10, max(1, int(catalyst_score)))
            },
            "company_name": company_name,
            "current_price": current_price,
            "daily_change": daily_change
        }
        
    except Exception as e:
        st.error(f"Error analyzing {symbol}: {str(e)}")
        return None

def score_color(val: int) -> str:
    if val >= 7: return "#d4af37"
    if val >= 5: return "#c8a96e"
    return "#8b7355"


def render_score_bar(label: str, value: int):
    color = score_color(value)
    pct = value * 10
    st.markdown(f"""
    <div class="score-container">
        <div class="score-label-row">
            <span class="score-label">{label}</span>
            <span class="score-value" style="color:{color};">{value}/10</span>
        </div>
        <div class="score-track">
            <div class="score-fill" style="width:{pct}%;background:linear-gradient(90deg,{color}88,{color});box-shadow:0 0 8px {color}66;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── UI ────────────────────────────────────────────────────────────────────────

def render_header():
    st.markdown("""
    <div class="rr-header">
        <div class="rr-eyebrow">◆ SISTEM ANALISIS INVESTASI KELAS CHAEBOL ◆</div>
        <h1 class="rr-title">REBORN RICH</h1>
        <div class="rr-subtitle">"Lihat apa yang belum dilihat orang lain"</div>
    </div>
    """, unsafe_allow_html=True)


def render_result(result: dict):
    keputusan = result.get("keputusan", "TAHAN").upper()
    conviction = result.get("conviction", 5)
    css_class = f"rr-decision-{keputusan.lower()}"
    word_class = f"decision-word-{keputusan.lower()}"

    filled = "▮" * conviction
    empty  = "▯" * (10 - conviction)

    # Show current price info
    current_price = result.get('current_price', 0)
    daily_change = result.get('daily_change', 0)
    change_color = "#4ade80" if daily_change >= 0 else "#f87171"
    change_sign = "+" if daily_change >= 0 else ""

    # ── Decision Banner ─────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="rr-card {css_class}" style="text-align:center;padding:2rem 1.5rem;">
        <div class="rr-card-label">KEPUTUSAN FINAL</div>
        <div style="font-family:'Courier Prime',monospace; color:#8b7355; font-size:0.9rem; margin-bottom:0.5rem;">
            {result.get('company_name', '')} | Rp{current_price:,.0f} 
            <span style="color:{change_color};">({change_sign}{daily_change:.2f}%)</span>
        </div>
        <div class="{word_class}" style="font-family:'Playfair Display',serif;font-size:clamp(2.5rem,8vw,4rem);font-weight:700;letter-spacing:0.1em;">
            {keputusan}
        </div>
        <div class="conviction-bar" style="margin:0.5rem 0 1rem;">
            CONVICTION {conviction}/10 — {filled}{empty}
        </div>
        <div class="rr-card-body" style="font-style:italic;max-width:580px;margin:0 auto;">
            {result.get("ringkasan", "")}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── 2-column cards ───────────────────────────────────────────────────────
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="rr-card">
            <div class="rr-card-label" style="color:#6ba3d6;">🌐 KONDISI MAKRO</div>
            <div class="rr-card-body">{result.get("kondisi_makro","")}</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        <div class="rr-card">
            <div class="rr-card-label" style="color:#f87171;">⚠ RISIKO UTAMA</div>
            <div class="rr-card-body">{result.get("risiko_utama","")}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="rr-card">
            <div class="rr-card-label" style="color:#d4af37;">👁 PELUANG TERSEMBUNYI</div>
            <div class="rr-card-body">{result.get("peluang_tersembunyi","")}</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        <div class="rr-card">
            <div class="rr-card-label" style="color:#4ade80;">📈 TARGET HARGA</div>
            <div class="rr-card-body">{result.get("target_harga","")}</div>
        </div>
        """, unsafe_allow_html=True)

    # ── Strategi Masuk ───────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="rr-card">
        <div class="rr-card-label">🎯 STRATEGI MASUK</div>
        <div class="rr-card-body">{result.get("strategi_masuk","")}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Score Matrix ─────────────────────────────────────────────────────────
    st.markdown("""
    <div class="rr-card">
        <div class="rr-card-label">📊 MATRIX PENILAIAN</div>
    """, unsafe_allow_html=True)
    skor = result.get("skor", {})
    render_score_bar("Fundamental", skor.get("fundamental", 5))
    render_score_bar("Momentum Pasar", skor.get("momentum", 5))
    render_score_bar("Valuasi", skor.get("valuasi", 5))
    render_score_bar("Kekuatan Katalis", skor.get("katalis", 5))
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Filosofi Quote ───────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="rr-quote">
        <div class="rr-card-label">💬 FILOSOFI INVESTASI</div>
        <div class="rr-quote-text">"{result.get("filosofi","")}"</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Disclaimer ───────────────────────────────────────────────────────────
    st.markdown("""
    <div class="rr-disclaimer">
        ⚠ Analisis ini bersifat edukatif dan tidak merupakan saran investasi resmi.<br>
        Selalu lakukan riset mandiri dan konsultasikan dengan advisor keuangan profesional.
    </div>
    """, unsafe_allow_html=True)


def render_empty_state():
    st.markdown("""
    <div style="text-align:center;padding:3rem 1rem;color:#3d2e15;
                font-style:italic;line-height:2.2;font-family:'Playfair Display',serif;font-size:1rem;">
        "Yang membedakan investor biasa dengan yang luar biasa<br>
        bukan seberapa banyak yang mereka tahu —<br>
        tapi seberapa cepat mereka melihat apa yang belum terlihat."
    </div>
    """, unsafe_allow_html=True)


# ── Main App ──────────────────────────────────────────────────────────────────

def main():
    render_header()
    
    # Add info that we're using yfinance
    st.markdown("""
    <div style="text-align:center; margin-bottom:1rem;">
        <span style="background:#1a1410; color:#d4af37; padding:0.2rem 1rem; border-radius:20px; font-size:0.7rem;">
            📊 Real-time data dari Yahoo Finance
        </span>
    </div>
    """, unsafe_allow_html=True)

    # Input area
    st.markdown('<div class="rr-card-label" style="padding:0 0 0.4rem;">TARGET ANALISIS</div>', unsafe_allow_html=True)
    query = st.text_area(
        label="target",
        label_visibility="collapsed",
        placeholder="Contoh: BBCA, Tesla TSLA, Bitcoin BTC, Emas, BREN...",
        height=90,
        key="query_input"
    )

    # Example buttons
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("🇮🇩 BBCA", use_container_width=True):
            st.session_state.query_input = "BBCA"
    with col2:
        if st.button("🇺🇸 TSLA", use_container_width=True):
            st.session_state.query_input = "TSLA"
    with col3:
        if st.button("₿ BTC", use_container_width=True):
            st.session_state.query_input = "BTC"
    with col4:
        if st.button("🏦 BREN", use_container_width=True):
            st.session_state.query_input = "BREN"

    analyze_btn = st.button("▶  ANALISIS SEKARANG", use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    if analyze_btn:
        if not query.strip():
            st.warning("Masukkan nama saham atau instrumen investasi terlebih dahulu.")
            return

        # Extract symbol and analyze
        with st.spinner("🔍 Mengambil data pasar real-time..."):
            symbol = extract_symbol(query.strip())
            
            phases = [
                f"🔍 Memindai data {symbol}...",
                "📡 Membaca pola teknikal...",
                "🧮 Menghitung indikator dan probabilitas...",
                "⚡ Menyusun keputusan final..."
            ]
            status_placeholder = st.empty()
            for i, phase_text in enumerate(phases):
                status_placeholder.info(phase_text)
                if i < len(phases) - 1:
                    time.sleep(0.1)

            try:
                result = analyze_with_yfinance(symbol)
                status_placeholder.empty()
                
                if result:
                    render_result(result)

                    # Simpan ke history session
                    if "history" not in st.session_state:
                        st.session_state["history"] = []
                    st.session_state["history"].insert(0, {
                        "query": query.strip(),
                        "symbol": symbol,
                        "keputusan": result.get("keputusan"),
                        "conviction": result.get("conviction"),
                        "ringkasan": result.get("ringkasan", "")[:100] + "..."
                    })
                else:
                    st.error(f"⚠ Tidak dapat menemukan data untuk '{query}'. Coba gunakan kode saham yang valid (contoh: BBCA.JK untuk Indonesia, TSLA untuk US).")

            except Exception as e:
                status_placeholder.empty()
                st.error(f"⚠ Error: {str(e)}")
    else:
        # History sidebar
        if st.session_state.get("history"):
            with st.sidebar:
                st.markdown('<div class="rr-card-label" style="color:#5c4a2a;">RIWAYAT ANALISIS</div>', unsafe_allow_html=True)
                for item in st.session_state["history"][:10]:
                    keputusan = item["keputusan"]
                    color = "#4ade80" if keputusan == "BELI" else "#f87171" if keputusan == "JUAL" else "#fbbf24"
                    st.markdown(f"""
                    <div class="rr-card" style="margin-bottom:0.5rem;padding:0.75rem 1rem;">
                        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;">
                            <strong style="color:#c8a96e;font-size:0.85rem;">{item['query']}</strong>
                            <span style="color:{color};font-weight:700;font-size:0.75rem;">{keputusan}</span>
                        </div>
                        <div style="color:#5c4a2a;font-size:0.65rem;">Conviction: {item['conviction']}/10</div>
                        <div style="color:#3d2e15;font-size:0.6rem;">{item.get('symbol', '')}</div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            render_empty_state()


if __name__ == "__main__":
    main()
