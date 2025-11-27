import streamlit as st
import math
import numpy as np
import pandas as pd

try:
    from scipy import stats
    SCIPY_AVAILABLE = True
except:
    SCIPY_AVAILABLE = False

# ==============================================================
# Page config
# ==============================================================

st.set_page_config(
    page_title="Pemilihan & Implementasi Uji Parametrik", 
    layout="wide",
    page_icon="🌌"
)

st.title("**📚Aplikasi Pemilihan & Implementasi Uji Parametrik (Berdasarkan Flowchart)**")
st.caption("Dibuat oleh: Kelompok (I.P.K 4) Kelas Pemrograman Komputer D")

# ==============================================================
# 🌌 CUSTOM SPACE THEME (BLUE GALAXY)
# ==============================================================

space_css = """
<style>

@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800&display=swap');

html, body, [class*="css"]  {
    font-family: 'Orbitron', sans-serif !important;
    background: radial-gradient(circle at top, #001133, #000814, #00010f);
    color: #e0eaff !important;
}

h1, h2, h3, h4 {
    color: #78aaff !important;
    text-shadow: 0 0 8px #4ea0ff;
}

.sidebar .sidebar-content {
    background: #001a33;
    color: white;
}

.css-1d391kg {
    background: #001a33 !important;
}

.stButton>button {
    background-color: #001f4d;
    border: 1px solid #4ea0ff;
    color: #cfe3ff;
    padding: 0.6rem;
    border-radius: 10px;
    transition: 0.3s;
}

.stButton>button:hover {
    background-color: #003f87;
    border-color: #77b5ff;
    transform: scale(1.05);
}

.stTabs [data-baseweb="tab"] {
    background: rgba(0, 34, 68, 0.7);
    border-radius: 10px;
    padding: 10px;
    color: #99c2ff;
    font-weight: 600;
}

.stTabs [aria-selected="true"] {
    background: rgba(0, 60, 120, 0.9);
    color: #ffffff !important;
    border-bottom: 2px solid #4ea0ff;
}

.reportview-container {
    background: #000814;
}

.block-container {
    padding-top: 1rem;
}
</style>
"""

st.markdown(space_css, unsafe_allow_html=True)

# ==============================================================
# SIDEBAR (Galaxy themed)
# ==============================================================

st.sidebar.markdown(
    """
    <div style='text-align:center; padding:10px; color:#8db2ff'>
        <h2>🚀 Menu Navigasi</h2>
        <p>Eksplorasi galaksi uji parametrik</p>
    </div>
    """,
    unsafe_allow_html=True
)


# -----------------------------------
# Sidebar: navigasi utama
# -----------------------------------
st.sidebar.header("Menu Utama")
test_menu = st.sidebar.selectbox(
    "Pilih jenis uji statistik (setiap anggota kelompok menjelaskan 1 uji):",
    [
        "Flowchart (tampilan & upload)",
        "Uji Proporsi 1 Sampel",
        "Uji Proporsi 2 Sampel",
        "Uji Rata-rata 1 Sampel (z jika σ diketahui)",
        "Uji t 1 Sampel (σ tidak diketahui)",
        "Uji Rata-rata 2 Sampel Independen — Varians Diketahui (Z)",
        "Uji Kesamaan Varians (F-test)",
        "Uji Rata-rata 2 Sampel Independen — Varians Sama (Pooled t-test)",
        "Uji Rata-rata 2 Sampel Independen — Varians Tidak Sama (Welch t-test)",
        "Uji Rata-rata 2 Sampel Dependen (Paired t-test)"
    ]
)
st.sidebar.markdown(
    """
    <div style='background:rgba(0,40,80,0.6);
                padding:15px; 
                border-radius:12px; 
                margin-top:10px;
                border:1px solid #4ea0ff;
                box-shadow:0 0 8px #4ea0ff;'>
        <h3 style='text-align:center; color:#9ec8ff;'>👩‍🚀 Anggota Kelompok (I.P.K 4):</h3>
        <p style='text-align:center; color:#cfe3ff;'>
            <li><strong>Tia Lisnawati</strong> — 140610250072</li>
                <li><strong>Zerlina Aisyah</strong> — 140610250012</li>
                   <li><strong>Naila Arziki Gunawan 140610250109</li>
                        <li><strong>Fransiskus Asisi Listyo Nugroho 140610250085</li>
                            <li><strong>Ghaisan Adlan Falah 140610250064</li>
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


st.sidebar.caption("Aplikasi ini menyediakan penjelasan, rumus, contoh, dan kalkulator interaktif.")

# Utility: normal CDF and tail
def normal_cdf(z):
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))

def normal_sf(z):  # survival function for standard normal
    return 1 - normal_cdf(z)

def two_sided_p_from_z(z):
    return 2 * normal_sf(abs(z))

def one_sided_p_from_z(z, alternative):
    if alternative == "two-sided":
        return two_sided_p_from_z(z)
    elif alternative == "greater":
        # H1: parameter > H0 -> upper tail
        return normal_sf(z)
    else:
        # "less": H1: parameter < H0 -> lower tail
        return normal_cdf(z)

# Flowchart display page
if test_menu == "Flowchart (tampilan & upload)":
    st.header("Flowchart Pemilihan Uji Statistik")
    st.markdown(
        "Unggah gambar flowchart yang diberikan dosen/kelompokmu (opsional). "
        "Jika tidak diunggah, aplikasi menampilkan flowchart ilustratif sederhana."
    )
    uploaded = st.file_uploader("Upload flowchart (png/jpg/pdf):", type=["png", "jpg", "jpeg", "pdf"])
    if uploaded:
        st.image(uploaded, caption="Flowchart yang diunggah", use_column_width=True)
    else:
        st.info("Tidak ada flowchart diunggah — menampilkan flowchart ilustratif berbasis graphviz.")
        # Simple illustrative flowchart via graphviz (Streamlit has st.graphviz_chart)
        graph = """
        digraph {
            node [shape=box, style=rounded];
            Start -> "Data & Tujuan uji";
            "Data & Tujuan uji" -> "Parameter: proporsi / rata-rata / varians?";
            "Parameter: proporsi / rata-rata / varians?" -> Prop [label="proporsi"];
            "Parameter: proporsi / rata-rata / varians?" -> Mean [label="rata-rata"];
            "Parameter: proporsi / rata-rata / varians?" -> Var [label="varians"];
            Prop -> "1 sampel atau 2 sampel?";
            Mean -> "sigma diketahui? (z) : tidak (t)";
            "2 sampel" [shape=oval];
            "1 sampel atau 2 sampel?" -> "1 sampel";
            "1 sampel atau 2 sampel?" -> "2 sampel";
            "2 sampel" -> "independen atau dependen?";
            "independen atau dependen?" -> "independen";
            "independen atau dependen?" -> "dependent";
            "independen" -> "cek kesamaan varians -> pooled t / welch";
            "cek kesamaan varians -> pooled t / welch" -> "Uji kesamaan varians (F-test)";
        }
        """
        st.graphviz_chart(graph)
    st.markdown("---")
    st.write("Panduan singkat penggunaan aplikasi:")
    st.write(
        "- Pilih salah satu uji di sidebar untuk melihat penjelasan, rumus, contoh, dan kalkulator interaktif.\n"
        "- Gunakan tab di setiap halaman uji untuk berpindah bagian (Penjelasan, Hipotesis, Rumus, Parameter, Contoh, Kalkulasi, Nilai Kritis / p-value, Flowchart)."
    )

# Helper to show tabs structure for any test: we will reuse
def render_common_tabs(title):
    return st.tabs(["Penjelasan", "Hipotesis", "Rumus", "Parameter", "Contoh", "Kalkulasi Interaktif", "Nilai Kritis / p-value", "Referensi Flowchart"])

# Now implement each test page with tabs and interactive calculator
# 1) Uji Proporsi 1 Sampel
if test_menu == "Uji Proporsi 1 Sampel":
    st.header("Uji Proporsi 1 Sampel")
    tabs = render_common_tabs("Proporsi 1 Sampel")
    # PENJELASAN
    with tabs[0]:
        st.markdown(
            "Uji proporsi 1 sampel digunakan untuk menguji hipotesis tentang proporsi populasi `p` "
            "dengan data berupa jumlah keberhasilan `x` pada sampel ukuran `n`."
        )
        st.write("Contoh: apakah proporsi pengguna yang puas >= 0.6?")
    # HIPOTESIS
    with tabs[1]:
        st.write("Hipotesis umum:")
        st.latex(r"H_0: p = p_0")
        st.latex(r"H_1: p \ne p_0 \quad \text{(atau >, < sesuai alternatif)}")
    # RUMUS
    with tabs[2]:
        st.write("Statistik uji (Z):")
        st.latex(r"\hat{p} = \frac{x}{n}")
        st.latex(r"Z = \frac{\hat{p} - p_0}{\sqrt{\dfrac{p_0(1-p_0)}{n}}}")
    # PARAMETER
    with tabs[3]:
        st.write("- x: jumlah keberhasilan pada sampel\n- n: ukuran sampel\n- p0: proporsi hipotesis nol\n- alternatif: two-sided / greater / less")
    # CONTOH
    with tabs[4]:
        st.write("Contoh singkat:")
        st.write("n=100, x=62, p0=0.6")
        phat = 62/100
        z = (phat - 0.6)/math.sqrt(0.6*0.4/100)
        pval = two_sided_p_from_z(z)
        st.write(f"phat = {phat:.3f}, Z = {z:.3f}, p-value(two-sided) ≈ {pval:.4f}")
    # KALKULASI INTERAKTIF
    with tabs[5]:
        st.subheader("Kalkulasi Proporsi 1 Sampel")
        n = st.number_input("Masukkan n (ukuran sampel):", min_value=1, step=1, value=50)
        x = st.number_input("Masukkan x (jumlah keberhasilan):", min_value=0, step=1, value=30)
        p0 = st.number_input("Masukkan p0 (proporsi H0):", min_value=0.0, max_value=1.0, value=0.5, step=0.01)
        alt = st.selectbox("Pilih alternatif H1:", ("two-sided", "greater", "less"))
        if st.button("Hitung Z & p-value (Proporsi 1 sampel)"):
            phat = x / n
            se = math.sqrt(p0 * (1 - p0) / n)
            z = (phat - p0) / se
            p = one_sided_p_from_z(z, alt)
            st.write(f"phat = {phat:.4f}")
            st.write(f"Z = {z:.4f}")
            st.write(f"p-value (berdasarkan alternatif '{alt}') ≈ {p:.6f}")
            st.info("Keputusan: Bandingkan p-value dengan alpha (mis. 0.05) atau gunakan nilai kritis z.")
    # NILAI KRITIS / PVALUE
    with tabs[6]:
        st.write("Menentukan nilai kritis untuk z:")
        alpha = st.number_input("Alpha (signifikansi):", min_value=0.0001, max_value=0.5, value=0.05, step=0.01)
        if st.button("Tampilkan nilai kritis z"):
            if st.session_state.get('last_z') is None:
                st.write("Nilai z/hitung pada tab Kalkulasi untuk membandingkan.")
            z_crit_two = abs(stats.norm.ppf(alpha/2)) if SCIPY_AVAILABLE else abs(math.sqrt(2) * math.erfinv(1 - alpha))
            # note: math.erfinv may not be present in Python <3.8; using scipy preferable
            try:
                if SCIPY_AVAILABLE:
                    z_crit_2 = abs(stats.norm.ppf(alpha/2))
                    z_crit_upper = stats.norm.ppf(1-alpha)
                    st.write(f"Two-sided z critical ≈ ±{z_crit_2:.4f}")
                    st.write(f"One-sided z critical ≈ {z_crit_upper:.4f} (upper)")
                else:
                    st.warning("SciPy tidak tersedia — nilai kritis dihitung dengan aproksimasi.")
            except Exception:
                st.warning("Silakan install scipy untuk nilai kritis numerik yang akurat.")
    # FLOWCHART
    with tabs[7]:
        st.write("Flowchart referensi untuk memilih uji proporsi: (lihat panel Flowchart utama atau unggah file)")
        st.info("Biasanya: apakah parameter proporsi? → apakah sampel 1 atau 2? → gunakan z-test proporsi.")

# 2) Uji Proporsi 2 Sampel
if test_menu == "Uji Proporsi 2 Sampel":
    st.header("Uji Proporsi 2 Sampel")
    tabs = render_common_tabs("Proporsi 2 Sampel")
    with tabs[0]:
        st.markdown("Uji untuk membandingkan dua proporsi populasi p1 dan p2 (independen).")
    with tabs[1]:
        st.latex(r"H_0: p_1 = p_2")
        st.latex(r"H_1: p_1 \ne p_2 \text{ (atau >, <)}")
    with tabs[2]:
        st.latex(r"\hat{p}_1 = x_1 / n_1,\quad \hat{p}_2 = x_2 / n_2")
        st.latex(r"\hat{p} = \frac{x_1 + x_2}{n_1 + n_2}")
        st.latex(r"Z = \frac{\hat{p}_1 - \hat{p}_2}{\sqrt{\hat{p}(1-\hat{p})(\frac{1}{n_1}+\frac{1}{n_2})}}")
    with tabs[3]:
        st.write("Parameter: x1,x2,n1,n2, alternatif")
    with tabs[4]:
        st.write("Contoh: x1=30,n1=100 ; x2=20,n2=100")
        p1 = 30/100; p2 = 20/100; p_pooled = (30+20)/(100+100)
        z = (p1-p2)/math.sqrt(p_pooled*(1-p_pooled)*(1/100+1/100))
        st.write(f"Z ≈ {z:.4f}, p(two-sided)≈{two_sided_p_from_z(z):.4f}")
    with tabs[5]:
        st.subheader("Kalkulasi Proporsi 2 Sampel")
        n1 = st.number_input("n1:", min_value=1, step=1, value=50, key="n1_prop2")
        x1 = st.number_input("x1:", min_value=0, step=1, value=25, key="x1_prop2")
        n2 = st.number_input("n2:", min_value=1, step=1, value=50, key="n2_prop2")
        x2 = st.number_input("x2:", min_value=0, step=1, value=20, key="x2_prop2")
        alt = st.selectbox("Alternatif H1:", ("two-sided", "greater", "less"), key="alt_prop2")
        if st.button("Hitung (Proporsi 2 sampel)"):
            p1 = x1/n1; p2 = x2/n2
            p_pool = (x1 + x2) / (n1 + n2)
            se = math.sqrt(p_pool*(1-p_pool)*(1/n1 + 1/n2))
            z = (p1 - p2) / se
            p = one_sided_p_from_z(z, alt)
            st.write(f"p1={p1:.4f}, p2={p2:.4f}, Z={z:.4f}, p-value({alt})≈{p:.6f}")
    with tabs[6]:
        st.write("Menentukan nilai kritis z sama seperti uji proporsi 1 sampel.")
    with tabs[7]:
        st.write("Flowchart: pilih proporsi → 2 sampel → gunakan pooled prop formula & z-test.")

# 3) Uji Rata-rata 1 Sampel (z jika sigma diketahui)
if test_menu == "Uji Rata-rata 1 Sampel (z jika σ diketahui)":
    st.header("Uji Rata-rata 1 Sampel (σ diketahui → Z-test)")
    tabs = render_common_tabs("1-Sample Mean (Z)")
    with tabs[0]:
        st.write("Digunakan bila populasi variance (σ^2) diketahui atau sampel besar (n besar).")
    with tabs[1]:
        st.latex(r"H_0: \mu = \mu_0")
        st.latex(r"H_1: \mu \ne \mu_0 \text{ (atau >, <)}")
    with tabs[2]:
        st.latex(r"Z = \frac{\bar{x} - \mu_0}{\sigma / \sqrt{n}}")
    with tabs[3]:
        st.write("Parameter: xbar, mu0, sigma, n")
    with tabs[4]:
        st.write("Contoh: xbar=52, mu0=50, sigma=5, n=36")
        z = (52-50)/(5/math.sqrt(36))
        st.write(f"Z = {z:.4f}, p(two-sided)≈{two_sided_p_from_z(z):.4f}")
    with tabs[5]:
        st.header("Kalkulasi Z 1-sample")
        xbar = st.number_input("Masukkan x̄:", value=0.0, key="xbar_z1")
        mu0 = st.number_input("Masukkan µ0:", value=0.0, key="mu0_z1")
        sigma = st.number_input("Masukkan σ (populasi):", min_value=0.0001, value=1.0, key="sigma_z1")
        n = st.number_input("Masukkan n:", min_value=1, step=1, value=30, key="n_z1")
        alt = st.selectbox("Alternatif H1:", ("two-sided", "greater", "less"), key="alt_z1")
        if st.button("Hitung Z (1 sample)"):
            z = (xbar - mu0) / (sigma / math.sqrt(n))
            p = one_sided_p_from_z(z, alt)
            st.write(f"Z = {z:.4f}, p-value({alt}) ≈ {p:.6f}")
    with tabs[6]:
        st.write("Nilai kritis z bisa dilihat dari distribusi normal (mis. ±1.96 untuk α=0.05 two-sided).")
    with tabs[7]:
        st.write("Flowchart: parameter rata-rata, sigma diketahui? → Z-test jika ya.")

# 4) Uji t 1 Sampel (sigma tidak diketahui)
if test_menu == "Uji t 1 Sampel (σ tidak diketahui)":
    st.header("Uji t 1 Sampel (σ tidak diketahui)")
    tabs = render_common_tabs("1-sample t")
    with tabs[0]:
        st.write("Digunakan bila σ populasi tidak diketahui dan n relatif kecil; gunakan s (sample sd).")
    with tabs[1]:
        st.latex(r"H_0: \mu = \mu_0")
        st.latex(r"H_1: \mu \ne \mu_0 \text{ (atau >, <)}")
    with tabs[2]:
        st.latex(r"t = \frac{\bar{x} - \mu_0}{s / \sqrt{n}}, \quad df = n - 1")
    with tabs[3]:
        st.write("Parameter: data sampel (atau x̄ & s & n), µ0")
    with tabs[4]:
        st.write("Contoh (data langsung): gunakan data = [..]")
        st.write("Contoh singkat: xbar=5.2, s=1.1, n=10, mu0=5 => t = (5.2-5)/(1.1/√10)")
    with tabs[5]:
        st.header("Kalkulasi t 1-sample")
        data_input = st.text_area("Masukkan data (pisahkan koma) atau kosongkan untuk input x̄, s, n", value="")
        mu0 = st.number_input("Masukkan µ0:", value=0.0, key="mu0_t1")
        alt = st.selectbox("Alternatif H1:", ("two-sided", "greater", "less"), key="alt_t1")
        if st.button("Hitung t 1-sample"):
            try:
                if data_input.strip():
                    arr = np.array(list(map(float, data_input.split(","))))
                    n = len(arr)
                    xbar = arr.mean()
                    s = arr.std(ddof=1)
                else:
                    xbar = st.number_input("Masukkan x̄:", value=0.0, key="xbar_t1_manual")
                    s = st.number_input("Masukkan s (sample sd):", min_value=0.0001, value=1.0, key="s_t1_manual")
                    n = st.number_input("Masukkan n:", min_value=2, step=1, value=10, key="n_t1_manual")
                t_stat = (xbar - mu0) / (s / math.sqrt(n))
                df = n - 1
                if SCIPY_AVAILABLE:
                    if alt == "two-sided":
                        p = 2 * stats.t.sf(abs(t_stat), df)
                    elif alt == "greater":
                        p = stats.t.sf(t_stat, df)
                    else:
                        p = stats.t.cdf(t_stat, df)
                    st.write(f"t = {t_stat:.4f}, df = {df}, p-value ({alt}) = {p:.6f}")
                else:
                    st.write("t = {:.4f}, df = {}".format(t_stat, df))
                    st.warning("Untuk p-value akurat, install scipy (pip install scipy).")
            except Exception as e:
                st.error(f"Error: {e}")
    with tabs[6]:
        st.write("Nilai kritis t didapat dari distribusi t dengan df = n-1 (gunakan tabel t atau scipy.stats.t.ppf).")
    with tabs[7]:
        st.write("Flowchart: µ? sigma diketahui? jika tidak → gunakan t 1-sample.")

# 5) Uji Rata-rata 2 Sampel Independen — Varians Diketahui (Uji Z)
if test_menu == "Uji Rata-rata 2 Sampel Independen — Varians Diketahui (Z)":
    st.header("Uji Rata-rata 2 Sampel Independen — Varians Diketahui (Z-test)")
    tabs = render_common_tabs("2-sample mean z")
    with tabs[0]:
        st.write("Digunakan bila kedua populasi varians diketahui (jarang), atau aproksimasi untuk n besar.")
    with tabs[1]:
        st.latex(r"H_0: \mu_1 = \mu_2")
        st.latex(r"H_1: \mu_1 \ne \mu_2")
    with tabs[2]:
        st.latex(r"Z = \frac{\bar{x}_1 - \bar{x}_2}{\sqrt{\sigma_1^2/n_1 + \sigma_2^2/n_2}}")
    with tabs[3]:
        st.write("Parameter: xbar1,xbar2, sigma1, sigma2, n1,n2")
    with tabs[4]:
        st.write("Contoh singkat: x1bar=10, x2bar=8, sigma1=2, sigma2=3, n1=40, n2=35")
        z = (10-8)/math.sqrt(2**2/40 + 3**2/35)
        st.write(f"Z ≈ {z:.4f}, p(two-sided)≈{two_sided_p_from_z(z):.4f}")
    with tabs[5]:
        st.header("Kalkulasi Z 2-sample (varians diketahui)")
        x1 = st.number_input("x̄1:", value=0.0, key="x1_z2")
        x2 = st.number_input("x̄2:", value=0.0, key="x2_z2")
        s1 = st.number_input("σ1 (populasi):", min_value=0.0001, value=1.0, key="sig1_z2")
        s2 = st.number_input("σ2 (populasi):", min_value=0.0001, value=1.0, key="sig2_z2")
        n1 = st.number_input("n1:", min_value=1, step=1, value=30, key="n1_z2")
        n2 = st.number_input("n2:", min_value=1, step=1, value=30, key="n2_z2")
        alt = st.selectbox("Alternatif H1:", ("two-sided", "greater", "less"), key="alt_z2")
        if st.button("Hitung Z (2-sample known var)"):
            z = (x1 - x2) / math.sqrt(s1**2 / n1 + s2**2 / n2)
            p = one_sided_p_from_z(z, alt)
            st.write(f"Z = {z:.4f}, p-value ({alt}) ≈ {p:.6f}")
    with tabs[6]:
        st.write("Nilai kritis sama dengan uji z lainnya.")
    with tabs[7]:
        st.write("Flowchart: dua sampel independen & varians diketahui -> gunakan z-test 2 sampel.")

# 6) Uji Kesamaan Varians (F-test)
if test_menu == "Uji Kesamaan Varians (F-test)":
    st.header("Uji Kesamaan Varians (F-test)")
    tabs = render_common_tabs("F-test")
    with tabs[0]:
        st.write("Uji F untuk membandingkan dua varians: H0: σ1^2 = σ2^2")
    with tabs[1]:
        st.latex(r"H_0: \sigma_1^2 = \sigma_2^2")
        st.latex(r"H_1: \sigma_1^2 \ne \sigma_2^2")
    with tabs[2]:
        st.latex(r"F = \frac{s_1^2}{s_2^2}, \quad df_1 = n_1-1, \ df_2 = n_2-1")
    with tabs[3]:
        st.write("Parameter: sample variances s1^2, s2^2, n1, n2")
    with tabs[4]:
        st.write("Contoh singkat: s1^2=4, s2^2=2, n1=10, n2=12")
        F = 4/2
        st.write(f"F = {F:.4f}")
    with tabs[5]:
        st.header("Kalkulasi F-test")
        s1sq = st.number_input("s1^2 (var sampel 1):", min_value=0.0, value=4.0, key="s1sq")
        s2sq = st.number_input("s2^2 (var sampel 2):", min_value=0.0, value=2.0, key="s2sq")
        n1 = st.number_input("n1:", min_value=2, step=1, value=10, key="n1_f")
        n2 = st.number_input("n2:", min_value=2, step=1, value=12, key="n2_f")
        alt = st.selectbox("Alternatif H1:", ("two-sided", "greater", "less"), key="alt_f")
        if st.button("Hitung F"):
            if s2sq == 0:
                st.error("s2^2 tidak boleh 0.")
            else:
                F = s1sq / s2sq
                df1 = n1 - 1
                df2 = n2 - 1
                st.write(f"F = {F:.4f}, df1={df1}, df2={df2}")
                if SCIPY_AVAILABLE:
                    if alt == "two-sided":
                        # two-sided: p = 2 * min(P(F>f), P(F<f))
                        p_upper = stats.f.sf(F, df1, df2)
                        p_lower = stats.f.cdf(F, df1, df2)
                        p = 2 * min(p_upper, p_lower)
                    elif alt == "greater":
                        p = stats.f.sf(F, df1, df2)
                    else:
                        p = stats.f.cdf(F, df1, df2)
                    st.write(f"p-value ({alt}) = {p:.6f}")
                else:
                    st.warning("Untuk p-value akurat, install scipy (pip install scipy).")
    with tabs[6]:
        st.write("Menentukan nilai kritis F: gunakan tabel F atau scipy.stats.f.ppf.")
    with tabs[7]:
        st.write("Flowchart: jika membandingkan varians dua sampel → gunakan F-test untuk check equal variances.")

# 7) Pooled t-test (equal variances)
if test_menu == "Uji Rata-rata 2 Sampel Independen — Varians Sama (Pooled t-test)":
    st.header("Pooled t-test (Two-sample t, equal variances)")
    tabs = render_common_tabs("Pooled t")
    with tabs[0]:
        st.write("Untuk dua sampel independen dengan asumsi varians populasi sama.")
    with tabs[1]:
        st.latex(r"H_0: \mu_1 = \mu_2")
        st.latex(r"H_1: \mu_1 \ne \mu_2")
    with tabs[2]:
        st.latex(r"s_p^2 = \frac{(n_1-1)s_1^2 + (n_2-1)s_2^2}{n_1 + n_2 - 2}")
        st.latex(r"t = \frac{\bar{x}_1 - \bar{x}_2}{s_p\sqrt{\frac{1}{n_1}+\frac{1}{n_2}}},\quad df = n_1+n_2-2")
    with tabs[3]:
        st.write("Parameter: xbar1,xbar2,s1,s2,n1,n2")
    with tabs[4]:
        st.write("Contoh singkat: x1bar=5, x2bar=3, s1=1.2, s2=1.1, n1=12, n2=10")
        sp2 = ((12-1)*1.2**2 + (10-1)*1.1**2) / (12+10-2)
        t = (5-3)/(math.sqrt(sp2)*math.sqrt(1/12+1/10))
        st.write(f"t ≈ {t:.4f}")
    with tabs[5]:
        st.header("Kalkulasi Pooled t")
        x1 = st.number_input("x̄1:", value=0.0, key="x1_pt")
        x2 = st.number_input("x̄2:", value=0.0, key="x2_pt")
        s1 = st.number_input("s1 (sd sampel):", min_value=0.0001, value=1.0, key="s1_pt")
        s2 = st.number_input("s2 (sd sampel):", min_value=0.0001, value=1.0, key="s2_pt")
        n1 = st.number_input("n1:", min_value=2, step=1, value=12, key="n1_pt")
        n2 = st.number_input("n2:", min_value=2, step=1, value=10, key="n2_pt")
        alt = st.selectbox("Alternatif H1:", ("two-sided", "greater", "less"), key="alt_pt")
        if st.button("Hitung Pooled t"):
            sp2 = ((n1-1)*s1**2 + (n2-1)*s2**2) / (n1 + n2 - 2)
            sp = math.sqrt(sp2)
            t_stat = (x1 - x2) / (sp * math.sqrt(1/n1 + 1/n2))
            df = n1 + n2 - 2
            if SCIPY_AVAILABLE:
                if alt == "two-sided":
                    p = 2 * stats.t.sf(abs(t_stat), df)
                elif alt == "greater":
                    p = stats.t.sf(t_stat, df)
                else:
                    p = stats.t.cdf(t_stat, df)
                st.write(f"t = {t_stat:.4f}, df = {df}, p-value ({alt}) = {p:.6f}")
            else:
                st.write(f"t = {t_stat:.4f}, df = {df}")
                st.warning("Install scipy untuk p-value akurat.")
    with tabs[6]:
        st.write("Nilai kritis t: gunakan t-table atau scipy.stats.t.ppf dengan df = n1+n2-2.")
    with tabs[7]:
        st.write("Flowchart: jika equal variances TRUE → gunakan pooled t-test.")

# 8) Welch t-test (varians tidak sama)
if test_menu == "Uji Rata-rata 2 Sampel Independen — Varians Tidak Sama (Welch t-test)":
    st.header("Welch t-test (Two-sample t, unequal variances)")
    tabs = render_common_tabs("Welch t")
    with tabs[0]:
        st.write("Digunakan bila varians populasi kedua kelompok tidak sama.")
    with tabs[1]:
        st.latex(r"H_0: \mu_1 = \mu_2")
        st.latex(r"H_1: \mu_1 \ne \mu_2")
    with tabs[2]:
        st.latex(r"t = \frac{\bar{x}_1 - \bar{x}_2}{\sqrt{s_1^2/n_1 + s_2^2/n_2}}")
        st.latex(r"\nu \approx \frac{(s_1^2/n_1 + s_2^2/n_2)^2}{\frac{(s_1^2/n_1)^2}{n_1-1} + \frac{(s_2^2/n_2)^2}{n_2-1}}  \quad \text{(Welch–Satterthwaite)}")
    with tabs[3]:
        st.write("Parameter: xbars, s1,s2, n1,n2")
    with tabs[4]:
        st.write("Contoh singkat: x1bar=8, x2bar=6, s1=2, s2=3, n1=15, n2=12")
        t = (8-6)/math.sqrt(2**2/15 + 3**2/12)
        st.write(f"t ≈ {t:.4f}")
    with tabs[5]:
        st.header("Kalkulasi Welch t")
        x1 = st.number_input("x̄1:", value=0.0, key="x1_welch")
        x2 = st.number_input("x̄2:", value=0.0, key="x2_welch")
        s1 = st.number_input("s1 (sd):", min_value=0.0001, value=1.0, key="s1_welch")
        s2 = st.number_input("s2 (sd):", min_value=0.0001, value=1.0, key="s2_welch")
        n1 = st.number_input("n1:", min_value=2, step=1, value=15, key="n1_welch")
        n2 = st.number_input("n2:", min_value=2, step=1, value=12, key="n2_welch")
        alt = st.selectbox("Alternatif H1:", ("two-sided", "greater", "less"), key="alt_welch")
        if st.button("Hitung Welch t"):
            numerator = (s1**2 / n1 + s2**2 / n2)**2
            denom = ( (s1**2 / n1)**2 / (n1 - 1) ) + ( (s2**2 / n2)**2 / (n2 - 1) )
            df_approx = numerator / denom if denom != 0 else 1
            t_stat = (x1 - x2) / math.sqrt(s1**2 / n1 + s2**2 / n2)
            if SCIPY_AVAILABLE:
                if alt == "two-sided":
                    p = 2 * stats.t.sf(abs(t_stat), df_approx)
                elif alt == "greater":
                    p = stats.t.sf(t_stat, df_approx)
                else:
                    p = stats.t.cdf(t_stat, df_approx)
                st.write(f"t = {t_stat:.4f}, df ≈ {df_approx:.2f}, p-value({alt}) = {p:.6f}")
            else:
                st.write(f"t = {t_stat:.4f}, df ≈ {df_approx:.2f}")
                st.warning("Install scipy untuk p-value akurat.")
    with tabs[6]:
        st.write("Nilai kritis: gunakan distribusi t dengan df ditentukan oleh formula Welch–Satterthwaite.")
    with tabs[7]:
        st.write("Flowchart: jika equal variances FALSE → gunakan Welch t-test.")

# 9) Paired t-test (dependent samples)
if test_menu == "Uji Rata-rata 2 Sampel Dependen (Paired t-test)":
    st.header("Paired t-test (2-sample dependent)")
    tabs = render_common_tabs("Paired t")
    with tabs[0]:
        st.write("Digunakan ketika observasi berpasangan (mis. sebelum-sesudah pada subjek yang sama).")
    with tabs[1]:
        st.latex(r"H_0: \mu_d = 0 \quad \text{(sering)}")
        st.latex(r"H_1: \mu_d \ne 0 \text{ (atau >, <)}")
    with tabs[2]:
        st.latex(r"d_i = x_i - y_i,\quad \bar{d} = \frac{1}{n}\sum d_i")
        st.latex(r"t = \frac{\bar{d} - \mu_{d,0}}{s_d / \sqrt{n}},\quad df = n-1")
    with tabs[3]:
        st.write("Parameter: pasangan data X dan Y (per baris), atau masukkan beda secara langsung.")
    with tabs[4]:
        st.write("Contoh singkat: X = [10,12,11], Y = [9,11,10] → d=[1,1,1] → t ...")
        d = np.array([1,1,1])
        st.write(f"d mean = {d.mean():.3f}, sd(d) = {d.std(ddof=1):.3f}")
    with tabs[5]:
        st.header("Kalkulasi Paired t")
        data_X = st.text_area("Masukkan data X (pisahkan koma):", value="")
        data_Y = st.text_area("Masukkan data Y (pisahkan koma):", value="")
        mu_d0 = st.number_input("µ_d0 (null difference):", value=0.0, key="mud0")
        alt = st.selectbox("Alternatif H1:", ("two-sided", "greater", "less"), key="alt_paired")
        if st.button("Hitung Paired t"):
            try:
                X = np.array(list(map(float, data_X.split(","))))
                Y = np.array(list(map(float, data_Y.split(","))))
                if len(X) != len(Y):
                    st.error("Panjang data X dan Y harus sama.")
                else:
                    d = X - Y
                    n = len(d)
                    dbar = d.mean()
                    sd = d.std(ddof=1)
                    t_stat = (dbar - mu_d0) / (sd / math.sqrt(n))
                    df = n - 1
                    if SCIPY_AVAILABLE:
                        if alt == "two-sided":
                            p = 2 * stats.t.sf(abs(t_stat), df)
                        elif alt == "greater":
                            p = stats.t.sf(t_stat, df)
                        else:
                            p = stats.t.cdf(t_stat, df)
                        st.write(f"t = {t_stat:.4f}, df = {df}, p-value({alt}) = {p:.6f}")
                    else:
                        st.write(f"t = {t_stat:.4f}, df = {df}")
                        st.warning("Install scipy untuk p-value akurat.")
            except Exception as e:
                st.error(f"Error parsing data: {e}")
    with tabs[6]:
        st.write("Nilai kritis t: gunakan t-table dengan df = n-1.")
    with tabs[7]:
        st.write("Flowchart: jika dua sampel dependen → gunakan paired t-test.")

# Footer / help
st.markdown("---")
st.markdown(
    "**Catatan:***\n"
    "- Pastikan memahami asumsi tiap uji (normalitas, independensi, ukuran sampel, dsb.).\n"
    "- Untuk p-value distribusi t/F presisi, sebaiknya install `scipy` (`pip install scipy`).\n"
    "- Aplikasi ini menampilkan rumus, contoh singkat, dan kalkulator interaktif untuk membantu penentuan uji.\n"
    "- Jika kamu punya flowchart yang diberikan dosen, unggah di menu **Flowchart** untuk referensi kelompok."
)
if not SCIPY_AVAILABLE:
    st.warning("Modul scipy tidak tersedia pada environment ini — beberapa p-value (t, F) tidak dihitung otomatis. "
               "Install scipy untuk hasil numerik lengkap: pip install scipy")
