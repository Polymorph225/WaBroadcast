import streamlit as st
import pandas as pd
import urllib.parse
import time

st.set_page_config(page_title="WA Blast Pro", page_icon="🚀")

st.title("🚀 WA Blast - One Click Sender")
st.info("Catatan: Izinkan 'Pop-up' di browser Anda agar fitur kirim sekaligus berfungsi.")

uploaded_file = st.file_uploader("Upload Excel/CSV", type=['csv', 'xlsx'])

if uploaded_file:
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    st.dataframe(df.head())
    
    msg_template = st.text_area("Pesan (Gunakan {Nama} untuk personalisasi)", "Halo {Nama}, ini pesan dari sistem.")
    delay = st.slider("Jeda antar pesan (detik)", 2, 10, 3)

    if st.button("🚀 KIRIM KE SEMUA NOMOR"):
        if 'Nomor' in df.columns:
            links = []
            for _, row in df.iterrows():
                nama = row.get('Nama', 'Pelanggan')
                # Bersihkan nomor (harus awali 62)
                phone = str(row['Nomor']).replace("+", "").replace(" ", "").replace("-", "")
                if not phone.startswith('62'):
                    phone = "62" + phone.lstrip('0')
                
                custom_msg = msg_template.format(Nama=nama)
                encoded_msg = urllib.parse.quote(custom_msg)
                links.append(f"https://web.whatsapp.com/send?phone={phone}&text={encoded_msg}")

            # JavaScript untuk membuka tab satu per satu
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
            st.components.v1.html(js_code, height=0)
            st.success(f"Sedang memproses {len(links)} pesan. Mohon tunggu...")
        else:
            st.error("Kolom 'Nomor' tidak ditemukan!")

---

### Hal Penting Agar Berhasil:

1.  **Izin Pop-up:** Saat Anda menekan tombol, browser (Chrome/Edge) biasanya akan memunculkan ikon kecil di baris alamat (kanan atas) yang bertuliskan *"Pop-up blocked"*. Anda **WAJIB** klik ikon tersebut dan pilih **"Always allow pop-ups from..."**.
2.  **WhatsApp Web:** Pastikan Anda sudah login ke WhatsApp Web di browser yang sama.
3.  **Jeda Waktu (Delay):** Jangan gunakan delay terlalu cepat (di bawah 2 detik). WhatsApp bisa mendeteksi aktivitas bot jika ratusan tab terbuka sekaligus dalam waktu singkat.
4.  **Limitasi Browser:** Jika daftar nomor Anda sangat banyak (misal > 50), browser mungkin akan menjadi berat karena membuka banyak tab. Disarankan mengirim dalam kelompok kecil (per 20 nomor).

Metode ini adalah cara paling stabil untuk menjalankan fitur "Blast" di **Streamlit Cloud** tanpa perlu library tambahan yang berat.
