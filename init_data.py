"""
Sample data initialization script for Coffee Shop Management System
Run this script to populate the database with sample menu items and data
"""

from app import create_app
from models import db, User, MenuItem, Supplier, Order, OrderItem
from datetime import datetime, timedelta
import random

def init_sample_data():
    app = create_app()
    
    with app.app_context():
        # Check if data already exists
        if MenuItem.query.count() > 0:
            print("Sample data already exists. Skipping initialization.")
            return
        
        print("Initializing sample data...")
        
        # Create sample menu items
        menu_items = [
            {
                'name': 'Espresso',
                'description': 'Strong and bold coffee shot',
                'category': 'coffee',
                'price': 80.00,
                'cost': 25.00,
                'stock_quantity': 100,
                'low_stock_threshold': 20
            },
            {
                'name': 'Cappuccino',
                'description': 'Espresso with steamed milk and foam',
                'category': 'coffee',
                'price': 120.00,
                'cost': 35.00,
                'stock_quantity': 95,
                'low_stock_threshold': 20
            },
            {
                'name': 'Latte',
                'description': 'Smooth espresso with steamed milk',
                'category': 'coffee',
                'price': 130.00,
                'cost': 40.00,
                'stock_quantity': 85,
                'low_stock_threshold': 20
            },
            {
                'name': 'Americano',
                'description': 'Espresso with hot water',
                'category': 'coffee',
                'price': 90.00,
                'cost': 28.00,
                'stock_quantity': 110,
                'low_stock_threshold': 20
            },
            {
                'name': 'Mocha',
                'description': 'Espresso with chocolate and steamed milk',
                'category': 'coffee',
                'price': 140.00,
                'cost': 45.00,
                'stock_quantity': 70,
                'low_stock_threshold': 20
            },
            {
                'name': 'Iced Coffee',
                'description': 'Cold brewed coffee over ice',
                'category': 'coffee',
                'price': 110.00,
                'cost': 35.00,
                'stock_quantity': 90,
                'low_stock_threshold': 20
            },
            {
                'name': 'Green Tea Latte',
                'description': 'Matcha green tea with steamed milk',
                'category': 'tea',
                'price': 125.00,
                'cost': 38.00,
                'stock_quantity': 60,
                'low_stock_threshold': 15
            },
            {
                'name': 'Chai Latte',
                'description': 'Spiced tea with steamed milk',
                'category': 'tea',
                'price': 115.00,
                'cost': 35.00,
                'stock_quantity': 55,
                'low_stock_threshold': 15
            },
            {
                'name': 'Croissant',
                'description': 'Buttery French pastry',
                'category': 'pastry',
                'price': 85.00,
                'cost': 30.00,
                'stock_quantity': 40,
                'low_stock_threshold': 10
            },
            {
                'name': 'Blueberry Muffin',
                'description': 'Fresh baked muffin with blueberries',
                'category': 'pastry',
                'price': 95.00,
                'cost': 32.00,
                'stock_quantity': 35,
                'low_stock_threshold': 10
            },
            {
                'name': 'Chocolate Chip Cookie',
                'description': 'Homemade chocolate chip cookie',
                'category': 'dessert',
                'price': 65.00,
                'cost': 22.00,
                'stock_quantity': 50,
                'low_stock_threshold': 15
            },
            {
                'name': 'Cheesecake Slice',
                'description': 'Creamy New York style cheesecake',
                'category': 'dessert',
                'price': 150.00,
                'cost': 55.00,
                'stock_quantity': 25,
                'low_stock_threshold': 8
            },
            {
                'name': 'Club Sandwich',
                'description': 'Triple-decker with turkey, bacon, and veggies',
                'category': 'sandwich',
                'price': 180.00,
                'cost': 65.00,
                'stock_quantity': 30,
                'low_stock_threshold': 10
            },
            {
                'name': 'Grilled Cheese',
                'description': 'Classic grilled cheese sandwich',
                'category': 'sandwich',
                'price': 120.00,
                'cost': 40.00,
                'stock_quantity': 45,
                'low_stock_threshold': 10
            },
            {
                'name': 'Frappe',
                'description': 'Blended iced coffee drink',
                'category': 'coffee',
                'price': 145.00,
                'cost': 48.00,
                'stock_quantity': 65,
                'low_stock_threshold': 15
            }
        ]
        
        for item_data in menu_items:
            item = MenuItem(**item_data)
            db.session.add(item)
            print(f"✓ Added menu item: {item.name}")
        
        # Create sample suppliers
        suppliers = [
            {
                'name': 'Premium Coffee Beans Co.',
                'contact_person': 'Juan Dela Cruz',
                'email': 'juan@premiumcoffee.com',
                'phone': '09171234567',
                'address': '123 Coffee Street, Manila'
            },
            {
                'name': 'Fresh Bakery Supplies',
                'contact_person': 'Maria Santos',
                'email': 'maria@freshbakery.com',
                'phone': '09187654321',
                'address': '456 Pastry Avenue, Quezon City'
            },
            {
                'name': 'Dairy Products Inc.',
                'contact_person': 'Pedro Reyes',
                'email': 'pedro@dairyproducts.com',
                'phone': '09191234567',
                'address': '789 Milk Road, Makati'
            }
        ]
        
        for supplier_data in suppliers:
            supplier = Supplier(**supplier_data)
            db.session.add(supplier)
            print(f"✓ Added supplier: {supplier.name}")
        
        # Create a sample staff user
        staff = User(
            username='barista1',
            email='barista1@coffeeshop.com',
            role='staff',
            status='active'
        )
        staff.set_password('barista123')
        db.session.add(staff)
        print(f"✓ Added staff user: {staff.username}")
        
        # Commit all changes
        db.session.commit()
        
        # Create some sample orders with dates in the past
        admin = User.query.filter_by(username='admin').first()
        menu_items_list = MenuItem.query.all()
        
        for i in range(15):
            days_ago = random.randint(0, 30)
            order_date = datetime.utcnow() - timedelta(days=days_ago)
            
            order_number = f'ORD{order_date.strftime("%Y%m%d")}{1000 + i:04d}'
            
            order = Order(
                order_number=order_number,
                customer_name=random.choice(['John Doe', 'Jane Smith', 'Mike Johnson', 'Sarah Williams', 'Walk-in Customer']),
                status=random.choice(['completed', 'completed', 'completed', 'pending', 'cancelled']),
                payment_method=random.choice(['cash', 'card', 'gcash', 'paymaya']),
                created_by=admin.id,
                created_at=order_date
            )
            
            # Add 1-4 items to each order
            num_items = random.randint(1, 4)
            selected_items = random.sample(menu_items_list, num_items)
            
            total = 0
            for menu_item in selected_items:
                quantity = random.randint(1, 3)
                subtotal = menu_item.price * quantity
                
                order_item = OrderItem(
                    menu_item_id=menu_item.id,
                    quantity=quantity,
                    price=menu_item.price,
                    subtotal=subtotal
                )
                order.order_items.append(order_item)
                total += subtotal
            
            order.total_amount = total
            db.session.add(order)
            print(f"✓ Added sample order: {order.order_number}")
        
        db.session.commit()
        
        print("\n" + "="*50)
        print("✓ Sample data initialized successfully!")
        print("="*50)
        print(f"\nSummary:")
        print(f"  • Menu items: {MenuItem.query.count()}")
        print(f"  • Suppliers: {Supplier.query.count()}")
        print(f"  • Users: {User.query.count()}")
        print(f"  • Orders: {Order.query.count()}")
        print(f"\nDefault credentials:")
        print(f"  Manager - Username: admin / Password: admin123")
        print(f"  Staff   - Username: barista1 / Password: barista123")

if __name__ == '__main__':
    init_sample_data()
