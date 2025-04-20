# 🩺 Cancer Patient Detection & Reporting System

A web-based application designed to manage patient records and medical reports for cancer detection. This project aims to simplify how healthcare professionals handle diagnostic data using a clean and efficient database-backed web system.

---

## 🚀 Project Overview

This system helps healthcare centers store, retrieve, and manage cancer-related patient data. It offers a secure login system for doctors, an intuitive dashboard, and a querying tool to explore medical reports based on doctors and patients.

The system is designed for hospitals, research centers, or personal projects to understand the basics of combining **Python (Flask)** with **MySQL** for medical data management.

---

## 💻 Tech Stack

| Technology        | Purpose                  |
|--------------------|---------------------------|
| **Python (Flask)** | Backend Web Framework     |
| **MySQL**          | Database Management       |
| **HTML / CSS**     | Frontend UI               |
| **mysql-connector-python** | Database Connector |

---

## 📂 Features

✅ Secure Admin Login  
✅ Patient & Doctor Management  
✅ Medical Reports Querying (via dropdown)  
✅ Custom SQL Query Execution (*Read-Only*)  
✅ Clean, Minimal Flask Web UI  
✅ Future-friendly for Machine Learning Integration  

---

## 🗂 Database Design

| Table Name      | Purpose                                         |
|-----------------|-------------------------------------------------|
| `Doctors`        | Stores doctor information.                     |
| `Patients`       | Stores patient demographics and references.    |
| `MedicalReports` | Holds medical diagnostic results and tests.    |

**Relationships:**  
- One **doctor** can be assigned to many **patients**.  
- One **patient** can have multiple **medical reports** over time.

---

## 🔐 Default Admin Credentials

| Username | Password |
|----------|----------|
| `admin`  | `password` |

---

## 🧠 Future Improvements

- 📌 Machine Learning Model Integration for Real-Time Cancer Prediction.
- 🌐 Multi-user role management (Doctors, Nurses, Admins).
- 🏥 Support for Electronic Health Records (EHR).
- 📊 Statistical Data Visualization for report insights.

---
