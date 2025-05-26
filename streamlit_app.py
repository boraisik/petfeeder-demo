import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import json
from plotly.subplots import make_subplots

# Sayfa konfigürasyonu
st.set_page_config(
    page_title="PetFeeder Pro - Akıllı Köpek Besleme Sistemi",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Modern CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.5rem;
        animation: gradient 3s ease infinite;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .sub-header {
        text-align: center;
        color: #6c757d;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 60px 40px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 40px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .feature-card {
        background: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        margin: 20px 0;
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .feature-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.15);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 15px;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #667eea;
    }
    
    .metric-label {
        color: #6c757d;
        font-size: 1rem;
        margin-top: 5px;
    }
    
    .pet-profile-card {
        background: white;
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        text-align: center;
        margin: 20px 0;
    }
    
    .pet-avatar {
        font-size: 5rem;
        margin-bottom: 20px;
        animation: bounce 2s infinite;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    .price-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 40px;
        border-radius: 20px;
        text-align: center;
        margin: 20px 0;
        position: relative;
        overflow: hidden;
    }
    
    .price-card::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .cta-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px 40px;
        border-radius: 50px;
        font-size: 1.2rem;
        font-weight: 600;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
    }
    
    .cta-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.6);
    }
    
    .testimonial-card {
        background: #f8f9fa;
        padding: 30px;
        border-radius: 15px;
        margin: 20px 0;
        position: relative;
    }
    
    .testimonial-card::before {
        content: '"';
        font-size: 4rem;
        position: absolute;
        top: -10px;
        left: 20px;
        color: #667eea;
        opacity: 0.3;
    }
    
    .alert-card {
        background: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
    }
    
    .success-card {
        background: #d4edda;
        border-left: 4px solid #28a745;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
    }
    
    .info-card {
        background: #e3f2fd;
        border-left: 4px solid #2196f3;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
    }
    
    .dashboard-stat {
        background: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.08);
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .dashboard-stat:hover {
        transform: scale(1.05);
    }
    
    .loading-animation {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid #f3f3f3;
        border-top: 3px solid #667eea;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
</style>
""", unsafe_allow_html=True)

# Session state initialization
if 'user_data' not in st.session_state:
    st.session_state.user_data = None

if 'demo_stage' not in st.session_state:
    st.session_state.demo_stage = 'welcome'

if 'feeding_history' not in st.session_state:
    st.session_state.feeding_history = []

if 'health_records' not in st.session_state:
    st.session_state.health_records = []

# Dog breed data
DOG_BREEDS = {
    "Golden Retriever": {"min_weight": 25, "max_weight": 34, "daily_food_factor": 30},
    "Labrador Retriever": {"min_weight": 25, "max_weight": 36, "daily_food_factor": 32},
    "German Shepherd": {"min_weight": 22, "max_weight": 40, "daily_food_factor": 28},
    "Bulldog": {"min_weight": 18, "max_weight": 25, "daily_food_factor": 25},
    "Poodle": {"min_weight": 20, "max_weight": 32, "daily_food_factor": 26},
    "Beagle": {"min_weight": 9, "max_weight": 11, "daily_food_factor": 35},
    "Yorkshire Terrier": {"min_weight": 2, "max_weight": 3, "daily_food_factor": 40},
    "Pug": {"min_weight": 6, "max_weight": 9, "daily_food_factor": 30},
    "Shih Tzu": {"min_weight": 4, "max_weight": 7, "daily_food_factor": 32},
    "Siberian Husky": {"min_weight": 20, "max_weight": 27, "daily_food_factor": 30},
    "Boxer": {"min_weight": 25, "max_weight": 32, "daily_food_factor": 28},
    "Dachshund": {"min_weight": 7, "max_weight": 14, "daily_food_factor": 30},
    "Great Dane": {"min_weight": 50, "max_weight": 82, "daily_food_factor": 25},
    "Chihuahua": {"min_weight": 1.5, "max_weight": 3, "daily_food_factor": 40},
    "Rottweiler": {"min_weight": 35, "max_weight": 60, "daily_food_factor": 25},
    "Border Collie": {"min_weight": 12, "max_weight": 20, "daily_food_factor": 30},
    "Cocker Spaniel": {"min_weight": 12, "max_weight": 15, "daily_food_factor": 30},
    "French Bulldog": {"min_weight": 8, "max_weight": 13, "daily_food_factor": 28},
    "Maltese": {"min_weight": 3, "max_weight": 4, "daily_food_factor": 35},
    "Diğer": {"min_weight": 5, "max_weight": 50, "daily_food_factor": 30}
}

# Helper functions
def calculate_age(birth_date):
    today = datetime.now().date()
    age_days = (today - birth_date).days
    years = age_days // 365
    months = (age_days % 365) // 30
    return years, months

def calculate_daily_food(weight, breed, age_years):
    base_amount = weight * DOG_BREEDS.get(breed, {"daily_food_factor": 30})["daily_food_factor"]
    
    # Age adjustment
    if age_years < 1:
        base_amount *= 1.5  # Puppies need more
    elif age_years > 7:
        base_amount *= 0.9  # Senior dogs need less
    
    return int(base_amount)

def get_health_status(weight, breed):
    breed_info = DOG_BREEDS.get(breed, {"min_weight": 5, "max_weight": 50})
    if weight < breed_info["min_weight"]:
        return "Düşük Kilo", "warning", "Veteriner kontrolü önerilir"
    elif weight > breed_info["max_weight"]:
        return "Fazla Kilo", "danger", "Diyet programı önerilir"
    else:
        return "İdeal Kilo", "success", "Sağlıklı kilo aralığında"

def generate_feeding_schedule(daily_amount):
    morning = int(daily_amount * 0.6)
    evening = int(daily_amount * 0.4)
    return {
        "morning": {"time": "07:00", "amount": morning},
        "evening": {"time": "18:00", "amount": evening}
    }

# Welcome Screen
if st.session_state.demo_stage == 'welcome':
    st.markdown('<h1 class="main-header">🐾 PetFeeder Pro</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Köpeğinizin Sağlığı İçin Akıllı Besleme Çözümü</p>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="hero-section">
        <h2 style="font-size: 2.5rem; margin-bottom: 20px;">Köpeğinizi Uzaktan Besleyin, Sağlığını Takip Edin! 🦮</h2>
        <p style="font-size: 1.3rem; margin-bottom: 30px;">
            Yapay zeka destekli besleme programları, sağlık takibi ve 
            uzaktan kontrol ile köpeğinizin mutluluğu artık cebinizde!
        </p>
        <p style="font-size: 1.1rem; opacity: 0.9;">
            🎯 10.000+ mutlu köpek sahibi • ⭐ 4.9/5 kullanıcı puanı • 🏆 2024 En İyi Pet Tech Ödülü
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Features
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📱</div>
            <h3>Uzaktan Kontrol</h3>
            <p>İster evde ister işte olun, köpeğinizi tek tuşla besleyin. 
            Anlık bildirimlerle her şey kontrolünüzde!</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🤖</div>
            <h3>AI Destekli Öneriler</h3>
            <p>Claude AI ile köpeğinize özel beslenme programı, 
            sağlık tavsiyeleri ve aktivite önerileri!</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <h3>Detaylı Analitik</h3>
            <p>Kilo takibi, besleme geçmişi, sağlık raporları 
            ve maliyet analizleri tek panoda!</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Call to action
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; margin: 40px 0;">
            <h2>🎁 Özel Demo Deneyimi</h2>
            <p style="font-size: 1.2rem; color: #6c757d; margin: 20px 0;">
                Köpeğinizin bilgilerini girin, size özel hazırlanmış 
                akıllı besleme programınızı hemen görün!
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 Hemen Başla", key="start_demo", use_container_width=True):
            st.session_state.demo_stage = 'user_input'
            st.rerun()

# User Input Screen
elif st.session_state.demo_stage == 'user_input':
    st.markdown('<h1 class="main-header">🐾 Köpeğinizi Tanıyalım</h1>', unsafe_allow_html=True)
    
    with st.form("user_info_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            user_name = st.text_input("👤 Adınız", placeholder="Örn: Ahmet")
            dog_name = st.text_input("🐕 Köpeğinizin Adı", placeholder="Örn: Max")
            dog_breed = st.selectbox("🦴 Cinsi", options=list(DOG_BREEDS.keys()))
        
        with col2:
            dog_weight = st.number_input("⚖️ Kilosu (kg)", min_value=0.5, max_value=100.0, step=0.5, value=10.0)
            dog_birthdate = st.date_input("🎂 Doğum Tarihi", 
                                        min_value=datetime(2000, 1, 1), 
                                        max_value=datetime.now(),
                                        value=datetime.now() - timedelta(days=730))
            dog_gender = st.radio("⚥ Cinsiyeti", ["Erkek", "Dişi"], horizontal=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit = st.form_submit_button("✨ Demo'yu Başlat", use_container_width=True)
        
        if submit:
            if all([user_name, dog_name]):
                # Calculate age
                age_years, age_months = calculate_age(dog_birthdate)
                
                # Store user data
                st.session_state.user_data = {
                    "user_name": user_name,
                    "dog_name": dog_name,
                    "dog_breed": dog_breed,
                    "dog_weight": dog_weight,
                    "dog_birthdate": dog_birthdate,
                    "dog_gender": dog_gender,
                    "age_years": age_years,
                    "age_months": age_months,
                    "daily_food": calculate_daily_food(dog_weight, dog_breed, age_years),
                    "avatar": "🦮" if dog_breed in ["Golden Retriever", "Labrador Retriever"] else "🐕"
                }
                
                st.session_state.demo_stage = 'dashboard'
                st.rerun()
            else:
                st.error("⚠️ Lütfen tüm alanları doldurun!")

# Dashboard
elif st.session_state.demo_stage == 'dashboard':
    user = st.session_state.user_data
    
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f'<h1 class="main-header">Merhaba {user["user_name"]}! 👋</h1>', unsafe_allow_html=True)
    with col2:
        if st.button("🔄 Yeni Demo"):
            st.session_state.demo_stage = 'welcome'
            st.session_state.user_data = None
            st.rerun()
    
    # Pet Profile Card
    st.markdown(f"""
    <div class="pet-profile-card">
        <div class="pet-avatar">{user["avatar"]}</div>
        <h2>{user["dog_name"]}</h2>
        <p style="color: #6c757d; font-size: 1.2rem;">
            {user["dog_breed"]} • {user["age_years"]} yaş {user["age_months"]} ay • {user["dog_weight"]} kg
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main Tabs
    tabs = st.tabs(["📊 Özet", "🍖 Besleme", "💰 Maliyet", "🏥 Sağlık", "🤖 AI Asistan"])
    
    # Summary Tab
    with tabs[0]:
        # Key Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            weight_status, status_type, status_message = get_health_status(user["dog_weight"], user["dog_breed"])
            color = {"success": "#28a745", "warning": "#ffc107", "danger": "#dc3545"}[status_type]
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value" style="color: {color};">{weight_status}</div>
                <div class="metric-label">Kilo Durumu</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{user["daily_food"]}g</div>
                <div class="metric-label">Günlük Mama</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            monthly_cost = (user["daily_food"] * 30 / 1000) * 450  # 450 TL/kg average
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{monthly_cost:,.0f}₺</div>
                <div class="metric-label">Aylık Maliyet</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            feeding_rate = random.randint(85, 98)
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">%{feeding_rate}</div>
                <div class="metric-label">Besleme Başarısı</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Quick Actions
        st.markdown("### ⚡ Hızlı İşlemler")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🍖 Hemen Besle", use_container_width=True):
                st.success(f"✅ {user['dog_name']} için {user['daily_food']//2}g mama verildi!")
                st.balloons()
        
        with col2:
            if st.button("📸 Canlı Görüntü", use_container_width=True):
                st.info("📹 Canlı yayın özelliği yakında aktif!")
        
        with col3:
            if st.button("📊 Günlük Rapor", use_container_width=True):
                st.info("📈 Detaylı raporlar hazırlanıyor...")
        
        # Health Alert
        if status_type != "success":
            st.markdown(f"""
            <div class="alert-card">
                <h4>⚠️ Sağlık Uyarısı</h4>
                <p>{user['dog_name']} {weight_status.lower()} kategorisinde. {status_message}.</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Feeding Tab
    with tabs[1]:
        st.markdown("## 🍖 Akıllı Besleme Programı")
        
        schedule = generate_feeding_schedule(user["daily_food"])
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="dashboard-stat">
                <h3>☀️ Sabah Öğünü</h3>
                <p style="font-size: 2rem; color: #667eea; margin: 20px 0;">
                    {schedule['morning']['time']}
                </p>
                <p style="font-size: 1.5rem;">
                    {schedule['morning']['amount']}g
                </p>
                <button style="width: 100%; padding: 10px; background: #667eea; color: white; border: none; border-radius: 10px; margin-top: 10px;">
                    Sabah Beslemesini Ayarla
                </button>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="dashboard-stat">
                <h3>🌙 Akşam Öğünü</h3>
                <p style="font-size: 2rem; color: #764ba2; margin: 20px 0;">
                    {schedule['evening']['time']}
                </p>
                <p style="font-size: 1.5rem;">
                    {schedule['evening']['amount']}g
                </p>
                <button style="width: 100%; padding: 10px; background: #764ba2; color: white; border: none; border-radius: 10px; margin-top: 10px;">
                    Akşam Beslemesini Ayarla
                </button>
            </div>
            """, unsafe_allow_html=True)
        
        # Weekly Schedule
        st.markdown("### 📅 Haftalık Besleme Grafiği")
        
        # Generate sample data
        dates = [(datetime.now() - timedelta(days=i)).strftime("%d/%m") for i in range(7, 0, -1)]
        planned = [user["daily_food"]] * 7
        actual = [user["daily_food"] + random.randint(-50, 50) for _ in range(7)]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates, y=planned,
            mode='lines+markers',
            name='Planlanan',
            line=dict(color='#667eea', width=3)
        ))
        fig.add_trace(go.Scatter(
            x=dates, y=actual,
            mode='lines+markers',
            name='Gerçekleşen',
            line=dict(color='#764ba2', width=3)
        ))
        
        fig.update_layout(
            title="Son 7 Günlük Besleme Takibi",
            xaxis_title="Tarih",
            yaxis_title="Mama Miktarı (g)",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Cost Tab
    with tabs[2]:
        st.markdown("## 💰 Maliyet Analizi ve Tasarruf")
        
        # Monthly cost calculation
        daily_kg = user["daily_food"] / 1000
        monthly_kg = daily_kg * 30
        
        # Price comparison
        prices = {
            "Premium Mama": 550,
            "Standart Mama": 450,
            "Ekonomik Mama": 350
        }
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Cost comparison chart
            fig = go.Figure()
            
            for food_type, price_per_kg in prices.items():
                monthly_costs = [monthly_kg * price_per_kg * (i+1) for i in range(12)]
                fig.add_trace(go.Scatter(
                    x=list(range(1, 13)),
                    y=monthly_costs,
                    mode='lines+markers',
                    name=f'{food_type} ({price_per_kg}₺/kg)'
                ))
            
            fig.update_layout(
                title="12 Aylık Maliyet Projeksiyonu",
                xaxis_title="Ay",
                yaxis_title="Toplam Maliyet (₺)",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            current_monthly = monthly_kg * 450
            yearly = current_monthly * 12
            
            st.markdown(f"""
            <div class="price-card">
                <h3>Mevcut Giderler</h3>
                <p style="font-size: 0.9rem; opacity: 0.8; margin: 10px 0;">Aylık</p>
                <p style="font-size: 2.5rem; margin: 0;">{current_monthly:,.0f}₺</p>
                <hr style="opacity: 0.3; margin: 20px 0;">
                <p style="font-size: 0.9rem; opacity: 0.8; margin: 10px 0;">Yıllık</p>
                <p style="font-size: 2rem; margin: 0;">{yearly:,.0f}₺</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Savings tips
        st.markdown("### 💡 Tasarruf Önerileri")
        
        savings = [
            {"tip": "🛍️ Toplu alımda %15 indirim", "amount": current_monthly * 0.15},
            {"tip": "📅 Aylık abonelikte %10 indirim", "amount": current_monthly * 0.10},
            {"tip": "🥗 Haftada 2 öğün ev yemeği", "amount": current_monthly * 0.20}
        ]
        
        total_savings = sum(s["amount"] for s in savings)
        
        for saving in savings:
            st.markdown(f"""
            <div class="success-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span>{saving['tip']}</span>
                    <span style="font-size: 1.2rem; font-weight: 600;">
                        {saving['amount']:,.0f}₺/ay
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="text-align: center; margin: 30px 0;">
            <h3>💰 Toplam Tasarruf Potansiyeli</h3>
            <p style="font-size: 2.5rem; color: #28a745; font-weight: 700;">
                {total_savings:,.0f}₺/ay
            </p>
            <p style="color: #6c757d;">Yıllık {total_savings * 12:,.0f}₺ tasarruf!</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Health Tab
    with tabs[3]:
        st.markdown("## 🏥 Sağlık Takibi")
        
        # Weight tracking
        breed_info = DOG_BREEDS[user["dog_breed"]]
        
        # Generate sample weight data
        dates = [(datetime.now() - timedelta(days=i*30)).strftime("%B") for i in range(6, 0, -1)]
        weights = [user["dog_weight"] + random.uniform(-1, 1) for _ in range(6)]
        
        fig = go.Figure()
        
        # Add weight line
        fig.add_trace(go.Scatter(
            x=dates, y=weights,
            mode='lines+markers',
            name='Kilo',
            line=dict(color='#667eea', width=3)
        ))
        
        # Add ideal weight range
        fig.add_trace(go.Scatter(
            x=dates, y=[breed_info["min_weight"]] * 6,
            mode='lines',
            name='Min İdeal',
            line=dict(color='green', dash='dash')
        ))
        
        fig.add_trace(go.Scatter(
            x=dates, y=[breed_info["max_weight"]] * 6,
            mode='lines',
            name='Max İdeal',
            line=dict(color='red', dash='dash'),
            fill='tonexty',
            fillcolor='rgba(0,255,0,0.1)'
        ))
        
        fig.update_layout(
            title=f"{user['dog_name']} - Kilo Takibi",
            xaxis_title="Ay",
            yaxis_title="Kilo (kg)",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Health recommendations
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="info-card">
                <h4>📋 Sağlık Durumu</h4>
                <ul style="margin: 15px 0;">
                    <li>Kilo durumu: """ + weight_status + """</li>
                    <li>Aktivite seviyesi: Normal</li>
                    <li>Son veteriner kontrolü: 2 ay önce</li>
                    <li>Aşı durumu: Güncel</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="alert-card">
                <h4>💊 Yaklaşan İşlemler</h4>
                <ul style="margin: 15px 0;">
                    <li>Kuduz aşısı - 3 ay sonra</li>
                    <li>Parazit tedavisi - 1 ay sonra</li>
                    <li>Diş kontrolü - 6 ay sonra</li>
                    <li>Genel kontrol - 4 ay sonra</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    # AI Assistant Tab
    with tabs[4]:
        st.markdown("## 🤖 Claude AI Asistanı")
        
        # Pre-made questions
        questions = [
            f"{user['dog_name']} için ideal beslenme programı nedir?",
            f"{user['dog_breed']} ırkı için dikkat edilmesi gerekenler",
            "Kilo kontrolü için öneriler",
            "Aktivite ve egzersiz programı"
        ]
        
        st.markdown("### 💡 Hızlı Sorular")
        
        cols = st.columns(2)
        for i, question in enumerate(questions):
            with cols[i % 2]:
                if st.button(question, key=f"q_{i}", use_container_width=True):
                    with st.spinner("Claude AI yanıt hazırlıyor..."):
                        # Simulate AI response
                        if i == 0:
                            response = f"""
                            🤖 **{user['dog_name']} için Özel Beslenme Programı:**
                            
                            {user['dog_breed']} ırkı ve {user['dog_weight']}kg ağırlığı göz önüne alındığında:
                            
                            **Günlük Öneriler:**
                            - Sabah 07:00: {schedule['morning']['amount']}g ({schedule['morning']['amount']*4} kalori)
                            - Akşam 18:00: {schedule['evening']['amount']}g ({schedule['evening']['amount']*4} kalori)
                            - Toplam: {user['daily_food']}g/gün
                            
                            **Mama Önerileri:**
                            1. Royal Canin {user['dog_breed']} Adult
                            2. Hill's Science Diet Large Breed
                            3. Acana Heritage Free-Run Poultry
                            
                            **Özel Notlar:**
                            - Bol taze su bulundurun
                            - Öğünler arası atıştırmalık vermeyin
                            - Haftada 1-2 kez kemik verilebilir
                            """
                        elif i == 1:
                            response = f"""
                            🦴 **{user['dog_breed']} Irkı Hakkında:**
                            
                            **Karakteristik Özellikler:**
                            - Ortalama yaşam süresi: 10-12 yıl
                            - Enerji seviyesi: Yüksek
                            - Egzersiz ihtiyacı: Günde 60-90 dakika
                            
                            **Sağlık Riskleri:**
                            - Kalça displazisi riski
                            - Göz problemleri
                            - Cilt alerjileri
                            
                            **Bakım Önerileri:**
                            - Düzenli tüy bakımı
                            - Haftalık kulak temizliği
                            - 3 ayda bir tırnak kesimi
                            """
                        else:
                            response = "AI yanıtı hazırlanıyor..."
                        
                        st.markdown(f"""
                        <div class="info-card" style="margin-top: 20px;">
                            {response}
                        </div>
                        """, unsafe_allow_html=True)
        
        # Custom question
        st.markdown("### 💬 Soru Sorun")
        user_question = st.text_area("Claude AI'ya sorunuzu yazın...", height=100)
        
        if st.button("🤖 Yanıt Al", use_container_width=True):
            if user_question:
                with st.spinner("Yanıt hazırlanıyor..."):
                    st.markdown(f"""
                    <div class="info-card" style="margin-top: 20px;">
                        <h4>🤖 Claude AI Yanıtı:</h4>
                        <p>Sorunuz analiz ediliyor. {user['dog_name']} için özel yanıt hazırlanıyor...</p>
                        <p style="margin-top: 15px;">
                        Demo versiyonda temel AI desteği sunulmaktadır. 
                        Gelişmiş özellikler için tam sürümü kullanabilirsiniz!
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
    

# Footer
st.markdown("""
<hr style="margin: 60px 0 20px 0;">
<div style="text-align: center; color: #6c757d; padding: 20px;">
    <p>🐾 PetFeeder Pro - Akıllı Köpek Besleme Sistemi</p>
    <p>Made with ❤️ for pet lovers | © 2024</p>
    <p style="margin-top: 10px;">
        <a href="#" style="color: #667eea; text-decoration: none; margin: 0 10px;">Gizlilik</a> |
        <a href="#" style="color: #667eea; text-decoration: none; margin: 0 10px;">Kullanım Koşulları</a> |
        <a href="#" style="color: #667eea; text-decoration: none; margin: 0 10px;">İletişim</a>
    </p>
</div>
""", unsafe_allow_html=True)
