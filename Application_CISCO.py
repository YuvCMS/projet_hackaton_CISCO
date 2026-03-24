import streamlit as st
import pandas as pd
import time
import requests

st.set_page_config(layout="wide")

# ============================
# SIDEBAR
# ============================

page = st.sidebar.radio(
    "Select View",
    ["Immersion Cooling (IC)", "Air Cooling (AC)", "Comparison (PUE & CUE)"]
)

st.title("⚡Data Center Racks Monitoring Dashboard")

group_size = st.slider("Servers per rack", 1, 20, 5)

# 🌍 choix facteur carbone
region = st.selectbox("🌍 Region", ["France", "Europe", "World"])

if region == "France":
    carbon_factor = 0.05  # kgCO2/kWh
elif region == "Europe":
    carbon_factor = 0.3
else:
    carbon_factor = 0.475

# ============================
# API
# ============================

def get_sensor_data():
    try:
        r = requests.get("http://localhost:5000/datacenter")
        d = r.json()

        return (
            d.get("it_power"),     # IT uniquement
            d.get("energy_ic"),   
            d.get("energy_ac"),   
            d.get("cpu_usage"),
            d.get("gpu_usage")
        )
    except:
        return None, None, None, None, None

# ============================
# STREAM
# ============================

placeholder = st.empty()

data_list = []

group_IT = 0
group_ic = 0
group_ac = 0
group_cpu = 0
group_gpu = 0
count = 0

for _ in range(200):

    it, ic, ac, cpu, gpu = get_sensor_data()

    if it is None:
        with placeholder.container():
            st.warning("⏳ Waiting for API data...")
        time.sleep(1)
        continue

    # accumulation
    group_IT += it
    group_ic += ic
    group_ac += ac
    group_cpu += cpu
    group_gpu += gpu
    count += 1

    if count == group_size:

        # ============================
        # CONVERSIONS
        # ============================

        IT_kw = group_IT / 1000
        CPU_kw = group_cpu / 1000
        GPU_kw = group_gpu / 1000

        # 🔥 NOUVELLE LOGIQUE
        overhead_ic = group_ic
        overhead_ac = group_ac

        IC_kw =  overhead_ic/ 1000
        AC_kw = overhead_ac/ 1000

        # ============================
        # PUE
        # ============================

        PUE_IC = IC_kw / IT_kw if IT_kw != 0 else 0
        PUE_AC = AC_kw / IT_kw if IT_kw != 0 else 0

        # ============================
        # CUE (ISO 30134-8)
        # ============================

        CO2_IC = IC_kw * carbon_factor
        CO2_AC = AC_kw * carbon_factor

        CUE_IC = CO2_IC / IT_kw if IT_kw != 0 else 0
        CUE_AC = CO2_AC / IT_kw if IT_kw != 0 else 0

        data_list.append({
            "IT": IT_kw,
            "IC": IC_kw,
            "AC": AC_kw,
            "CPU": CPU_kw,
            "GPU": GPU_kw,
            "PUE_IC": PUE_IC,
            "PUE_AC": PUE_AC,
            "CUE_IC": CUE_IC,
            "CUE_AC": CUE_AC,
            "CO2_IC": CO2_IC,
            "CO2_AC": CO2_AC
        })

        # reset
        group_IT = 0
        group_ic = 0
        group_ac = 0
        group_cpu = 0
        group_gpu = 0
        count = 0

    df = pd.DataFrame(data_list)

    # ============================
    # UI
    # ============================

    with placeholder.container():

        st.write(f"Servers in rack: {count}/{group_size}")

        if len(data_list) > 0:

            last = data_list[-1]

            # ============================
            # 🧊 IC PAGE
            # ============================

            if page == "Immersion Cooling (IC)":

                st.subheader("🧊 Immersion Cooling")

                col1, col2, col3 = st.columns(3)
                col1.metric("CPU (kW)", f"{last['CPU']:.2f}")
                col2.metric("GPU (kW)", f"{last['GPU']:.2f}")
                col3.metric("IT (kW)", f"{last['IT']:.2f}")

                col4, col5 = st.columns(2)
                col4.metric("Total Energy IC (kW)", f"{last['IC']:.2f}")
                col5.metric("PUE IC", f"{last['PUE_IC']:.2f}")

                col6, col7 = st.columns(2)
                col6.metric("CO₂ IC (kg)", f"{last['CO2_IC']:.2f}")
                col7.metric("CUE IC", f"{last['CUE_IC']:.3f}")

                st.line_chart(df[["IC", "IT"]])
                st.line_chart(df[["PUE_IC", "CUE_IC"]])

            # ============================
            # 🌬️ AC PAGE
            # ============================

            elif page == "Air Cooling (AC)":

                st.subheader("🌬️ Air Cooling")

                col1, col2, col3 = st.columns(3)
                col1.metric("CPU (kW)", f"{last['CPU']:.2f}")
                col2.metric("GPU (kW)", f"{last['GPU']:.2f}")
                col3.metric("IT (kW)", f"{last['IT']:.2f}")

                col4, col5 = st.columns(2)
                col4.metric("Total Energy AC (kW)", f"{last['AC']:.2f}")
                col5.metric("PUE AC", f"{last['PUE_AC']:.2f}")

                col6, col7 = st.columns(2)
                col6.metric("CO₂ AC (kg)", f"{last['CO2_AC']:.2f}")
                col7.metric("CUE AC", f"{last['CUE_AC']:.3f}")

                st.line_chart(df[["AC", "IT"]])
                st.line_chart(df[["PUE_AC", "CUE_AC"]])

            # ============================
            # ⚖️ COMPARISON
            # ============================

            else:

                st.subheader("⚖️ IC vs AC Comparison")

                col1, col2 = st.columns(2)
                col1.metric("PUE IC", f"{last['PUE_IC']:.2f}")
                col2.metric("PUE AC", f"{last['PUE_AC']:.2f}")

                col3, col4 = st.columns(2)
                col3.metric("CUE IC", f"{last['CUE_IC']:.3f}")
                col4.metric("CUE AC", f"{last['CUE_AC']:.3f}")

                st.markdown("### 🌍 CO₂ Emissions")
                col5, col6 = st.columns(2)
                col5.metric("CO₂ IC (kg)", f"{last['CO2_IC']:.2f}")
                col6.metric("CO₂ AC (kg)", f"{last['CO2_AC']:.2f}")

                st.line_chart(df[["PUE_IC", "PUE_AC"]])
                st.line_chart(df[["CUE_IC", "CUE_AC"]])

    time.sleep(1)