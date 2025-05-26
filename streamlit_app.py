import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import asyncio

# Sayfa konfigürasyonu
st.set_page_config(
    page_title="PetKit Akıllı Besleyici Kontrol Sistemi",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.5rem;
        color: #1f2937;
    }
    
    .device-card {
        background: white;
        border: 2px solid #e5e7eb;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    .device-online {
        border-color: #10b981;
        background: #f0fdf4;
    }
    
    .feed-button {
        background: #10b981;
        color: white;
        padding: 12px 24px;
        border-radius: 8px;
        border: none;
        font-weight: 600;
        cursor: pointer;
        width: 100%;
        transition: all 0.2s;
    }
    
    .feed-button:hover {
        background: #059669;
        transform: translateY(-2px);
    }
    
    .status-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 8px;
    }
    
    .status-online {
        background: #10b981;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    .metric-card {
        background: #f9fafb;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        border: 1px solid #e5e7eb;
    }
    
    .weather-card {
        background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        margin: 20px 0;
    }
    
    .ai-chat {
        background: #f3f4f6;
        padding: 20px;
        border-radius: 12px;
        margin: 10px 0;
    }
    
    .feeding-log {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
    }
    
    .demo-banner {
        background: #fef3c7;
        border: 1px solid #f59e0b;
        color: #92400e;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Session state
if 'user_data' not in st.session_state:
    st.session_state.user_data = None

if 'demo_stage' not in st.session_state:
    st.session_state.demo_stage = 'welcome'

if 'feeding_logs' not in st.session_state:
    st.session_state.feeding_logs = []

if 'devices' not in st.session_state:
    st.session_state.devices = {}

# Helper functions
def simulate_feeding(device_id, amount):
    """PetKit cihazına besleme komutu gönderme simülasyonu"""
    # Gerçek sistemde: await client.control_feeder(device_id, amount)
    return {
        "success": True,
        "device_id": device_id,
        "amount": amount,
        "timestamp": datetime.now()
    }

def get_weather_alerts():
    """AccuWeather API simülasyonu"""
    weather = random.choice(["Güneşli", "Bulutlu", "Yağmurlu", "Fırtınalı"])
    temp = random.randint(10, 35)
    
    alerts = []
    if weather in ["Yağmurlu", "Fırtınalı"]:
        alerts.append("⚠️ Yağışlı hava: Köpeklerin pati temizliği önemli!")
    if temp > 30:
        alerts.append("🌡️ Sıcak hava: Su tüketimini artırın!")
    elif temp < 5:
        alerts.append("❄️ Soğuk hava: Mama miktarını %10 artırabilirsiniz")
    
    return {
        "condition": weather,
        "temperature": temp,
        "alerts": alerts
    }

def calculate_costs(devices):
    """Maliyet hesaplama"""
    total_daily = sum(device['daily_amount'] for device in devices.values())
    total_monthly = total_daily * 30
    
    # Ortalama mama fiyatı 450 TL/kg
    monthly_cost = (total_monthly / 1000) * 450
    
    return {
        "daily_grams": total_daily,
        "monthly_kg": total_monthly / 1000,
        "monthly_cost": monthly_cost,
        "yearly_cost": monthly_cost * 12
    }

# Welcome Screen
if st.session_state.demo_stage == 'welcome':
    st.markdown('<h1 class="main-header">🐾 PetKit Akıllı Besleyici Kontrol Sistemi</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="demo-banner">
        <h3>📱 DEMO MODU - Gerçek Sistem Simülasyonu</h3>
        <p>Bu demo, PetKit cihazlarınızı uzaktan kontrol eden gerçek sistemin bir gösterimidir</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sistem özellikleri
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="device-card">
            <h3>🔌 PetKit Entegrasyonu</h3>
            <p>• Gerçek PetKit cihazlarınızı kontrol edin</p>
            <p>• Çoklu cihaz desteği</p>
            <p>• Anlık durum takibi</p>
            <p>• Otomatik besleme programları</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="device-card">
            <h3>🤖 Claude AI Desteği</h3>
            <p>• "Köpekleri besle" komutunu anlama</p>
            <p>• Özel besleme önerileri</p>
            <p>• Sağlık tavsiyeleri</p>
            <p>• Doğal dil işleme</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="device-card">
            <h3>🌦️ Akıllı Özellikler</h3>
            <p>• Hava durumu entegrasyonu</p>
            <p>• Besleme geçmişi takibi</p>
            <p>• Maliyet analizi</p>
            <p>• Sağlık raporları</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Kullanıcı bilgileri formu
    st.markdown("### 🚀 Demo'yu Başlatmak İçin Bilgilerinizi Girin")
    
    with st.form("demo_setup"):
        col1, col2 = st.columns(2)
        
        with col1:
            user_name = st.text_input("👤 Adınız", placeholder="Örn: Ahmet")
            petkit_email = st.text_input("📧 PetKit Email (Demo)", value="demo@petkit.com", disabled=True)
        
        with col2:
            dog_count = st.number_input("🐕 Köpek Sayısı", min_value=1, max_value=4, value=2)
            location = st.text_input("📍 Konum", placeholder="İstanbul")
        
        st.markdown("#### 🐾 Köpek Bilgileri")
        
        dogs = []
        for i in range(int(dog_count)):
            st.markdown(f"**Köpek {i+1}**")
            col1, col2, col3 = st.columns(3)
            with col1:
                name = st.text_input(f"İsim", key=f"dog_name_{i}", placeholder=f"Örn: {'Max' if i==0 else 'Luna'}")
            with col2:
                breed = st.selectbox(f"Cins", key=f"dog_breed_{i}", 
                                   options=["Pug", "Golden Retriever", "Beagle", "Bulldog", "Husky", "Diğer"])
            with col3:
                weight = st.number_input(f"Kilo (kg)", key=f"dog_weight_{i}", min_value=1.0, max_value=80.0, value=15.0 if i==0 else 8.0)
            
            dogs.append({"name": name, "breed": breed, "weight": weight})
        
        submit = st.form_submit_button("✨ Sistemi Başlat", use_container_width=True)
        
        if submit and user_name and all(dog['name'] for dog in dogs):
            # Cihazları oluştur
            devices = {}
            for i, dog in enumerate(dogs):
                device_id = f"D22{random.randint(100000, 999999)}"
                devices[device_id] = {
                    "name": f"{dog['name']} Besleyici",
                    "dog": dog['name'],
                    "breed": dog['breed'],
                    "weight": dog['weight'],
                    "daily_amount": int(dog['weight'] * 30),  # Basit hesaplama
                    "online": True,
                    "battery": random.randint(70, 100),
                    "food_level": random.randint(40, 90)
                }
            
            st.session_state.user_data = {
                "name": user_name,
                "location": location,
                "dogs": dogs
            }
            st.session_state.devices = devices
            st.session_state.demo_stage = 'dashboard'
            st.rerun()

# Dashboard
elif st.session_state.demo_stage == 'dashboard':
    user = st.session_state.user_data
    devices = st.session_state.devices
    
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f'<h1 class="main-header">Hoş geldiniz, {user["name"]}! 👋</h1>', unsafe_allow_html=True)
    with col2:
        if st.button("🔄 Yeni Demo"):
            st.session_state.demo_stage = 'welcome'
            st.session_state.user_data = None
            st.rerun()
    
    # Ana sekmeler
    tabs = st.tabs(["🏠 Kontrol Paneli", "🤖 AI Asistan", "📊 Raporlar", "⚙️ Ayarlar"])
    
    # Kontrol Paneli
    with tabs[0]:
        # Hava durumu
        weather = get_weather_alerts()
        if weather['alerts']:
            st.markdown(f"""
            <div class="weather-card">
                <h3>🌡️ {weather['temperature']}°C - {weather['condition']}</h3>
                {"<br>".join(weather['alerts'])}
            </div>
            """, unsafe_allow_html=True)
        
        # Cihazlar
        st.markdown("### 🔌 PetKit Cihazlarınız")
        
        device_cols = st.columns(len(devices))
        
        for idx, (device_id, device) in enumerate(devices.items()):
            with device_cols[idx]:
                status_class = "device-online" if device['online'] else ""
                st.markdown(f"""
                <div class="device-card {status_class}">
                    <span class="status-indicator status-online"></span>
                    <strong>{device['name']}</strong>
                    <p style="color: #6b7280; margin: 5px 0;">ID: {device_id}</p>
                    <hr style="margin: 10px 0;">
                    <p>🐕 {device['dog']} ({device['breed']})</p>
                    <p>⚖️ {device['weight']} kg</p>
                    <p>🍖 Günlük: {device['daily_amount']}g</p>
                    <p>🔋 Pil: %{device['battery']}</p>
                    <p>🥫 Mama: %{device['food_level']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Besleme butonları
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"Sabah ({device['daily_amount']*0.6:.0f}g)", key=f"morning_{device_id}"):
                        result = simulate_feeding(device_id, device['daily_amount']*0.6)
                        st.success(f"✅ {device['dog']} beslendi!")
                        st.session_state.feeding_logs.append({
                            "time": datetime.now(),
                            "dog": device['dog'],
                            "amount": device['daily_amount']*0.6,
                            "type": "Sabah"
                        })
                
                with col2:
                    if st.button(f"Akşam ({device['daily_amount']*0.4:.0f}g)", key=f"evening_{device_id}"):
                        result = simulate_feeding(device_id, device['daily_amount']*0.4)
                        st.success(f"✅ {device['dog']} beslendi!")
                        st.session_state.feeding_logs.append({
                            "time": datetime.now(),
                            "dog": device['dog'],
                            "amount": device['daily_amount']*0.4,
                            "type": "Akşam"
                        })
        
        # Toplu besleme
        st.markdown("### 🍖 Hızlı İşlemler")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🐕 Tüm Köpekleri Besle", use_container_width=True):
                with st.spinner("Cihazlara komut gönderiliyor..."):
                    for device_id, device in devices.items():
                        simulate_feeding(device_id, device['daily_amount']//2)
                        st.session_state.feeding_logs.append({
                            "time": datetime.now(),
                            "dog": device['dog'],
                            "amount": device['daily_amount']//2,
                            "type": "Manuel"
                        })
                    st.success("✅ Tüm köpekler beslendi!")
                    st.balloons()
        
        with col2:
            if st.button("📊 Günlük Rapor", use_container_width=True):
                st.info("📈 Rapor hazırlanıyor...")
        
        with col3:
            if st.button("🔄 Cihaz Durumunu Yenile", use_container_width=True):
                st.success("✅ Cihaz durumları güncellendi!")
        
        # Son beslemeler
        if st.session_state.feeding_logs:
            st.markdown("### 📜 Son Beslemeler")
            for log in st.session_state.feeding_logs[-5:]:
                st.markdown(f"""
                <div class="feeding-log">
                    🕐 {log['time'].strftime('%H:%M')} - 
                    🐕 {log['dog']} - 
                    🍖 {log['amount']:.0f}g - 
                    📍 {log['type']}
                </div>
                """, unsafe_allow_html=True)
    
    # AI Asistan
    with tabs[1]:
        st.markdown("### 🤖 Claude AI Asistanı")
        
        # Örnek komutlar
        st.markdown("#### 💡 Örnek Komutlar")
        example_commands = [
            "Köpekleri besle",
            "Max'i besle",
            "Sabah besleme zamanı",
            "Bugün kaç gram mama verildi?",
            "Hava durumuna göre besleme önerisi"
        ]
        
        cols = st.columns(3)
        for i, cmd in enumerate(example_commands):
            with cols[i % 3]:
                if st.button(cmd, key=f"ex_cmd_{i}"):
                    st.session_state.ai_command = cmd
        
        # AI chat
        user_input = st.text_area("Claude'a komut verin veya soru sorun...", 
                                 value=st.session_state.get('ai_command', ''),
                                 height=100)
        
        if st.button("🤖 Gönder", use_container_width=True) and user_input:
            with st.spinner("Claude yanıt hazırlıyor..."):
                # Besleme komutlarını kontrol et
                if any(word in user_input.lower() for word in ["besle", "mama ver", "yemek"]):
                    st.markdown("""
                    <div class="ai-chat">
                        <strong>🤖 Claude:</strong><br>
                        Besleme komutunu algıladım. İşlemi gerçekleştiriyorum...<br><br>
                        <strong>&lt;BESLEME_KOMUTU&gt;</strong>Tüm köpekler besleniyor<strong>&lt;/BESLEME_KOMUTU&gt;</strong><br><br>
                        ✅ Besleme komutları PetKit cihazlarına gönderildi!
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Otomatik besleme
                    for device_id, device in devices.items():
                        simulate_feeding(device_id, device['daily_amount']//2)
                    st.success("✅ Tüm köpekler Claude tarafından beslendi!")
                    
                else:
                    # Diğer yanıtlar
                    st.markdown(f"""
                    <div class="ai-chat">
                        <strong>🤖 Claude:</strong><br>
                        Sorunuzu analiz ediyorum: "{user_input}"<br><br>
                        Sisteminizdeki {len(devices)} adet PetKit cihazı aktif durumda. 
                        İstediğiniz zaman "köpekleri besle" komutu ile tüm cihazları aktive edebilirim.
                    </div>
                    """, unsafe_allow_html=True)
    
    # Raporlar
    with tabs[2]:
        st.markdown("### 📊 Sistem Raporları")
        
        # Maliyet analizi
        costs = calculate_costs(devices)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>{costs['daily_grams']}g</h3>
                <p>Günlük Tüketim</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3>{costs['monthly_kg']:.1f} kg</h3>
                <p>Aylık Tüketim</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h3>{costs['monthly_cost']:,.0f}₺</h3>
                <p>Aylık Maliyet</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <h3>{costs['yearly_cost']:,.0f}₺</h3>
                <p>Yıllık Maliyet</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Besleme grafiği
        if st.session_state.feeding_logs:
            df = pd.DataFrame(st.session_state.feeding_logs)
            
            fig = px.bar(df.groupby('dog')['amount'].sum().reset_index(),
                        x='dog', y='amount',
                        title='Köpeklere Göre Toplam Besleme',
                        labels={'amount': 'Miktar (g)', 'dog': 'Köpek'})
            
            st.plotly_chart(fig, use_container_width=True)
    
    # Ayarlar
    with tabs[3]:
        st.markdown("### ⚙️ Sistem Ayarları")
        
        st.markdown("#### 🕐 Otomatik Besleme Zamanları")
        col1, col2 = st.columns(2)
        with col1:
            morning_time = st.time_input("Sabah Besleme", datetime.strptime("07:00", "%H:%M").time())
        with col2:
            evening_time = st.time_input("Akşam Besleme", datetime.strptime("18:00", "%H:%M").time())
        
        st.markdown("#### 📱 Bildirimler")
        notifications = st.multiselect(
            "Bildirim Tercihleri",
            ["Besleme tamamlandı", "Mama azaldı", "Pil zayıf", "Cihaz çevrimdışı"],
            default=["Besleme tamamlandı", "Mama azaldı"]
        )
        
        st.markdown("#### 🌡️ Hava Durumu Ayarları")
        weather_alerts = st.checkbox("Hava durumu uyarılarını göster", value=True)
        
        if st.button("💾 Ayarları Kaydet", use_container_width=True):
            st.success("✅ Ayarlar kaydedildi!")

# Footer
st.markdown("""
<hr style="margin: 60px 0 20px 0;">
<div style="text-align: center; color: #6b7280; padding: 20px;">
    <p>🐾 PetKit Akıllı Besleyici Kontrol Sistemi - Demo</p>
    <p>Gerçek sistem PetKit API ile entegre çalışır</p>
</div>
""", unsafe_allow_html=True)
