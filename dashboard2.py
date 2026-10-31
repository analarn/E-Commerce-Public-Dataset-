import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Konfigurasi halaman
st.set_page_config(
    page_title="Dashboard E-Commerce",
    layout="wide")

# Membaca data
monthly_sales = pd.read_csv("monthly_sales.csv")
category_sales = pd.read_csv("category_sales.csv")
category_performance = pd.read_csv("category_performance.csv")


# Judul dashboard
st.title("E-Commerce Sales Dashboard")
st.write(
    "Dashboard ini menyajikan hasil analisis penjualan E-Commerce Public Dataset")

st.divider()


# Ringkasan penjualan
st.subheader("Ringkasan Penjualan")

col1, col2 = st.columns(2)

with col1:
    total_sales = monthly_sales["total_sales"].sum()

    st.metric(
        label="Total Penjualan",
        value=f"{total_sales:,.2f}")

with col2:
    total_orders = monthly_sales["total_orders"].sum()

    st.metric(
        label="Total Pesanan",
        value=f"{total_orders:,.0f}")

st.divider()


# Grafik penjualan bulanan
st.subheader("Tren Penjualan Bulanan")

monthly_sales["order_month"] = pd.to_datetime(
    monthly_sales["order_month"].astype(str))

monthly_sales = monthly_sales.sort_values("order_month")

fig, ax = plt.subplots(figsize=(12, 5))

ax.plot(
    monthly_sales["order_month"],
    monthly_sales["total_sales"],
    marker="o")

ax.set_xlabel("Bulan")
ax.set_ylabel("Total Penjualan")
ax.grid(axis="y", linestyle="--", alpha=0.4)

plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(fig)
plt.close(fig)

st.divider()


# Kategori penjualan tertinggi dan terendah
st.subheader("Analisis Kategori Produk")

category_col = "product_category_name_english"

top_categories = (
    category_sales.nlargest(5, "total_sales")
    .sort_values("total_sales"))

bottom_categories = (
    category_sales.nsmallest(5, "total_sales")
    .sort_values("total_sales"))

col3, col4 = st.columns(2)


# 5 Kategori Penjualan Tertinggi
with col3:
    st.write("**5 Kategori Penjualan Tertinggi**")

    fig, ax = plt.subplots(figsize=(7, 4))

    colors = plt.cm.Blues(
        np.linspace(0.3, 1.0, len(top_categories)))

    ax.barh(
        top_categories[category_col],
        top_categories["total_sales"],
        color=colors,
        edgecolor="white")

    ax.set_xlabel("Total Penjualan")
    ax.set_facecolor("#F8FAFC")
    fig.patch.set_facecolor("#F8FAFC")

    plt.tight_layout()

    st.pyplot(fig)
    plt.close(fig)


# 5 Kategori Penjualan Terendah
with col4:
    st.write("**5 Kategori Penjualan Terendah**")

    fig, ax = plt.subplots(figsize=(7, 4))

    colors = plt.cm.Oranges(
        np.linspace(0.3, 1.0, len(bottom_categories)))

    ax.barh(
        bottom_categories[category_col],
        bottom_categories["total_sales"],
        color=colors,
        edgecolor="white")

    ax.set_xlabel("Total Penjualan")
    ax.set_facecolor("#F8FAFC")
    fig.patch.set_facecolor("#F8FAFC")

    plt.tight_layout()

    st.pyplot(fig)
    plt.close(fig)

st.divider()


# Perbandingan penjualan dan jumlah pesanan
st.subheader("Perbandingan Penjualan dan Jumlah Pesanan")

top_10 = (
    category_performance
    .nlargest(10, "total_sales")
    .sort_values("total_sales", ascending=False))

fig, ax1 = plt.subplots(figsize=(12, 6))

ax1.bar(
    top_10[category_col],
    top_10["total_sales"],
    label="Total Penjualan")

ax1.set_xlabel("Kategori Produk")
ax1.set_ylabel("Total Penjualan")
ax1.tick_params(axis="x", rotation=45)

ax2 = ax1.twinx()

ax2.plot(
    top_10[category_col],
    top_10["total_orders"],
    color="orange",
    marker="o",
    linestyle="--",
    label="Jumlah Pesanan")

ax2.set_ylabel("Jumlah Pesanan")

plt.title("10 Kategori dengan Penjualan Tertinggi")
fig.tight_layout()

st.pyplot(fig)
plt.close(fig)


# Menampilkan data
with st.expander("Lihat Data Penjualan Bulanan"):
    st.dataframe(monthly_sales, use_container_width=True)

with st.expander("Lihat Data Penjualan per Kategori"):
    st.dataframe(category_performance, use_container_width=True)