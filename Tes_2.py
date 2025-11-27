import streamlit as st
import numpy as np
from scipy.stats import norm.cdf, t.cdf

st.title("📊 Dashboard Pengujian Hipotesis — Uji Rata-rata 1 Sampel (Z & T Test)")

# =============================
# INPUT DATA
# =============================
st.header("Input Data Sampel")

input_type = st.radio("Pilih cara input data:", ["Input Manual", "Upload CSV"])

if input_type == "Input Manual":
    data_str = st.text_area("Masukkan data (pisahkan dengan koma)", "10, 12, 11, 13, 12, 14, 9")
    try:
        sample = np.array([float(x) for x in data_str.split(",")])
    except:
        st.error("Format data salah.")
        st.stop()
else:
    file = st.file_uploader("Upload file CSV (kolom berisi data)", type=["csv"])
    if file is None:
        st.stop()
    import pandas as pd
    df = pd.read_csv(file)
    sample = df.iloc[:, 0].values
    st.write("Preview Data:", df.head())

n = len(sample)
xbar = np.mean(sample)

st.write(f"Jumlah data (n): {n}")
st.write(f"Rata-rata sampel (x̄): {xbar}")

# =============================
# PILIHAN UJI (flowchart: varians diketahui?)
# =============================
st.header("Jenis Pengujian ")

varians_diketahui = st.radio(
    "Apakah Varians Populasi Diketahui?",
    ["Ya (Uji Z)", "Tidak (Uji t)"]
)

mu0 = st.number_input("Masukkan nilai hipotesis H0 (μ₀):", value=11.0)
alpha = st.number_input("Tingkat Signifikansi (α):", value=0.05, step=0.01)

if varians_diketahui == "Ya (Uji Z)":
    sigma = st.number_input("Masukkan nilai standar deviasi populasi (σ):", value=2.0)

# =============================
# PERHITUNGAN
# =============================
st.header("Hasil Pengujian")

if st.button("Hitung"):

    # =====================================
    # UJI Z — Varians diketahui
    # =====================================
    if varians_diketahui == "Ya (Uji Z)":
        z_stat = (xbar - mu0) / (sigma / np.sqrt(n))
        p_val = 2 * (1 - norm.cdf(abs(z_stat)))

        st.subheader("📌 Hasil Uji Z (Varians Diketahui)")
        st.write(f"Z-statistic = {z_stat}")
        st.write(f"p-value     = {p_val}")

        if p_val < alpha:
            st.error("❌ Keputusan: Tolak H0")
        else:
            st.success("✔ Keputusan: Terima H0")

    # =====================================
    # UJI t — Varians tidak diketahui
    # =====================================
    else:
        s = np.std(sample, ddof=1)
        t_stat = (xbar - mu0) / (s / np.sqrt(n))
        p_val = 2 * (1 - t.cdf(abs(t_stat), df=n-1))

        st.subheader("📌 Hasil Uji t (Varians Tidak Diketahui)")
        st.write(f"Standar deviasi sampel (s): {s}")
        st.write(f"t-statistic = {t_stat}")
        st.write(f"p-value     = {p_val}")

        if p_val < alpha:
            st.error("❌ Keputusan: Tolak H0")
        else:
            st.success("✔ Keputusan: Terima H0")

st.markdown("---")
