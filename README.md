# VisionEdge Opticals 👓
### Smart Optical Store, Virtual Try-On (VTO) & Practice Management System

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Netlify-00C7B7?style=for-the-badge&logo=netlify)](https://visionopticals.netlify.app)
[![Backend API](https://img.shields.io/badge/API-Render-46E3B7?style=for-the-badge&logo=render)](https://visionedge-opticals.onrender.com/api/payment/razorpay/config)
[![Database](https://img.shields.io/badge/Database-Supabase%20PostgreSQL-3ECF8E?style=for-the-badge&logo=supabase)](https://supabase.com)
[![Payment](https://img.shields.io/badge/Payment-Razorpay%20Verified-02042B?style=for-the-badge&logo=razorpay)](https://razorpay.com)

---

## 🌟 Live Deployments

- **Frontend Web Application (Netlify)**: [https://visionopticals.netlify.app](https://visionopticals.netlify.app)
- **Production REST API (Render)**: [https://visionedge-opticals.onrender.com](https://visionedge-opticals.onrender.com)
- **GitHub Repository**: [https://github.com/devanshu19/VisionEdge-Opticals-](https://github.com/devanshu19/VisionEdge-Opticals-)

---

## 📌 Project Overview

**VisionEdge Opticals** is a full-stack, enterprise-grade optical retail, virtual try-on, practice management, and e-commerce platform. It integrates modern web technologies, AI-powered prescription parsing, interactive real-time canvas Virtual Try-On, an authoritative inventory management engine, and bank-grade payment processing with instant GST tax invoice generation.

---

## 🚀 Key Features

### 🛒 E-Commerce & Customer Experience
- **Interactive Eyewear Catalog**: 25 curated, photorealistic frames and lenses across 5 categories:
  - Eyeglasses (Wayfarer, Round Metal, Browline, Crystal Clear, Titanium Square)
  - Sunglasses (Aviator, Sport Wayfarer, Round Vintage, Glamour Cat-Eye, Hexagonal)
  - Computer & Blue-Block Glasses (Shield Transparent, Matte Anti-Glare, Ray-Cut, Pro Gamer Amber, Executive Workstation)
  - Contact & Optical Lenses (Acuvue Oasys, Daily Disposable, High-Index 1.67, Progressive Precision, Blue-Defense)
  - Kids Eyewear (Flexible Blue TR90, Dark Blue Oval, Junior Red-Black, Teal Sporty, Coral Pink Oval)
- **Virtual Try-On (VTO)**: Live face and frame superposition with high-definition transparent PNG cutouts.
- **Cart & Dynamic Pricing**: Real-time persistent cart, coupon discount engine (`VISION30`, `BOGO2026`, `STUDENT15`, `FREESHIP`), and seamless checkout synchronization.
- **Customer Portal**: Account profile, order tracking, downloadable GST tax invoices, and prescription history.

### 💳 Payment & Invoicing Gateway
- **Razorpay Standard Checkout**: 256-bit bank-grade encryption with support for UPI (Google Pay, PhonePe, Paytm, BHIM), Credit/Debit Cards, NetBanking, and Wallets.
- **Cash on Delivery (COD)**: Doorstep collection option with instant order confirmation.
- **PayU Sandbox Gateway**: Redundant secondary payment gateway integration.
- **Automated GST Tax Invoices**: Generates authentic, downloadable computer-generated 18% GST Tax Invoices (PDF format) upon payment verification.

### 🛡️ Admin Portal & Practice Management
- **Single Passcode Access**: Streamlined authentication for store managers at `/admin/` with pass: `Dev@7272`.
- **Real-Time Inventory (CRUD)**: Complete Create, Read, Update, and Delete operations synced directly to **Supabase PostgreSQL**.
- **Payment Gateway Settings**: Manage and verify Razorpay API keys (`RAZORPAY_KEY_ID`, `RAZORPAY_KEY_SECRET`) directly from the admin interface.
- **Sales & Transaction Analytics**: Real-time sales charts, volume metrics, and refund controls.

---

## 🏗️ Architecture & Tech Stack

| Layer | Technologies |
|---|---|
| **Frontend** | HTML5, CSS3, JavaScript (ES6+), Bootstrap 5.3.2, Bootstrap Icons, AOS Animations, Canvas VTO |
| **Backend** | Python 3.11+, Flask 3.0, Flask-JWT-Extended, Flask-SQLAlchemy, FPDF2, Psycopg2-binary |
| **Payment Gateway** | Official Razorpay Python SDK & Checkout JS, PayU Sandbox |
| **Database** | Supabase Cloud PostgreSQL (Supavisor Transaction Pooler, Port 6543) / SQLite offline fallback |
| **Cloud Hosting** | Netlify (Static Frontend SPA with API Proxy), Render (PaaS Web Service for Flask) |

---

## 📁 Repository Structure

```
VisionEdge/
├── frontend/                     # Frontend Client Application
│   ├── index.html                # Home Landing Page
│   ├── products.html             # Eyewear Catalog & Category Filters
│   ├── checkout.html             # Multi-gateway Checkout & Order Summary
│   ├── cart.html                 # Cart View & Line Item Editor
│   ├── login.html                # Customer Authentication
│   ├── signup.html               # Registration & Profile Creation
│   ├── orders.html               # Order History & Tracking
│   ├── payment-success.html      # Order Confirmation & PDF Download
│   ├── payment-failed.html       # Retry Payment Portal
│   ├── admin/                    # Store Management Portal
│   │   ├── index.html            # Admin Passcode Sign-In (Dev@7272)
│   │   ├── dashboard.html        # Analytics & Metric Counters
│   │   ├── inventory.html        # Supabase Real-Time Inventory CRUD
│   │   ├── settings.html         # Payment Gateway Credentials & Settings
│   │   └── billing-history.html  # Invoice Archive & Downloads
│   └── assets/                   # CSS, JS, & Media Assets
│       ├── js/checkout.js        # Razorpay & COD Controller
│       ├── js/cart.js            # Cart Management
│       └── js/products.js        # Catalog Renderer
├── backend/                      # Python Flask Backend Service
│   ├── app.py                    # Application Entrypoint & CORS Config
│   ├── config.py                 # Supabase PostgreSQL & Gateway Config
│   ├── models.py                 # SQLAlchemy Relational Models (24 tables)
│   ├── routes/
│   │   ├── razorpay_routes.py    # Order Creation, Signature Verification, Admin Creds
│   │   ├── order_routes.py       # Order Fulfillment & COD Processing
│   │   ├── billing_routes.py     # Billing & Invoice Lookups
│   │   └── inventory_routes.py   # Real-Time Supabase Product CRUD
│   └── utils/
│       └── pdf_generator.py      # GST Tax Invoice PDF Engine
├── docs/                         # Project Documentation & Reports
│   ├── reports/                  # Project Report (DOCX)
│   ├── presentations/            # Project Review Slides (PPTX)
│   ├── srs/                      # Software Requirements Specification (DOCX)
│   └── diagrams/                 # Database ER Diagrams (PNG, SVG)
├── netlify.toml                  # Netlify Publish & Proxy Configuration
└── render.yaml                   # Render Cloud Deployment Blueprint
```

---

## ⚙️ Local Setup Instructions

### 1. Clone Repository
```bash
git clone https://github.com/devanshu19/VisionEdge-Opticals-.git
cd VisionEdge-Opticals-
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
python app.py
```
*Backend runs locally at `http://127.0.0.1:5000`.*

### 3. Frontend Setup
In a new terminal:
```bash
cd frontend
python -m http.server 8000
```
*Open `http://localhost:8000` in your web browser.*

---

## 🌐 Deploying to Netlify in 3 Simple Steps

1. Log into your [Netlify Dashboard](https://app.netlify.com/).
2. Click **"Add new site" &rarr; "Import an existing project" &rarr; "GitHub"**.
3. Select `devanshu19/VisionEdge-Opticals-`.
4. Netlify will automatically detect [netlify.toml](netlify.toml):
   - **Publish directory**: `frontend`
   - **Build command**: *(empty)*
5. Click **"Deploy site"** — your project is instantly live!

---

## 👨‍💻 Author & Credits

- **Developer**: Devanshu Chaudhari ([@devanshu19](https://github.com/devanshu19))
- **Project**: VisionEdge Opticals System
- **License**: MIT
