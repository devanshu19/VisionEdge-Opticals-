# Original UI Prototypes & Interface Design Document
### *for*
# VisionEdge: AI-Powered Optical Store Management & Virtual Try-On System

**Version:** 1.0  
**Design System:** Bootstrap 5.3 + Custom CSS Variables + Dark/Light Theme Switching  
**Interactions:** MediaPipe Computer Vision, Canvas API, AOS Animations, Swiper Carousel  
**Date:** August 2026  

---

## Table of Contents

- [1. Design System & UI Architecture](#1-design-system--ui-architecture)
- [2. Page Layout Prototype Specifications](#2-page-layout-prototype-specifications)
  - [2.1 Prototype 1: Homepage & Customer Landing (`index.html`)](#21-prototype-1-homepage--customer-landing-indexhtml)
  - [2.2 Prototype 2: Authentication Suite (`login.html` & `signup.html`)](#22-prototype-2-authentication-suite-loginhtml--signuphtml)
  - [2.3 Prototype 3: Staff & Customer Dashboard (`dashboard.html`)](#23-prototype-3-staff--customer-dashboard-dashboardhtml)
  - [2.4 Prototype 4: Clinical Eye Exam & AI OCR Scanner (`eye-test.html`)](#24-prototype-4-clinical-eye-exam--ai-ocr-scanner-eye-testhtml)
  - [2.5 Prototype 5: Virtual Try-On Suite & Frame Catalog (`frames.html` & `products.html`)](#25-prototype-5-virtual-try-on-suite--frame-catalog-frameshtml--productshtml)
  - [2.6 Prototype 6: AI Lens Recommendation Engine (`lens-recommendation.html`)](#26-prototype-6-ai-lens-recommendation-engine-lens-recommendationhtml)
  - [2.7 Prototype 7: Checkout & POS Invoicing (`checkout.html`)](#27-prototype-7-checkout--pos-invoicing-checkouthtml)
  - [2.8 Prototype 8: Prescriptions, Orders & Payment History (`prescriptions.html`, `orders.html`, `payment-history.html`)](#28-prototype-8-prescriptions-orders--payment-history-prescriptionshtml-ordershtml-payment-historyhtml)
- [3. Component Design System & Responsive Breakpoints](#3-component-design-system--responsive-breakpoints)

---

## 1. Design System & UI Architecture

The VisionEdge user interface is built on a responsive Bootstrap 5.3 foundation augmented with modern CSS variable design tokens, glassmorphism cards, and dynamic light/dark theme switching stored in local storage (`data-bs-theme`).

### Core Design Tokens & Palette:

```css
:root {
    --primary-color: #2563eb;      /* Royal Blue (Primary Action/Buttons) */
    --secondary-color: #0f172a;    /* Slate Navy (Headers & Hero Overlay) */
    --accent-color: #06b6d4;       /* Neon Cyan (AI Highlights & Badges) */
    --success-color: #10b981;      /* Emerald Green (Active/Completed Status) */
    --warning-color: #f59e0b;      /* Amber (Pending Alerts & Low Stock) */
    --card-bg: #ffffff;            /* Card Container Background */
    --text-muted: #64748b;         /* Muted Subtitles & Labels */
    --border-radius-lg: 16px;      /* Rounded Large Card Radius */
    --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.1);
    --shadow-lg: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
}
```

### Global Shared Components:
1. **Top Navigation Bar (`navbar-container`)**:
   * Brand Logo: `VisionEdge Opticals` with icon `<i class="bi bi-eye"></i>`.
   * Main Nav Links: `Home`, `Frames & VTO`, `Lenses`, `Eye Test`, `AI Recommendations`, `About`.
   * Utility Actions: Light/Dark Theme Switcher toggle, Shopping Cart badge, Wishlist counter, User Profile avatar.
2. **Global Preloader (`#loader`)**:
   * Centered CSS spinner with smooth fade-out animation upon page mount.
3. **Footer (`footer-container`)**:
   * 4-column layout: Store Branding, Quick Links, Optical Care Services, Store Location & Contact Details.

---

## 2. Page Layout Prototype Specifications

### 2.1 Prototype 1: Homepage & Customer Landing (`index.html`)

The entry point for retail customers showcasing eyewear collections and computer vision AR features.

```
+-----------------------------------------------------------------------------------+
|  [LOGO] VisionEdge   Home  Frames & VTO  Lenses  Eye Test  AI Tools  [Theme] (User)|
+-----------------------------------------------------------------------------------+
|  HERO SECTION (Video Background + Gradient Overlay)                              |
|  "See The Future with Precision Eyewear"                                          |
|  "AI-Powered Prescription Scanning & 3D Virtual Try-On"                          |
|  [Explore Frames & Try On]   [Book Free Eye Test]                                 |
+-----------------------------------------------------------------------------------+
|  ENGINEERED FOR COMFORT (Category Cards)                                         |
|  +--------------------+  +--------------------+  +--------------------+          |
|  |  Titanium Frames   |  |  Premium Acetate   |  | TR90 Memory Flex   |          |
|  |  50% Lighter       |  |  Hand-polished     |  | Ultra-flexible     |          |
|  |  [Shop Titanium]   |  |  [Shop Acetate]    |  | [Shop TR90]        |          |
|  +--------------------+  +--------------------+  +--------------------+          |
+-----------------------------------------------------------------------------------+
|  PROMOTIONAL BANNER: VIRTUAL TRY-ON ROOM                                          |
|  "Try Frames Before You Buy with Real-Time 3D Webcam Tracking"                    |
|  [Launch 3D Virtual Try-On]                                                       |
+-----------------------------------------------------------------------------------+
```

Key UI Interactions:
* Video background player (`hero-video`) with dark linear gradient overlay (`hero-overlay`).
* Dynamic text animation powered by Typed.js highlighting optical benefits.
* Category cards with hover lift animations (`transform: translateY(-5px)`).

---

### 2.2 Prototype 2: Authentication Suite (`login.html` & `signup.html`)

Provides secure JWT access for Store Administrators, Optometrists/Staff, and Customers.

```
+-----------------------------------------------------------------------------------+
|                                                                                   |
|    +--------------------------------+----------------------------------------+    |
|    | BRAND CARD (Left Col)          | LOGIN FORM (Right Col)                 |    |
|    |                                |                                        |    |
|    | VisionEdge Opticals            | Welcome Back 👋                        |    |
|    | AI-Powered Management System   | Please enter your account credentials   |    |
|    |                                |                                        |    |
|    | [Eye Icon Graphic]             | Role Selector:                         |    |
|    | * Admin Control                | ( ) Admin   (•) Staff   ( ) Customer   |    |
|    | * Staff POS & Eye Exams        |                                        |    |
|    | * Customer VTO Suite           | Username / Email: [__________________] |    |
|    |                                | Password:         [__________________] |    |
|    |                                | [ ] Remember Me      [Forgot Password?]|    |
|    |                                |                                        |    |
|    |                                | [======= SIGN IN TO DASHBOARD =======] |    |
|    |                                |                                        |    |
|    |                                | Don't have an account? [Sign Up]       |    |
|    +--------------------------------+----------------------------------------+    |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

Key UI Interactions:
* Role selector radio pills allowing instant credential routing.
* Toggle password visibility eye icon.
* Form validation with interactive error popups.

---

### 2.3 Prototype 3: Staff & Customer Dashboard (`dashboard.html`)

Central workspace for managing clinical tasks, orders, saved prescriptions, and store metrics.

```
+-----------------------------------------------------------------------------------+
|  [LOGO] VisionEdge   Dashboard  Customers  Eye Exam  VTO  Orders  [Theme] (Profile) |
+-----------------------------------------------------------------------------------+
| SIDEBAR (Col 3)         | MAIN DASHBOARD CONTENT (Col 9)                          |
|                         |                                                         |
| [User Avatar]           | Welcome back, Staff Administrator! 👋                    |
| Rahul Sharma (Staff)    |                                                         |
| staff@visionedge.com    | +----------------+ +----------------+ +----------------+ |
| ----------------------- | | Active Orders  | | Prescriptions  | | Reward Points  | |
| [•] Dashboard           | |      3         | |      2         | |     150        | |
| [ ] Customer CRM        | +----------------+ +----------------+ +----------------+ |
| [ ] Eye Exam & AI OCR   |                                                         |
| [ ] Virtual Try-On      | RECENT ORDERS & CLINICAL QUEUE                          |
| [ ] Orders & Inventory  | +---------+--------------+--------------+-------------+ |
| [ ] Prescriptions       | | Order   | Customer     | Prescription | Status      | |
| [ ] Billing & Invoices  | +---------+--------------+--------------+-------------+ |
| ----------------------- | | ORD-101 | Rahul Sharma | RX-2026-04   | Ready       | |
| [ ] Account Settings    | | ORD-102 | Priya Patel  | RX-2026-05   | Processing  | |
| [x] Logout              | +---------+--------------+--------------+-------------+ |
+-------------------------+---------------------------------------------------------+
```

Key UI Interactions:
* Sticky sidebar with active tab navigation states (`.nav-link.active`).
* KPI stat cards displaying numeric counters with background opacity icons.

---

### 2.4 Prototype 4: Clinical Eye Exam & AI OCR Scanner (`eye-test.html`)

Enables optometrists to record clinical diopters or scan physical prescription scans using Google Gemini AI.

```
+-----------------------------------------------------------------------------------+
|  CLINICAL EYE EXAMINATION & AI PRESCRIPTION SCANNER                               |
+-----------------------------------------------------------------------------------+
|  LEFT PANEL: AI OCR PRESCRIPTION SCAN   | RIGHT PANEL: CLINICAL DIOPTER INPUTS    |
|                                         |                                         |
|  +-----------------------------------+  | Customer: [ Rahul Sharma (CUST-001) v ] |
|  | DRAG & DROP PRESCRIPTION SCAN     |  | Store:    [ Tech City Mall Branch   v ] |
|  | [ Upload Image: JPG / PNG ]       |  | Doctor:   [ Dr. Smith (Optometrist) v ] |
|  |                                   |  |                                         |
|  | [ Image Preview: RX_Scan_01.jpg ] |  | RIGHT EYE (OD):                         |
|  |                                   |  | SPH: [-1.25]  CYL: [-0.50]  AXIS: [90]  |
|  | [=== RUN GEMINI AI OCR SCAN ===]  |  |                                         |
|  +-----------------------------------+  | LEFT EYE (OS):                          |
|  AI EXTRACTION RESULT:                  | SPH: [-1.50]  CYL: [-0.75]  AXIS: [180] |
|  Status: [ Green Badge: Success 98% ]   |                                         |
|  Extracted: SPH -1.25, CYL -0.50, AX 90  | ADD POWER: [+2.00]   PD: [62 mm]        |
|  [ Apply AI Values to Form ]            | [ Save Eye Exam ]  [ Proceed to VTO ->] |
+-----------------------------------------+-----------------------------------------+
```

Key UI Interactions:
* Drag-and-drop file upload container with instant canvas preview.
* Progress spinner during Gemini API processing.
* Auto-fill button transferring parsed JSON values into form inputs.

---

### 2.5 Prototype 5: Virtual Try-On Suite & Frame Catalog (`frames.html` & `products.html`)

Interactive browser room where customers preview spectacle frames on their face via webcam.

```
+-----------------------------------------------------------------------------------+
|  3D VIRTUAL TRY-ON EYECATALOG ROOM                                                |
+-----------------------------------------------------------------------------------+
|  WEBCAM LIVE FEED CANVAS (Center Area)        | RIGHT CONTROL PANEL               |
|  +-----------------------------------------+  |                                   |
|  |                                         |  | SELECTED FRAME SPECS              |
|  |       [ Video Feed with Face Mesh ]     |  | Ray-Ban Wayfarer Classic          |
|  |           ( . . Facial Grid . . )       |  | Frame Code: FRM-001               |
|  |           |___Spectacle Overlay___|     |  | Shape: Square                     |
|  |                                         |  | Material: Premium Acetate         |
|  |                                         |  | Price: ₹4,500                     |
|  +-----------------------------------------+  |                                   |
|  AI DETECTED TAG:                             | FRAME COLORS:                     |
|  "Face Shape: Oval -> Match Rating 95%"        | (•) Black  ( ) Tortoise  ( ) Blue  |
|                                               |                                   |
|  [ Camera On/Off ]  [ Take Snapshot ]         | [ Add to Order ] [ Wishlist ]     |
+-----------------------------------------------+-----------------------------------+
|  FRAME SELECTION CAROUSEL                                                         |
|  +--------------+  +--------------+  +--------------+  +--------------+       |
|  | Ray-Ban Square|  | Oakley Holbr |  | Vogue Cat-Eye|  | Titan Metal  |       |
|  | ₹4,500       |  | ₹5,200       |  | ₹3,800       |  | ₹2,900       |       |
|  | [Try On Now] |  | [Try On Now] |  | [Try On Now] |  | [Try On Now] |       |
|  +--------------+  +--------------+  +--------------+  +--------------+       |
+-----------------------------------------------------------------------------------+
```

Key UI Interactions:
* HTML5 MediaPipe face mesh canvas video stream.
* Frame carousel switcher updating the active overlay PNG in real time.
* Canvas snapshot generator producing downloadable try-on photos.

---

### 2.6 Prototype 6: AI Lens Recommendation Engine (`lens-recommendation.html`)

Suggests optimal lens designs and coatings based on prescription diopters.

```
+-----------------------------------------------------------------------------------+
|  AI OPTICAL LENS RECOMMENDATION ENGINE                                            |
+-----------------------------------------------------------------------------------+
|  PRESCRIPTION INPUT PARAMETERS                 | AI LENS RECOMMENDATION RESULTS   |
|  Customer: Rahul Sharma                        |                                  |
|  Prescription: SPH -2.50, CYL -0.75, ADD +2.00 | Recommended Design:              |
|  Usage: 8+ Hours Screen Time (Digital Devices) | [ Badge: Progressive Lens ]      |
|                                                | High near-addition power (+2.00)  |
|  SELECT LENS COATINGS:                         | requires seamless multifocal.    |
|  [x] Anti-Reflective (Crizal)                  |                                  |
|  [x] Blue Cut (Digital Protection)             | Recommended Coating:             |
|  [ ] Photochromic (Sun-Adaptive)               | [ Badge: Zeiss BlueGuard ]       |
|                                                | Blocks harmful 420nm blue light. |
|  [=== GENERATE AI RECOMMENDATION ===]          | Price: ₹3,500                    |
|                                                | [ Select Lens for Order ]        |
+------------------------------------------------+----------------------------------+
```

---

### 2.7 Prototype 7: Checkout & POS Invoicing (`checkout.html`)

Point-of-Sale checkout interface calculating items, GST taxes, and issuing invoices.

```
+-----------------------------------------------------------------------------------+
|  POINT OF SALE CHECKOUT & BILLING                                                 |
+-----------------------------------------------------------------------------------+
|  ITEMIZED ORDER SUMMARY (Left Col 7)            | BILLING & TAX BREAKDOWN (Col 5) |
|  +-------------------------------------------+  |                                 |
|  | Item                    Qty   Price Total |  | Subtotal:              ₹8,000.00 |
|  +-------------------------------------------+  | Discount:               - ₹500.00 |
|  | Ray-Ban Wayfarer Frame   1   ₹4,500 ₹4,500 |  | Taxable Amount:        ₹7,500.00 |
|  | Zeiss BlueGuard Lens     1   ₹3,500 ₹3,500 |  | GST Tax (18%):         ₹1,350.00 |
|  +-------------------------------------------+  | ------------------------------- |
|                                                 | NET PAYABLE TOTAL:     ₹8,850.00 |
|  CUSTOMER DETAILED INFO:                        |                                 |
|  Name:  Rahul Sharma  (CUST-001)                | PAYMENT TENDER METHOD:          |
|  Phone: 9812345678                              | (•) Cash   ( ) Card   ( ) UPI   |
|  City:  Mumbai                                  |                                 |
|                                                 | [=== COMPLETE BILL & PRINT ===] |
|  [ + Add Frame Item ]   [ + Add Lens Item ]     | [ Download PDF Invoice ]        |
+-------------------------------------------------+---------------------------------+
```

---

### 2.8 Prototype 8: Prescriptions, Orders & Payment History (`prescriptions.html`, `orders.html`, `payment-history.html`)

Customer history portal for viewing past medical eye tests and order receipts.

```
+-----------------------------------------------------------------------------------+
|  CUSTOMER SAVED PRESCRIPTIONS & ORDER HISTORY                                    |
+-----------------------------------------------------------------------------------+
|  PRESCRIPTION HISTORY (Card View)               | SALES ORDERS HISTORY            |
|  +-------------------------------------------+  | +-----------------------------+ |
|  | Prescription #: RX-2026-04                |  | | Order #: ORD-1001           | |
|  | Date: 15 Aug 2026 | Dr. Smith              |  | | Date: 15 Aug 2026           | |
|  | OD: SPH -1.25  CYL -0.50  AX 90           |  | | Total: ₹8,850.00            | |
|  | OS: SPH -1.50  CYL -0.75  AX 180          |  | | Status: [ Green: Delivered] | |
|  | [ View Scan Image ]  [ Download PDF ]     |  | | [ Download PDF Invoice ]    | |
|  +-------------------------------------------+  | +-----------------------------+ |
+-------------------------------------------------+---------------------------------+
```

---

## 3. Component Design System & Responsive Breakpoints

### Target Breakpoints:
* **Desktop Grid (`>= 1200px`)**: Full multi-column view with sidebar navigation.
* **Tablet Grid (`768px - 1199px`)**: Collapsible sidebar drawer, 2-column card layouts.
* **Mobile Web View (`< 768px`)**: Stacked single-column layouts with off-canvas slide-out navbar menu.

---
*End of UI Prototypes & Interface Design Document for VisionEdge.*
