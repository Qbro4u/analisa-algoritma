import streamlit as st
import pandas as pd
import time
import matplotlib.pyplot as plt

# ==========================================
# 1. LOGIKA ALGORITMA
# ==========================================

def solve_greedy(items, capacity):
    # Hitung densitas dan urutkan
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
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        item = items[i-1]
        for w in range(1, capacity + 1):
            if item['jam'] <= w:
                dp[i][w] = max(item['profit'] + dp[i-1][w-item['jam']], dp[i-1][w])
            else:
                dp[i][w] = dp[i-1][w]
    
    # Backtracking untuk mencari item
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

st.set_page_config(page_title="Analisis Greedy vs DP", layout="wide")

st.title("🚀 Optimasi Penjadwalan Tugas: Knapsack Problem")
st.markdown("""
Aplikasi ini membandingkan **Algoritma Greedy** dan **Dynamic Programming** 
dalam menyelesaikan studi kasus optimasi keuntungan proyek freelancer.
""")

# --- SIDEBAR INPUT ---
st.sidebar.header("Konfigurasi Input")
kapasitas = st.sidebar.slider("Kapasitas Waktu (Jam)", min_value=1, max_value=20, value=10)

# --- DATASET ---
data_proyek = [
    {'nama': 'Proyek A', 'jam': 2, 'profit': 400000},
    {'nama': 'Proyek B', 'jam': 3, 'profit': 500000},
    {'nama': 'Proyek C', 'jam': 5, 'profit': 600000},
    {'nama': 'Proyek D', 'jam': 4, 'profit': 100000},
    {'nama': 'Proyek E', 'jam': 1, 'profit': 300000}
]

df = pd.DataFrame(data_proyek)
df['Densitas (Profit/Jam)'] = df['profit'] / df['jam']

st.subheader("1. Dataset Proyek Tersedia")
st.table(df.style.format({'profit': 'Rp {:,.0f}', 'Densitas (Profit/Jam)': '{:.2f}'}))

# --- EKSEKUSI ---
profit_g, items_g, time_g = solve_greedy(data_proyek, kapasitas)
profit_d, items_d, time_d = solve_dp(data_proyek, kapasitas)

# --- DISPLAY HASIL ---
st.subheader(f"2. Hasil Perbandingan (Kapasitas: {kapasitas} Jam)")

col1, col2 = st.columns(2)

with col1:
    st.info("### Algoritma Greedy")
    st.metric("Total Keuntungan", f"Rp {profit_g:,.0f}")
    st.write(f"**Proyek Terpilih:** {', '.join(items_g)}")
    st.write(f"**Waktu Eksekusi:** {time_g:.4f} ms")

with col2:
    st.success("### Dynamic Programming")
    st.metric("Total Keuntungan", f"Rp {profit_d:,.0f}")
    st.write(f"**Proyek Terpilih:** {', '.join(items_d)}")
    st.write(f"**Waktu Eksekusi:** {time_d:.4f} ms")

# --- VISUALISASI ---
st.subheader("3. Visualisasi Perbandingan")

fig, ax = plt.subplots(figsize=(10, 4))
# Gunakan tema gelap agar sesuai standar presentasi
plt.style.use('dark_background')

labels = ['Greedy', 'DP']
profits = [profit_g, profit_dp := profit_d]
colors = ['#10B981', '#3B82F6']

bars = ax.barh(labels, profits, color=colors)
ax.set_xlabel('Total Keuntungan (Rupiah)')
ax.set_title('Perbandingan Profit Akhir')

# Tambahkan label harga di ujung bar
for bar in bars:
    width = bar.get_width()
    ax.text(width, bar.get_y() + bar.get_height()/2, f' Rp {width:,.0f}', 
            va='center', fontweight='bold', color='white')

st.pyplot(fig)

# --- KESIMPULAN ---
st.subheader("4. Analisis Singkat")
if profit_d > profit_g:
    st.warning(f"Pada kasus ini, **Dynamic Programming** lebih unggul Rp {profit_d - profit_g:,.0f} dibandingkan Greedy karena berhasil menemukan kombinasi optimal global.")
else:
    st.info("Pada kapasitas ini, Greedy berhasil menemukan solusi yang sama optimalnya dengan DP.")

st.markdown("---")
st.caption("Dibuat untuk Presentasi Analisis Algoritma - Kelompok IF")