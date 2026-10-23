import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(
    page_title="Penetapan Kadar Tiamin - UV-Vis",
    page_icon="🧪",
    layout="wide"
)

st.markdown("""
<style>
.hero {background:linear-gradient(135deg,#0B3C5D,#1D6FA5);color:white;padding:2rem;border-radius:18px;}
.hero h1 {color:white;}
.card {background:#F5F8FB;border-left:6px solid #1D6FA5;padding:1rem;border-radius:12px;}
</style>
""", unsafe_allow_html=True)

st.sidebar.title("🧪 Navigasi")
halaman = st.sidebar.radio(
    "Pilih halaman",
    ["Beranda", "Cara Kerja Instrumen", "Prosedur Pengukuran",
     "Kurva Kalibrasi & Kadar", "Presisi & Akurasi", "Kuis"]
)

# Data dari file Excel kelompok
konsentrasi = [0, 5, 10, 15, 20, 25]
absorbansi_standar = [-0.002, 0.166, 0.325, 0.519, 0.667, 0.896]

absorbansi_sampel = [0.575, 0.567, 0.598, 0.610, 0.574]
massa_sampel = [0.0102, 0.0100, 0.0101, 0.0102, 0.0100]
volume_sampel = 200
kadar_mg_kg = [326348.42, 328349.77, 342461.92, 345759.77, 332309.68]
kadar_mg_tablet = [56.62, 56.97, 59.42, 59.99, 57.66]

# Regresi linear
slope, intercept = np.polyfit(konsentrasi, absorbansi_standar, 1)
y_pred = slope * np.array(konsentrasi) + intercept
r2 = 1 - np.sum((np.array(absorbansi_standar) - y_pred) ** 2) / \
     np.sum((np.array(absorbansi_standar) - np.mean(absorbansi_standar)) ** 2)

if halaman == "Beranda":
    st.markdown("""
    <div class="hero">
    <h1>Penetapan Kadar Tiamin dalam Tablet Vitamin B1 Menggunakan Spektrofotometri UV-Vis</h1>
    <p>Media pembelajaran pengukuran absorbansi, kurva kalibrasi, presisi, dan akurasi.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
    Website ini menjelaskan cara spektrofotometer UV-Vis mengukur absorbansi tiamin,
    penggunaan kurva kalibrasi, serta evaluasi hasil melalui RSD dan persen recovery.
    </div>
    """, unsafe_allow_html=True)

    st.success("Kelompok 2A/2 — Proyek Akhir Analisis Kimia")

elif halaman == "Cara Kerja Instrumen":
    st.title("🔬 Cara Kerja Spektrofotometer UV-Vis")

    st.markdown("""
    1. **Sumber radiasi** menghasilkan cahaya UV dan tampak.  
    2. **Monokromator** memilih panjang gelombang tertentu.  
    3. Cahaya melewati **kuvet** berisi blanko, standar, atau sampel.  
    4. Tiamin menyerap sebagian cahaya.  
    5. **Detektor** mengubah cahaya yang lolos menjadi sinyal listrik.  
    6. **Pengolah sinyal** menghitung dan menampilkan absorbansi.  
    """)

    komponen = ["Sumber", "Monokromator", "Kuvet/Sampel", "Detektor", "Pengolah Sinyal"]
    pilihan = st.selectbox("Pelajari komponen", komponen)

    penjelasan = {
        "Sumber": "Menghasilkan radiasi UV dan cahaya tampak.",
        "Monokromator": "Memilih panjang gelombang yang digunakan untuk pengukuran.",
        "Kuvet/Sampel": "Menampung larutan blanko, standar, atau sampel.",
        "Detektor": "Mengubah cahaya yang lolos sampel menjadi sinyal listrik.",
        "Pengolah Sinyal": "Menghitung absorbansi dari intensitas cahaya sebelum dan sesudah sampel."
    }

    st.markdown(f"""
    <div class="card">
    <b>{pilihan}</b><br>{penjelasan[pilihan]}
    </div>
    """, unsafe_allow_html=True)

    st.latex(r"A = -\log\left(\frac{I}{I_0}\right)")

    st.info("Semakin besar konsentrasi tiamin, semakin besar absorbansi yang terbaca.")

elif halaman == "Prosedur Pengukuran":
    st.title("🧪 Prosedur Pengukuran UV-Vis")

    langkah = [
        "Siapkan blanko, larutan standar, dan larutan sampel.",
        "Nyalakan spektrofotometer UV-Vis dan biarkan stabil.",
        "Pilih panjang gelombang pengukuran sesuai metode.",
        "Masukkan blanko dan lakukan kalibrasi nol.",
        "Ukur absorbansi larutan standar dari konsentrasi terendah ke tertinggi.",
        "Ukur absorbansi larutan sampel.",
        "Catat seluruh nilai absorbansi.",
        "Bersihkan kuvet dan matikan instrumen sesuai SOP."
    ]

    if "idx" not in st.session_state:
        st.session_state.idx = 0

    st.progress((st.session_state.idx + 1) / len(langkah))
    st.subheader(f"Langkah {st.session_state.idx + 1} dari {len(langkah)}")
    st.markdown(f'<div class="card">{langkah[st.session_state.idx]}</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    if col1.button("⬅️ Sebelumnya"):
        st.session_state.idx = max(0, st.session_state.idx - 1)

    if col2.button("Berikutnya ➡️"):
        st.session_state.idx = min(len(langkah) - 1, st.session_state.idx + 1)

    if col3.button("🔄 Reset"):
        st.session_state.idx = 0

elif halaman == "Kurva Kalibrasi & Kadar":
    st.title("📈 Kurva Kalibrasi dan Kadar Tiamin")

    df = pd.DataFrame({
        "Konsentrasi (mg/L)": konsentrasi,
        "Absorbansi": absorbansi_standar
    })

    st.dataframe(df, use_container_width=True)

    st.success(
        f"Persamaan kurva kalibrasi: A = {slope:.5f}C + {intercept:.5f}  |  R² = {r2:.5f}"
    )

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=konsentrasi, y=absorbansi_standar,
        mode="markers", name="Data standar"
    ))

    x_line = np.linspace(0, 25, 100)
    y_line = slope * x_line + intercept

    fig.add_trace(go.Scatter(
        x=x_line, y=y_line,
        mode="lines", name="Garis regresi"
    ))

    fig.update_layout(
        title="Kurva Kalibrasi Tiamin",
        xaxis_title="Konsentrasi (mg/L)",
        yaxis_title="Absorbansi",
        height=450
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Kalkulator Kadar Sampel")

    col1, col2, col3 = st.columns(3)

    A = col1.number_input("Absorbansi sampel", value=0.5848, format="%.4f")
    V = col2.number_input("Volume sampel (mL)", value=200.0)
    W = col3.number_input("Massa sampel (g)", value=0.0101, format="%.5f")

    if st.button("Hitung Kadar"):
        C = (A - intercept) / slope
        kadar = C * (V / 1000) / W

        col1, col2 = st.columns(2)
        col1.metric("Konsentrasi terukur", f"{C:.3f} mg/L")
        col2.metric("Kadar tiamin", f"{kadar:,.0f} mg/kg")

elif halaman == "Presisi & Akurasi":
    st.title("🎯 Presisi dan Akurasi")

    st.subheader("Presisi")

    rerata = np.mean(kadar_mg_kg)
    sd = np.std(kadar_mg_kg, ddof=1)
    rsd = sd / rerata * 100

    col1, col2, col3 = st.columns(3)
    col1.metric("Rata-rata kadar", f"{rerata:,.0f} mg/kg")
    col2.metric("Simpangan baku", f"{sd:,.0f} mg/kg")
    col3.metric("RSD", f"{rsd:.3f} %")

    st.success("RSD 2,575% menunjukkan variasi antarulangan relatif kecil, sehingga presisi tergolong baik.")

    st.subheader("Akurasi / Recovery")

    C1 = 335045.91
    C2 = 99009.90
    C3 = 435998.83

    recovery = (C3 - C1) / C2 * 100

    st.metric("Persen recovery", f"{recovery:.2f} %")

    st.latex(r"\%R = \frac{C_3 - C_1}{C_2} \times 100\%")

    st.info("Recovery 101,96% menunjukkan hasil akurasi mendekati 100%.")

elif halaman == "Kuis":
    st.title("🧠 Kuis Interaktif")

    soal = [
        ("Fungsi blanko adalah...", 
         ["Menambah absorbansi", "Menyetel nol instrumen", "Membuat standar", "Menghitung recovery"], 1),
        
        ("Komponen yang memilih panjang gelombang adalah...", 
         ["Detektor", "Monokromator", "Kuvet", "Neraca analitik"], 1),
        
        ("Absorbansi sebanding dengan...", 
         ["Konsentrasi analit", "Volume labu takar", "Suhu ruangan", "Berat kuvet"], 0),
        
        ("RSD digunakan untuk menilai...", 
         ["Presisi", "Akurasi", "Linearitas", "Stabilitas"], 0),
        
        ("Persen recovery digunakan untuk menilai...", 
         ["Presisi", "Akurasi", "Kadar pelarut", "Berat tablet"], 1)
    ]

    if "jawaban" not in st.session_state:
        st.session_state.jawaban = {}

    for i, (soal_text, opsi, kunci) in enumerate(soal):
        st.markdown(f"**{i+1}. {soal_text}**")
        jawab = st.radio("", opsi, key=f"soal{i}", index=None, label_visibility="collapsed")

        if jawab is not None:
            st.session_state.jawaban[i] = opsi.index(jawab)

    if st.button("Periksa Skor"):
        benar = sum(st.session_state.jawaban.get(i, -1) == kunci for i, (_, _, kunci) in enumerate(soal))
        st.success(f"Skor Anda: {benar} dari {len(soal)}")

        for i, (_, opsi, kunci) in enumerate(soal):
            st.write(f"**{i+1}. Jawaban benar:** {opsi[kunci]}")

    if st.button("🔄 Ulangi Kuis"):
        st.session_state.jawaban = {}
        st.rerun()
