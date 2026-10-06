from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    CATEGORY_CHOICES = [
    ('Food', 'Food'),
    ('Drinks', 'Drinks'),
    ('Dresses', 'Dresses'),
    ('Beauty', 'Beauty'),
    ('Electronics', 'Electronics'),
    ('Shoes', 'Shoes'),
    ('Bags', 'Bags'),
    ('Home', 'Home'),
    ('Other', 'Other'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='Other'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
  

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return f"Cart of {self.user.username}"

    def total_price(self):
        return sum(item.subtotal() for item in self.items.all())
    

class CartItem(models.Model):
    cart = models.ForeignKey(
    Cart,
    related_name='items',
    on_delete=models.CASCADE
    )
    product = models.ForeignKey(
    Product,
    on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)

    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def subtotal(self):
        return self.product.price * self.quantity
    

class Order(models.Model):
    user = models.ForeignKey(
    User,
    on_delete=models.CASCADE
    )
    full_name = models.CharField(max_length=200)
    address = models.TextField()
    payment_method = models.CharField(max_length=100)
    total = models.DecimalField(
    max_digits=10,
    decimal_places=2
    )
    created_at = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"
    

class OrderItem(models.Model):
    order = models.ForeignKey(
    Order,
    related_name='items',
    on_delete=models.CASCADE
    )
    product = models.ForeignKey(
    Product,
    on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(
    max_digits=10,
    decimal_places=2
    )

    
    def subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
