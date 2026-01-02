# Coffee Shop Management System - Conceptual Framework

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           INPUT LAYER (USERS)                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  ┌──────────────────┐  ┌──────────────────┐  ┌─────────────────────┐   │
│  │     MANAGER      │  │  STAFF/BARISTA   │  │  CUSTOMER/TRANSACTION│   │
│  │  (Administrator) │  │ (Operational User)│  │      (Source)        │   │
│  └────────┬─────────┘  └────────┬─────────┘  └──────────┬──────────┘   │
│           │                     │                        │               │
│           │                     │                        │               │
└───────────┼─────────────────────┼────────────────────────┼───────────────┘
            │                     │                        │
            │ • Authentication    │ • Order Processing     │ • Orders
            │ • 2FA Setup         │ • QR Scanning          │ • Payments
            │ • Menu Management   │ • Status Updates       │ • Sales Data
            │ • Inventory Control │ • Queue Management     │
            │ • Staff Management  │                        │
            │ • Analytics Access  │                        │
            │ • System Config     │                        │
            │                     │                        │
            └─────────────────────┴────────────────────────┘
                                   │
┌─────────────────────────────────┼─────────────────────────────────────────┐
│                        PROCESSING LAYER (MODULES)                         │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │        A. AUTHENTICATION & SECURITY MODULE                       │   │
│  │  • User Login/Registration    • QR Code Generation              │   │
│  │  • Password Hashing (Werkzeug) • Session Management             │   │
│  │  • 2FA with PyOTP              • Access Control                 │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                           │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │        B. MENU & INVENTORY MANAGEMENT MODULE                     │   │
│  │  • CRUD Operations            • Low-Stock Alerts                │   │
│  │  • Profit Calculation         • Supplier Tracking               │   │
│  │  • Stock Monitoring           • Cost Management                 │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                           │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │        C. ORDER MANAGEMENT MODULE                                │   │
│  │  • Order Creation (JSON)      • QR-based Retrieval              │   │
│  │  • Status Filtering           • Payment Tracking                │   │
│  │  • Real-time Updates          • Order Queue Management          │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                           │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │        D. SALES ANALYTICS & REPORTING MODULE                     │   │
│  │  • Sales Trends (Daily/Weekly/Monthly)                          │   │
│  │  • Top-Selling Items          • Revenue Computation             │   │
│  │  • Interactive Charts (Chart.js)                                │   │
│  │  • Decision-Support Insights                                    │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                           │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │        E. STAFF MANAGEMENT MODULE                                │   │
│  │  • Account Creation           • Status Monitoring               │   │
│  │  • Role-based Access Control  • (Active/Pending/Inactive)       │   │
│  │  • Verification System                                          │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                           │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │        F. ACTIVITY LOGS & MONITORING MODULE                      │   │
│  │  • Automatic Action Logging   • IP Address Tracking             │   │
│  │  • User Type Recording        • Audit Trail                     │   │
│  │  • Timestamp Logging          • Accountability System           │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                           │
└───────────────────────────────────┬───────────────────────────────────────┘
                                    │
┌───────────────────────────────────┼───────────────────────────────────────┐
│                    TECHNOLOGICAL COMPONENTS (SUPPORT LAYER)               │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  ┌─────────────────────────────┐  ┌──────────────────────────────────┐  │
│  │     BACKEND TECHNOLOGIES    │  │    FRONTEND TECHNOLOGIES         │  │
│  │                             │  │                                  │  │
│  │  • Python 3.11+             │  │  • HTML5, CSS3                   │  │
│  │  • Flask 3.0+               │  │  • JavaScript ES6+               │  │
│  │  • SQLAlchemy 2.0+          │  │  • Chart.js                      │  │
│  │  • SQLite Database          │  │  • Font Awesome                  │  │
│  │  • RESTful APIs             │  │  • Html5-QRCode                  │  │
│  │  • Werkzeug                 │  │                                  │  │
│  │  • PyOTP (2FA)              │  │  SUPPORTING APIs:                │  │
│  │  • QRCode Library           │  │  • Fetch API                     │  │
│  │                             │  │  • MediaDevices API              │  │
│  └─────────────────────────────┘  │  • Canvas API                    │  │
│                                    └──────────────────────────────────┘  │
│                                                                           │
└───────────────────────────────────┬───────────────────────────────────────┘
                                    │
                                    ▼
┌───────────────────────────────────────────────────────────────────────────┐
│                          OUTPUT LAYER (RESULTS)                           │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  • Real-time Dashboards and Statistics                                   │
│  • Inventory Status and Low-Stock Alerts                                 │
│  • Order Summaries and Transaction History                               │
│  • Sales Analytics Graphs and Charts                                     │
│  • Activity Logs and Audit Reports                                       │
│  • Secure and Verified User Access                                       │
│  • Decision-Support Insights                                             │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘
```

## Data Flow Diagram

```
┌─────────────┐
│   MANAGER   │
│   (Admin)   │
└──────┬──────┘
       │
       │ Login + 2FA
       │
       ▼
┌──────────────────────┐
│  AUTHENTICATION      │
│  • Verify Credentials│
│  • Check 2FA Code    │
│  • Create Session    │
└──────┬───────────────┘
       │
       │ Authenticated
       │
       ▼
┌──────────────────────────────────────────────────────────────┐
│                         DASHBOARD                            │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────────┐  │
│  │  Statistics │  │Recent Orders │  │ Top Selling Items  │  │
│  └─────────────┘  └──────────────┘  └────────────────────┘  │
└──────┬──────────────────┬──────────────────┬─────────────────┘
       │                  │                  │
       ▼                  ▼                  ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│    MENU      │   │   ORDERS     │   │  ANALYTICS   │
│ MANAGEMENT   │   │ MANAGEMENT   │   │   REPORTS    │
└──────┬───────┘   └──────┬───────┘   └──────┬───────┘
       │                  │                  │
       │                  │                  │
       ▼                  ▼                  ▼
┌────────────────────────────────────────────────────┐
│              DATABASE (SQLite)                     │
│  ┌──────────┐ ┌──────────┐ ┌────────────────────┐ │
│  │  Users   │ │MenuItem  │ │  Orders & Items    │ │
│  ├──────────┤ ├──────────┤ ├────────────────────┤ │
│  │Suppliers │ │Activity  │ │  Other Tables      │ │
│  └──────────┘ └──────────┘ └────────────────────┘ │
└────────────────────────────────────────────────────┘
```

## Order Processing Workflow

```
┌─────────────┐
│  CUSTOMER   │
└──────┬──────┘
       │
       │ Places Order
       │
       ▼
┌──────────────────────┐
│   ORDER CREATION     │
│  • Select Items      │
│  • Set Quantities    │
│  • Choose Payment    │
└──────┬───────────────┘
       │
       │ Submit
       │
       ▼
┌──────────────────────┐      Generate Order #
│  ORDER VALIDATION    │◄─────(ORD + Date + Seq)
│  • Check Stock       │
│  • Calculate Total   │
│  • Create Record     │
└──────┬───────────────┘
       │
       │ Order Confirmed
       │
       ▼
┌──────────────────────┐
│   ORDER STATUS       │
│                      │
│   ┌──────────┐       │
│   │ PENDING  │       │
│   └────┬─────┘       │
│        │             │
│        ▼             │
│   ┌──────────┐       │
│   │PREPARING │       │
│   └────┬─────┘       │
│        │             │
│        ▼             │
│   ┌──────────┐       │
│   │  READY   │       │
│   └────┬─────┘       │
│        │             │
│        ▼             │
│   ┌──────────┐       │
│   │COMPLETED │       │
│   └──────────┘       │
│                      │
│   (or CANCELLED)     │
└──────────────────────┘
```

## Security Architecture

```
┌───────────────────────────────────────────────────────────────┐
│                     SECURITY LAYERS                           │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  Layer 1: Authentication                                      │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ • Username/Password Login                               │ │
│  │ • Werkzeug Password Hashing (pbkdf2:sha256)            │ │
│  │ • Session-based Authentication                          │ │
│  └─────────────────────────────────────────────────────────┘ │
│                          ▼                                    │
│  Layer 2: Two-Factor Authentication (Optional)                │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ • PyOTP TOTP Generation                                 │ │
│  │ • QR Code for Authenticator Apps                        │ │
│  │ • 6-digit Time-based Codes                             │ │
│  │ • Compatible with Google Authenticator, Authy, etc.     │ │
│  └─────────────────────────────────────────────────────────┘ │
│                          ▼                                    │
│  Layer 3: Session Management                                  │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ • Secure HTTP-only Cookies                              │ │
│  │ • Session Timeout (1 hour)                              │ │
│  │ • CSRF Protection                                       │ │
│  └─────────────────────────────────────────────────────────┘ │
│                          ▼                                    │
│  Layer 4: Role-Based Access Control                           │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ • Manager: Full Access                                  │ │
│  │ • Staff: Limited Operational Access                     │ │
│  │ • Route-level Authorization Decorators                  │ │
│  └─────────────────────────────────────────────────────────┘ │
│                          ▼                                    │
│  Layer 5: Activity Logging                                    │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ • All Actions Logged                                    │ │
│  │ • User Type, IP Address, Timestamp                      │ │
│  │ • Complete Audit Trail                                  │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

## Database Entity Relationship Diagram

```
┌──────────────────┐           ┌─────────────────────┐
│      USERS       │           │    ACTIVITY_LOGS    │
├──────────────────┤           ├─────────────────────┤
│ id (PK)          │───────┐   │ id (PK)             │
│ username         │       │   │ user_id (FK)        │
│ email            │       └──▶│ user_type           │
│ password_hash    │           │ action              │
│ role             │           │ details             │
│ status           │           │ ip_address          │
│ 2fa_secret       │           │ timestamp           │
│ 2fa_enabled      │           └─────────────────────┘
│ created_at       │
└────┬─────────────┘
     │
     │ created_by
     │
     ▼
┌──────────────────┐           ┌─────────────────────┐
│     ORDERS       │           │    ORDER_ITEMS      │
├──────────────────┤           ├─────────────────────┤
│ id (PK)          │───────┐   │ id (PK)             │
│ order_number     │       └──▶│ order_id (FK)       │
│ customer_name    │           │ menu_item_id (FK)   │
│ status           │           │ quantity            │
│ payment_method   │           │ price               │
│ total_amount     │           │ subtotal            │
│ order_data       │           └──────┬──────────────┘
│ qr_code          │                  │
│ created_by (FK)  │                  │
│ created_at       │                  │
└──────────────────┘                  │
                                      │
                                      ▼
                            ┌─────────────────────┐
                            │    MENU_ITEMS       │
                            ├─────────────────────┤
                            │ id (PK)             │
                            │ name                │
                            │ description         │
                            │ category            │
                            │ price               │
                            │ cost                │
                            │ stock_quantity      │
                            │ low_stock_threshold │
                            │ is_available        │
                            │ created_at          │
                            └─────────────────────┘

┌──────────────────┐
│    SUPPLIERS     │
├──────────────────┤
│ id (PK)          │
│ name             │
│ contact_person   │
│ email            │
│ phone            │
│ address          │
│ created_at       │
└──────────────────┘
```

## System Features Overview

### Core Modules

1. **Authentication & Security**
   - Multi-factor authentication
   - Role-based access control
   - Session management
   - Activity logging

2. **Inventory Management**
   - Real-time stock tracking
   - Automatic low-stock alerts
   - Profit calculation
   - Supplier management

3. **Order Processing**
   - Quick order creation
   - Status workflow tracking
   - Payment method recording
   - QR code generation

4. **Analytics & Reporting**
   - Sales trend analysis
   - Top-selling items
   - Revenue tracking
   - Interactive visualizations

5. **Staff Management**
   - User account creation
   - Status monitoring
   - Role assignment
   - Activity tracking

### Key Performance Indicators (KPIs)

```
┌──────────────────────────────────────────────────────┐
│              DASHBOARD METRICS                       │
├──────────────────────────────────────────────────────┤
│                                                      │
│  📊 Total Orders      │  💰 Total Revenue           │
│  ⏳ Pending Orders    │  ⚠️  Low Stock Items        │
│  📈 Sales Trend       │  🏆 Top Sellers             │
│  👥 Active Staff      │  📝 Recent Activity         │
│                                                      │
└──────────────────────────────────────────────────────┘
```

## Technology Integration

### Backend → Frontend Communication

```
┌─────────────┐                    ┌──────────────┐
│   Flask     │◄──────REST API────►│  JavaScript  │
│   Routes    │                    │   (Fetch)    │
└──────┬──────┘                    └──────┬───────┘
       │                                  │
       │ SQLAlchemy                       │ Chart.js
       │                                  │ Html5-QRCode
       ▼                                  ▼
┌─────────────┐                    ┌──────────────┐
│   SQLite    │                    │  HTML/CSS    │
│  Database   │                    │  Templates   │
└─────────────┘                    └──────────────┘
```

---

**System Version:** 1.0.0  
**Documentation Date:** January 2026  
**Framework Type:** Three-Layer Architecture with MVC Pattern
