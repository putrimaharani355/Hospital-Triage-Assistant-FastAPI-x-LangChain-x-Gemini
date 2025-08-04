import streamlit as st
import requests

st.set_page_config(page_title="Hospital Triage Assistant", layout="centered")

st.title("🏥 Hospital Triage Assistant")
st.write("Masukkan data pasien untuk mendapatkan rekomendasi departemen rumah sakit.")

# Input user
gender = st.selectbox("Jenis Kelamin", ["female", "male"])
age = st.number_input("Usia", min_value=0, max_value=120, step=1)
symptoms_input = st.text_area("Gejala (pisahkan dengan koma)", placeholder="mual, pusing, sulit berjalan")

# Tombol submit
if st.button("Dapatkan Rekomendasi"):
    if not symptoms_input.strip():
        st.warning("Mohon isi gejala pasien terlebih dahulu.")
    else:
        symptoms = [s.strip() for s in symptoms_input.split(",")]
        payload = {
            "gender": gender,
            "age": age,
            "symptoms": symptoms
        }

        try:
            # Kirim request ke backend FastAPI
            response = requests.post(
            "https://hospital-triage-api-production.up.railway.app/rekomendasi-departemen",
            json=payload
            )
            if response.status_code == 200:
                result = response.json()
                st.success(f"✅ Rekomendasi Departemen: **{result['recommended_department']}**")
            else:
                st.error(f"❌ Error dari server: {response.status_code}\n{response.text}")
        except Exception as e:
            st.error(f"🔌 Gagal terhubung ke server backend: {e}")


