import streamlit as st
import asyncio
import os
import base64
import json
import requests
from io import BytesIO
from PIL import Image
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import uuid

# Demo için session state temizleme
if 'demo_reset' not in st.session_state:
    st.session_state.demo_reset = True
    for key in list(st.session_state.keys()):
        if key.startswith('demo_'):
            del st.session_state[key]

# Sayfa konfigürasyonu
st.set_page_config(
    page_title="🐾 PetFeeder Pro - DEMO",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://petfeeder.demo/help',
        'Report a bug': 'https://petfeeder.demo/bug',
        'About': "# PetFeeder Pro Demo\nKöpek besleyici sistemi satış demosu"
    }
)

# Sales banner ve iletişim bilgileri
st.markdown("""
<div style="background: linear-gradient(90deg, #ff6b6b, #4ecdc4); color: white; padding: 20px; text-align: center; border-radius: 15px; margin-bottom: 30px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
    <h1>🐾 PetFeeder Pro - CANLI DEMO 🐾</h1>
    <h3>Profesyonel Köpek Besleyici Yönetim Sistemi</h3>
    <p style="font-size: 18px; margin: 15px 0;">✨ Bu canlı demo ile sistemin tüm özelliklerini test edebilirsiniz ✨</p>
    <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; margin: 20px 0;">
        <h4>📞 Satış & Bilgi:</h4>
        <p style="font-size: 16px;">
            📧 <strong>Email:</strong> satis@petfeeder.pro | 
            📱 <strong>WhatsApp:</strong> +90 XXX XXX XXXX | 
            🌐 <strong>Web:</strong> www.petfeeder.pro
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# Ana stil dosyası
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #FF4B4B;
        text-align: center;
        margin-bottom: 1rem;
    }
    .pet-card {
        border: 1px solid #ddd;
        border-radius: 15px;
        padding: 15px;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
        margin-bottom: 15px;
        text-align: center;
        height: 400px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    .pet-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 12px 24px rgba(0,0,0,0.15);
    }
    .pet-card img {
        max-width: 100%;
        max-height: 300px;
        width: 300px;
        height: 300px;
        object-fit: cover;
        border-radius: 15px;
        border: 3px solid #fff;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .demo-feature {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin: 15px 0;
        text-align: center;
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
    }
    .sales-cta {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        color: white;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        margin: 20px 0;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    .weight-card {
        border-left: 5px solid #FF4B4B;
        padding: 15px;
        border-radius: 10px;
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        margin-bottom: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
    }
    .demo-notice {
        background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
        color: white;
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        text-align: center;
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
    }
    .contact-form {
        background: linear-gradient(135deg, #00b894 0%, #00a085 100%);
        color: white;
        padding: 25px;
        border-radius: 15px;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# Demo köpek bilgileri
DEMO_DOGS = {
    "bella": {
        "id": 1001,
        "name": "Bella",
        "image": "bella_demo.jpg",
        "default_amount": 25,
        "breed": "Pug",
        "birthdate": "2020-01-15",
        "ideal_weight": {"min": 6.0, "max": 9.0}
    },
    "max": {
        "id": 1002,
        "name": "Max",
        "image": "max_demo.jpg",
        "default_amount": 22,
        "breed": "Pug",
        "birthdate": "2021-03-20",
        "ideal_weight": {"min": 6.0, "max": 9.0}
    },
    "golden": {
        "id": 1003,
        "name": "Golden",
        "image": "golden_demo.jpg",
        "default_amount": 45,
        "breed": "Golden Retriever",
        "birthdate": "2022-05-05",
        "ideal_weight": {"min": 25.0, "max": 34.0}
    }
}

# Demo resim oluşturma
def create_demo_image(image_name, caption=""):
    colors = {
        "bella_demo.jpg": (255, 182, 193),  # Pembe
        "max_demo.jpg": (173, 216, 230),    # Mavi
        "golden_demo.jpg": (255, 215, 0)    # Altın
    }
    
    color = colors.get(image_name, (200, 200, 200))
    image = Image.new('RGB', (300, 300), color=color)
    
    buffered = BytesIO()
    image.save(buffered, format="JPEG", quality=95)
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    return f"""
    <div class="pet-card">
        <img src="data:image/jpeg;base64,{img_str}" alt="{caption}">
        <h3 style="margin-top: 15px; color: #2c3e50;">{caption}</h3>
    </div>
    """

# Demo besleme simülasyonu
async def demo_feed_pet(feeder_id, amount, dog_name):
    await asyncio.sleep(2)
    st.toast(f"✅ {dog_name} başarıyla beslendi! ({amount}g)")
    return True

# Session state başlatma
if 'demo_feeding_history' not in st.session_state:
    st.session_state.demo_feeding_history = []

# Ana uygulama
def main():
    # Ana başlık
    st.markdown('<h1 class="main-header">🎮 CANLI SİSTEM DEMOSU</h1>', unsafe_allow_html=True)
    
    # Feature highlight
    st.markdown("""
    <div class="demo-feature">
        <h2>🚀 Bu Demo ile Neler Yapabilirsiniz?</h2>
        <div style="display: flex; justify-content: space-around; flex-wrap: wrap; margin-top: 20px;">
            <div style="text-align: center; margin: 10px;">
                <h3>🍽️</h3>
                <p>Uzaktan Besleme</p>
            </div>
            <div style="text-align: center; margin: 10px;">
                <h3>📊</h3>
                <p>Kilo Takibi</p>
            </div>
            <div style="text-align: center; margin: 10px;">
                <h3>🤖</h3>
                <p>AI Asistanı</p>
            </div>
            <div style="text-align: center; margin: 10px;">
                <h3>📱</h3>
                <p>Mobil Uyumlu</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Demo köpekler
    st.markdown("## 🐕 Demo Köpeklerimiz")
    cols = st.columns(len(DEMO_DOGS))
    
    for i, (dog_key, dog_info) in enumerate(DEMO_DOGS.items()):
        with cols[i]:
            st.markdown(create_demo_image(dog_info['image'], f"{dog_info['name']} ❤️"), unsafe_allow_html=True)
    
    # Hızlı besleme
    st.markdown("## 🚀 Hızlı Demo Besleme")
    
    quick_cols = st.columns(len(DEMO_DOGS))
    for i, (dog_key, dog_info) in enumerate(DEMO_DOGS.items()):
        with quick_cols[i]:
            if st.button(f"🍽️ {dog_info['name']} Besle\n({dog_info['default_amount']}g)", 
                        key=f"feed_{dog_key}", 
                        type="primary"):
                with st.spinner(f"🎮 {dog_info['name']} besleniyor..."):
                    asyncio.run(demo_feed_pet(dog_info['id'], dog_info['default_amount'], dog_info['name']))
                    
                    # Geçmişe ekle
                    st.session_state.demo_feeding_history.append({
                        "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M"),
                        "dog": dog_info['name'],
                        "amount": dog_info['default_amount'],
                        "type": "Hızlı Besleme"
                    })
                    
                st.success(f"✅ {dog_info['name']} başarıyla beslendi!")
    
    # Toplu besleme
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎯 TÜM KÖPEKLERI AYNI ANDA BESLE", 
                    type="primary", 
                    use_container_width=True):
            with st.spinner("🎮 Tüm köpekler besleniyor..."):
                for dog_key, dog_info in DEMO_DOGS.items():
                    asyncio.run(demo_feed_pet(dog_info['id'], dog_info['default_amount'], dog_info['name']))
                    st.session_state.demo_feeding_history.append({
                        "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M"),
                        "dog": dog_info['name'],
                        "amount": dog_info['default_amount'],
                        "type": "Toplu Besleme"
                    })
                    time.sleep(0.5)
            
            st.success("🎉 Tüm köpekler başarıyla beslendi!")
            st.balloons()
    
    # Besleme geçmişi
    if st.session_state.demo_feeding_history:
        st.markdown("## 📊 Canlı Besleme Geçmişi")
        
        df = pd.DataFrame(st.session_state.demo_feeding_history)
        
        # Son beslemeler
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 🕒 Son Beslemeler")
            for record in st.session_state.demo_feeding_history[-3:]:
                st.info(f"🐕 **{record['dog']}**: {record['amount']}g - {record['timestamp']}")
        
        with col2:
            # Grafik
            if len(df) > 0:
                total_by_dog = df.groupby('dog')['amount'].sum().reset_index()
                fig = px.pie(
                    total_by_dog, 
                    values='amount', 
                    names='dog',
                    title='🥘 Köpeklere Göre Toplam Besleme Dağılımı',
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
    
    # Sistem özellikleri
    st.markdown("---")
    feature_cols = st.columns(4)
    
    features = [
        ("🎯", "Hassas Besleme", "0.1g hassasiyetle porsiyon kontrolü"),
        ("📱", "Mobil Kontrol", "Her yerden telefon ile erişim"),
        ("🤖", "Yapay Zeka", "Akıllı beslenme önerileri"),
        ("📊", "Analitik", "Detaylı beslenme raporları")
    ]
    
    for i, (icon, title, desc) in enumerate(features):
        with feature_cols[i]:
            st.markdown(f"""
            <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); border-radius: 15px; height: 150px; display: flex; flex-direction: column; justify-content: center;">
                <h2>{icon}</h2>
                <h4>{title}</h4>
                <p style="font-size: 12px;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Call to Action
    st.markdown("""
    <div class="sales-cta">
        <h2>🎯 SİSTEMİ SATIN ALMAK İSTİYOR MUSUNUZ?</h2>
        <p style="font-size: 18px;">Bu demoda gördüğünüz tüm özellikler gerçek sistemde daha gelişmiş şekilde bulunmaktadır!</p>
        <h3>💰 Fiyat Bilgisi ve Sipariş için İletişime Geçin</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # İletişim formu
    st.markdown("## 📞 Hemen İletişime Geçin!")
    
    contact_col1, contact_col2 = st.columns(2)
    
    with contact_col1:
        st.markdown("""
        <div class="contact-form">
            <h3>📱 Doğrudan İletişim</h3>
            <p><strong>📧 Email:</strong> satis@petfeeder.pro</p>
            <p><strong>📱 WhatsApp:</strong> +90 XXX XXX XXXX</p>
            <p><strong>☎️ Telefon:</strong> +90 XXX XXX XXXX</p>
            <p><strong>🌐 Website:</strong> www.petfeeder.pro</p>
        </div>
        """, unsafe_allow_html=True)
    
    with contact_col2:
        with st.form("demo_contact_form"):
            st.markdown("### 💌 Hızlı İletişim Formu")
            name = st.text_input("👤 Adınız Soyadınız")
            email = st.text_input("📧 Email Adresiniz")
            phone = st.text_input("📱 Telefon Numaranız")
            message = st.text_area("💭 Mesajınız", 
                                  placeholder="Sistem hakkında detaylı bilgi almak istiyorum...")
            
            if st.form_submit_button("📨 Mesaj Gönder", type="primary"):
                if name and email:
                    st.success("✅ Mesajınız alındı! En kısa sürede size dönüş yapacağız.")
                    st.balloons()
                else:
                    st.error("❌ Lütfen ad ve email alanlarını doldurun.")
    
    # Demo temizleme
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔄 Demo'yu Sıfırla", type="secondary"):
            st.session_state.demo_feeding_history = []
            st.success("🎮 Demo sıfırlandı!")
            st.rerun()
    
    # Footer
    st.markdown("""
    <div style="text-align: center; margin-top: 50px; padding: 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 15px;">
        <h3>🐾 PetFeeder Pro</h3>
        <p>Profesyonel Köpek Besleyici Yönetim Sistemi</p>
        <p style="font-size: 14px; opacity: 0.8;">Bu demo gerçek sistem özelliklerinin sadece bir kısmını göstermektedir.</p>
        <p style="font-size: 12px; opacity: 0.6;">© 2024 PetFeeder Pro. Tüm hakları saklıdır.</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
