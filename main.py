import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
import base64
from io import BytesIO
import time
import random

# Page configuration
st.set_page_config(
    page_title="Reborn Rich Stock Analyzer",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Source+Code+Pro&display=swap');
    
    .stApp {
        background-color: #0a0705;
    }
    
    .main-title {
        font-family: 'Playfair Display', serif;
        font-size: 48px;
        color: #d4af37;
        text-align: center;
        text-shadow: 0 0 20px #d4af3799;
        letter-spacing: 0.05em;
        margin-bottom: 10px;
    }
    
    .subtitle {
        font-family: 'Playfair Display', serif;
        font-size: 14px;
        color: #5c4a2a;
        text-align: center;
        font-style: italic;
        letter-spacing: 0.2em;
        margin-bottom: 40px;
    }
    
    .section-header {
        font-family: 'Source Code Pro', monospace;
        font-size: 10px;
        color: #8b7355;
        letter-spacing: 0.3em;
        text-transform: uppercase;
        margin-bottom: 10px;
    }
    
    .decision-box {
        background: linear-gradient(135deg, #0d0b07, #110e08);
        border: 1px solid;
        border-radius: 4px;
        padding: 36px 28px;
        text-align: center;
        position: relative;
        overflow: hidden;
        margin-bottom: 20px;
    }
    
    .decision-badge {
        font-family: 'Playfair Display', serif;
        font-size: 64px;
        font-weight: 700;
        margin-bottom: 12px;
        animation: pulse 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.8; transform: scale(1.05); }
    }
    
    .info-card {
        background: #0d0b07;
        border: 1px solid #1e1810;
        border-radius: 4px;
        padding: 20px;
        transition: all 0.3s;
    }
    
    .info-card:hover {
        border-color: #d4af3766;
        box-shadow: 0 0 20px #d4af3720;
    }
    
    .quote-box {
        border-left: 2px solid #d4af37;
        padding: 20px 20px 20px 24px;
        background: #0d0b0788;
        border-radius: 0 4px 4px 0;
        margin: 20px 0;
    }
    
    .stTextInput > div > div > input {
        background-color: #0d0b07;
        color: #e8d5a0;
        border: 1px solid #2a2010;
        font-family: 'Playfair Display', serif;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #d4af37, #a07d20);
        color: #0a0705;
        border: none;
        border-radius: 2px;
        padding: 12px 28px;
        font-family: 'Playfair Display', serif;
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        box-shadow: 0 0 20px #d4af3733;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = []
if 'watchlist' not in st.session_state:
    st.session_state.watchlist = []
if 'comparison' not in st.session_state:
    st.session_state.comparison = []
if 'current_analysis' not in st.session_state:
    st.session_state.current_analysis = None

# Helper functions
def generate_analysis(symbol, include_web_search=False):
    """Generate simulated analysis based on stock symbol"""
    time.sleep(2)  # Simulate processing
    
    # Base decisions with some randomness
    decisions = ["BELI", "TAHAN", "JUAL"]
    weights = [0.4, 0.3, 0.3]  # 40% chance of BUY
    
    # Adjust based on symbol (just for demo variety)
    if symbol.upper() in ['BBCA', 'BBRI', 'TLKM', 'ASII']:
        weights = [0.6, 0.3, 0.1]  # Blue chips more likely BUY
    elif symbol.upper() in ['GOTO', 'BREN']:
        weights = [0.2, 0.4, 0.4]  # Tech more volatile
    
    keputusan = np.random.choice(decisions, p=weights)
    conviction = np.random.randint(7, 11) if keputusan == "BELI" else np.random.randint(5, 9)
    
    # Generate scores
    fundamental = np.random.randint(6, 10) if keputusan == "BELI" else np.random.randint(3, 7)
    momentum = np.random.randint(5, 9)
    valuasi = np.random.randint(4, 9)
    katalis = np.random.randint(6, 9) if keputusan == "BELI" else np.random.randint(3, 6)
    
    # Current price simulation
    current_price = np.random.uniform(1000, 50000)
    target_price = current_price * np.random.uniform(1.05, 1.25) if keputusan == "BELI" else current_price * np.random.uniform(0.85, 1.0)
    
    analysis = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "symbol": symbol.upper(),
        "keputusan": keputusan,
        "conviction": conviction,
        "ringkasan": f"Analisis komprehensif untuk {symbol.upper()} menunjukkan potensi " +
                    ("signifikan" if keputusan == "BELI" else "terbatas" if keputusan == "TAHAN" else "penurunan"),
        "kondisi_makro": "Suku bunga diprediksi stabil, inflasi terkendali. Ekonomi global menunjukkan tanda pemulihan.",
        "peluang_tersembunyi": "Valuasi masih di bawah rata-rata historis. Ada potensi katalis dari ekspansi bisnis.",
        "risiko_utama": "Persaingan ketat dan ketidakpastian regulasi menjadi faktor utama yang perlu diwaspadai.",
        "strategi_masuk": f"Accumulate secara bertahap di level {current_price:,.0f}-{current_price*0.95:,.0f}. " +
                         "Gunakan average down strategy.",
        "target_harga": f"Rp {target_price:,.0f} - {target_price*1.1:,.0f} (6-12 bulan)",
        "filosofi": "Kesabaran dan disiplin adalah kunci. Pasar memberi hadiah kepada mereka yang berani berbeda.",
        "skor": {
            "fundamental": fundamental,
            "momentum": momentum,
            "valuasi": valuasi,
            "katalis": katalis
        },
        "harga_saat_ini": current_price,
        "rekomendasi_tambahan": "Pertimbangkan untuk diversifikasi portofolio."
    }
    
    return analysis

def create_radar_chart(scores):
    """Create radar chart for scores"""
    categories = ['Fundamental', 'Momentum', 'Valuasi', 'Katalis']
    values = [scores['fundamental'], scores['momentum'], scores['valuasi'], scores['katalis']]
    values += values[:1]  # Close the loop
    
    fig = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=categories + [categories[0]],
        fill='toself',
        fillcolor='rgba(212, 175, 55, 0.2)',
        line=dict(color='#d4af37', width=2)
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10],
                gridcolor='#2a2010',
                gridwidth=1
            ),
            bgcolor='#0d0b07',
            angularaxis=dict(
                gridcolor='#2a2010',
                gridwidth=1,
                tickfont=dict(color='#8b7355')
            )
        ),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=300,
        margin=dict(l=80, r=80, t=20, b=20)
    )
    
    return fig

def create_comparison_chart(analyses):
    """Create comparison bar chart"""
    symbols = [a['symbol'] for a in analyses]
    metrics = ['fundamental', 'momentum', 'valuasi', 'katalis']
    metric_names = ['Fundamental', 'Momentum', 'Valuasi', 'Katalis']
    
    fig = go.Figure()
    
    for i, metric in enumerate(metrics):
        values = [a['skor'][metric] for a in analyses]
        fig.add_trace(go.Bar(
            name=metric_names[i],
            x=symbols,
            y=values,
            marker_color=['#d4af37', '#6ba3d6', '#4ade80', '#f87171'][i],
            opacity=0.8
        ))
    
    fig.update_layout(
        barmode='group',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#8b7355'),
        xaxis=dict(gridcolor='#2a2010'),
        yaxis=dict(gridcolor='#2a2010', range=[0, 10]),
        height=400,
        margin=dict(l=40, r=40, t=40, b=40)
    )
    
    return fig

def export_to_pdf(analysis):
    """Export analysis to PDF"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        textColor=colors.HexColor('#d4af37'),
        fontSize=24,
        spaceAfter=30,
        alignment=1  # Center alignment
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        textColor=colors.HexColor('#d4af37'),
        fontSize=14,
        spaceAfter=12
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        textColor=colors.HexColor('#c8a96e'),
        fontSize=10,
        spaceAfter=6
    )
    
    # Title
    story.append(Paragraph(f"Analisis Saham: {analysis['symbol']}", title_style))
    story.append(Spacer(1, 20))
    
    # Decision
    decision_color = colors.HexColor('#4ade80') if analysis['keputusan'] == 'BELI' else \
                    colors.HexColor('#f87171') if analysis['keputusan'] == 'JUAL' else \
                    colors.HexColor('#fbbf24')
    
    decision_style = ParagraphStyle(
        'Decision',
        parent=styles['Heading1'],
        textColor=decision_color,
        fontSize=36,
        alignment=1
    )
    story.append(Paragraph(analysis['keputusan'], decision_style))
    story.append(Spacer(1, 10))
    
    # Summary
    story.append(Paragraph(f"Conviction: {analysis['conviction']}/10", normal_style))
    story.append(Spacer(1, 20))
    
    # Key sections
    sections = [
        ("RINGKASAN", analysis['ringkasan']),
        ("KONDISI MAKRO", analysis['kondisi_makro']),
        ("PELUANG TERSEMBUNYI", analysis['peluang_tersembunyi']),
        ("RISIKO UTAMA", analysis['risiko_utama']),
        ("STRATEGI MASUK", analysis['strategi_masuk']),
        ("TARGET HARGA", analysis['target_harga']),
        ("FILOSOFI", f"\"{analysis['filosofi']}\"")
    ]
    
    for title, content in sections:
        story.append(Paragraph(title, heading_style))
        story.append(Paragraph(content, normal_style))
        story.append(Spacer(1, 12))
    
    # Scores table
    story.append(Paragraph("SKOR PENILAIAN", heading_style))
    scores_data = [
        ['Aspek', 'Skor'],
        ['Fundamental', str(analysis['skor']['fundamental'])],
        ['Momentum', str(analysis['skor']['momentum'])],
        ['Valuasi', str(analysis['skor']['valuasi'])],
        ['Katalis', str(analysis['skor']['katalis'])]
    ]
    
    scores_table = Table(scores_data, colWidths=[2*inch, 1*inch])
    scores_table.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#c8a96e')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#2a2010')),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e1810')),
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10)
    ]))
    story.append(scores_table)
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer

# Main UI
st.markdown('<p class="main-title">REBORN RICH</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">"Lihat apa yang belum dilihat orang lain"</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown('<p class="section-header">NAVIGASI</p>', unsafe_allow_html=True)
    
    menu = st.radio(
        "Menu",
        ["🔍 Analisis Saham", "📊 Bandingkan", "📜 Riwayat", "👀 Watchlist"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    if menu == "👀 Watchlist":
        st.markdown('<p class="section-header">WATCHLIST</p>', unsafe_allow_html=True)
        for item in st.session_state.watchlist:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"📌 {item}")
            with col2:
                if st.button("❌", key=f"remove_{item}"):
                    st.session_state.watchlist.remove(item)
                    st.rerun()
        
        if st.button("+ Tambah ke Watchlist", use_container_width=True):
            new_item = st.text_input("Symbol (e.g., BBCA)")
            if new_item and new_item.upper() not in st.session_state.watchlist:
                st.session_state.watchlist.append(new_item.upper())
                st.rerun()

# Main content area
if menu == "🔍 Analisis Saham":
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        symbol = st.text_input("", placeholder="Contoh: BBCA, TLKM, ASII, GOTO...", 
                              label_visibility="collapsed").upper()
        
        analyze_button = st.button("ANALISIS ▶", use_container_width=True)
        
        if analyze_button and symbol:
            with st.spinner("Menganalisis..."):
                analysis = generate_analysis(symbol)
                st.session_state.current_analysis = analysis
                st.session_state.history.append(analysis)
                st.rerun()
    
    # Display current analysis if exists
    if st.session_state.current_analysis:
        analysis = st.session_state.current_analysis
        
        # Decision box
        decision_color = "#4ade80" if analysis['keputusan'] == "BELI" else \
                        "#f87171" if analysis['keputusan'] == "JUAL" else "#fbbf24"
        
        st.markdown(f"""
        <div class="decision-box" style="border-color: {decision_color}44;">
            <div style="position: absolute; inset: 0; background: radial-gradient(ellipse at 50% 0%, {decision_color}33, transparent 70%);"></div>
            <p class="section-header">KEPUTUSAN FINAL</p>
            <div class="decision-badge" style="color: {decision_color};">{analysis['keputusan']}</div>
            <div style="font-family: monospace; color: #8b7355; margin-bottom: 16px;">
                CONVICTION {analysis['conviction']}/10 — {"▮" * analysis['conviction']}{"▯" * (10 - analysis['conviction'])}
            </div>
            <div style="color: #c8a96e; font-style: italic; max-width: 580px; margin: 0 auto;">
                {analysis['ringkasan']}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Export buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("📥 Export PDF", use_container_width=True):
                pdf_buffer = export_to_pdf(analysis)
                b64 = base64.b64encode(pdf_buffer.getvalue()).decode()
                href = f'<a href="data:application/octet-stream;base64,{b64}" download="analisis_{analysis["symbol"]}.pdf">Klik untuk download PDF</a>'
                st.markdown(href, unsafe_allow_html=True)
        
        with col2:
            if st.button("📌 Tambah ke Watchlist", use_container_width=True):
                if analysis['symbol'] not in st.session_state.watchlist:
                    st.session_state.watchlist.append(analysis['symbol'])
                    st.success(f"{analysis['symbol']} ditambahkan ke watchlist!")
        
        with col3:
            if st.button("📊 Bandingkan", use_container_width=True):
                st.session_state.comparison.append(analysis)
                st.success("Ditambahkan ke perbandingan!")
        
        # 2-column layout for key info
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<p class="section-header">KONDISI MAKRO</p>', unsafe_allow_html=True)
            st.markdown(f'<div class="info-card">{analysis["kondisi_makro"]}</div>', unsafe_allow_html=True)
            
            st.markdown('<p class="section-header">PELUANG TERSEMBUNYI</p>', unsafe_allow_html=True)
            st.markdown(f'<div class="info-card">{analysis["peluang_tersembunyi"]}</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<p class="section-header">RISIKO UTAMA</p>', unsafe_allow_html=True)
            st.markdown(f'<div class="info-card">{analysis["risiko_utama"]}</div>', unsafe_allow_html=True)
            
            st.markdown('<p class="section-header">TARGET HARGA</p>', unsafe_allow_html=True)
            st.markdown(f'<div class="info-card">{analysis["target_harga"]}</div>', unsafe_allow_html=True)
        
        # Strategy
        st.markdown('<p class="section-header">STRATEGI MASUK</p>', unsafe_allow_html=True)
        st.markdown(f'<div class="info-card">{analysis["strategi_masuk"]}</div>', unsafe_allow_html=True)
        
        # Radar Chart
        st.markdown('<p class="section-header">MATRIX PENILAIAN</p>', unsafe_allow_html=True)
        fig = create_radar_chart(analysis['skor'])
        st.plotly_chart(fig, use_container_width=True)
        
        # Quote
        st.markdown(f'''
        <div class="quote-box">
            <p class="section-header">FILOSOFI INVESTASI</p>
            <p style="color: #d4af37; font-style: italic; font-size: 16px; margin: 0;">"{analysis['filosofi']}"</p>
        </div>
        ''', unsafe_allow_html=True)
        
        # Disclaimer
        st.markdown("""
        <div style="text-align: center; padding: 16px; font-size: 10px; color: #3d2e15; font-family: monospace;">
            ⚠ Analisis ini bersifat simulasi dan tidak merupakan saran investasi resmi.<br>
            Selalu lakukan riset mandiri dan konsultasikan dengan advisor keuangan profesional.
        </div>
        """, unsafe_allow_html=True)

elif menu == "📊 Bandingkan":
    st.markdown('<p class="section-header">BANDINGKAN SAHAM</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        symbol1 = st.text_input("Saham 1", placeholder="BBCA").upper()
    with col2:
        symbol2 = st.text_input("Saham 2", placeholder="BBRI").upper()
    
    symbol3 = st.text_input("Saham 3 (Opsional)", placeholder="TLKM").upper()
    
    if st.button("Bandingkan", use_container_width=True):
        symbols = [s for s in [symbol1, symbol2, symbol3] if s]
        if len(symbols) >= 2:
            with st.spinner("Menganalisis perbandingan..."):
                analyses = [generate_analysis(sym) for sym in symbols]
                
                # Comparison table
                comparison_data = []
                for analysis in analyses:
                    comparison_data.append({
                        "Saham": analysis['symbol'],
                        "Keputusan": analysis['keputusan'],
                        "Conviction": f"{analysis['conviction']}/10",
                        "Fundamental": analysis['skor']['fundamental'],
                        "Momentum": analysis['skor']['momentum'],
                        "Valuasi": analysis['skor']['valuasi'],
                        "Katalis": analysis['skor']['katalis']
                    })
                
                df = pd.DataFrame(comparison_data)
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                # Comparison chart
                fig = create_comparison_chart(analyses)
                st.plotly_chart(fig, use_container_width=True)
                
                # Detailed comparison
                st.markdown('<p class="section-header">ANALISIS DETAIL</p>', unsafe_allow_html=True)
                
                cols = st.columns(len(analyses))
                for idx, analysis in enumerate(analyses):
                    with cols[idx]:
                        st.markdown(f"### {analysis['symbol']}")
                        st.markdown(f"**Keputusan:** {analysis['keputusan']}")
                        st.markdown(f"**Target Harga:** {analysis['target_harga']}")
                        st.markdown(f"**Ringkasan:** {analysis['ringkasan']}")
                        
                        if st.button(f"📥 Export PDF {analysis['symbol']}", key=f"export_{idx}"):
                            pdf_buffer = export_to_pdf(analysis)
                            b64 = base64.b64encode(pdf_buffer.getvalue()).decode()
                            href = f'<a href="data:application/octet-stream;base64,{b64}" download="analisis_{analysis["symbol"]}.pdf">Download PDF</a>'
                            st.markdown(href, unsafe_allow_html=True)

elif menu == "📜 Riwayat":
    st.markdown('<p class="section-header">RIWAYAT ANALISIS</p>', unsafe_allow_html=True)
    
    if st.session_state.history:
        # Create a DataFrame for history
        history_data = []
        for i, analysis in enumerate(reversed(st.session_state.history[-10:])):  # Show last 10
            history_data.append({
                "No": len(st.session_state.history) - i,
                "Timestamp": analysis['timestamp'],
                "Saham": analysis['symbol'],
                "Keputusan": analysis['keputusan'],
                "Conviction": f"{analysis['conviction']}/10"
            })
        
        df = pd.DataFrame(history_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Load previous analysis
        selected_idx = st.selectbox(
            "Lihat analisis sebelumnya",
            options=range(len(st.session_state.history)),
            format_func=lambda x: f"{st.session_state.history[x]['timestamp']} - {st.session_state.history[x]['symbol']} ({st.session_state.history[x]['keputusan']})"
        )
        
        if st.button("Lihat Analisis"):
            st.session_state.current_analysis = st.session_state.history[selected_idx]
            st.rerun()
    else:
        st.info("Belum ada riwayat analisis. Lakukan analisis saham terlebih dahulu.")

elif menu == "👀 Watchlist":
    st.markdown('<p class="section-header">WATCHLIST</p>', unsafe_allow_html=True)
    
    if st.session_state.watchlist:
        cols = st.columns(3)
        for idx, item in enumerate(st.session_state.watchlist):
            with cols[idx % 3]:
                st.markdown(f"""
                <div class="info-card" style="text-align: center;">
                    <h3 style="color: #d4af37;">{item}</h3>
                    <p style="color: #8b7355;">Klik untuk analisis</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Analisis {item}", key=f"watch_{item}"):
                    st.session_state.current_analysis = generate_analysis(item)
                    st.rerun()
        
        if st.button("Refresh Watchlist", use_container_width=True):
            st.rerun()
    else:
        st.info("Watchlist masih kosong. Tambahkan saham dari halaman analisis.")
