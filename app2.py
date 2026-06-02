import streamlit as st
import pandas as pd
import time
import matplotlib.pyplot as plt

# ==========================================
# 1. LOGIKA ALGORITMA
# ==========================================

def solve_greedy(items, capacity):
    # Urutkan berdasarkan densitas tertinggi (Profit/Jam)
    start_time = time.perf_counter()
    sorted_items = sorted(items, key=lambda x: x['profit']/x['jam'], reverse=True)
    
    total_profit = 0
    used_capacity = 0
    chosen_names = []
    
    for item in sorted_items:
        if used_capacity + item['jam'] <= capacity:
            used_capacity += item['jam']
            total_profit += item['profit']
            chosen_names.append(item['nama'])
    
    end_time = time.perf_counter()
    return total_profit, chosen_names, (end_time - start_time) * 1000

def solve_dp(items, capacity):
    start_time = time.perf_counter()
    n = len(items)
    # Matrix DP [n+1][kapasitas+1]
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        item = items[i-1]
        for w in range(1, capacity + 1):
            if item['jam'] <= w:
                dp[i][w] = max(item['profit'] + dp[i-1][w-item['jam']], dp[i-1][w])
            else:
                dp[i][w] = dp[i-1][w]
    
    # Backtracking untuk melacak proyek yang dipilih
    res = dp[n][capacity]
    w = capacity
    chosen_names = []
    for i in range(n, 0, -1):
        if res <= 0: break
        if res == dp[i-1][w]: continue
        else:
            item = items[i-1]
            chosen_names.append(item['nama'])
            res -= item['profit']
            w -= item['jam']
            
    end_time = time.perf_counter()
    return dp[n][capacity], chosen_names, (end_time - start_time) * 1000

# ==========================================
# 2. TAMPILAN STREAMLIT
# ==========================================

st.set_page_config(page_title="Simulasi Optimasi Penjadwalan", layout="wide")

st.title("🚀 Dashboard Optimasi Penjadwalan: Greedy vs DP")
st.markdown("""
Aplikasi ini melakukan simulasi pemilihan proyek IT untuk mendapatkan keuntungan maksimal 
dari sekumpulan tawaran proyek dengan batas waktu tertentu.
""")

# --- SIDEBAR INPUT ---
st.sidebar.header("Konfigurasi Simulasi")
# Kapasitas ditambah hingga 30 jam karena jumlah item sekarang lebih banyak
kapasitas = st.sidebar.slider("Kapasitas Waktu Kerja (Jam)", min_value=1, max_value=30, value=15)

# --- DATASET (10 PROYEK) ---
data_proyek = [
    {'nama': 'Proyek A', 'jam': 2, 'profit': 400000},
    {'nama': 'Proyek B', 'jam': 3, 'profit': 500000},
    {'nama': 'Proyek C', 'jam': 5, 'profit': 600000},
    {'nama': 'Proyek D', 'jam': 4, 'profit': 100000},
    {'nama': 'Proyek E', 'jam': 1, 'profit': 300000},
    # 5 Proyek Baru
    {'nama': 'Proyek F (Audit Keamanan)', 'jam': 6, 'profit': 950000},
    {'nama': 'Proyek G (UI/UX Design)', 'jam': 4, 'profit': 750000},
    {'nama': 'Proyek H (Database Opt)', 'jam': 3, 'profit': 450000},
    {'nama': 'Proyek I (Integrasi API)', 'jam': 2, 'profit': 380000},
    {'nama': 'Proyek J (Fixing Bug)', 'jam': 1, 'profit': 180000}
]

df = pd.DataFrame(data_proyek)
df['Profit/Jam (Densitas)'] = df['profit'] / df['jam']

st.subheader(f"1. Dataset Proyek (Total: {len(data_proyek)} Proyek)")
st.table(df.style.format({'profit': 'Rp {:,.0f}', 'Profit/Jam (Densitas)': 'Rp {:,.0f}'}))

# --- EKSEKUSI ALGORITMA ---
profit_g, items_g, time_g = solve_greedy(data_proyek, kapasitas)
profit_d, items_d, time_d = solve_dp(data_proyek, kapasitas)

# --- TAMPILAN HASIL ---
st.subheader(f"2. Hasil Analisis (Kapasitas: {kapasitas} Jam)")

col1, col2 = st.columns(2)

with col1:
    st.info("### Algoritma Greedy")
    st.metric("Total Keuntungan", f"Rp {profit_g:,.0f}")
    st.write(f"**Proyek Terpilih:** {', '.join(items_g)}")
    st.caption(f"Waktu Komputasi: {time_g:.4f} ms")

with col2:
    st.success("### Dynamic Programming")
    st.metric("Total Keuntungan", f"Rp {profit_d:,.0f}")
    st.write(f"**Proyek Terpilih:** {', '.join(items_d)}")
    st.caption(f"Waktu Komputasi: {time_d:.4f} ms")

# --- VISUALISASI ---
st.subheader("3. Perbandingan Keuntungan Akhir")

fig, ax = plt.subplots(figsize=(10, 4))
plt.style.use('dark_background')

metode = ['Greedy (Lokal)', 'DP (Global)']
keuntungan = [profit_g, profit_d]
colors = ['#10B981', '#3B82F6'] # Hijau Emerald & Biru

bars = ax.barh(metode, keuntungan, color=colors)
ax.set_xlabel('Keuntungan (Rupiah)')
ax.set_title('Selisih Profit: Greedy vs Dynamic Programming')

# Tambahkan label angka di bar
for bar in bars:
    width = bar.get_width()
    ax.text(width, bar.get_y() + bar.get_height()/2, f' Rp {width:,.0f}', 
            va='center', fontweight='bold', color='white', fontsize=10)

st.pyplot(fig)

# --- ANALISIS ---
st.subheader("4. Kesimpulan Efisiensi")
selisih = profit_d - profit_g
if selisih > 0:
    st.warning(f"Pada kapasitas {kapasitas} jam, **Dynamic Programming** berhasil memberikan keuntungan **Rp {selisih:,.0f} lebih besar** daripada Greedy. Ini membuktikan bahwa Greedy sering terjebak dalam solusi 'terbaik saat ini' tanpa mempertimbangkan kombinasi masa depan.")
else:
    st.info(f"Pada kapasitas {kapasitas} jam, kedua algoritma memberikan hasil yang sama optimalnya.")

st.markdown("---")
st.caption("Penerapan Analisis Algoritma - Knapsack 0/1 Study Case")