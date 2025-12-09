# 🧾 Expense Tracker — Django Project

A simple but powerful Expense Tracking web application built with **Django**, featuring:

- User authentication (login/signup/logout)
- Create, view, filter and delete transactions
- Category management (income/expense categories)
- Dashboard with totals + recent transactions
- Monthly financial report with category breakdown
- CSV export for offline usage (Excel/Sheets compatible)

---

## 🚀 Features

### 🔐 Authentication
- User registration & login  
- Per-user data isolation (each user sees only their own categories & transactions)

### 💸 Transactions
- Add income/expense entries  
- Sort & filter by month  
- Delete functionality with confirmation  
- CSV export including:
  - date  
  - category  
  - amount  
  - description  
  - type  

### 🗂 Categories
- Create custom categories  
- Categories are user-specific  
- Edit & delete  
- Prevent accidental deletion if category is in use (optional improvement)

### 📊 Dashboard
- Total income
- Total expenses
- Net savings
- Last 5 transactions preview
- Quick access to add/view transactions

### 📅 Monthly Report
- Select month (YYYY-MM)
- See:
  - total income  
  - total expenses  
  - net (income – expenses)  
  - category-wise breakdown with percentages  

---

## 🛠️ Tech Stack

- **Django**
- **SQLite** (default, easy for dev)
- **Bootstrap 5** for styling
- Python 3.10+ (recommended)
- Uses Django Template Language (DTL) for frontend

---

## 📦 Installation & Setup

Follow these steps to run the project locally:

### 1️⃣ Clone the repository

```bash
git clone https://github.com/saxamrawat/expense-tracker.git
cd expense-tracker
