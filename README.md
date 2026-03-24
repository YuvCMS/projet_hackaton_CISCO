# 🚀 Cisco Hackathon – Data Center Cooling Comparison

This project was developed as part of a Cisco hackathon focused on improving the efficiency of AI data centers.

## 🎯 Objective
The goal is to objectively compare different data center cooling technologies:
- Air Cooling (AC)
- Immersion Cooling (IC)

using standardized performance metrics defined by ISO/IEC 30134.

## 💡 Problem Statement
Data centers consume a significant amount of energy, with cooling systems representing a major part of this consumption.

👉 Our challenge:
- Identify relevant metrics
- Collect real-time data
- Compare cooling systems performance

## 📊 Key Metrics
We use several ISO-based indicators:
- **PUE (Power Usage Effectiveness)**
- **WUE (Water Usage Effectiveness)**
- **CUE (Carbon Usage Effectiveness)**
- **ERF (Energy Reuse Factor)**
- **ITEEsv (IT Equipment Energy Efficiency)**

These allow analysis from:
- Energy efficiency
- Environmental impact
- IT performance


## ⚙️ Solution
We developed a system that:
- Collects data from data centers (API)
- Processes energy and IT consumption
- Computes metrics (PUE, CUE, etc.)
- Displays results in real time via a dashboard (Streamlit)

## 🏗️ Architecture
- `Extracteur_donnée.py` → Data extraction
- `Api_server_CISCO.py` → Backend (Flask API)
- `application_CISCO.py` → Visualization (Streamlit)

## 📈 Outcome
The solution enables:
- Real-time monitoring
- Objective comparison between AC and IC
- Decision support for optimizing cooling strategies

## 👥 Team
- GUIRY Yuvaas  
- MADDI Radia  
- FENDES Iness  
- AMARI Ghanem  

## 🏫 Context
Master 2 – Cybersecurity & Data Science (2025/2026)  
Université Paris 8  
Cisco Hackathon – Generative AI


## ▶️ How to Run

Follow these steps to launch the application:

1. Extract data:
```bash
1) python extracteur_donnee.py
2) python api_server.py
3) streamlit run application.py

