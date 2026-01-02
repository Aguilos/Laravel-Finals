# Coffee Shop Management System - System Documentation

## Table of Contents
1. [System Overview](#system-overview)
2. [Architecture](#architecture)
3. [Database Schema](#database-schema)
4. [API Documentation](#api-documentation)
5. [User Guide](#user-guide)
6. [Security Features](#security-features)
7. [Deployment Guide](#deployment-guide)

## System Overview

The Coffee Shop Management System is a comprehensive web-based application designed to manage all aspects of a coffee shop's operations, from inventory and orders to staff management and sales analytics.

### Key Features
- User authentication with Two-Factor Authentication (2FA)
- Menu and inventory management
- Order processing and tracking
- Sales analytics with interactive charts
- Staff management with role-based access
- Supplier management
- Activity logging and audit trail

## Architecture

### Three-Layer Architecture

#### 1. Input Layer
**Users and Data Sources:**
- **Manager (Administrator)**: Full system access
  - Authentication management (including 2FA)
  - Menu and inventory control
  - Staff management
  - Sales analytics access
  - System configuration
  
- **Staff/Barista**: Operational access
  - Order processing
  - Order status updates
  - Menu viewing
  - Basic inventory viewing
  
- **Customer/Transaction**: Data generation
  - Orders creation
  - Payment processing

#### 2. Processing Layer

**A. Authentication & Security Module**
- User login/logout
- Password hashing (Werkzeug)
- Two-Factor Authentication (PyOTP)
- QR code generation for 2FA setup
- Session management
- Role-based access control

**B. Menu & Inventory Management Module**
- CRUD operations for menu items
- Automatic profit calculation
- Stock level monitoring
- Low-stock alert system
- Supplier tracking

**C. Order Management Module**
- Order creation with JSON storage
- Order filtering by status
- Real-time status updates
- QR-based order retrieval
- Payment method tracking

**D. Sales Analytics & Reporting Module**
- Sales trend analysis (daily, weekly, monthly)
- Top-selling items visualization
- Revenue computation
- Interactive charts (Chart.js)

**E. Staff Management Module**
- Staff account creation
- Role assignment
- Status monitoring (Active, Pending, Inactive)

**F. Activity Logs & Monitoring Module**
- Automatic action logging
- User type tracking
- Timestamp recording
- IP address logging

#### 3. Output Layer
- Real-time dashboards
- Inventory status reports
- Order summaries
- Sales analytics graphs
- Activity logs
- Alert notifications

### Technology Stack

**Backend:**
- Python 3.11+
- Flask 3.0+
- SQLAlchemy 2.0+
- SQLite
- Werkzeug (password hashing)
- PyOTP (2FA)
- QRCode (QR generation)

**Frontend:**
- HTML5, CSS3
- JavaScript ES6+
- Chart.js (data visualization)
- Font Awesome (icons)
- Html5-QRCode (QR scanning)

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL,  -- 'manager' or 'staff'
    status VARCHAR(20) DEFAULT 'active',  -- 'active', 'pending', 'inactive'
    two_factor_secret VARCHAR(32),
    two_factor_enabled BOOLEAN DEFAULT 0,
    created_at DATETIME,
    updated_at DATETIME
);
```

### Menu Items Table
```sql
CREATE TABLE menu_items (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    category VARCHAR(50),  -- 'coffee', 'tea', 'pastry', etc.
    price FLOAT NOT NULL,
    cost FLOAT NOT NULL,
    stock_quantity INTEGER DEFAULT 0,
    low_stock_threshold INTEGER DEFAULT 10,
    image_url VARCHAR(255),
    is_available BOOLEAN DEFAULT 1,
    created_at DATETIME,
    updated_at DATETIME
);
```

### Orders Table
```sql
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    order_number VARCHAR(20) UNIQUE NOT NULL,
    customer_name VARCHAR(100),
    status VARCHAR(20) DEFAULT 'pending',
    payment_method VARCHAR(20),
    total_amount FLOAT DEFAULT 0.0,
    order_data TEXT,  -- JSON storage
    qr_code VARCHAR(255),
    created_by INTEGER,
    created_at DATETIME,
    updated_at DATETIME,
    FOREIGN KEY (created_by) REFERENCES users (id)
);
```

### Order Items Table
```sql
CREATE TABLE order_items (
    id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    menu_item_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    price FLOAT NOT NULL,
    subtotal FLOAT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders (id),
    FOREIGN KEY (menu_item_id) REFERENCES menu_items (id)
);
```

### Suppliers Table
```sql
CREATE TABLE suppliers (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    contact_person VARCHAR(100),
    email VARCHAR(120),
    phone VARCHAR(20),
    address TEXT,
    created_at DATETIME,
    updated_at DATETIME
);
```

### Activity Logs Table
```sql
CREATE TABLE activity_logs (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    user_type VARCHAR(20),  -- 'manager', 'staff', 'system'
    action VARCHAR(255) NOT NULL,
    details TEXT,
    ip_address VARCHAR(45),
    timestamp DATETIME,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
```

## API Documentation

### Authentication Endpoints

#### POST /login
Login user with username and password.

**Request:**
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Response:**
- Redirects to 2FA verification if enabled
- Redirects to dashboard if successful
- Returns error message if invalid

#### POST /verify-2fa
Verify two-factor authentication code.

**Request:**
```json
{
  "code": "123456"
}
```

**Response:**
- Success: Redirect to dashboard
- Error: Invalid code message

#### GET /logout
Logout current user and clear session.

### Menu Management Endpoints

#### GET /menu
List all menu items.

**Response:**
- HTML page with menu items

#### POST /menu/add
Add new menu item (Manager only).

**Request:**
```json
{
  "name": "Latte",
  "description": "Smooth espresso with milk",
  "category": "coffee",
  "price": 130.00,
  "cost": 40.00,
  "stock_quantity": 100,
  "low_stock_threshold": 20
}
```

#### POST /menu/edit/<id>
Update menu item (Manager only).

#### POST /menu/delete/<id>
Delete menu item (Manager only).

### Order Management Endpoints

#### GET /orders
List orders with optional status filter.

**Query Parameters:**
- `status`: Filter by status (pending, preparing, ready, completed, cancelled)

#### POST /orders/create
Create new order.

**Request:**
```json
{
  "customer_name": "John Doe",
  "payment_method": "cash",
  "items": [
    {
      "menu_item_id": 1,
      "quantity": 2
    },
    {
      "menu_item_id": 3,
      "quantity": 1
    }
  ]
}
```

**Response:**
```json
{
  "success": true,
  "order_id": 123,
  "order_number": "ORD202401010001"
}
```

#### POST /orders/<id>/update-status
Update order status.

**Request:**
```json
{
  "status": "preparing"
}
```

### Staff Management Endpoints

#### GET /staff
List all staff members (Manager only).

#### POST /staff/add
Add new staff member (Manager only).

**Request:**
```json
{
  "username": "barista2",
  "email": "barista2@coffeeshop.com",
  "password": "secure_password"
}
```

#### POST /staff/<id>/update-status
Update staff status (Manager only).

**Request:**
```json
{
  "status": "active"
}
```

### Analytics Endpoints

#### GET /analytics
View sales analytics (Manager only).

**Query Parameters:**
- `period`: Time period (daily, weekly, monthly)

### API Routes

#### GET /api/menu
Get available menu items as JSON.

**Response:**
```json
[
  {
    "id": 1,
    "name": "Espresso",
    "price": 80.00,
    "cost": 25.00,
    "profit": 55.00,
    "profit_margin": 68.75,
    "stock_quantity": 100,
    "is_available": true
  }
]
```

#### GET /api/orders/<order_number>
Get order details by order number.

**Response:**
```json
{
  "id": 1,
  "order_number": "ORD202401010001",
  "customer_name": "John Doe",
  "status": "preparing",
  "total_amount": 390.00,
  "items": [...]
}
```

#### GET /api/low-stock-alerts
Get items with low stock (Manager only).

**Response:**
```json
[
  {
    "id": 5,
    "name": "Mocha",
    "stock_quantity": 8,
    "low_stock_threshold": 10,
    "is_low_stock": true
  }
]
```

## User Guide

### For Managers

#### Accessing the System
1. Navigate to the login page
2. Enter username: `admin` and password: `admin123`
3. If 2FA is enabled, enter the verification code from your authenticator app

#### Managing Menu Items
1. Go to Menu section
2. Click "Add Item" to create new menu item
3. Fill in details: name, description, category, price, cost, stock quantity
4. The system automatically calculates profit and profit margin
5. Edit or delete items as needed

#### Monitoring Inventory
1. View menu items to see stock levels
2. Items with low stock are highlighted
3. Set low stock thresholds for each item
4. Check dashboard for low stock alerts

#### Managing Orders
1. View all orders in Orders section
2. Filter by status: pending, preparing, ready, completed, cancelled
3. Update order status as needed
4. View order details and items

#### Viewing Analytics
1. Go to Analytics section
2. Select time period: daily, weekly, or monthly
3. View sales trends chart
4. See top-selling items
5. Check revenue reports

#### Managing Staff
1. Go to Staff section
2. Click "Add Staff" to create new barista account
3. Set status: active, pending, or inactive
4. Monitor staff activity

### For Staff/Baristas

#### Processing Orders
1. Go to Orders section
2. Click "New Order"
3. Enter customer name (optional)
4. Select payment method
5. Click menu items to add to order
6. Adjust quantities as needed
7. Click "Place Order" to submit

#### Updating Order Status
1. View orders list
2. Change status dropdown for each order
3. Status updates are saved automatically

#### Viewing Menu
1. Go to Menu section
2. View available items and stock levels
3. Check prices and descriptions

### Enabling Two-Factor Authentication

1. Click on the shield icon in the navigation bar
2. Click "Enable 2FA"
3. Scan the QR code with your authenticator app (Google Authenticator, Authy, etc.)
4. Or manually enter the secret key
5. Enter the 6-digit code from your app to verify
6. 2FA is now enabled for your account

## Security Features

### Password Security
- Passwords are hashed using Werkzeug's secure hashing
- Never stored in plain text
- Strong password requirements enforced

### Two-Factor Authentication
- Optional but recommended for all users
- Uses PyOTP for TOTP generation
- Compatible with Google Authenticator, Authy, etc.
- QR code generation for easy setup

### Session Management
- Secure session cookies
- HTTP-only cookies prevent XSS attacks
- Session timeout after 1 hour of inactivity
- Automatic session cleanup

### Role-Based Access Control
- Manager role: Full system access
- Staff role: Limited to operational functions
- Route-level access control decorators

### Activity Logging
- All user actions are logged
- Includes user type, action, timestamp, and IP address
- Provides complete audit trail
- Manager-only access to logs

### Data Protection
- SQL injection prevention via SQLAlchemy ORM
- XSS protection in templates
- CSRF tokens for forms
- Input validation and sanitization

## Deployment Guide

### Development Deployment

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Initialize Database**
   ```bash
   python init_data.py  # Optional: Load sample data
   ```

4. **Run Application**
   ```bash
   python app.py
   ```

5. **Access System**
   - Open browser to http://localhost:5000
   - Login with default credentials

### Production Deployment

1. **Server Setup**
   - Use a production WSGI server (Gunicorn, uWSGI)
   - Configure reverse proxy (Nginx, Apache)
   - Enable HTTPS with SSL certificate

2. **Environment Configuration**
   ```bash
   # Set production environment variables
   export FLASK_ENV=production
   export SECRET_KEY="generate-secure-random-key"
   export SESSION_COOKIE_SECURE=True
   ```

3. **Database**
   - Consider migrating to PostgreSQL or MySQL for production
   - Set up regular backups
   - Configure connection pooling

4. **Security**
   - Change all default passwords
   - Enable 2FA for all admin accounts
   - Configure firewall rules
   - Set up SSL/TLS certificates
   - Enable security headers

5. **Monitoring**
   - Set up application logging
   - Configure error tracking
   - Monitor system resources
   - Set up alerts for critical events

### Using Gunicorn (Production)

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 "app:create_app()"
```

### Nginx Configuration Example

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
    
    location /static {
        alias /path/to/Laravel-Finals/static;
    }
}
```

## Troubleshooting

### Common Issues

**Database Locked Error**
- Close all connections to the database
- Restart the application

**Import Errors**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Activate virtual environment

**Permission Denied**
- Check file permissions on database file
- Ensure write access to application directory

**Session Timeout**
- Adjust `PERMANENT_SESSION_LIFETIME` in config.py
- Check server time synchronization for 2FA

## Support and Maintenance

### Regular Maintenance Tasks
1. Review activity logs weekly
2. Monitor disk space for database growth
3. Update dependencies monthly
4. Backup database daily
5. Review and update user accounts
6. Monitor system performance

### Backup Strategy
- Database: Daily automated backups
- Configuration: Version control
- Static files: Regular snapshots
- Activity logs: Archive monthly

---

**Version:** 1.0.0  
**Last Updated:** January 2026  
**Documentation:** Complete System Documentation
