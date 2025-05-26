import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import random
import json

# Sayfa konfigürasyonu
st.set_page_config(
    page_title="🐾 PetFeeder Pro - Demo",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS stilleri
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .welcome-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 30px;
        border-radius: 20px;
        margin: 20px 0;
        text-align: center;
    }
    
    .info-card {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
        border-left: 5px solid #667eea;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .pet-profile-card {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        margin: 20px 0;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
    }
    
    .feature-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        height: 100%;
        transition: transform 0.3s;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
    }
    
    .food-recommendation {
        background: linear-gradient(135deg, #f6d365 0%, #fda085 100%);
        color: white;
        padding: 25px;
        border-radius: 20px;
        margin: 20px 0;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 10px 30px;
        border-radius: 25px;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
</style>
""", unsafe_allow_html=True)

# Session state başlatma
if 'demo_started' not in st.session_state:
    st.session_state.demo_started = False
    st.session_state.user_name = ""
    st.session_state.dog_name = ""
    st.session_state.dog_breed = ""
    st.session_state.dog_birthdate = None
    st.session_state.dog_weight = 10.0
    st.session_state.feeding_history = []
    st.session_state.weight_history = []
    st.session_state.current_page = "home"

# Başlık
st.markdown("""
<div class="main-header">
    <h1>🐾 PetFeeder Pro</h1>
    <p style="font-size: 20px; margin-top: 10px;">Akıllı Köpek Besleme ve Takip Sistemi</p>
    <p style="font-size: 16px; opacity: 0.9;">Demo Sürümü</p>
</div>
""", unsafe_allow_html=True)

# Giriş ekranı
if not st.session_state.demo_started:
    st.markdown("""
    <div class="welcome-card">
        <h2>Hoş Geldiniz! 👋</h2>
        <p>PetFeeder Pro ile köpeğinizin beslenmesini ve sağlığını takip etmenin en kolay yolu!</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("user_info_form"):
        st.markdown("### 👤 Kullanıcı Bilgileri")
        col1, col2 = st.columns(2)
        
        with col1:
            user_name = st.text_input("Adınız", placeholder="Örn: Ahmet Yılmaz")
        
        with col2:
            st.empty()
        
        st.markdown("### 🐕 Köpek Bilgileri")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            dog_name = st.text_input("Köpeğinizin Adı", placeholder="Örn: Max")
            dog_breed = st.selectbox("Cinsi", [
                "Pug", "Golden Retriever", "Labrador", "Beagle", 
                "French Bulldog", "German Shepherd", "Poodle", "Chihuahua", "Diğer"
            ])
        
        with col2:
            dog_birthdate = st.date_input(
                "Doğum Tarihi",
                min_value=datetime.now().date() - timedelta(days=365*20),
                max_value=datetime.now().date(),
                value=datetime.now().date() - timedelta(days=365*2)
            )
            
        with col3:
            dog_weight = st.number_input("Kilosu (kg)", min_value=0.5, max_value=100.0, value=10.0, step=0.1)
        
        submitted = st.form_submit_button("🚀 Demo'yu Başlat", use_container_width=True)
        
        if submitted:
            if user_name and dog_name:
                st.session_state.demo_started = True
                st.session_state.user_name = user_name
                st.session_state.dog_name = dog_name
                st.session_state.dog_breed = dog_breed
                st.session_state.dog_birthdate = dog_birthdate
                st.session_state.dog_weight = dog_weight
                
                # İlk ağırlık kaydı
                st.session_state.weight_history.append({
                    "date": datetime.now().date(),
                    "weight": dog_weight
                })
                
                st.rerun()
            else:
                st.error("Lütfen tüm alanları doldurun!")

# Ana uygulama
else:
    # Yan menü
    with st.sidebar:
        st.markdown(f"### 👋 Merhaba {st.session_state.user_name}!")
        st.markdown(f"🐕 **{st.session_state.dog_name}**")
        
        # Köpek yaşını hesapla
        age_days = (datetime.now().date() - st.session_state.dog_birthdate).days
        age_years = age_days // 365
        age_months = (age_days % 365) // 30
        
        st.markdown(f"📅 Yaş: {age_years} yıl {age_months} ay")
        st.markdown(f"⚖️ Kilo: {st.session_state.dog_weight} kg")
        st.markdown(f"🐕 Cins: {st.session_state.dog_breed}")
        
        st.markdown("---")
        
        # Menü
        menu_items = {
            "home": "🏠 Ana Sayfa",
            "feed": "🍽️ Besleme",
            "food": "🥘 Mama Önerileri",
            "weight": "⚖️ Kilo Takibi",
            "health": "🏥 Sağlık",
            "reports": "📊 Raporlar",
            "settings": "⚙️ Ayarlar"
        }
        
        for key, label in menu_items.items():
            if st.button(label, key=f"menu_{key}", use_container_width=True):
                st.session_state.current_page = key
                st.rerun()
    
    # Ana içerik
    if st.session_state.current_page == "home":
        st.markdown(f"""
        <div class="pet-profile-card">
            <h2>🐾 {st.session_state.dog_name}'in Profili</h2>
            <p style="font-size: 18px;">Sağlıklı ve mutlu bir köpek!</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Özet bilgiler
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h3>🍽️</h3>
                <h4>Bugünkü Öğün</h4>
                <p style="font-size: 24px; font-weight: bold;">2 / 3</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h3>⚖️</h3>
                <h4>Güncel Kilo</h4>
                <p style="font-size: 24px; font-weight: bold;">{:.1f} kg</p>
            </div>
            """.format(st.session_state.dog_weight), unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card">
                <h3>💊</h3>
                <h4>Sonraki Aşı</h4>
                <p style="font-size: 24px; font-weight: bold;">15 gün</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="metric-card">
                <h3>📅</h3>
                <h4>Yaş</h4>
                <p style="font-size: 24px; font-weight: bold;">{} yıl</p>
            </div>
            """.format(age_years), unsafe_allow_html=True)
        
        # Özellikler
        st.markdown("### 🌟 Sistem Özellikleri")
        
        feature_cols = st.columns(3)
        
        with feature_cols[0]:
            st.markdown("""
            <div class="feature-card">
                <h3>🤖 Akıllı Besleme</h3>
                <p>Köpeğinizin ihtiyaçlarına göre otomatik porsiyon ayarlama</p>
            </div>
            """, unsafe_allow_html=True)
        
        with feature_cols[1]:
            st.markdown("""
            <div class="feature-card">
                <h3>📱 Uzaktan Kontrol</h3>
                <p>Dünyanın her yerinden telefonunuzla kontrol</p>
            </div>
            """, unsafe_allow_html=True)
        
        with feature_cols[2]:
            st.markdown("""
            <div class="feature-card">
                <h3>📊 Detaylı Raporlar</h3>
                <p>Besleme ve sağlık verileri ile kapsamlı analizler</p>
            </div>
            """, unsafe_allow_html=True)
    
    elif st.session_state.current_page == "feed":
        st.markdown("## 🍽️ Besleme Kontrol Paneli")
        
        # Manuel besleme
        st.markdown("""
        <div class="info-card">
            <h4>🎯 Hızlı Besleme</h4>
            <p>Köpeğinizi hemen şimdi beslemek için aşağıdaki butonu kullanın.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            # Porsiyon miktarı
            portion = st.slider(
                "Porsiyon Miktarı (gram)",
                min_value=5,
                max_value=100,
                value=25,
                step=5
            )
            
            if st.button(f"🍽️ {st.session_state.dog_name}'i Besle ({portion}g)", use_container_width=True):
                with st.spinner("Besleme işlemi başlatılıyor..."):
                    time.sleep(2)
                
                # Besleme geçmişine ekle
                st.session_state.feeding_history.append({
                    "timestamp": datetime.now(),
                    "amount": portion,
                    "type": "Manuel"
                })
                
                st.success(f"✅ {st.session_state.dog_name} başarıyla beslendi!")
                st.balloons()
        
        # Besleme geçmişi
        if st.session_state.feeding_history:
            st.markdown("### 📜 Besleme Geçmişi")
            
            # DataFrame oluştur
            df_history = pd.DataFrame([
                {
                    "Tarih": f.get("timestamp").strftime("%d.%m.%Y"),
                    "Saat": f.get("timestamp").strftime("%H:%M"),
                    "Miktar (g)": f.get("amount"),
                    "Tip": f.get("type")
                }
                for f in st.session_state.feeding_history
            ])
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.dataframe(df_history.tail(10), use_container_width=True)
            
            with col2:
                # Bugünkü toplam
                today_total = sum([
                    f["amount"] for f in st.session_state.feeding_history 
                    if f["timestamp"].date() == datetime.now().date()
                ])
                
                st.markdown(f"""
                <div class="metric-card">
                    <h4>Bugünkü Toplam</h4>
                    <p style="font-size: 36px; font-weight: bold;">{today_total}g</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Otomatik besleme zamanlaması
        st.markdown("### ⏰ Otomatik Besleme Zamanları")
        st.info("💡 Demo modunda otomatik besleme simülasyonu gösterilmektedir.")
        
        schedule_data = {
            "Öğün": ["Sabah", "Öğle", "Akşam"],
            "Saat": ["08:00", "13:00", "19:00"],
            "Miktar (g)": [20, 15, 25],
            "Durum": ["✅ Tamamlandı", "✅ Tamamlandı", "⏳ Bekliyor"]
        }
        
        st.dataframe(pd.DataFrame(schedule_data), use_container_width=True)
    
    elif st.session_state.current_page == "food":
        st.markdown("## 🥘 Mama Önerileri")
        
        st.markdown("""
        <div class="food-recommendation">
            <h3>🎯 Kişiselleştirilmiş Mama Önerileri</h3>
            <p>Mama bilgilerinizi girerek köpeğiniz için en uygun mama önerilerini alabilirsiniz!</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Mama bilgi formu
        with st.form("food_info_form"):
            st.markdown("### 📝 Mevcut Mama Bilgileri")
            
            col1, col2 = st.columns(2)
            
            with col1:
                current_brand = st.selectbox("Marka", [
                    "Seçiniz...",
                    "Royal Canin",
                    "Pro Plan",
                    "Hill's",
                    "Acana",
                    "Orijen",
                    "N&D",
                    "Brit Care",
                    "Diğer"
                ])
                
                food_type = st.selectbox("Mama Tipi", [
                    "Kuru Mama",
                    "Yaş Mama",
                    "Karışık"
                ])
            
            with col2:
                activity_level = st.select_slider(
                    "Aktivite Seviyesi",
                    options=["Düşük", "Normal", "Yüksek"]
                )
                
                health_issues = st.multiselect(
                    "Sağlık Durumları",
                    ["Alerji", "Kilo Problemi", "Sindirim Hassasiyeti", "Eklem Problemleri", "Yok"]
                )
            
            special_notes = st.text_area("Özel Notlar (opsiyonel)", placeholder="Örn: Tavuk alerjisi var")
            
            submitted = st.form_submit_button("🔍 Öneri Al", use_container_width=True)
            
            if submitted and current_brand != "Seçiniz...":
                with st.spinner("Analiz ediliyor..."):
                    time.sleep(2)
                
                # Öneri oluştur
                st.markdown("### 🎯 Size Özel Mama Önerileri")
                
                # Örnek öneriler
                recommendations = [
                    {
                        "name": "Royal Canin " + st.session_state.dog_breed,
                        "reason": f"{st.session_state.dog_breed} ırkına özel formül",
                        "price": "₺450-550/kg",
                        "rating": 4.5
                    },
                    {
                        "name": "Pro Plan Sensitive Skin",
                        "reason": "Hassas ciltli köpekler için ideal",
                        "price": "₺400-480/kg",
                        "rating": 4.3
                    },
                    {
                        "name": "Hill's Science Plan",
                        "reason": "Dengeli beslenme ve kilo kontrolü",
                        "price": "₺420-500/kg",
                        "rating": 4.4
                    }
                ]
                
                for rec in recommendations:
                    st.markdown(f"""
                    <div class="info-card">
                        <h4>{rec['name']}</h4>
                        <p><strong>Neden öneriyoruz:</strong> {rec['reason']}</p>
                        <p><strong>Fiyat aralığı:</strong> {rec['price']}</p>
                        <p><strong>Kullanıcı puanı:</strong> {'⭐' * int(rec['rating'])}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Porsiyon hesaplama
                st.markdown("### 📏 Günlük Porsiyon Hesaplama")
                
                daily_amount = round(st.session_state.dog_weight * 25)  # Basit hesaplama
                
                st.markdown(f"""
                <div class="metric-card">
                    <h4>Önerilen Günlük Miktar</h4>
                    <p style="font-size: 36px; font-weight: bold;">{daily_amount}g</p>
                    <p>3 öğüne bölünmüş: {daily_amount//3}g x 3</p>
                </div>
                """, unsafe_allow_html=True)
            
            elif submitted:
                st.warning("Lütfen mevcut mama markanızı seçin!")
    
    elif st.session_state.current_page == "weight":
        st.markdown("## ⚖️ Kilo Takibi")
        
        # Kilo girişi
        col1, col2 = st.columns([2, 1])
        
        with col1:
            new_weight = st.number_input(
                "Yeni Kilo Ölçümü (kg)",
                min_value=0.5,
                max_value=100.0,
                value=st.session_state.dog_weight,
                step=0.1
            )
        
        with col2:
            if st.button("📊 Kaydet", use_container_width=True):
                st.session_state.dog_weight = new_weight
                st.session_state.weight_history.append({
                    "date": datetime.now().date(),
                    "weight": new_weight
                })
                st.success("✅ Kilo kaydedildi!")
        
        # İdeal kilo aralığı
        ideal_ranges = {
            "Pug": (6.0, 9.0),
            "Golden Retriever": (25.0, 34.0),
            "Labrador": (25.0, 36.0),
            "Beagle": (9.0, 11.0),
            "French Bulldog": (8.0, 14.0),
            "German Shepherd": (22.0, 40.0),
            "Poodle": (20.0, 32.0),
            "Chihuahua": (1.5, 3.0)
        }
        
        ideal_min, ideal_max = ideal_ranges.get(st.session_state.dog_breed, (5.0, 50.0))
        
        # Kilo durumu
        if st.session_state.dog_weight < ideal_min:
            status = "⚠️ Düşük Kilo"
            status_color = "orange"
            advice = "Veterinerinizle görüşmenizi öneririz."
        elif st.session_state.dog_weight > ideal_max:
            status = "⚠️ Fazla Kilo"
            status_color = "red"
            advice = "Porsiyon kontrolü ve egzersiz önerilir."
        else:
            status = "✅ İdeal Kilo"
            status_color = "green"
            advice = "Harika! Bu kiloyu korumaya devam edin."
        
        st.markdown(f"""
        <div class="info-card" style="border-left-color: {status_color};">
            <h3>{status}</h3>
            <p><strong>Mevcut:</strong> {st.session_state.dog_weight} kg</p>
            <p><strong>İdeal aralık:</strong> {ideal_min} - {ideal_max} kg</p>
            <p><strong>Öneri:</strong> {advice}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Kilo grafiği
        if len(st.session_state.weight_history) > 1:
            st.markdown("### 📈 Kilo Değişim Grafiği")
            
            df_weight = pd.DataFrame(st.session_state.weight_history)
            
            fig = go.Figure()
            
            # Kilo çizgisi
            fig.add_trace(go.Scatter(
                x=df_weight['date'],
                y=df_weight['weight'],
                mode='lines+markers',
                name='Kilo',
                line=dict(color='blue', width=3),
                marker=dict(size=8)
            ))
            
            # İdeal aralık
            fig.add_hline(y=ideal_min, line_dash="dash", line_color="green", 
                         annotation_text=f"Min: {ideal_min} kg")
            fig.add_hline(y=ideal_max, line_dash="dash", line_color="green",
                         annotation_text=f"Max: {ideal_max} kg")
            
            fig.update_layout(
                title="Kilo Takip Grafiği",
                xaxis_title="Tarih",
                yaxis_title="Kilo (kg)",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    elif st.session_state.current_page == "health":
        st.markdown("## 🏥 Sağlık Takibi")
        
        st.info("🎮 Demo modunda örnek sağlık verileri gösterilmektedir.")
        
        # Aşı takvimi
        st.markdown("### 💉 Aşı Takvimi")
        
        vaccine_data = {
            "Aşı": ["Karma", "Kuduz", "Lyme", "Parazit"],
            "Son Tarih": ["15.01.2024", "20.02.2024", "10.03.2024", "05.04.2024"],
            "Sonraki Tarih": ["15.01.2025", "20.02.2025", "10.03.2025", "05.07.2024"],
            "Durum": ["✅", "✅", "✅", "⏳"]
        }
        
        st.dataframe(pd.DataFrame(vaccine_data), use_container_width=True)
        
        # Sağlık metrikleri
        st.markdown("### 📊 Sağlık Göstergeleri")
        
        health_cols = st.columns(3)
        
        with health_cols[0]:
            st.markdown("""
            <div class="metric-card">
                <h4>❤️ Kalp Atışı</h4>
                <p style="font-size: 24px;">70-120 bpm</p>
                <p style="color: lightgreen;">Normal</p>
            </div>
            """, unsafe_allow_html=True)
        
        with health_cols[1]:
            st.markdown("""
            <div class="metric-card">
                <h4>🌡️ Vücut Isısı</h4>
                <p style="font-size: 24px;">38.5°C</p>
                <p style="color: lightgreen;">Normal</p>
            </div>
            """, unsafe_allow_html=True)
        
        with health_cols[2]:
            st.markdown("""
            <div class="metric-card">
                <h4>🏃 Aktivite</h4>
                <p style="font-size: 24px;">Orta</p>
                <p style="color: yellow;">İyi</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Veteriner notları
        st.markdown("### 👨‍⚕️ Veteriner Notları")
        
        st.markdown("""
        <div class="info-card">
            <h4>Son Kontrol: 01.05.2024</h4>
            <p><strong>Veteriner:</strong> Dr. Ayşe Yılmaz</p>
            <p><strong>Not:</strong> Genel sağlık durumu iyi. Dişlerde hafif tartar birikimi var, 
            düzenli diş temizliği önerilir. Kilo takibi devam etmeli.</p>
        </div>
        """, unsafe_allow_html=True)
    
    elif st.session_state.current_page == "reports":
        st.markdown("## 📊 Raporlar ve Analizler")
        
        # Özet istatistikler
        total_meals = len(st.session_state.feeding_history)
        if total_meals > 0:
            total_food = sum([f["amount"] for f in st.session_state.feeding_history])
            avg_portion = total_food / total_meals if total_meals > 0 else 0
        else:
            total_food = 0
            avg_portion = 0
        
        stat_cols = st.columns(4)
        
        with stat_cols[0]:
            st.metric("Toplam Öğün", total_meals)
        
        with stat_cols[1]:
            st.metric("Toplam Mama", f"{total_food}g")
        
        with stat_cols[2]:
            st.metric("Ort. Porsiyon", f"{avg_portion:.1f}g")
        
        with stat_cols[3]:
            weight_change = 0
            if len(st.session_state.weight_history) > 1:
                weight_change = st.session_state.weight_history[-1]["weight"] - st.session_state.weight_history[0]["weight"]
            st.metric("Kilo Değişimi", f"{weight_change:+.1f} kg")
        
        # Grafikler
        if st.session_state.feeding_history:
            st.markdown("### 📈 Besleme Analizi")
            
            # Günlük besleme grafiği
            daily_data = {}
            for feed in st.session_state.feeding_history:
                date_str = feed["timestamp"].strftime("%d.%m")
                if date_str not in daily_data:
                    daily_data[date_str] = 0
                daily_data[date_str] += feed["amount"]
            
            if daily_data:
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=list(daily_data.keys()),
                    y=list(daily_data.values()),
                    marker_color='lightblue'
                ))
                
                fig.update_layout(
                    title="Günlük Toplam Besleme",
                    xaxis_title="Tarih",
                    yaxis_title="Miktar (g)",
                    height=300
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        # Rapor indirme
        st.markdown("### 📥 Rapor İndirme")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.button("📄 Aylık Rapor (PDF)", use_container_width=True, disabled=True)
            st.caption("Demo sürümünde kullanılamaz")
        
        with col2:
            st.button("📊 Excel Raporu", use_container_width=True, disabled=True)
            st.caption("Demo sürümünde kullanılamaz")
        
        with col3:
            st.button("🏥 Sağlık Özeti", use_container_width=True, disabled=True)
            st.caption("Demo sürümünde kullanılamaz")
    
    elif st.session_state.current_page == "settings":
        st.markdown("## ⚙️ Ayarlar")
        
        st.markdown("### 🔔 Bildirim Ayarları")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.checkbox("Besleme hatırlatıcıları", value=True)
            st.checkbox("Kilo takibi hatırlatıcıları", value=True)
            st.checkbox("Aşı hatırlatıcıları", value=True)
        
        with col2:
            st.checkbox("Mama azaldı uyarısı", value=True)
            st.checkbox("Anormal besleme uyarısı", value=False)
            st.checkbox("Haftalık özet raporu", value=True)
        
        st.markdown("### 🎨 Görünüm")
        
        theme = st.selectbox("Tema", ["Açık", "Koyu", "Otomatik"])
        language = st.selectbox("Dil", ["Türkçe", "English", "Deutsch"])
        
        st.markdown("### 🔄 Demo Ayarları")
        
        if st.button("🗑️ Demo Verilerini Temizle", type="secondary"):
            st.session_state.feeding_history = []
            st.session_state.weight_history = [{
                "date": datetime.now().date(),
                "weight": st.session_state.dog_weight
            }]
            st.success("Demo verileri temizlendi!")
        
        if st.button("🚪 Çıkış Yap", type="secondary"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <p>🐾 PetFeeder Pro - Demo Sürümü</p>
    <p>Bu demo sürümde tüm özellikler simüle edilmektedir.</p>
    <p>Gerçek sistem için: <strong>info@auxohome.com</strong></p>
</div>
""", unsafe_allow_html=True)

