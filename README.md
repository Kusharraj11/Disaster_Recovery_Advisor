# Disaster_Recovery_Advisor
 # 👋 Author Introduction

I am **Kushar Raj Kashyap**, a final-year Master of Computer Applications (MCA) student at **Haldia Institute of Technology**, West Bengal. This project, **Disaster Recovery Advisor**, was developed as part of my major project submission for the 4th semester (2024–2025), under the guidance of **Ms. Kankana Datta**, Assistant Professor, Department of Computer Applications.

---

# 🌍 Disaster Recovery Advisor

An AI/ML-powered project designed to predict natural disasters and assist in efficient post-disaster recovery planning using intelligent resource allocation and recommendation systems.

## 📌 Project Overview

The **Disaster Recovery Advisor** is an AI/ML-based system that predicts natural disasters such as floods, earthquakes, and storms using historical data, geographical attributes (latitude, longitude), and time-based environmental factors. The platform provides not only disaster prediction but also offers **impact estimation** (casualties, economic loss, infrastructure damage) and **tailored recovery strategies** like evacuation plans, medical assistance, and relief inventory management.

---

## 🎯 Core Objectives

- Predict type, severity, and duration of upcoming natural disasters.
- Generate custom recovery plans and smart resource distribution strategies.
- Assist government bodies, NGOs, and citizens in real-time disaster preparedness.
- Monitor and manage disaster relief inventory efficiently.

---

## 🛠️ Tech Stack

| Category            | Technology/Tools                     |
|---------------------|--------------------------------------|
| Programming         | Python 3.x                           |
| ML Frameworks       | Scikit-learn, Pandas, NumPy          |
| Backend             | Flask / FastAPI                      |
| Frontend (optional) | HTML, CSS, JavaScript                |
| Visualization       | Matplotlib, Seaborn                  |
| Database            | SQLite                               |
| Dev Tools           | VS Code, Jupyter, GitHub             |

---

## 🧠 Key Features

- ✅ **AI-Powered Disaster Prediction** using Random Forest
- 📈 **Impact Forecasting** (e.g., disaster duration, casualty estimation)
- 🚨 **Real-Time Recovery Suggestions**
- 🚑 **Relief Resource Monitoring System**
- 🧾 **User Roles** for General Public, Government, and NGOs
- 📊 **Interactive Dashboard** with visual insights

---

## 🖥️ System Architecture

- **Presentation Layer**: User Interface (Login, Dashboard)
- **Business Logic Layer**: Receives user input, triggers ML processes
- **Application Layer**: Prediction engine + Recommendation system
- **Data Layer**: Historical disaster dataset + SQLite DB

---

## 🧪 Sample Test Cases

| Feature                  | Expected Result                            | Status |
|--------------------------|---------------------------------------------|--------|
| Disaster Type Prediction | Predicts correctly with >85% F1 score       | ✅     |
| Relief Material Planner  | Warns if insufficient inventory             | ✅     |
| Recovery Plan Suggestion | Suggests valid recovery strategies          | ✅     |
| Invalid Input Handling   | Graceful message for unknown disaster types | ✅     |

---

## 🚀 Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/disaster-recovery-advisor.git
   cd disaster-recovery-advisor
