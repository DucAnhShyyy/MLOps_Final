# 🧠 Diabetes Prediction ML Workflow

An end-to-end, portable machine learning workflow for predicting the likelihood of diabetes—designed to streamline the entire process from data preparation to deployment, and make early detection more accessible.

---

## 📌 Introduction

This project presents a **portable, end-to-end machine learning pipeline** built to predict diabetes risk. It automates the flow from **data preparation**, through **training and testing machine learning models**, to **production deployment**, making it suitable for real-world applications.

---

## 🩺 Background

Traditional diabetes diagnosis methods are often time-consuming and resource-intensive. This leads to key issues:

- 🕒 **Time constraints**: Many people avoid or delay hospital visits due to busy schedules.  
- ❗ **Perceived low risk**: Some individuals consider check-ups unnecessary until symptoms become severe.

These barriers often result in **delayed detection**, increasing health risks over time.

---

## 💡 Solution

To address this challenge, we developed a **machine learning-based application** that predicts diabetes risk using **daily, self-reported data**. Features include:

- 🖥️ **Interactive web interface** for user input.
- ⚙️ **Immediate predictions** to inform health-related decisions.
- 🔄 **Deployable and reproducible ML workflow**, encouraging further use and development.

> ⚠️ **Note**: The model serves as an *early warning tool*—not a replacement for professional medical diagnosis.

---

## ⚠️ Limitation

While the tool offers fast and accessible predictions, it is subject to limitations:

- 📉 **Probabilistic results**, not deterministic.
- ⚖️ **Data quality and bias** may affect outcomes.
- 🌐 **Generalizability** across populations is not guaranteed.

> Please consult a licensed medical professional for a definitive diagnosis.

---

## 🛠️ Tech Stack

| Category         | Tools & Frameworks                             |
|------------------|-------------------------------------------------|
| 👨‍💻 Programming   | Python, Streamlit, Pytest                      |
| 📊 Monitoring     | Weights & Biases (WandB)                       |
| 🔄 CI/CD         | GitHub Actions                                 |

---

## 🚀 How to Use This Project

### 🧰 Setup & Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd <your-repo-directory>

# Install dependencies
pip install -r requirements.txt
```

### ▶️ Run the Application
```bash
# Launch the frontend app
streamlit run st_apps/frontend.py

# Launch the backend app
uvicorn st_apps.backend:api --reload
```

### 🌐 Access the Web App
👉 https://diabetes-predicted-app.streamlit.app/
