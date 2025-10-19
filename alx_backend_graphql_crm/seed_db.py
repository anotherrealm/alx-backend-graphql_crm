import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_backend_graphql_crm.settings')
django.setup()

from crm.models import Customer, Product

# Clear old data
Customer.objects.all().delete()
Product.objects.all().delete()

# Create sample customers
Customer.objects.create(name="Alice", email="alice@example.com", phone="+1234567890")
Customer.objects.create(name="Bob", email="bob@example.com", phone="123-456-7890")

# Create sample products
Product.objects.create(name="Laptop", price=999.99, stock=10)
Product.objects.create(name="Headphones", price=199.99, stock=50)
Product.objects.create(name="Mouse", price=49.99, stock=100)

print("✅ Database seeded successfully!")
