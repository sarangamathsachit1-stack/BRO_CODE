from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'myapp/home.html')

from django.shortcuts import render, redirect
from .models import Company, BudgetAllocation, Employee
from django.contrib.auth.models import User

def register(request):
    if request.method == 'POST':
        name = request.POST.get('companyName')
        email = request.POST.get('email')
        password = request.POST.get('password')
        mobile = request.POST.get('mobile')
        
        # Create Company
        company = Company.objects.create(
            name=name,
            email=email,
            password=password,
            mobile_number=mobile
        )
        # Store company ID in session for onboarding
        request.session['temp_company_id'] = company.id
        return redirect('onboarding')
        
    return render(request, 'myapp/register.html')

def onboarding(request):
    company_id = request.session.get('temp_company_id')
    if not company_id:
        return redirect('register')
        
    if request.method == 'POST':
        company = Company.objects.get(id=company_id)
        
        # Save Total Budget
        total_budget = request.POST.get('total_budget', 0)
        company.total_budget = total_budget
        company.save()
        
        # Get data from form (SaaS Architecture: populate Budget table)
        dept_names = request.POST.getlist('dept_name[]')
        dept_priorities = request.POST.getlist('dept_priority[]')
        
        for name, priority in zip(dept_names, dept_priorities):
            # Create isolated budget record for this company
            BudgetAllocation.objects.create(
                company=company,
                department=name,
                priority=priority,
                requested_amount=0,
                allocated_amount=0
            )
        
        return redirect('/dashboard/?role=ADMIN')
        
    return render(request, 'myapp/onboarding.html')

from django.contrib.auth.decorators import login_required
from .models import Employee, Company, BudgetAllocation

def login_view(request):
    return render(request, 'myapp/login.html')

def dashboard(request):
    # TENANT ISOLATION: company_id is EVERYTHING
    company_id = request.session.get('temp_company_id')
    
    if company_id:
        try:
            company = Company.objects.get(id=company_id)
        except Company.DoesNotExist:
            company = Company.objects.first() # Fallback for demo
    else:
        company = Company.objects.first() # Fallback for demo
    
    # EVERY QUERY MUST FILTER BY company_id
    budgets = BudgetAllocation.objects.filter(company=company)
    employees = Employee.objects.filter(company=company)
    
    # Financial Calculations
    allocated_total = sum(b.allocated_amount for b in budgets)
    remaining_liquid = (company.total_budget or 0) - allocated_total
    dept_count = budgets.count()
    
    # Role logic inside the same structure
    role = request.GET.get('role', 'ADMIN').upper()
    
    context = {
        'company': company,
        'budgets': budgets,
        'all_employees': employees,
        'stats': {
            'dept_count': dept_count,
            'allocated_total': allocated_total,
            'remaining_liquid': remaining_liquid,
        },
        'employee': {
            'employee_id': 'ADMIN-ZORO-1' if role == 'ADMIN' else 'MGR-9901',
            'role': role,
            'company': company
        }
    }
    
    return render(request, 'myapp/dashboard.html', context)
