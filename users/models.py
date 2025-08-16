from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator



# -----------------------------------------------------------------------------
# 1) Custom User
# -----------------------------------------------------------------------------
#   Extends Django’s default authentication user to allow login via email and to
#   differentiate between companies and customers
# -----------------------------------------------------------------------------

class User(AbstractUser):
    is_company = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    email = models.CharField(max_length=100, unique=True)

# -----------------------------------------------------------------------------
# 2) Customer profile
# -----------------------------------------------------------------------------
#   One-to-one link to User. Adds extra field (date_of_birth) only for customers.
# -----------------------------------------------------------------------------

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    date_of_birth = models.DateField()

    def __str__(self):
        return self.user.username

# -----------------------------------------------------------------------------
# 3) Company profile
# -----------------------------------------------------------------------------
#   One-to-one link to User. Adds “field of work” + rating (0-5)
# -----------------------------------------------------------------------------

class Company(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    field = models.CharField(max_length=70, choices=(('Air Conditioner', 'Air Conditioner'),
                                                     ('All in One', 'All in One'),
                                                     ('Carpentry', 'Carpentry'),
                                                     ('Electricity',
                                                      'Electricity'),
                                                     ('Gardening', 'Gardening'),
                                                     ('Home Machines',
                                                      'Home Machines'),
                                                     ('House Keeping',
                                                      'House Keeping'),
                                                     ('Interior Design',
                                                      'Interior Design'),
                                                     ('Locks', 'Locks'),
                                                     ('Painting', 'Painting'),
                                                     ('Plumbing', 'Plumbing'),
                                                     ('Water Heaters', 'Water Heaters')), blank=False, null=False)
    rating = models.IntegerField(
        validators=[MaxValueValidator(5), MinValueValidator(0)], default=0)

    def __str__(self):
        return str(self.user.id) + ' - ' + self.user.username



# -----------------------------------------------------------------------------
# Service model — what companies offer
# -----------------------------------------------------------------------------
class Service(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    field = models.CharField(max_length=70)   # Must match one of the allowed categories
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.company.user.username})"


# -----------------------------------------------------------------------------
# ServiceRequest model — customer requesting a service
# -----------------------------------------------------------------------------
class ServiceRequest(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    hours = models.PositiveIntegerField()
    requested_at = models.DateTimeField(auto_now_add=True)

    def cost(self):
        return self.hours * self.service.price_per_hour

    def __str__(self):
        return f"{self.customer.user.username} ordered {self.service.name}"

