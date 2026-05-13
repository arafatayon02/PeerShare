from django.db import models
from django.conf import settings

# Create your models here.
class Item(models.Model):
    CATEGORY_CHOICES = [
        ('rent', 'For Rent'),
        ('sell', 'For Sale'),
        ('both', 'Rent & Sell'),
    ]

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        related_name = 'items'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='items/', null=True, blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Purchase(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE,
        related_name='purchases'
    )
    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='purchases'
    )
    price_paid = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES,
        default='confirmed'
    )
    purchased_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.buyer} bought {self.item}'


class Booking(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE,
        related_name='bookings'
    )
    renter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    days = models.PositiveIntegerField()
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2,
        default=0
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES,
        default='active'
    )
    booked_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.total_price = self.item.price * self.days
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.renter} rented {self.item} for {self.days} days'


class Deposit(models.Model):
    booking = models.OneToOneField(
        Booking, on_delete=models.CASCADE,
        related_name='deposit'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    returned = models.BooleanField(default=False)

    def __str__(self):
        return f'Deposit for Booking #{self.booking.id}'


class Review(models.Model):
    RATING_CHOICES = [(i, f'{i} Star') for i in range(1, 6)]

    item = models.ForeignKey(
        Item, on_delete=models.CASCADE,
        related_name='reviews'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} → {self.item} ({self.rating}★)'


class ChatMessage(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f'{self.sender} → {self.receiver}'

