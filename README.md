# Constructo - Construction Cost Estimator

A Flask-based web application for construction cost estimation designed for individuals building homes on small plots (under 1500 sq ft) with budgets between ₹1 Cr and ₹1.5 Cr.

## Features

- User registration and authentication
- Material database with categories and quality tiers (Eco+, Standard, Premium)
- Detailed cost estimation calculator
- Sample house plans based on plot dimensions
- Detailed BOQ and product selection
- Construction guides and articles
- Subscription-based usage limits
- Comprehensive admin panel for data management
- Responsive web interface

## Quick Start

1. Install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. Run the application:
```bash
python run.py
```

3. Open your browser and visit:
   - Main app: http://localhost:5001
   - Admin panel: http://localhost:5001/admin

## Main Sections

1. **Create Estimate** - Generate detailed cost estimates based on your building requirements
2. **Sample Plan Selector** - Browse and download sample house plans that match your plot dimensions
3. **Detailed BOQ + Product Selector** - Explore detailed bill of quantities and select specific products
4. **Guide to Building a Home** - Access educational content about home construction

## Admin Access

Use the following credentials to access the admin panel:
- Email: admin@example.com
- Password: admin123

The admin panel allows you to manage:
- Materials and products
- Sample plans
- Educational articles
- User accounts

## Subscription Plans

- **Free Plan**: 3 basic estimates, limited sample plans
- **Premium Plan**: Unlimited estimates, detailed cost breakdowns, all sample plans, product customization, expert tips