import streamlit as st
import pandas as pd
import urllib.parse

# 1. Konfigurasi Halaman
st.set_page_config(page_title="WA Blast Pro", page_icon="🚀")

st.title("🚀 WA Blast - One Click Sender")
st.info("Catatan: Izinkan 'Pop-up' di browser Anda agar fitur kirim sekaligus berfungsi.")

# 2. Upload File
uploaded_file = st.file_uploader("Upload Excel/CSV", type=['csv', 'xlsx'])

if uploaded_file:
    # Membaca file berdasarkan format
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
        
    st.write("Preview Data:")
    st.dataframe(df.head())
    
    # 3. Input Pesan & Delay
    msg_template = st.text_area("Pesan (Gunakan {Nama} untuk personalisasi)", 
                                  "Halo {Nama}, ini pesan otomatis dari sistem.")
    
    delay = st.slider("Jeda antar pesan (detik)", 2, 15, 3)

    # 4. Tombol Eksekusi
    if st.button("🚀 KIRIM KE SEMUA NOMOR"):
        if 'Nomor' in df.columns:
            links = []
            for index, row in df.iterrows():
                nama = row.get('Nama', 'Pelanggan')
                
                # Membersihkan nomor telepon agar hanya angka
                phone = str(row['Nomor']).replace("+", "").replace(" ", "").replace("-", "")
                
                # Pastikan format 62
                if not phone.startswith('62'):
                    if phone.startswith('0'):
                        phone = "62" + phone[1:]
                    else:
                        phone = "62" + phone
                
                # Encode pesan untuk URL
                custom_msg = msg_template.format(Nama=nama)
                encoded_msg = urllib.parse.quote(custom_msg)
                
                # Buat link WhatsApp Web
                wa_link = f"https://web.whatsapp.com/send?phone={phone}&text={encoded_msg}"
                links.append(wa_link)

            # 5. JavaScript untuk membuka tab secara berurutan
            js_code = f"""
            <script>
            const links = {links};
            const delay = {delay * 1000};
            
            links.forEach((link, index) => {{
                setTimeout(() => {{
                    window.open(link, '_blank');
                }}, index * delay);
            }});
            </script>
            """
            # Menjalankan JavaScript di latar belakang
            st.components.v1.html(js_code, height=0)
            st.success(f"Sedang memproses {len(links)} pesan. Mohon cek pop-up di browser Anda.")
        else:
            st.error("Gagal: Kolom bernama 'Nomor' tidak ditemukan di file Anda.")
