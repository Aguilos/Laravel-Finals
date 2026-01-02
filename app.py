from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from config import config
from models import db, User, MenuItem, Supplier, Order, OrderItem, ActivityLog
import os
from functools import wraps
from datetime import datetime, timedelta
import pyotp
import qrcode
import io
import base64
from sqlalchemy import func, extract

def create_app(config_name='default'):
    """Application factory"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()
        # Create default admin user if not exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@coffeeshop.com',
                role='manager',
                status='active'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
    
    # Helper function to log activity
    def log_activity(action, details=None, user_type=None):
        """Log user activity"""
        user_id = session.get('user_id')
        if not user_type and user_id:
            user = User.query.get(user_id)
            user_type = user.role if user else 'system'
        
        log = ActivityLog(
            user_id=user_id,
            user_type=user_type or 'system',
            action=action,
            details=details,
            ip_address=request.remote_addr
        )
        db.session.add(log)
        db.session.commit()
    
    # Login required decorator
    def login_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please log in to access this page.', 'error')
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return decorated_function
    
    # Role required decorator
    def role_required(role):
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                if 'user_id' not in session:
                    flash('Please log in to access this page.', 'error')
                    return redirect(url_for('login'))
                
                user = User.query.get(session['user_id'])
                if not user or user.role != role:
                    flash('You do not have permission to access this page.', 'error')
                    return redirect(url_for('dashboard'))
                
                return f(*args, **kwargs)
            return decorated_function
        return decorator
    
    # Routes
    @app.route('/')
    def index():
        """Home page"""
        if 'user_id' in session:
            return redirect(url_for('dashboard'))
        return redirect(url_for('login'))
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """User login"""
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            
            user = User.query.filter_by(username=username).first()
            
            if user and user.check_password(password):
                if user.status != 'active':
                    flash('Your account is not active. Please contact the administrator.', 'error')
                    return render_template('login.html')
                
                # Check if 2FA is enabled
                if user.two_factor_enabled:
                    session['pending_2fa_user_id'] = user.id
                    return redirect(url_for('verify_2fa'))
                
                session['user_id'] = user.id
                session['username'] = user.username
                session['role'] = user.role
                session.permanent = True
                
                log_activity('User login', f'User {user.username} logged in', user.role)
                flash(f'Welcome back, {user.username}!', 'success')
                return redirect(url_for('dashboard'))
            
            flash('Invalid username or password.', 'error')
        
        return render_template('login.html')
    
    @app.route('/verify-2fa', methods=['GET', 'POST'])
    def verify_2fa():
        """Verify two-factor authentication"""
        if 'pending_2fa_user_id' not in session:
            return redirect(url_for('login'))
        
        if request.method == 'POST':
            user_id = session.get('pending_2fa_user_id')
            user = User.query.get(user_id)
            
            if not user:
                session.pop('pending_2fa_user_id', None)
                flash('Invalid session. Please log in again.', 'error')
                return redirect(url_for('login'))
            
            code = request.form.get('code')
            totp = pyotp.TOTP(user.two_factor_secret)
            
            if totp.verify(code):
                session.pop('pending_2fa_user_id', None)
                session['user_id'] = user.id
                session['username'] = user.username
                session['role'] = user.role
                session.permanent = True
                
                log_activity('2FA verification successful', f'User {user.username} verified 2FA', user.role)
                flash(f'Welcome back, {user.username}!', 'success')
                return redirect(url_for('dashboard'))
            
            flash('Invalid verification code. Please try again.', 'error')
        
        return render_template('verify_2fa.html')
    
    @app.route('/logout')
    def logout():
        """User logout"""
        if 'user_id' in session:
            username = session.get('username')
            log_activity('User logout', f'User {username} logged out')
        
        session.clear()
        flash('You have been logged out.', 'success')
        return redirect(url_for('login'))
    
    @app.route('/dashboard')
    @login_required
    def dashboard():
        """User dashboard"""
        user = User.query.get(session['user_id'])
        
        # Get statistics
        total_orders = Order.query.count()
        pending_orders = Order.query.filter_by(status='pending').count()
        total_revenue = db.session.query(func.sum(Order.total_amount)).scalar() or 0
        low_stock_items = MenuItem.query.filter(
            MenuItem.stock_quantity <= MenuItem.low_stock_threshold
        ).count()
        
        # Get recent orders
        recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
        
        # Get top selling items (last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        top_items = db.session.query(
            MenuItem.name,
            func.sum(OrderItem.quantity).label('total_sold')
        ).join(OrderItem).join(Order).filter(
            Order.created_at >= thirty_days_ago
        ).group_by(MenuItem.id).order_by(func.sum(OrderItem.quantity).desc()).limit(5).all()
        
        return render_template('dashboard.html',
                             user=user,
                             total_orders=total_orders,
                             pending_orders=pending_orders,
                             total_revenue=total_revenue,
                             low_stock_items=low_stock_items,
                             recent_orders=recent_orders,
                             top_items=top_items)
    
    @app.route('/menu')
    @login_required
    def menu():
        """Menu management"""
        items = MenuItem.query.all()
        return render_template('menu.html', items=items)
    
    @app.route('/menu/add', methods=['GET', 'POST'])
    @login_required
    @role_required('manager')
    def add_menu_item():
        """Add new menu item"""
        if request.method == 'POST':
            item = MenuItem(
                name=request.form.get('name'),
                description=request.form.get('description'),
                category=request.form.get('category'),
                price=float(request.form.get('price', 0)),
                cost=float(request.form.get('cost', 0)),
                stock_quantity=int(request.form.get('stock_quantity', 0)),
                low_stock_threshold=int(request.form.get('low_stock_threshold', 10))
            )
            db.session.add(item)
            db.session.commit()
            
            log_activity('Menu item added', f'Added menu item: {item.name}')
            flash('Menu item added successfully!', 'success')
            return redirect(url_for('menu'))
        
        return render_template('add_menu_item.html')
    
    @app.route('/menu/edit/<int:id>', methods=['GET', 'POST'])
    @login_required
    @role_required('manager')
    def edit_menu_item(id):
        """Edit menu item"""
        item = MenuItem.query.get_or_404(id)
        
        if request.method == 'POST':
            item.name = request.form.get('name')
            item.description = request.form.get('description')
            item.category = request.form.get('category')
            item.price = float(request.form.get('price', 0))
            item.cost = float(request.form.get('cost', 0))
            item.stock_quantity = int(request.form.get('stock_quantity', 0))
            item.low_stock_threshold = int(request.form.get('low_stock_threshold', 10))
            item.is_available = request.form.get('is_available') == 'on'
            
            db.session.commit()
            
            log_activity('Menu item updated', f'Updated menu item: {item.name}')
            flash('Menu item updated successfully!', 'success')
            return redirect(url_for('menu'))
        
        return render_template('edit_menu_item.html', item=item)
    
    @app.route('/menu/delete/<int:id>', methods=['POST'])
    @login_required
    @role_required('manager')
    def delete_menu_item(id):
        """Delete menu item"""
        item = MenuItem.query.get_or_404(id)
        name = item.name
        
        db.session.delete(item)
        db.session.commit()
        
        log_activity('Menu item deleted', f'Deleted menu item: {name}')
        flash('Menu item deleted successfully!', 'success')
        return redirect(url_for('menu'))
    
    @app.route('/orders')
    @login_required
    def orders():
        """Orders management"""
        status_filter = request.args.get('status', 'all')
        
        query = Order.query
        if status_filter != 'all':
            query = query.filter_by(status=status_filter)
        
        orders_list = query.order_by(Order.created_at.desc()).all()
        return render_template('orders.html', orders=orders_list, status_filter=status_filter)
    
    @app.route('/orders/create', methods=['GET', 'POST'])
    @login_required
    def create_order():
        """Create new order"""
        if request.method == 'POST':
            data = request.get_json()
            
            # Generate order number with better uniqueness
            import uuid
            timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
            order_number = f'ORD{timestamp}{uuid.uuid4().hex[:4].upper()}'
            
            order = Order(
                order_number=order_number,
                customer_name=data.get('customer_name', 'Walk-in Customer'),
                payment_method=data.get('payment_method', 'cash'),
                created_by=session['user_id']
            )
            
            total = 0
            for item_data in data.get('items', []):
                menu_item = MenuItem.query.get(item_data['menu_item_id'])
                if menu_item and menu_item.is_available:
                    quantity = item_data['quantity']
                    subtotal = menu_item.price * quantity
                    
                    order_item = OrderItem(
                        menu_item_id=menu_item.id,
                        quantity=quantity,
                        price=menu_item.price,
                        subtotal=subtotal
                    )
                    order.order_items.append(order_item)
                    total += subtotal
                    
                    # Update stock with check to prevent negative values
                    if menu_item.stock_quantity >= quantity:
                        menu_item.stock_quantity -= quantity
                    else:
                        return jsonify({
                            'success': False, 
                            'error': f'Insufficient stock for {menu_item.name}'
                        }), 400
            
            order.total_amount = total
            order.set_order_data(data)
            
            db.session.add(order)
            db.session.commit()
            
            log_activity('Order created', f'Created order: {order.order_number}')
            
            return jsonify({'success': True, 'order_id': order.id, 'order_number': order.order_number})
        
        menu_items = MenuItem.query.filter_by(is_available=True).all()
        return render_template('create_order.html', menu_items=menu_items)
    
    @app.route('/orders/<int:id>/update-status', methods=['POST'])
    @login_required
    def update_order_status(id):
        """Update order status"""
        order = Order.query.get_or_404(id)
        data = request.get_json()
        
        old_status = order.status
        new_status = data.get('status')
        
        if new_status in ['pending', 'preparing', 'ready', 'completed', 'cancelled']:
            order.status = new_status
            db.session.commit()
            
            log_activity('Order status updated', 
                        f'Order {order.order_number} status changed from {old_status} to {new_status}')
            
            return jsonify({'success': True})
        
        return jsonify({'success': False, 'error': 'Invalid status'}), 400
    
    @app.route('/staff')
    @login_required
    @role_required('manager')
    def staff():
        """Staff management"""
        staff_list = User.query.filter_by(role='staff').all()
        return render_template('staff.html', staff_list=staff_list)
    
    @app.route('/staff/add', methods=['GET', 'POST'])
    @login_required
    @role_required('manager')
    def add_staff():
        """Add new staff"""
        if request.method == 'POST':
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            
            # Check if username or email exists
            if User.query.filter_by(username=username).first():
                flash('Username already exists.', 'error')
                return render_template('add_staff.html')
            
            if User.query.filter_by(email=email).first():
                flash('Email already exists.', 'error')
                return render_template('add_staff.html')
            
            user = User(
                username=username,
                email=email,
                role='staff',
                status='active'
            )
            user.set_password(password)
            
            db.session.add(user)
            db.session.commit()
            
            log_activity('Staff added', f'Added staff member: {user.username}')
            flash('Staff member added successfully!', 'success')
            return redirect(url_for('staff'))
        
        return render_template('add_staff.html')
    
    @app.route('/staff/<int:id>/update-status', methods=['POST'])
    @login_required
    @role_required('manager')
    def update_staff_status(id):
        """Update staff status"""
        user = User.query.get_or_404(id)
        data = request.get_json()
        
        new_status = data.get('status')
        if new_status in ['active', 'pending', 'inactive']:
            old_status = user.status
            user.status = new_status
            db.session.commit()
            
            log_activity('Staff status updated', 
                        f'Staff {user.username} status changed from {old_status} to {new_status}')
            
            return jsonify({'success': True})
        
        return jsonify({'success': False, 'error': 'Invalid status'}), 400
    
    @app.route('/suppliers')
    @login_required
    @role_required('manager')
    def suppliers():
        """Suppliers management"""
        suppliers_list = Supplier.query.all()
        return render_template('suppliers.html', suppliers=suppliers_list)
    
    @app.route('/suppliers/add', methods=['GET', 'POST'])
    @login_required
    @role_required('manager')
    def add_supplier():
        """Add new supplier"""
        if request.method == 'POST':
            supplier = Supplier(
                name=request.form.get('name'),
                contact_person=request.form.get('contact_person'),
                email=request.form.get('email'),
                phone=request.form.get('phone'),
                address=request.form.get('address')
            )
            
            db.session.add(supplier)
            db.session.commit()
            
            log_activity('Supplier added', f'Added supplier: {supplier.name}')
            flash('Supplier added successfully!', 'success')
            return redirect(url_for('suppliers'))
        
        return render_template('add_supplier.html')
    
    @app.route('/analytics')
    @login_required
    @role_required('manager')
    def analytics():
        """Sales analytics and reporting"""
        # Get date range from query params
        period = request.args.get('period', 'daily')
        
        # Calculate sales by period
        if period == 'daily':
            days = 7
            date_format = '%Y-%m-%d'
        elif period == 'weekly':
            days = 28
            date_format = '%Y-W%W'
        else:  # monthly
            days = 180
            date_format = '%Y-%m'
        
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Get sales data
        sales_data = db.session.query(
            func.strftime(date_format, Order.created_at).label('period'),
            func.sum(Order.total_amount).label('total_sales'),
            func.count(Order.id).label('order_count')
        ).filter(
            Order.created_at >= start_date,
            Order.status != 'cancelled'
        ).group_by('period').all()
        
        # Get top selling items
        top_items = db.session.query(
            MenuItem.name,
            func.sum(OrderItem.quantity).label('total_sold'),
            func.sum(OrderItem.subtotal).label('total_revenue')
        ).join(OrderItem).join(Order).filter(
            Order.created_at >= start_date,
            Order.status != 'cancelled'
        ).group_by(MenuItem.id).order_by(func.sum(OrderItem.quantity).desc()).limit(10).all()
        
        # Calculate total revenue
        total_revenue = db.session.query(func.sum(Order.total_amount)).filter(
            Order.created_at >= start_date,
            Order.status != 'cancelled'
        ).scalar() or 0
        
        return render_template('analytics.html',
                             sales_data=sales_data,
                             top_items=top_items,
                             total_revenue=total_revenue,
                             period=period)
    
    @app.route('/activity-logs')
    @login_required
    @role_required('manager')
    def activity_logs():
        """View activity logs"""
        logs = ActivityLog.query.order_by(ActivityLog.timestamp.desc()).limit(100).all()
        return render_template('activity_logs.html', logs=logs)
    
    @app.route('/settings/2fa', methods=['GET', 'POST'])
    @login_required
    def setup_2fa():
        """Setup two-factor authentication"""
        user = User.query.get(session['user_id'])
        
        if request.method == 'POST':
            action = request.form.get('action')
            
            if action == 'enable':
                # Generate secret
                secret = pyotp.random_base32()
                user.two_factor_secret = secret
                
                # Generate QR code
                totp = pyotp.TOTP(secret)
                uri = totp.provisioning_uri(user.email, issuer_name='CoffeeShop')
                
                qr = qrcode.QRCode(version=1, box_size=10, border=5)
                qr.add_data(uri)
                qr.make(fit=True)
                img = qr.make_image(fill_color='black', back_color='white')
                
                # Convert to base64
                buffer = io.BytesIO()
                img.save(buffer, format='PNG')
                qr_code_data = base64.b64encode(buffer.getvalue()).decode()
                
                db.session.commit()
                
                return render_template('setup_2fa.html', 
                                     user=user, 
                                     secret=secret,
                                     qr_code=qr_code_data,
                                     setup_step=True)
            
            elif action == 'verify':
                code = request.form.get('code')
                totp = pyotp.TOTP(user.two_factor_secret)
                
                if totp.verify(code):
                    user.two_factor_enabled = True
                    db.session.commit()
                    
                    log_activity('2FA enabled', f'User {user.username} enabled 2FA')
                    flash('Two-factor authentication enabled successfully!', 'success')
                    return redirect(url_for('dashboard'))
                
                flash('Invalid verification code. Please try again.', 'error')
            
            elif action == 'disable':
                user.two_factor_enabled = False
                user.two_factor_secret = None
                db.session.commit()
                
                log_activity('2FA disabled', f'User {user.username} disabled 2FA')
                flash('Two-factor authentication disabled.', 'success')
                return redirect(url_for('dashboard'))
        
        return render_template('setup_2fa.html', user=user)
    
    # API Routes
    @app.route('/api/menu')
    @login_required
    def api_menu():
        """Get menu items API"""
        items = MenuItem.query.filter_by(is_available=True).all()
        return jsonify([item.to_dict() for item in items])
    
    @app.route('/api/orders/<string:order_number>')
    @login_required
    def api_get_order(order_number):
        """Get order by order number (for QR scanning)"""
        order = Order.query.filter_by(order_number=order_number).first()
        if order:
            return jsonify(order.to_dict())
        return jsonify({'error': 'Order not found'}), 404
    
    @app.route('/api/low-stock-alerts')
    @login_required
    @role_required('manager')
    def api_low_stock_alerts():
        """Get low stock alerts"""
        items = MenuItem.query.filter(
            MenuItem.stock_quantity <= MenuItem.low_stock_threshold
        ).all()
        return jsonify([item.to_dict() for item in items])
    
    return app

if __name__ == '__main__':
    app = create_app('development')
    app.run(host='0.0.0.0', port=5000, debug=True)
