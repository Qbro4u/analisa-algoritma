import streamlit as st
import pandas as pd
import time
import matplotlib.pyplot as plt
import numpy as np

# ==========================================
# 1. LOGIKA ALGORITMA
# ==========================================

def solve_greedy(items, capacity):
    start_time = time.perf_counter()
    # Greedy: O(N log N) karena sorting
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
    return total_profit, chosen_names, (end_time - start_time) * 1000 # ms

def solve_dp(items, capacity):
    start_time = time.perf_counter()
    n = len(items)
    # DP: O(N * W) karena mengisi matriks
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        item = items[i-1]
        for w in range(1, capacity + 1):
            if item['jam'] <= w:
                dp[i][w] = max(item['profit'] + dp[i-1][w-item['jam']], dp[i-1][w])
            else:
                dp[i][w] = dp[i-1][w]
    
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
    return dp[n][capacity], chosen_names, (end_time - start_time) * 1000 # ms

# ==========================================
# 2. TAMPILAN STREAMLIT
# ==========================================

st.set_page_config(page_title="Analisis Kompleksitas Algoritma", layout="wide")

st.title("📊 Analisis Kompleksitas & Performa: Greedy vs DP")
st.markdown("Dashboard ini membandingkan efisiensi waktu (kompleksitas) dan kualitas solusi (akurasi).")

# --- DATASET (10 PROYEK) ---
data_proyek = [
    {'nama': 'Proyek A', 'jam': 2, 'profit': 400000},
    {'nama': 'Proyek B', 'jam': 3, 'profit': 500000},
    {'nama': 'Proyek C', 'jam': 5, 'profit': 600000},
    {'nama': 'Proyek D', 'jam': 4, 'profit': 100000},
    {'nama': 'Proyek E', 'jam': 1, 'profit': 300000},
    {'nama': 'Proyek F', 'jam': 6, 'profit': 950000},
    {'nama': 'Proyek G', 'jam': 4, 'profit': 750000},
    {'nama': 'Proyek H', 'jam': 3, 'profit': 450000},
    {'nama': 'Proyek I', 'jam': 2, 'profit': 380000},
    {'nama': 'Proyek J', 'jam': 1, 'profit': 180000}
]

# --- LAYOUT TABS ---
tab1, tab2 = st.tabs(["💡 Simulasi Kasus", "📈 Analisis Kompleksitas Waktu"])

with tab1:
    st.sidebar.header("Konfigurasi Simulasi")
    kapasitas = st.sidebar.slider("Pilih Kapasitas Waktu (Jam)", 1, 30, 15)

    profit_g, items_g, time_g = solve_greedy(data_proyek, kapasitas)
    profit_d, items_d, time_d = solve_dp(data_proyek, kapasitas)

    col1, col2 = st.columns(2)
    col1.metric("Profit Greedy", f"Rp {profit_g:,.0f}", delta=None)
    col1.caption(f"Waktu: {time_g:.5f} ms")
    
    col2.metric("Profit DP", f"Rp {profit_d:,.0f}", delta=f"{(profit_d-profit_g):,.0f} Lebih Optimal")
    col2.caption(f"Waktu: {time_d:.5f} ms")

    # Visualisasi Bar Profit
    fig_p, ax_p = plt.subplots(figsize=(8, 2))
    plt.style.use('dark_background')
    ax_p.barh(['Greedy', 'DP'], [profit_g, profit_d], color=['#10B981', '#3B82F6'])
    ax_p.set_title("Perbandingan Keuntungan")
    st.pyplot(fig_p)

with tab2:
    st.subheader("Analisis Skalabilitas Waktu (Complexity Growth)")
    st.write("Grafik ini menunjukkan bagaimana waktu eksekusi meningkat seiring bertambahnya Kapasitas (W).")

    # Simulasi Penambahan Waktu Eksekusi
    w_range = np.arange(10, 1001, 50) # Kapasitas dari 10 sampai 1000
    g_times = []
    d_times = []

    for w in w_range:
        # Kita uji berkali-kali agar rata-rata stabil
        _, _, tg = solve_greedy(data_proyek, w)
        _, _, td = solve_dp(data_proyek, w)
        g_times.append(tg)
        d_times.append(td)

    # Visualisasi Line Chart Kompleksitas
    fig_c, ax_c = plt.subplots(figsize=(10, 5))
    ax_c.plot(w_range, g_times, label='Greedy (O(N log N))', color='#10B981', linewidth=2, marker='o')
    ax_c.plot(w_range, d_times, label='Dynamic Programming (O(N * W))', color='#3B82F6', linewidth=2, marker='s')
    
    ax_c.set_xlabel('Kapasitas Knapsack (W)')
    ax_c.set_ylabel('Waktu Eksekusi (ms)')
    ax_c.set_title("Skalabilitas: Greedy vs Dynamic Programming")
    ax_c.legend()
    ax_c.grid(True, alpha=0.2)
    
    st.pyplot(fig_c)

    st.markdown("""
    **Analisis Temuan:**
    - **Greedy (Garis Hijau):** Waktunya cenderung datar (konstan) meskipun kapasitas dinaikkan. Ini karena Greedy hanya melakukan pengurutan item di awal, tidak peduli seberapa besar kapasitasnya.
    - **Dynamic Programming (Garis Biru):** Waktunya meningkat secara linear seiring bertambahnya kapasitas ($W$). Hal ini terjadi karena algoritma harus mengisi setiap sel dalam tabel berukuran $N \times W$.
    - **Kesimpulan:** Jika kapasitas sangat besar (misal ribuan jam), DP akan melambat secara signifikan, sementara Greedy tetap sangat cepat.
    """)

st.sidebar.markdown("---")
st.sidebar.info("Gunakan Tab di atas untuk berpindah antara simulasi profit dan analisis waktu.")