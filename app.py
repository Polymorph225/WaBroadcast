import streamlit as st
import pywhatkit as kit
import pandas as pd
import time

# Konfigurasi Halaman
st.set_page_config(page_title="WA Blast Streamlit", page_icon="📲")

st.title("📲 WhatsApp Message Blaster")
st.markdown("Kirim pesan massal dengan mudah menggunakan Streamlit.")

# Sidebar untuk Panduan
with st.sidebar:
    st.header("Panduan Penggunaan")
    st.write("1. Pastikan Anda sudah login ke **WhatsApp Web** di browser default.")
    st.write("2. Upload file CSV/Excel dengan kolom **Nomor** (format: 628xxx) dan **Nama**.")
    st.write("3. Tulis pesan Anda (bisa menggunakan variabel {Nama}).")

# 1. Upload File
uploaded_file = st.file_uploader("Upload Database (CSV atau Excel)", type=['csv', 'xlsx'])

if uploaded_file:
    # Membaca Data
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    
    st.write("Preview Data:", df.head())

    # 2. Input Pesan
    message_template = st.text_area("Tulis Pesan Anda", 
                                  placeholder="Halo {Nama}, ada promo menarik untuk Anda!")
    
    # 3. Pengaturan Jeda
    wait_time = st.slider("Jeda antar pesan (detik)", 15, 60, 20)

    if st.button("Mulai Kirim Pesan"):
        if 'Nomor' in df.columns:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for index, row in df.iterrows():
                # Formatter nomor telepon (menghilangkan tanda plus atau spasi)
                phone_no = str(row['Nomor']).replace("+", "").replace(" ", "")
                if not phone_no.startswith('62'):
                    phone_no = "62" + phone_no.lstrip('0')
                
                # Personalisasi pesan
                custom_message = message_template.format(Nama=row.get('Nama', 'Pelanggan'))
                
                try:
                    status_text.text(f"Mengirim ke: {phone_no}...")
                    
                    # Mengirim pesan secara instan (Tab baru akan terbuka)
                    kit.sendwhatmsg_instantly(f"+{phone_no}", custom_message, wait_time, True, 4)
                    
                    st.success(f"Berhasil dikirim ke {phone_no}")
                except Exception as e:
                    st.error(f"Gagal mengirim ke {phone_no}: {str(e)}")
                
                # Update Progress
                progress = (index + 1) / len(df)
                progress_bar.progress(progress)
                
            st.balloons()
            st.success("Selesai! Pastikan semua tab browser yang terbuka sudah ditutup.")
        else:
            st.error("Kolom 'Nomor' tidak ditemukan dalam file!")
