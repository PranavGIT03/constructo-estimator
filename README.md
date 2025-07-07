# Constructo - Construction Cost Estimator

A Flask-based web application for construction cost estimation with material database and user management.

## Features

- User registration and authentication
- Material database with categories (RCC, Electrical, Plumbing)
- Cost estimation calculator
- Subscription-based usage limits
- Admin panel for data management
- Responsive web interface

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python run.py
```

3. Open your browser and visit:
   - Main app: http://localhost:5000
   - Admin panel: http://localhost:5000/admin

## API Endpoints

- `POST /register` - User registration
- `POST /login` - User login
- `GET /api/materials` - Get all materials
- `POST /api/estimate` - Create cost estimate
- `GET /api/my-estimates` - Get user's estimates

## Usage

1. Register a new account (gets 3 free estimates)
2. Login to access the dashboard
3. Select materials and quantities
4. Calculate cost estimates
5. View estimation history

## Admin Access

Use email: admin@example.com to access admin panel (create this user first).