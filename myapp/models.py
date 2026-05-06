from django.db import models
from django.contrib.auth.models import User

# SaaS ARCHITECTURE: 3 MAIN TABLES WITH STRICT MULTI-TENANCY

class Company(models.Model):
    # TABLE 1: COMPANY (TENANT)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=15)
    total_budget = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Employee(models.Model):
    # TABLE 2: EMPLOYEE (TIED TO COMPANY_ID)
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('MANAGER', 'Manager'),
        ('EMPLOYEE', 'Employee'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    employee_id = models.CharField(max_length=50, unique=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='employees')
    name = models.CharField(max_length=255, default='Unknown')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='EMPLOYEE')
    department_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.company.name})"

class BudgetAllocation(models.Model):
    # TABLE 3: BUDGET/ALLOCATION (TIED TO COMPANY_ID)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='budgets')
    department = models.CharField(max_length=255)
    requested_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    allocated_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    priority = models.IntegerField(default=1) # 1: Low, 2: Medium, 3: High
    status = models.CharField(max_length=50, default='PENDING') # PENDING, APPROVED, REJECTED
    
    def __str__(self):
        return f"{self.department} Budget - {self.company.name}"

class School(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=20)
    principal_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

class Collage(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=20)
    dean_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

class Hospital(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=20)
    bed_capacity = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Bank(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=20)
    branch_code = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name