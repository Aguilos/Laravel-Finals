# Coffee Shop Management System - Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### Prerequisites
- Python 3.11 or higher installed
- pip package manager
- A web browser

### Installation Steps

1. **Clone and Navigate**
   ```bash
   git clone https://github.com/Aguilos/Laravel-Finals.git
   cd Laravel-Finals
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize Sample Data** (Optional but Recommended)
   ```bash
   python init_data.py
   ```

5. **Run the Application**
   ```bash
   python app.py
   ```

6. **Access the System**
   - Open your browser
   - Navigate to: `http://localhost:5000`
   - Login with default credentials below

### Default Credentials

**Manager Account:**
- Username: `admin`
- Password: `admin123`
- Access: Full system control

**Staff Account:**
- Username: `barista1`
- Password: `barista123`
- Access: Order processing and basic operations

⚠️ **Security Note:** Change these passwords immediately in production!

## 📋 System Overview

### What's Included

✅ **User Management**
- Two-Factor Authentication (2FA)
- Role-based access control
- Password hashing and security

✅ **Menu & Inventory**
- 15 pre-loaded menu items
- Automatic profit calculation
- Low-stock alerts
- Stock level monitoring

✅ **Order Management**
- Quick order creation
- Real-time status tracking
- Payment method support
- Order history

✅ **Sales Analytics**
- Interactive charts with Chart.js
- Sales trends (daily/weekly/monthly)
- Top-selling items analysis
- Revenue reports

✅ **Staff Management**
- Account creation and status control
- Activity monitoring
- Role assignment

✅ **Activity Logs**
- Complete audit trail
- IP address tracking
- User action logging

## 🎯 Quick Tasks

### For First-Time Users

1. **Login as Manager**
   - Use admin credentials
   - Explore the dashboard

2. **View Sample Data**
   - Check Menu section (15 items)
   - Review Orders (15 sample orders)
   - View Analytics charts

3. **Create a Test Order**
   - Go to Orders → New Order
   - Select menu items
   - Complete the order

4. **Enable 2FA** (Recommended)
   - Click shield icon in navbar
   - Scan QR code with Google Authenticator
   - Verify and enable

### Common Operations

**Add Menu Item:**
1. Menu → Add Item
2. Fill in details (name, price, cost, stock)
3. System auto-calculates profit
4. Save

**Process Order:**
1. Orders → New Order
2. Select items and quantities
3. Choose payment method
4. Place order

**View Analytics:**
1. Analytics section
2. Select time period
3. View charts and reports

**Manage Staff:**
1. Staff → Add Staff
2. Enter username, email, password
3. Staff account created with "staff" role

## 📁 File Structure

```
Laravel-Finals/
├── app.py                    # Main application
├── models.py                 # Database models
├── config.py                 # Configuration
├── requirements.txt          # Dependencies
├── init_data.py             # Sample data loader
├── test_system.py           # System tests
├── README.md                # Main documentation
├── DOCUMENTATION.md         # Detailed docs
├── CONCEPTUAL_FRAMEWORK.md  # Architecture diagrams
├── templates/               # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   └── ...
├── static/
│   ├── css/style.css        # Styling
│   └── js/main.js           # JavaScript
└── coffeeshop.db            # SQLite database (auto-created)
```

## 🛠️ Available Commands

### Run Application
```bash
python app.py
```

### Initialize Sample Data
```bash
python init_data.py
```

### Run Tests
```bash
python test_system.py
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

## 📊 Sample Data Included

After running `init_data.py`:

- **15 Menu Items** across categories:
  - Coffee: Espresso, Cappuccino, Latte, Americano, Mocha, etc.
  - Tea: Green Tea Latte, Chai Latte
  - Pastries: Croissant, Blueberry Muffin
  - Desserts: Cheesecake, Cookies
  - Sandwiches: Club Sandwich, Grilled Cheese

- **3 Suppliers**:
  - Premium Coffee Beans Co.
  - Fresh Bakery Supplies
  - Dairy Products Inc.

- **15 Sample Orders**:
  - Various statuses (pending, completed, cancelled)
  - Different dates (last 30 days)
  - Multiple payment methods

- **2 User Accounts**:
  - 1 Manager (admin)
  - 1 Staff (barista1)

## 🔐 Security Features

### Password Security
- Hashed using Werkzeug (pbkdf2:sha256)
- Never stored in plain text
- Secure session management

### Two-Factor Authentication
- Optional but recommended
- Uses PyOTP (TOTP)
- Compatible with:
  - Google Authenticator
  - Authy
  - Microsoft Authenticator
  - Any TOTP app

### Activity Logging
- All actions logged
- IP address tracking
- Timestamp recording
- User type identification

## 📖 Documentation

- **README.md** - Main documentation and installation guide
- **DOCUMENTATION.md** - Complete system documentation
- **CONCEPTUAL_FRAMEWORK.md** - Architecture and diagrams
- **This file (QUICKSTART.md)** - Quick start guide

## 💡 Tips and Best Practices

1. **Change Default Passwords** immediately
2. **Enable 2FA** for all administrator accounts
3. **Regular Backups** of the database file
4. **Monitor Activity Logs** for security
5. **Update Stock Levels** regularly
6. **Review Analytics** weekly for insights

## 🐛 Troubleshooting

### Application won't start
- Check Python version: `python --version` (must be 3.11+)
- Verify dependencies: `pip install -r requirements.txt`
- Check if port 5000 is available

### Can't login
- Use default credentials: admin/admin123
- Database must be initialized
- Check if coffeeshop.db exists

### Database errors
- Delete coffeeshop.db and restart app
- Database will be recreated automatically
- Run init_data.py to reload sample data

### Import errors
- Activate virtual environment
- Reinstall dependencies
- Check Python version compatibility

## 🌐 Browser Compatibility

Tested and working on:
- ✅ Chrome/Chromium (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Edge (latest)

## 📞 Support

For issues or questions:
1. Check the documentation files
2. Review the code comments
3. Run test_system.py to diagnose issues
4. Open an issue on GitHub

## 🎉 Next Steps

After getting started:

1. **Customize the System**
   - Add your own menu items
   - Configure settings in config.py
   - Update branding and styling

2. **Explore Features**
   - Try all manager functions
   - Process orders as staff
   - Generate analytics reports

3. **Production Deployment**
   - Review DOCUMENTATION.md deployment section
   - Configure production settings
   - Set up proper database
   - Enable HTTPS

4. **Extend Functionality**
   - Add new features
   - Customize templates
   - Integrate external services

---

**System Version:** 1.0.0  
**Last Updated:** January 2026  
**Quick Start Guide**

**Ready to go? Start with:**
```bash
python init_data.py && python app.py
```

Then open http://localhost:5000 and login with admin/admin123! ☕
