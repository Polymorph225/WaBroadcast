import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="WA Sender", page_icon="📲")

st.title("📲 WhatsApp Link Generator")

uploaded_file = st.file_uploader("Upload Excel/CSV (Kolom: Nomor, Nama)", type=['csv', 'xlsx'])

if uploaded_file:
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    
    st.write("Preview Data:", df.head())
    
    msg_template = st.text_area("Pesan", "Halo {Nama}, ini adalah pesan otomatis.")
    
    if st.button("Generate Link Kirim"):
        if 'Nomor' in df.columns:
            for index, row in df.iterrows():
                nama = row.get('Nama', 'Pelanggan')
                # Bersihkan nomor
                phone = str(row['Nomor']).replace("+", "").replace(" ", "").replace("-", "")
                if not phone.startswith('62'):
                    phone = "62" + phone.lstrip('0')
                
                # Encode pesan agar aman untuk URL
                custom_msg = msg_template.format(Nama=nama)
                encoded_msg = urllib.parse.quote(custom_msg)
                
                # Buat link wa.me
                wa_link = f"https://wa.me/{phone}?text={encoded_msg}"
                
                col1, col2 = st.columns([3, 1])
                col1.write(f"Kirim ke {nama} ({phone})")
                col2.markdown(f"[Klik Kirim]({wa_link})", unsafe_allow_html=True)
        else:
            st.error("Kolom 'Nomor' tidak ditemukan!")
