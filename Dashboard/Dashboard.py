import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

# ── Load Data ──────────────────────────────────────────────
all_df = pd.read_csv("Dashboard/main_data.csv")
rfm_df = pd.read_csv("Dashboard/rfm_data.csv")
all_df["order_purchase_timestamp"] = pd.to_datetime(all_df["order_purchase_timestamp"])

# ── Membuat Fitur Interaktif (Sidebar Filter) ──────────────
with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png") 
    
    # Mengambil range tanggal dari dataset
    min_date = all_df["order_purchase_timestamp"].min()
    max_date = all_df["order_purchase_timestamp"].max()

    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter data utama berdasarkan input tanggal dari user (Inilah yang bikin interaktif)
main_df = all_df[(all_df["order_purchase_timestamp"] >= str(start_date)) & 
                 (all_df["order_purchase_timestamp"] <= str(end_date))]

# ── Identitas & Pertanyaan Bisnis ───
st.title("Proyek Analisis Data: E-Commerce Public Dataset")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("**Nama:** Rifa Agnia")
with col2:
    st.markdown("**Email:** cdcc001d6x1252@student.devacademy.id")
with col3:
    st.markdown("**ID Dicoding:** CDCC001D6X1252")

st.divider()

with st.expander("📋 Pertanyaan Bisnis (SMART Framework)"):
    st.markdown("""
    **Pertanyaan 1:** Bagaimana tren jumlah pesanan dan total pendapatan platform e-commerce Olist secara bulanan selama periode 2017?
    1. **Specific:** Fokus pada performa bisnis, yaitu jumlah pesanan dan total pendapatan yang dilihat per bulan.
    2. **Measurable:** Diukur dari jumlah order dan total revenue per bulan.
    3. **Action-Oriented:** Hasil tren bisa digunakan untuk mengevaluasi bulan dengan performa rendah dan menjadi bahan rekomendasi.
    4. **Relevant:** Memantau performa penjualan dan pendapatan merupakan kebutuhan dasar perusahaan untuk meninjau bisnis.
    5. **Time-bound:** Dibatasi pada periode 2017.

    ---

    **Pertanyaan 2:** Kategori produk apa yang memiliki jumlah pesanan dan pendapatan tertinggi dan terendah selama periode 2017?
    1. **Specific:** Fokus pada perbandingan volume penjualan dan pendapatan antar kategori produk.
    2. **Measurable:** Diukur dengan menjumlahkan setiap kategori produk yang sudah terjual.
    3. **Action-Oriented:** Kategori terlaris dapat diprioritaskan stoknya, dan kategori yang kurang laris dapat dievaluasi.
    4. **Relevant:** Mengetahui produk laris dan yang tidak dapat menjadi tolak ukur untuk keputusan bisnis.
    5. **Time-bound:** Dibatasi pada periode 2017.
    """)

st.divider()

# ── Header ─────────────────────────────────────────────────
st.header("E-Commerce Public Dataset Dashboard")

# ── Section 1: Tren Pesanan & Revenue ─────────────────────
st.subheader("Tren Jumlah Pesanan dan Pendapatan Kotor per Bulan")

main_df["month"] = main_df["order_purchase_timestamp"].dt.month
main_df["year"] = main_df["order_purchase_timestamp"].dt.year

monthly_sales = main_df.groupby("month").agg(
    total_orders=("order_id", "nunique"),
    total_revenue=("revenue", "sum")
).reset_index().sort_values("month")

col1, col2 = st.columns(2)
with col1:
    st.metric("Total Pesanan", value=f"{monthly_sales['total_orders'].sum():,}")
with col2:
    st.metric("Total Pendapatan Kotor", value=f"{monthly_sales['total_revenue'].sum():,.0f}")

month_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


current_month_labels = [month_labels[i-1] for i in monthly_sales["month"]]

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
axes[0].plot(monthly_sales["month"], monthly_sales["total_orders"], color="seagreen", marker='o')
axes[0].set_title("Total Pesanan per Bulan")
axes[0].set_xlabel("Bulan")
axes[0].set_ylabel("Total Pesanan")
axes[0].set_xticks(monthly_sales["month"])
axes[0].set_xticklabels(current_month_labels)
axes[0].grid(False)

axes[1].plot(monthly_sales["month"], monthly_sales["total_revenue"], color="indianred", marker='o')
axes[1].set_title("Total Pendapatan Kotor per Bulan")
axes[1].set_xlabel("Bulan")
axes[1].set_ylabel("Total Pendapatan Kotor")
axes[1].set_xticks(monthly_sales["month"])
axes[1].set_xticklabels(current_month_labels)
axes[1].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:,.0f}"))
axes[1].grid(False)
plt.tight_layout()
st.pyplot(fig)

# ── Section 2: Kategori Produk ─────────────────────────────
st.subheader("Performa Kategori Produk")
st.markdown("#### Kategori Produk berdasarkan Jumlah Pendapatan Kotor")

revenue_category = main_df.groupby("product_category_name_english").agg(
    total_orders=("order_id", "nunique"),
    total_revenue=("revenue", "sum")
).reset_index().sort_values("total_revenue", ascending=False)

top_r = revenue_category.nlargest(3, "total_revenue")
bottom_r = revenue_category.nsmallest(3, "total_revenue")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

sns.barplot(data=top_r, y="product_category_name_english", x="total_revenue", ax=axes[0], color="steelblue")
axes[0].set_title("Kategori Produk Pendapatan Tertinggi")
axes[0].set_xlabel("Total Pendapatan Kotor")
axes[0].set_ylabel("Kategori Produk")

sns.barplot(data=bottom_r, y="product_category_name_english", x="total_revenue", ax=axes[1], color="darkorange")
axes[1].set_title("Kategori Produk Pendapatan Terendah")
axes[1].set_xlabel("Total Pendapatan Kotor")
axes[1].set_ylabel("Kategori Produk")
plt.tight_layout()
st.pyplot(fig)

st.markdown("#### Kategori Produk berdasarkan Jumlah Pesanan")

orders_category = main_df.groupby("product_category_name_english").agg(
    total_orders=("order_id", "nunique"),
    total_revenue=("revenue", "sum")
).reset_index().sort_values("total_orders", ascending=False)

top_o = orders_category.nlargest(3, "total_orders")
bottom_o = orders_category.nsmallest(3, "total_orders")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

sns.barplot(data=top_o, y="product_category_name_english", x="total_orders", ax=axes[0], color="steelblue")
axes[0].set_title("Kategori Produk Pesanan Tertinggi")
axes[0].set_xlabel("Total Pesanan")
axes[0].set_ylabel("Kategori Produk")

sns.barplot(data=bottom_o, y="product_category_name_english", x="total_orders", ax=axes[1], color="darkorange")
axes[1].set_title("Kategori Produk Pesanan Terendah")
axes[1].set_xlabel("Total Pesanan")
axes[1].set_ylabel("Kategori Produk")
plt.tight_layout()
st.pyplot(fig)

# ── Section 3: RFM Analysis ────────────────────────────────
st.subheader("Analisis RFM Pelanggan")

fig, ax = plt.subplots(figsize=(7, 7))
category_counts = rfm_df["customer_category"].value_counts()
ax.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%',
       startangle=90, colors=["seagreen", "indianred"], explode=(0.05, 0))
ax.set_title("Persentase High Value vs Low Value Customer Berdasarkan RFM")
st.pyplot(fig)

st.caption("Rifa Agnia - CDCC001D6X1252")
