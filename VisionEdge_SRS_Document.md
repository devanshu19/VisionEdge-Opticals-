# Software Requirements Specification
### *for*
# VisionEdge: AI-Powered Optical Store Management & Virtual Try-On System

**Version 1.0**  
**Academic Context:** Computer Science & Engineering / Information Technology — Major Project  
**Author:** VisionEdge Development Team  
**Date:** August 2026  

---

## Table of Contents

- [1. Introduction](#1-introduction)
  - [1.1 Purpose](#11-purpose)
  - [1.2 Scope](#12-scope)
  - [1.3 Definitions, Acronyms, and Abbreviations](#13-definitions-acronyms-and-abbreviations)
  - [1.4 References](#14-references)
  - [1.5 Overview](#15-overview)
- [2. Problem Statement](#2-problem-statement)
- [3. Objectives](#3-objectives)
- [4. Literature Survey](#4-literature-survey)
- [5. Requirements Specification](#5-requirements-specification)
  - [5.1 Introduction](#51-introduction)
  - [5.2 Functional Requirements](#52-functional-requirements)
  - [5.3 Non-Functional Requirements](#53-non-functional-requirements)
  - [5.4 User Roles](#54-user-roles)
  - [5.5 Assumptions and Constraints](#55-assumptions-and-constraints)
  - [5.6 External Interface Requirements](#56-external-interface-requirements)
    - [5.6.1 User Interface](#561-user-interface)
    - [5.6.2 Hardware Interface](#562-hardware-interface)
    - [5.6.3 Software Interface](#563-software-interface)
    - [5.6.4 Communication Interface](#564-communication-interface)
- [6. Feasibility Analysis](#6-feasibility-analysis)
  - [6.1 Technical Feasibility](#61-technical-feasibility)
  - [6.2 Economic Feasibility](#62-economic-feasibility)
  - [6.3 Legal Feasibility](#63-legal-feasibility)
  - [6.4 Operational Feasibility](#64-operational-feasibility)
  - [6.5 Schedule Feasibility](#65-schedule-feasibility)
- [7. Technology Stack](#7-technology-stack)
- [8. Data Dictionary](#8-data-dictionary)
  - [8.1 Table: user](#81-table-user)
  - [8.2 Table: customer](#82-table-customer)
  - [8.3 Table: eye_test & prescription](#83-table-eye_test--prescription)
  - [8.4 Table: frame & lens](#84-table-frame--lens)
  - [8.5 Table: order & billing](#85-table-order--billing)
  - [8.6 Role-Based Access Control (RBAC) & Security Policy Summary](#86-role-based-access-control-rbac--security-policy-summary)

---

## 1. Introduction

### 1.1. Purpose
This document specifies the Software Requirements Specification (SRS) for **VisionEdge**, an end-to-end web platform designed to streamline optical store management, eye test recording, prescription digitization via Artificial Intelligence, face-shape frame recommendation, real-time interactive Virtual Try-On (VTO), inventory tracking, order fulfillment, and GST-compliant invoicing. 

This SRS serves as a technical blueprint for project developers, academic advisors, evaluators, and system administrators. It rigorously details both functional and non-functional requirements in compliance with **IEEE Std 830-1998** standards.

### 1.2. Scope
VisionEdge is a full-stack, AI-integrated web application comprising a Python Flask RESTful backend API and a responsive modern JavaScript/CSS frontend client. It provides a centralized digital ecosystem for optical retail management while introducing interactive computer vision tools directly to customers and staff.

**The system will:**
* Provide secure Role-Based Access Control (RBAC) supporting **Admin**, **Staff/Optometrist**, and **Customer** user roles via JWT token authentication.
* Maintain comprehensive Customer Relationship Management (CRM) including demographic records, medical history, eye condition profiles, and past prescriptions.
* Enable staff to record detailed clinical Eye Test parameters (OD/OS Sphere, Cylinder, Axis, Add Power, and Pupillary Distance).
* Digitally parse handwritten or printed prescription images using Google Gemini 1.5 Pro AI Vision OCR API, auto-extracting optical values into structured fields.
* Provide an interactive, canvas-based **Virtual Try-On (VTO)** engine allowing customers to preview spectacle frames live via webcam feed or uploaded photo.
* Execute automated AI recommendation models matching frame geometry to customer face shapes (Oval, Round, Square, Heart) and suggesting optical lens coatings (Blue-Cut, Anti-Reflective, Progressive, Photochromic) based on clinical prescription data.
* Manage dual inventory for spectacle frames and lenses, enforcing real-time stock reduction upon sales and low-stock alerts.
* Handle end-to-end order processing, payment status tracking, and automated PDF invoice generation with tax (GST) calculations.
* Host an AI Optical Assistant Chatbot for automated customer inquiry resolution.

**The system will NOT (in version 1.0):**
* Process direct credit card or online payment gateway transactions (transactions are registered as Cash, UPI, or Card at counter/POS).
* Require hardware-based automated refractometers or Bluetooth-connected optical devices (clinical values are entered manually or scanned via OCR).
* Perform clinical eye diagnostics or replace certified optometrists (AI outputs are advisory and subject to staff verification).

### 1.3. Definitions, Acronyms, and Abbreviations

| Term | Definition |
| :--- | :--- |
| **SRS** | Software Requirements Specification |
| **VTO** | Virtual Try-On — an interactive computer vision feature rendering digital 2D/3D frames onto a facial overlay |
| **OCR** | Optical Character Recognition — technology used to extract text and numbers from optical prescription images |
| **OD** | *Oculus Dexter* — standard medical abbreviation for the Right Eye |
| **OS** | *Oculus Sinister* — standard medical abbreviation for the Left Eye |
| **SPH** | Sphere — optical lens power measured in diopters for nearsightedness or farsightedness |
| **CYL** | Cylinder — optical power for astigmatism correction |
| **AXIS** | Axis — orientation angle (0 to 180 degrees) of the cylinder power |
| **ADD** | Add Power — magnifying power added to the bottom of multifocal/progressive lenses |
| **PD** | Pupillary Distance — distance in millimeters between the centers of the pupils |
| **RBAC** | Role-Based Access Control — restriction of system access based on user roles (Admin, Staff, Customer) |
| **JWT** | JSON Web Token — secure compact URL-safe mechanism for transmitting claims between server and client |
| **REST** | Representational State Transfer — software architectural style for stateless web services |
| **CRUD** | Create, Read, Update, Delete — fundamental persistence operations on database entities |

### 1.4. References
* **IEEE Std 830-1998**: *IEEE Recommended Practice for Software Requirements Specifications*.
* **Flask Documentation**: https://flask.palletsprojects.com/
* **SQLAlchemy & PyMySQL Documentation**: https://docs.sqlalchemy.org/
* **Google Gemini AI API Documentation**: https://ai.google.dev/docs
* **OpenCV / MediaPipe Vision Documentation**: https://google.github.io/mediapipe/
* **"Digital Transformation in Optical Retail Management"**, *International Journal of Computer Applications in Retail & Logistics*, 2024.
* **"Augmented Reality and Virtual Try-On Architectures for E-Commerce"**, *IEEE Transactions on Human-Machine Systems*, 2025.

### 1.5. Overview
The remainder of this document is organized into seven key sections:
* **Section 2 (Problem Statement)** highlights current optical industry operational bottlenecks.
* **Section 3 (Objectives)** defines project goals.
* **Section 4 (Literature Survey)** reviews existing solution paradigms and research gaps.
* **Section 5 (Requirements Specification)** outlines detailed Functional, Non-Functional, User Role, and Interface requirements.
* **Section 6 (Feasibility Analysis)** evaluates technical, economic, legal, operational, and schedule viability.
* **Section 7 (Technology Stack)** details software libraries, frameworks, and deployment components.
* **Section 8 (Data Dictionary)** provides entity schemas and security access policies.

---

## 2. Problem Statement

Traditional optical retail stores and brick-and-mortar optometry practices suffer from significant operational inefficiencies and fragmented customer experiences. Conventional practices rely heavily on manual paper-based clinical notes, physical binder record-keeping, and disconnected point-of-sale cash registers. 

Key challenges faced by current optical retailers include:
1. **Manual Prescription Errors**: Manual transcriptions of complex optical formulas (OD/OS sphere, cylinder, axis, prism) into sales orders lead to human error, incorrect lens fabrication, and customer dissatisfaction.
2. **Lack of Automated Personalization**: Customers often struggle to select appropriate spectacle frames that suit their physical face shape, leading to prolonged decision times and indecision.
3. **Absence of Virtual Try-On Technologies**: Brick-and-mortar stores limit try-ons to physical inventory in stock, while traditional e-commerce sites lack interactive preview tools to evaluate frame fit virtually.
4. **Inventory & Prescription Fragmentation**: Customer clinical eye exam records, lens stock levels, frame inventories, and billing invoices are managed across separate tools, creating stockouts, unfulfilled orders, and accounting overhead.
5. **No Integrated Clinical-to-Sales Workflow**: Optometrists lack a seamless tool to instantly push eye test measurements to the sales counter for frame recommendation, lens coating selection, and billing.

VisionEdge addresses this gap by synthesizing clinical eye test management, AI-driven OCR prescription extraction, face-shape recommendation algorithms, real-time webcam Virtual Try-On, inventory control, and automated billing into a single, cohesive software platform.

---

## 3. Objectives

* To design and implement a secure, scalable web-based optical store management system supporting multi-role authentication (Admin, Staff, Customer).
* To integrate an AI Vision OCR engine (Google Gemini 1.5 Pro) capable of extracting structured prescription parameters (OD/OS SPH, CYL, AXIS, ADD, PD) from image scans with high confidence scores.
* To build an interactive, browser-based **Virtual Try-On (VTO)** canvas application leveraging computer vision overlay techniques for real-time frame preview.
* To construct intelligent recommendation engines that evaluate face shapes (Oval, Round, Square, Heart) and prescription severity to suggest optimal frame geometry and lens coatings (Blue-Cut, Anti-Reflective, High-Index).
* To establish a unified database schema connecting customers, clinical appointments, eye tests, prescriptions, frame/lens stock, purchase orders, and PDF invoices.
* To enforce robust Role-Based Access Control (RBAC) ensuring data isolation and operational compliance across staff and administrative workflows.
* To evaluate system performance, UI responsiveness, and AI extraction accuracy through empirical validation in a simulated optical store environment.

---

## 4. Literature Survey

| # | Study / Platform | Focus | Gap Identified |
| :---: | :--- | :--- | :--- |
| **1** | Generic Retail POS Apps (QuickBooks, Tally) | Standard retail inventory and billing management | Lacks specialized optical data structures (OD/OS prescription parameters, lens refractive index, frame dimensions, cylinder axis tracking). |
| **2** | Optical Store Software (MyVisionExpress, FlexOptical) | Legacy desktop-based optical clinical management | Heavy desktop footprint, expensive licensing fees, lacks web-native Virtual Try-On and AI prescription image extraction. |
| **3** | E-Commerce Eyewear Platforms (Lenskart, Warby Parker) | Consumer-facing online eyewear web/mobile applications | Proprietary closed ecosystems tailored solely to single-brand sales; non-adaptable as an in-store management platform for independent optical retailers. |
| **4** | "Augmented Reality Virtual Try-On Systems" (*IEEE*, 2024) | Computer vision facial landmark positioning for glasses fitting | Focuses purely on 3D rendering algorithms without connecting to clinical eye test data, inventory levels, or POS billing workflows. |
| **5** | "AI OCR in Medical Prescription Analysis" (*IJCA*, 2025) | Deep learning extraction of handwritten prescriptions | Addresses OCR accuracy in isolation without integrating into an active retail order pipeline or customer CRM. |

**Conclusion**: Existing solutions are either narrow clinical desktop tools, generic retail POS systems lacking optical domain capabilities, or standalone AR research prototypes. VisionEdge fills this gap by uniting AI clinical vision tools, Virtual Try-On, retail inventory, and billing into an integrated web platform.

---

## 5. Requirements Specification

### 5.1. Introduction
* **Purpose**: A full-stack web application providing automated optical store administration, AI prescription scanning, facial frame recommendation, Virtual Try-On, and inventory billing.
* **Scope**: Clinical appointment booking, eye exam recording, Gemini AI OCR scanning, VTO canvas engine, frame/lens stock management, order processing, PDF invoicing, and role-restricted admin controls.
* **Intended Users**: Store Administrators, Optometrists, Sales Staff, and Retail Customers.

### 5.2. Functional Requirements

| ID | Requirement | Description |
| :--- | :--- | :--- |
| **FR1** | **User Authentication & RBAC** | User registration and login utilizing JWT tokens, supporting Admin, Staff, and Customer user roles. |
| **FR2** | **Customer CRM & Profile Management** | Create, view, update, and search customer records, including demographic data, eye conditions, and medical history. |
| **FR3** | **Appointment Scheduling** | Schedule, manage, and filter customer appointments for Eye Tests, Frame Trials, Lens Consultations, and Follow-Ups. |
| **FR4** | **Eye Test & Exam Recording** | Record detailed clinical eye measurements (OD/OS SPH, CYL, AXIS, ADD, PD, doctor remarks) linked to customer records. |
| **FR5** | **AI Prescription OCR Scan** | Upload optical prescription images (JPG/PNG) and automatically extract numerical parameters using Gemini 1.5 Pro Vision AI. |
| **FR6** | **AI Frame Recommendation** | Detect or input face shape geometry (Oval, Round, Square, Heart) and return algorithmic frame recommendations. |
| **FR7** | **AI Lens Recommendation** | Evaluate prescription power parameters and suggest suitable lens types (Single Vision, Progressive) and coatings (Blue Cut, Anti-Glare). |
| **FR8** | **Interactive Virtual Try-On (VTO)** | Render selected frame overlays live onto user webcam feed or static snapshot image via interactive canvas rendering. |
| **FR9** | **Frame & Lens Inventory Control** | Perform full CRUD operations on spectacle frames and optical lenses, tracking brand, model, material, price, stock, and min_stock levels. |
| **FR10** | **Order Processing & Fulfillment** | Generate sales orders linking customer, prescription, selected frame, and lens items; update fulfillment states (Pending, Processing, Ready, Delivered). |
| **FR11** | **Billing & PDF Invoice Generation** | Calculate subtotal, discounts, GST tax amounts, generate official PDF receipts, and update stock quantities automatically. |
| **FR12** | **Analytics & Reports** | Display administrative dashboards detailing total sales revenue, customer visit trends, low-stock warnings, and order status breakdowns. |

### 5.3. Non-Functional Requirements

| ID | Requirement | Standard / Target |
| :--- | :--- | :--- |
| **NFR1** | **Response Performance** | API endpoints respond within **< 300ms** under normal load; AI OCR extraction returns within **< 3.5 seconds**. |
| **NFR2** | **Data Isolation & Security** | Passwords hashed using `Werkzeug` bcrypt/PBKDF2; API routes protected by role-based JWT bearer authentication. |
| **NFR3** | **Real-Time VTO Frame Rate** | Virtual Try-On canvas maintains **>= 24 FPS** during live webcam video processing on standard client web browsers. |
| **NFR4** | **Cross-Browser Compatibility** | Web interface fully compatible with modern versions of Chrome, Edge, Firefox, and Safari across desktop and tablet viewports. |
| **NFR5** | **Reliability & Data Integrity** | Database operations execute within ACID compliant SQLAlchemy transactions; automatic error logging handles failovers. |
| **NFR6** | **Scalability** | Backend micro-architecture deployable via WSGI containers (Gunicorn / Waitress) behind Nginx reverse proxies. |

### 5.4. User Roles

* **Admin**: Complete system authority. Manages staff credentials, oversees full inventory, accesses financial analytics, configures system settings, and overrides audit permissions.
* **Staff / Optometrist**: Handles front-desk and clinical operations. Conducts eye exams, scans prescriptions via AI OCR, manages appointments, assists with VTO, creates sales orders, and generates customer bills.
* **Customer**: Registered end-user. Views personal appointment history, browses frame catalogs, uses the Virtual Try-On tool, accesses saved prescription records, and checks order fulfillment statuses.

### 5.5. Assumptions and Constraints

* **Assumptions**:
  * Users possess a web browser with camera access enabled for Virtual Try-On capabilities.
  * An active internet connection is available to communicate with the Google Gemini AI API endpoints.
  * In-store point-of-sale payments are settled at the counter (Cash, Card, UPI) before bill completion.
* **Constraints**:
  * The initial release targets web browsers (desktop/tablet/mobile web); native mobile app wrappers are reserved for future phases.
  * AI prescription parsing requires legible prescription images; low-resolution images trigger manual edit prompts for staff verification.

### 5.6. External Interface Requirements

#### 5.6.1. User Interface
* **Login & Auth Interface**: Responsive form supporting secure login, role selection, and password recovery.
* **Staff Dashboard & CRM**: Tabular interface with instant search and filter controls for customer profiles and appointments.
* **Clinical Eye Test & AI Scanner Module**: Interactive form for OD/OS clinical data entry, with side-by-side file drag-and-drop preview for AI prescription image parsing.
* **Virtual Try-On Suite**: Dynamic web canvas integrating live camera controls, frame selector carousel, snapshot capture, and history comparison.
* **Inventory & Order Management View**: Grid layout showcasing frame stock, lens types, pricing metrics, stock alert indicators, and status badges.
* **Billing & PDF Viewer Module**: Order itemization table with automatic GST calculation and single-click PDF invoice downloading.

#### 5.6.2. Hardware Interface
* **Standard HD Webcam / Device Camera**: 720p or higher video input for real-time Virtual Try-On facial tracking.
* **Standard Display Monitor**: Minimum resolution of 1024x768 pixels for desktop administration.

#### 5.6.3. Software Interface

| Interface | Description |
| :--- | :--- |
| **Flask RESTful API** | Serves JSON endpoints for all frontend client operations over HTTP/HTTPS. |
| **SQLAlchemy / PyMySQL** | Relational Database Abstraction Layer connecting Flask to MySQL or SQLite databases. |
| **Google Gemini 1.5 Pro API** | Multimodal AI Vision service used for optical prescription OCR parameter extraction. |
| **Canvas / MediaPipe API** | Client-side JavaScript library driving real-time webcam rendering for Virtual Try-On. |
| **ReportLab / FPDF** | Python server-side library generating formatted PDF billing receipts and invoices. |

#### 5.6.4. Communication Interface
* All client-server communication occurs securely via HTTP/HTTPS standard RESTful requests using JSON payloads.
* Media files (prescription uploads, VTO snapshots) are transmitted via `multipart/form-data` and served securely under token-validated `/media/` static routes.

---

## 6. Feasibility Analysis

### 6.1. Technical Feasibility
The technologies selected—Python Flask, SQLAlchemy, MySQL, JavaScript Canvas API, and Google Gemini AI—are mature, industry-standard, and well-documented. The development team has demonstrated proficiency in building RESTful architectures and integrating computer vision algorithms. The system requires no specialized hardware beyond standard retail PC configurations and webcams, confirming complete technical feasibility.

### 6.2. Economic Feasibility
VisionEdge is economically advantageous. Built on open-source frameworks (Flask, SQLAlchemy, MySQL), the system incurs zero initial software licensing overhead. Operational cloud deployment costs on PaaS platforms (e.g., Render, AWS EC2, digital VPS) combined with usage-based Gemini API pricing remain extremely modest ($5–$20/month for medium volume retail stores), yielding a highly favorable return on investment (ROI).

### 6.3. Legal Feasibility
VisionEdge complies with standard data privacy regulations. Customer medical notes and contact details are stored securely within protected databases using role-gated access. No biometric facial models are permanently sold or shared with third parties; VTO snapshots are stored locally or in secure app storage strictly for customer record history. No healthcare device certification is required as the platform functions as administrative management and decision-support software.

### 6.4. Operational Feasibility
The platform replaces fragmented paper-based processes with an intuitive web workflow. Front-desk staff and optometrists require minimal training due to clear user interface patterns mirroring traditional optical consultation steps (Appointment $\rightarrow$ Eye Exam $\rightarrow$ Frame VTO $\rightarrow$ Order $\rightarrow$ Invoice). High operational feasibility is assured.

### 6.5. Schedule Feasibility
The core functional system—including backend database modeling, RESTful API architecture, authentication, AI OCR scanning, Virtual Try-On canvas, inventory CRUD, and billing—has been modularly engineered and tested within a standard academic project timeline.

---

## 7. Technology Stack

| Layer | Technology | Justification |
| :--- | :--- | :--- |
| **Frontend UI** | HTML5, Vanilla CSS3, JavaScript (ES6+) | Lightweight, zero-dependency, ultra-fast rendering with native browser Canvas API support. |
| **Backend Framework** | Python 3.9+ / Flask 3.0 | Modular WSGI micro-framework offering lightweight RESTful routing and rapid extension integration. |
| **Database ORM** | SQLAlchemy 2.0 / Flask-SQLAlchemy | Robust relational mapping, transactional integrity, and automated model migrations. |
| **Database Engine** | MySQL 8.0 / SQLite 3 | Enterprise-grade relational storage supporting ACID compliance, indexing, and foreign key constraints. |
| **Authentication** | Flask-JWT-Extended / PyJWT | Secure, stateless JSON Web Token bearer authentication for API role restriction. |
| **AI Vision OCR** | Google Gemini 1.5 Pro Vision API | Multimodal AI model providing high-precision structural extraction from prescription images. |
| **Virtual Try-On Engine** | HTML5 Canvas / MediaPipe Vision | Real-time browser-based computer vision rendering for frame overlay without server latency. |
| **PDF Generation** | FPDF / ReportLab | Programmatic creation of branded, printable customer GST billing invoices. |
| **WSGI Server** | Gunicorn / Waitress | High-concurrency production server suited for Linux VPS and Windows server deployments. |
| **Version Control** | Git & GitHub | Source code control, collaborative branching, and continuous delivery tracking. |

---

## 8. Data Dictionary

The VisionEdge database is implemented in MySQL / SQLite using SQLAlchemy ORM models. All primary keys use auto-incrementing integers or UUID strings, enforcing strict relational integrity.

### 8.1. Table: user
Manages login credentials, staff account details, and role assignments.

| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | Integer | Primary Key, Auto Increment | Unique system user ID |
| `username` | String(80) | Unique, Not Null | Account login handle |
| `first_name` | String(50) | Nullable | User's given first name |
| `last_name` | String(50) | Nullable | User's surname |
| `email` | String(120) | Unique, Nullable | Account contact email |
| `password_hash` | String(255) | Not Null | Bcrypt/PBKDF2 secure hashed password |
| `phone` | String(20) | Nullable | Contact telephone number |
| `role` | String(50) | Default 'customer' | User authorization role (`admin`, `staff`, `customer`) |
| `created_at` | DateTime | Default `utcnow()` | Account creation timestamp |

### 8.2. Table: customer
Stores comprehensive retail customer profiles and demographic metadata.

| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | Integer | Primary Key, Auto Increment | Unique customer ID |
| `customer_code` | String(20) | Unique | System generated customer reference code |
| `first_name` | String(50) | Not Null | Customer's first name |
| `last_name` | String(50) | Not Null | Customer's last name |
| `gender` | String(20) | Nullable | Customer gender identification |
| `date_of_birth` | Date | Nullable | Customer birthdate |
| `phone` | String(20) | Not Null, Indexed | Primary mobile phone number |
| `email` | String(120) | Indexed | Contact email address |
| `address` | Text | Nullable | Residential street address |
| `city` | String(100) | Nullable | Resident city |
| `status` | String(20) | Default 'Active' | Customer account status (`Active`, `Inactive`) |
| `created_at` | DateTime | Default `utcnow()` | Registration timestamp |

### 8.3. Table: eye_test & prescription

#### Table: `eye_test`
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | Integer | Primary Key, Auto Increment | Unique eye exam record ID |
| `customer_id` | Integer | Foreign Key -> `customer.id` | Associated customer reference |
| `appointment_id` | Integer | Foreign Key -> `appointment.id` | Associated appointment (optional) |
| `right_sphere` | String(20) | Nullable | OD Sphere power value |
| `right_cylinder` | String(20) | Nullable | OD Cylinder power value |
| `right_axis` | String(20) | Nullable | OD Axis degree value |
| `left_sphere` | String(20) | Nullable | OS Sphere power value |
| `left_cylinder` | String(20) | Nullable | OS Cylinder power value |
| `left_axis` | String(20) | Nullable | OS Axis degree value |
| `pd_value` | String(20) | Nullable | Pupillary Distance (mm) |
| `remarks` | Text | Nullable | Optometrist clinical observations |
| `created_at` | DateTime | Default `utcnow()` | Examination timestamp |

#### Table: `prescription`
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | Integer | Primary Key, Auto Increment | Unique prescription record ID |
| `prescription_number`| String(50) | Unique | Tracking reference number |
| `customer_id` | Integer | Foreign Key -> `customer.id` | Linked customer reference |
| `eye_test_id` | Integer | Foreign Key -> `eye_test.id` | Associated clinical eye exam record |
| `add_power` | String(20) | Nullable | Near Add power for progressive lenses |
| `prescription_image` | String(255) | Nullable | File path to uploaded scan image |
| `ai_extracted_text` | Text | Nullable | Raw JSON text parsed by Gemini AI |
| `confidence_score` | Float | Nullable | AI parsing confidence rating (0.0 to 1.0) |
| `doctor_name` | String(100) | Nullable | Prescribing eye doctor/optometrist name |
| `created_at` | DateTime | Default `utcnow()` | Record entry timestamp |

### 8.4. Table: frame & lens

#### Table: `frame`
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | Integer | Primary Key, Auto Increment | Unique frame item ID |
| `frame_code` | String(50) | Unique | Frame SKU / Inventory code |
| `brand` | String(100) | Not Null | Frame manufacturer brand |
| `model` | String(100) | Not Null | Model designation |
| `shape` | String(50) | Not Null | Frame geometry (`Oval`, `Rectangle`, `Round`, `Square`, `Cat-Eye`) |
| `color` | String(50) | Not Null | Frame color description |
| `material` | String(50) | Nullable | Construction material (`Acetate`, `Titanium`, `Metal`) |
| `price` | Float | Not Null | Retail selling price (INR) |
| `stock` | Integer | Default 0 | Current quantity available in store |
| `min_stock` | Integer | Default 5 | Threshold for triggering low-stock alert |
| `vto_image` | String(255) | Nullable | Transparent PNG image URL for Virtual Try-On canvas |

#### Table: `lens`
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | Integer | Primary Key, Auto Increment | Unique lens item ID |
| `lens_code` | String(50) | Unique | Lens SKU / Inventory code |
| `brand` | String(100) | Not Null | Lens manufacturer |
| `type` | String(50) | Not Null | Lens optical design (`Single Vision`, `Bifocal`, `Progressive`) |
| `coating` | String(100) | Nullable | Specialty coating (`Anti-Glare`, `Blue Cut`, `Photochromic`) |
| `price` | Float | Not Null | Retail selling price (INR) |
| `stock` | Integer | Default 0 | Available lens blank stock quantity |
| `min_stock` | Integer | Default 10 | Minimum stock threshold |

### 8.5. Table: order & billing

#### Table: `order`
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | Integer | Primary Key, Auto Increment | Internal order system ID |
| `order_id` | String(50) | Unique | Customer-facing order code (e.g. `ORD-1002`) |
| `customer_id` | Integer | Foreign Key -> `customer.id` | Purchasing customer |
| `prescription_id` | Integer | Foreign Key -> `prescription.id` | Prescription applied to order |
| `status` | String(50) | Default 'Pending' | Order fulfillment stage (`Pending`, `Processing`, `Ready`, `Delivered`) |
| `total_amount` | Float | Default 0.0 | Calculated order gross total |
| `created_at` | DateTime | Default `utcnow()` | Order placement timestamp |

#### Table: `billing`
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | Integer | Primary Key, Auto Increment | Invoice record ID |
| `invoice_number` | String(50) | Unique, Not Null | Official legal invoice number (e.g. `INV-2026-008`) |
| `order_id` | Integer | Foreign Key -> `order.id` | Associated sales order |
| `subtotal` | Float | Default 0.0 | Net item amount before taxes |
| `discount` | Float | Default 0.0 | Total promotional discount applied |
| `gst` | Float | Default 0.0 | Calculated Goods & Services Tax amount |
| `total_amount` | Float | Not Null | Final payable invoice balance |
| `payment_status` | String(20) | Default 'Pending' | Payment completion state (`Paid`, `Pending`) |
| `payment_method` | String(50) | Nullable | Payment tender mode (`Cash`, `Card`, `UPI`) |
| `invoice_pdf` | String(255) | Nullable | File path to generated PDF invoice |

### 8.6. Role-Based Access Control (RBAC) & Security Policy Summary

| Endpoint / Target | Required Role | Access Rule / Policy Description |
| :--- | :--- | :--- |
| `/api/auth/register`, `/api/auth/login` | Public | Open access for user authentication and token creation. |
| `/api/customers/*` | `admin`, `staff` | Staff and Admin users may search, view, create, and update customer profiles. |
| `/api/ai/extract` | `admin`, `staff` | Staff and Admin users can upload prescription images to invoke Gemini OCR. |
| `/api/vto/frames`, `/api/vto/save-history` | `admin`, `staff`, `customer` | Authenticated users can fetch VTO-ready frames and persist try-on snapshots. |
| `/api/inventory/*` (POST, PUT, DELETE) | `admin` | Only Admin users may add new frame/lens inventory items or modify prices/stock. |
| `/api/billing/*` | `admin`, `staff` | Staff and Admin users may issue bills, process payments, and download invoices. |
| `/api/reports/*` | `admin` | Strictly restricted to Admin accounts for viewing revenue analytics and audit logs. |

---
*End of Software Requirements Specification (SRS) Document for VisionEdge.*
