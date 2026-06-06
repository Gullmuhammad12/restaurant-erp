# 🍽️ Restaurant ERP Web Application

A **production‑ready, full‑stack Restaurant ERP** built with **Django 5**, **Bootstrap 5**, **jQuery**, and **Chart.js**.  
Features include order management, kitchen queue with real‑time updates, inventory tracking with automatic stock deduction, staff management, advanced data filtering, Excel export, and a premium dark Dribbble‑inspired UI with light/dark mode.

![Dashboard Preview](https://via.placeholder.com/800x400?text=Restaurant+ERP+Dashboard)  
*(Replace with actual screenshot)*

---

## ✨ Features

### 🔐 Authentication & Security
- Custom User model with **email as unique identifier**
- Role‑based access control (Admin, Manager, Kitchen Staff, Waiter)
- Slug‑based URLs – **no primary keys exposed** in URLs
- Login/Signup with real‑time validation and toast notifications

### 📦 Order Management
- Create, update, delete orders (Dine‑in, Takeaway, Delivery)
- Dynamic order item addition with **automatic tax calculation** (10%)
- Status workflow: Pending → Preparing → Completed / Cancelled
- **Inventory deduction** automatically triggered when order status becomes "Preparing"

### 🍳 Kitchen Management System (KMS)
- Dedicated **live kitchen queue** dashboard
- Real‑time elapsed time counter for each order
- One‑click AJAX status updates (Pending → Preparing → Completed)

### 📦 Inventory Management
- Track ingredients with units (kg, liters, pieces, etc.)
- Set low‑stock thresholds – automatic notifications when stock runs low
- Ingredient‑recipe mapping for menu items

### 👥 Staff Management
- Manage staff profiles, shifts, contact details
- Role‑based access: only Admins can edit staff

### 📊 Reporting & Export
- **Monthly revenue trends** (line chart) and **top‑selling items** (bar chart) using Chart.js
- **Export orders to Excel** – styled headers, auto‑adjusted column widths, currency formatting

### 🎨 UI/UX
- **Dark premium theme** inspired by Dribbble
- Fixed sidebar navigation, fully responsive
- **Light/Dark mode toggle** with localStorage persistence
- **Glassmorphism toast notifications** for success, error, and warning messages
- Advanced filtering (search, status, type, date range) with **Reset Filters** button

### ⚡ Real‑time & Automation
- Notification bell with live low‑stock alerts
- Kitchen queue refreshes every 10 seconds via AJAX
- Automatic inventory deduction when order starts preparing

---

## 🛠️ Tech Stack

| Layer          | Technology                                      |
|----------------|-------------------------------------------------|
| Backend        | Django 5.x (Class‑Based Generic Views)         |
| Frontend       | Bootstrap 5, jQuery 3.7+, Chart.js             |
| Icons          | Font Awesome 6 (Free)                          |
| Database       | SQLite (default) – can be switched to PostgreSQL/MySQL |
| Excel Export   | openpyxl                                        |
| Authentication | Django’s built‑in auth with Custom User Model  |
| Real‑time      | AJAX polling (every 10s for kitchen)           |

---

## 📁 Project Structure
