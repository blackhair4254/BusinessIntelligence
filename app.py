# app_streamlit.py
import streamlit as st
import pandas as pd
import pickle

# Load dataset
product_df = pd.read_csv("/product.csv", delimiter=",", on_bad_lines='skip')

# Ambil subkategori unik
all_products = sorted(set(product_df['subCategory'].unique()))

# Load rules dari pickle
rules = pd.read_pickle("/rules.pkl")
rules['antecedents'] = rules['antecedents'].apply(lambda x: set(x) if not isinstance(x, set) else x)
rules['consequents'] = rules['consequents'].apply(lambda x: set(x) if not isinstance(x, set) else x)

# Tampilan UI
st.title("💡 Sistem Rekomendasi Produk UMKM")
st.markdown("Pilih produk yang dibeli pelanggan, lalu tekan tombol untuk mendapatkan rekomendasi berdasarkan **Association Rules**.")
st.markdown("**Bisa Lebih dari 1 Produk**")

# Pilihan produk
selected_products = st.multiselect("Pilih Produk:", options=all_products)

# Tombol Proses
if st.button("Proses Rekomendasi"):
    if selected_products:
        selected_set = set(selected_products)
        rekomendasi = []

        for _, row in rules.iterrows():
            if row['antecedents'].issubset(selected_set):
                rekom = row['consequents'] - selected_set
                rekomendasi.extend(rekom)

        rekomendasi = sorted(set(rekomendasi))

        if rekomendasi:
            st.success("Rekomendasi Produk:")
            st.write(rekomendasi)
        else:
            st.warning("Tidak ada rekomendasi baru. Semua produk yang relevan sudah dipilih.")
    else:
        st.warning("Silakan pilih minimal satu produk terlebih dahulu.")
