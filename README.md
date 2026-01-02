# Coffee Shop Management System

A comprehensive web-based management system for coffee shops built with Python Flask, featuring inventory management, order processing, sales analytics, and advanced security features including Two-Factor Authentication.

## System Overview

This system implements a complete conceptual framework with three main layers:

### 1. Input Layer (Users)
- **Manager (Administrator)**: Full system control with authentication, inventory, staff, and analytics management
- **Staff/Barista**: Order processing, QR scanning, and order status management
- **Customer/Transaction Source**: Order generation and payment processing

### 2. Processing Layer (Modules)
- **Authentication & Security**: Login/registration, password hashing, 2FA with PyOTP, session management
- **Menu & Inventory Management**: CRUD operations, profit calculation, stock monitoring, low-stock alerts
- **Order Management**: Order creation with JSON storage, status filtering, QR-based retrieval
- **Sales Analytics**: Trend analysis, top-selling items visualization, revenue computation with Chart.js
- **Staff Management**: Role-based access control, status monitoring
- **Activity Logs**: Comprehensive audit trail with user actions and IP tracking

### 3. Output Layer
- Real-time dashboards with statistics
- Inventory alerts and status reports
- Order summaries and transaction history
- Interactive sales analytics graphs
- Activity logs and audit reports

## Technology Stack

### Backend
- **Python 3.11+** - Core programming language
- **Flask 3.0+** - Web framework
- **SQLAlchemy 2.0+** - Database ORM
- **SQLite** - Database storage
- **Werkzeug** - Password hashing
- **PyOTP** - Two-Factor Authentication
- **QRCode** - QR code generation

### Frontend
- **HTML5, CSS3, JavaScript ES6+**
- **Chart.js** - Data visualization
- **Font Awesome** - Icons
- **Html5-QRCode** - QR scanning

## Features

### Core Features
✅ User authentication with login/logout
✅ Two-Factor Authentication (2FA) with QR code setup
✅ Role-based access control (Manager/Staff)
✅ Menu item management with CRUD operations
✅ Automatic profit calculation and margin display
✅ Stock level monitoring with low-stock alerts
✅ Supplier management
✅ Order creation and management
✅ Order status tracking (Pending → Preparing → Ready → Completed)
✅ Payment method tracking
✅ Sales analytics with interactive charts
✅ Top-selling items analysis
✅ Activity logging and audit trail
✅ Staff management with status control

### Security Features
- Password hashing using Werkzeug
- Two-Factor Authentication (2FA) via PyOTP
- Session management with secure cookies
- Activity logging with IP address tracking
- Role-based access control
- CSRF protection

## Installation

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/Aguilos/Laravel-Finals.git
   cd Laravel-Finals
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and update the values as needed:
   - `SECRET_KEY`: Generate a secure random key
   - `DATABASE_URL`: SQLite database path (default: sqlite:///coffeeshop.db)
   - `FLASK_ENV`: Set to 'development' or 'production'

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the system**
   Open your browser and navigate to: `http://localhost:5000`

## Default Credentials

```
Username: admin
Password: admin123
```

**⚠️ Important:** Change the default password immediately after first login!

## Usage Guide

### For Managers

1. **Dashboard**: View overall statistics, recent orders, and top-selling items
2. **Menu Management**: Add, edit, or remove menu items with cost and pricing
3. **Inventory Monitoring**: Track stock levels and receive low-stock alerts
4. **Staff Management**: Add barista accounts and manage their status
5. **Supplier Management**: Maintain supplier information and contacts
6. **Sales Analytics**: View sales trends, revenue reports, and item performance
7. **Activity Logs**: Monitor all system actions for audit purposes
8. **2FA Setup**: Enable two-factor authentication for enhanced security

### For Staff/Baristas

1. **Dashboard**: View pending orders and daily statistics
2. **Order Processing**: Create new orders and add items
3. **Order Management**: Update order status through workflow
4. **Menu Browsing**: View available items and stock levels
5. **2FA Setup**: Secure your account with two-factor authentication

### Order Workflow

```
Pending → Preparing → Ready → Completed
                    ↓
                Cancelled
```

## API Endpoints

### Public Endpoints
- `GET /` - Home page (redirects to login)
- `POST /login` - User authentication
- `GET /logout` - User logout

### Protected Endpoints (Require Login)
- `GET /dashboard` - Main dashboard
- `GET /menu` - View menu items
- `GET /orders` - View orders with filtering
- `POST /orders/create` - Create new order
- `POST /orders/<id>/update-status` - Update order status

### Manager-Only Endpoints
- `GET /staff` - Staff management
- `POST /staff/add` - Add new staff member
- `GET /suppliers` - Supplier management
- `GET /analytics` - Sales analytics
- `GET /activity-logs` - View activity logs

### API Routes
- `GET /api/menu` - Get available menu items
- `GET /api/orders/<order_number>` - Get order by number (for QR scanning)
- `GET /api/low-stock-alerts` - Get low stock items

## Database Schema

### Tables
- **users**: User accounts (managers and staff)
- **menu_items**: Products with pricing and inventory
- **suppliers**: Supplier information
- **orders**: Order records with JSON data
- **order_items**: Individual items in orders
- **activity_logs**: System activity audit trail

## Project Structure

```
Laravel-Finals/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── models.py             # Database models
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
├── .gitignore           # Git ignore rules
├── templates/           # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   ├── menu.html
│   ├── orders.html
│   ├── staff.html
│   ├── analytics.html
│   └── ...
├── static/              # Static files
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
└── README.md           # This file
```

## Security Considerations

1. **Always change default credentials** before deploying to production
2. **Use HTTPS** in production environments
3. **Set strong SECRET_KEY** in environment variables
4. **Enable 2FA** for all administrator accounts
5. **Regularly review activity logs** for suspicious activity
6. **Keep dependencies updated** to patch security vulnerabilities
7. **Use environment variables** for sensitive configuration
8. **Set proper file permissions** on the database file

## Development

### Running in Development Mode
```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
python app.py
```

### Database Management
The database is automatically created when the application first runs. To reset the database:
```bash
rm coffeeshop.db
python app.py  # Will recreate with default admin user
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is created for educational purposes.

## Support

For issues, questions, or contributions, please open an issue on GitHub.

## Acknowledgments

- Flask framework and its excellent documentation
- SQLAlchemy for robust ORM capabilities
- Chart.js for beautiful data visualizations
- Font Awesome for comprehensive icon library
- PyOTP for secure two-factor authentication
- The open-source community for various libraries and tools

---

**Built with ❤️ and ☕ for coffee shop management**