import streamlit as st
from datetime import datetime, timedelta, date
import calendar

# Sayfa ayarları
st.set_page_config(
    page_title="Ekip Vardiya Hesaplama",
    page_icon="👥",
    layout="centered"
)

# CSS stilleri
st.markdown("""
<style>
    .main { max-width: 700px; margin: 0 auto; }
    .stApp { background-color: #0f152b; }
    
    /* Başlık */
    .baslik {
        text-align: center;
        color: #ffffff;
        font-size: 28px;
        font-weight: bold;
        padding: 20px 0 10px 0;
    }
    
    /* Takvim grid */
    .takvim-grid {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 4px;
        padding: 10px;
    }
    
    /* Gün başlıkları */
    .gun-baslik {
        text-align: center;
        color: #9ca3af;
        font-weight: bold;
        font-size: 13px;
        padding: 8px 0;
    }
    
    /* Gün hücreleri */
    .gun-hucresi {
        text-align: center;
        padding: 10px 4px;
        border-radius: 10px;
        font-size: 14px;
        font-weight: bold;
        min-height: 45px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        line-height: 1.2;
    }
    
    .gun-no {
        font-size: 16px;
        font-weight: bold;
    }
    
    .gun-durum {
        font-size: 9px;
        margin-top: 2px;
        opacity: 0.9;
    }
    
    /* Renkler */
    .calisma1 {
        background-color: #4a7c59;
        color: white;
    }
    .calisma2 {
        background-color: #2d5a3a;
        color: white;
    }
    .izin {
        background-color: #c14953;
        color: white;
    }
    .bos {
        background-color: transparent;
    }
    .ayarsiz {
        background-color: #1e293b;
        color: #64748b;
    }
    
    /* Bugün vurgusu */
    .bugun {
        border: 3px solid #2196F3;
        box-shadow: 0 0 10px rgba(33, 150, 243, 0.4);
    }
    
    /* Bilgi kutuları */
    .bilgi-kutusu {
        display: inline-block;
        padding: 6px 14px;
        border-radius: 8px;
        margin: 3px;
        font-size: 13px;
        font-weight: bold;
        color: white;
    }
    
    /* Lejant */
    .lejant {
        display: flex;
        justify-content: center;
        gap: 10px;
        flex-wrap: wrap;
        padding: 10px 0;
    }
    
    /* Ay navigasyon */
    .ay-nav {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 20px;
        padding: 10px 0;
    }
    
    .ay-baslik {
        font-size: 20px;
        font-weight: bold;
        color: #ffffff;
        min-width: 200px;
        text-align: center;
    }
    
    /* Sonuç kutusu */
    .sonuc-kutusu {
        text-align: center;
        padding: 15px;
        border-radius: 12px;
        margin: 10px 0;
        font-size: 18px;
        font-weight: bold;
    }
    
    .sonuc-calisma1 {
        background-color: #4a7c59;
        color: white;
        border: 2px solid #5a9c6a;
    }
    .sonuc-calisma2 {
        background-color: #2d5a3a;
        color: white;
        border: 2px solid #3d7a4a;
    }
    .sonuc-izin {
        background-color: #c14953;
        color: white;
        border: 2px solid #d15963;
    }
    
    /* Selectbox ve date_input koyu tema */
    .stSelectbox > div > div,
    .stDateInput > div > div {
        background-color: #1e293b;
        color: white;
    }
    
    /* Divider */
    hr { border-color: #1e293b; }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Türkçe ay isimleri
AY_ISIMLERI = [
    "Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
    "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"
]

GUN_ISIMLERI = ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"]


def gun_durumu_hesapla(tarih, baslangic_tarihi, vardiya_offset):
    """Belirli bir tarihin çalışma/izin durumunu hesaplar"""
    fark = (tarih - baslangic_tarihi).days
    pozisyon = (fark + vardiya_offset) % 3

    if pozisyon == 0:
        return "1. Gün", "calisma1", "✅"
    elif pozisyon == 1:
        return "2. Gün", "calisma2", "✅"
    else:
        return "İzin", "izin", "🔴"


def takvim_html_olustur(yil, ay, baslangic_tarihi, vardiya_offset, ayar_yapildi):
    """Takvim HTML'i oluşturur"""
    bugun = date.today()
    ilk_gun_hafta = date(yil, ay, 1).weekday()
    son_gun = calendar.monthrange(yil, ay)[1]

    html = '<div class="takvim-grid">'

    # Gün başlıkları
    for gun in GUN_ISIMLERI:
        html += f'<div class="gun-baslik">{gun}</div>'

    # Boş hücreler
    for _ in range(ilk_gun_hafta):
        html += '<div class="gun-hucresi bos"></div>'

    # Günler
    for gun_no in range(1, son_gun + 1):
        gun_tarihi = date(yil, ay, gun_no)
        is_bugun = gun_tarihi == bugun
        bugun_class = " bugun" if is_bugun else ""

        if ayar_yapildi:
            durum, renk_class, emoji = gun_durumu_hesapla(
                gun_tarihi, baslangic_tarihi, vardiya_offset
            )
            html += f'''
            <div class="gun-hucresi {renk_class}{bugun_class}">
                <span class="gun-no">{gun_no}</span>
                <span class="gun-durum">{durum}</span>
            </div>'''
        else:
            html += f'''
            <div class="gun-hucresi ayarsiz{bugun_class}">
                <span class="gun-no">{gun_no}</span>
            </div>'''

    html += '</div>'
    return html


# ==========================================
# ANA UYGULAMA
# ==========================================

st.markdown('<div class="baslik">👥 Ekip Vardiya Hesaplama</div>', unsafe_allow_html=True)
st.markdown("---")

# Session state başlat
if "gorunen_ay" not in st.session_state:
    st.session_state.gorunen_ay = datetime.now().month
if "gorunen_yil" not in st.session_state:
    st.session_state.gorunen_yil = datetime.now().year

# Tarih ve Vardiya seçimi
col1, col2 = st.columns(2)

with col1:
    st.markdown("**📅 Başlangıç Tarihi**")
    baslangic = st.date_input(
        "Tarih seçin",
        value=date.today(),
        format="DD.MM.YYYY",
        label_visibility="collapsed"
    )

with col2:
    st.markdown("**🔄 Bugün Kaçıncı Gününüz?**")
    vardiya_secim = st.selectbox(
        "Vardiya günü",
        options=["Seçiniz", "1. Gün (Çalışma)", "2. Gün (Çalışma)"],
        label_visibility="collapsed"
    )

# Hesaplama yapılabilir mi?
ayar_yapildi = vardiya_secim != "Seçiniz"
vardiya_offset = 0

if ayar_yapildi:
    vardiya_offset = 0 if "1. Gün" in vardiya_secim else 1

    # Bugünün durumunu göster
    bugun_durum, bugun_class, bugun_emoji = gun_durumu_hesapla(
        date.today(), baslangic, vardiya_offset
    )
    st.markdown(
        f'<div class="sonuc-kutusu sonuc-{bugun_class}">'
        f'{bugun_emoji} Bugün: {bugun_durum}'
        f'</div>',
        unsafe_allow_html=True
    )
else:
    st.info("⬆️ Lütfen başlangıç tarihi ve vardiya gününüzü seçin")

st.markdown("---")

# Lejant
st.markdown("""
<div class="lejant">
    <span class="bilgi-kutusu calisma1">✅ 1. Gün</span>
    <span class="bilgi-kutusu calisma2">✅ 2. Gün</span>
    <span class="bilgi-kutusu izin">🔴 İzin</span>
</div>
""", unsafe_allow_html=True)

# Ay navigasyonu
nav_col1, nav_col2, nav_col3 = st.columns([1, 3, 1])

with nav_col1:
    if st.button("◀ Önceki", use_container_width=True):
        if st.session_state.gorunen_ay == 1:
            st.session_state.gorunen_ay = 12
            st.session_state.gorunen_yil -= 1
        else:
            st.session_state.gorunen_ay -= 1
        st.rerun()

with nav_col2:
    ay_adi = AY_ISIMLERI[st.session_state.gorunen_ay - 1]
    st.markdown(
        f'<div class="ay-baslik">{ay_adi} {st.session_state.gorunen_yil}</div>',
        unsafe_allow_html=True
    )

with nav_col3:
    if st.button("Sonraki ▶", use_container_width=True):
        if st.session_state.gorunen_ay == 12:
            st.session_state.gorunen_ay = 1
            st.session_state.gorunen_yil += 1
        else:
            st.session_state.gorunen_ay += 1
        st.rerun()

# Takvim
takvim_html = takvim_html_olustur(
    st.session_state.gorunen_yil,
    st.session_state.gorunen_ay,
    baslangic,
    vardiya_offset,
    ayar_yapildi
)
st.markdown(takvim_html, unsafe_allow_html=True)

# Seçilen güne tıklama (gün seçici)
if ayar_yapildi:
    st.markdown("---")
    st.markdown("**🔍 Belirli Bir Günü Kontrol Et**")

    son_gun = calendar.monthrange(
        st.session_state.gorunen_yil,
        st.session_state.gorunen_ay
    )[1]

    secilen_gun = st.slider(
        "Gün seçin",
        min_value=1,
        max_value=son_gun,
        value=min(datetime.now().day, son_gun),
        label_visibility="collapsed"
    )

    secilen_tarih = date(
        st.session_state.gorunen_yil,
        st.session_state.gorunen_ay,
        secilen_gun
    )

    durum, renk_class, emoji = gun_durumu_hesapla(
        secilen_tarih, baslangic, vardiya_offset
    )

    gun_adi_tr = GUN_ISIMLERI[secilen_tarih.weekday()]
    tarih_str = secilen_tarih.strftime("%d.%m.%Y")

    st.markdown(
        f'<div class="sonuc-kutusu sonuc-{renk_class}">'
        f'{emoji} {tarih_str} {gun_adi_tr} → {durum}'
        f'</div>',
        unsafe_allow_html=True
    )

# Footer
st.markdown("---")
st.markdown(
    '<div style="text-align:center; color:#64748b; font-size:12px;">'
    '2+1 Vardiya Sistemi | 2 Gün Çalışma + 1 Gün İzin'
    '</div>',
    unsafe_allow_html=True
)
