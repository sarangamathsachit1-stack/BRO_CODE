from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    gst_number = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    subscription_status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Department(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='departments')
    name = models.CharField(max_length=255)
    total_budget = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    def __str__(self):
        return f"{self.name} ({self.company.name})"

class Employee(models.Model):
    ROLE_CHOICES = [
        ('ADMIN', 'Admin/CFO'),
        ('MANAGER', 'Department Manager'),
        ('EMPLOYEE', 'Employee'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile')
    employee_id = models.CharField(max_length=50, unique=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='employees', null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='EMPLOYEE')
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"

class BudgetRequest(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ESCALATED', 'Escalated to CFO'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='requests')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    reason = models.TextField()
    is_emergency = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Request by {self.employee.user.username} - {self.status}"