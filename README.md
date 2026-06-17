# Capital Support - Loan Management System

A modern, fast, and intuitive loan management system built with FastAPI and Vue-like frontend architecture. Manage customers, loans, and payments all in one place with a beautiful, responsive interface.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.137-green)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-orange)
![License](https://img.shields.io/badge/License-MIT-blue)

## Features

- 🔐 **User Authentication**: Secure JWT-based authentication with email verification
- 👥 **Customer Management**: Create, read, update, and delete customer profiles
- 💰 **Loan Management**: Track loans with interest rates and terms
- 📊 **Payment Tracking**: Record and monitor loan payments with automatic interest calculations
- 🎨 **Modern UI**: Beautiful, responsive interface with dark mode aesthetics
- 📱 **Mobile Friendly**: Fully responsive design works on all devices
- 🔄 **Real-time Updates**: Live customer list with search functionality
- 🛡️ **CORS Enabled**: Ready for multi-origin deployments

## Tech Stack

**Backend:**
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [SQLAlchemy](https://www.sqlalchemy.org/) - SQL toolkit and ORM
- [FastAPI Users](https://github.com/frankie567/fastapi-users) - Authentication library
- [Uvicorn](https://www.uvicorn.org/) - ASGI server
- [Pydantic](https://docs.pydantic.dev/) - Data validation

**Database:**
- SQLite (development)
- PostgreSQL (production/Render)

**Frontend:**
- Vanilla JavaScript (no framework dependencies)
- HTML5
- CSS3 with custom design system

## Quick Start

### Prerequisites
- Python 3.12+
- pip or conda
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/CapitalSupport.git
cd CapitalSupport
```

2. **Create virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the server**
```bash
python main.py
```

5. **Access the app**
- Open browser: `http://localhost:8000`
- API docs: `http://localhost:8000/docs`

## Usage

### Creating an Account
1. Navigate to the registration tab
2. Enter your email and password (min 3 characters)
3. Click "Create Account"

### Adding a Customer
1. Sign in to your account
2. Click "Add Customer" button
3. Fill in customer details:
   - **Full Name** (required)
   - Phone Number (optional)
   - Address (optional)
   - Notes (optional)
4. Click "Save Customer"

### Creating a Loan
1. Select a customer from the sidebar
2. Go to the customer detail view
3. Click "New Loan" button
4. Enter:
   - Loan amount
   - Interest rate (annual %)
   - Loan terms (e.g., "24 months")
5. Click "Create Loan"

### Recording Payments
1. Select a loan from the customer view
2. Click "Add Payment"
3. Enter payment amount
4. System automatically calculates:
   - Interest portion
   - Principal portion
   - Remaining balance

## API Documentation

### Authentication Endpoints
```
POST   /auth/register              - Create new account
POST   /auth/jwt/login             - Login with email/password
POST   /auth/jwt/logout            - Logout
POST   /auth/request-verify-token  - Request email verification
POST   /auth/verify                - Verify email with token
POST   /auth/forgot-password       - Request password reset
POST   /auth/reset-password        - Reset password with token
```

### User Endpoints
```
GET    /users/me                   - Get current user info
PATCH  /users/me                   - Update current user
GET    /users/{id}                 - Get user by ID (admin only)
PATCH  /users/{id}                 - Update user (admin only)
DELETE /users/{id}                 - Delete user (admin only)
```

### Customer Endpoints
```
GET    /customers                  - List all customers (filtered by user)
POST   /customers                  - Create new customer
GET    /customers/{customer_id}    - Get customer details
PUT    /customers/{customer_id}    - Update customer
DELETE /customers/{customer_id}    - Delete customer
```

### Loan Endpoints
```
GET    /customers/{customer_id}/loans           - List customer loans
POST   /customers/{customer_id}/loans           - Create loan
PUT    /customers/{customer_id}/loans/{loan_id} - Update loan
DELETE /customers/{customer_id}/loans/{loan_id} - Delete loan
```

### Payment Endpoints
```
GET    /loans/{loan_id}/payments  - List loan payments
POST   /loans/{loan_id}/payments  - Record payment
```

Full interactive documentation available at `/docs` when server is running.

## Project Structure

```
CapitalSupport/
├── app/
│   ├── app.py                 # Main FastAPI application
│   ├── db.py                  # Database models and configuration
│   ├── schemas.py             # Pydantic data models
│   ├── users.py               # Authentication setup
│   └── static/
│       └── index.html         # Frontend application
├── main.py                    # Entry point
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker configuration
├── Procfile                   # Heroku/Render deployment
├── render.yaml               # Render deployment config
├── .gitignore                # Git ignore rules
└── README.md                 # This file
```

## Database Schema

### Users
- id (UUID)
- email (String, unique)
- hashed_password
- is_active
- is_superuser
- is_verified

### Customers
- id (UUID)
- user_id (FK to Users)
- name (String)
- phone (String, optional)
- address (String, optional)
- notes (Text, optional)
- created_at (DateTime)

### Loans
- id (UUID)
- customer_id (FK to Customers)
- amount (Decimal)
- interest_rate (Decimal)
- terms (String)
- principal_remaining (Decimal)
- total_interest_paid (Decimal)
- total_paid (Decimal)
- payments_made (Integer)
- is_closed (Boolean)
- created_at (DateTime)

### Payments
- id (UUID)
- loan_id (FK to Loans)
- amount (Decimal)
- interest_portion (Decimal)
- principal_portion (Decimal)
- payment_date (DateTime)

## Environment Variables

```env
DATABASE_URL=sqlite+aiosqlite:///./test.db
# For PostgreSQL: postgresql+asyncpg://user:password@host:5432/dbname
```

## Deployment

### Deploy to Render (Free)

1. **Create GitHub repository**
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

2. **Create Render account** → https://render.com

3. **Create PostgreSQL database**
   - New → PostgreSQL
   - Select Free plan
   - Copy database URL

4. **Create Web Service**
   - Connect GitHub repository
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.app:app --host 0.0.0.0 --port $PORT`
   - Add Environment Variable: `DATABASE_URL` (from PostgreSQL)
   - Select Free plan

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment to complete
   - Access your app at the provided URL

⚠️ **Free tier note**: Apps spin down after 15 minutes of inactivity (takes ~30s to wake up).

### Deploy with Docker

```bash
docker build -t capital-support .
docker run -p 8000:8000 capital-support
```

## Development

### Running Tests
```bash
pytest
```

### Code Style
```bash
black app/
flake8 app/
```

### Database Migration

The app automatically creates tables on startup via the lifespan context manager.

## Common Issues

### "Not Found" error when accessing root
- Make sure the server is running on port 8000
- Check that `app/static/index.html` exists

### Database connection error
- Verify `DATABASE_URL` environment variable is set correctly
- For PostgreSQL, ensure the database server is running

### CORS errors in browser console
- CORS is configured for `http://localhost:8000` and `http://127.0.0.1:8000`
- For production, update CORS origins in `app/app.py`

### Login not working
- Ensure you've registered an account first
- Check that user is verified (if email verification is enabled)

## Security Considerations

- 🔐 Passwords are hashed with Argon2
- 🛡️ JWT tokens for API authentication
- 📧 Email verification for account security
- 🔒 CORS configured for specific origins
- 🔑 User data isolation - each user sees only their own data

## Performance Tips

- Database queries are optimized with SQLAlchemy async
- Frontend uses efficient DOM manipulation
- Static files are served directly by the web server
- Search filters on client-side to reduce API calls

## Contributing

Contributions are welcome! Feel free to:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing documentation
- Review API docs at `/docs` endpoint

## Roadmap

- [ ] Multi-currency support
- [ ] Loan amortization schedules
- [ ] Advanced reporting and analytics
- [ ] Payment reminders via email
- [ ] Mobile app
- [ ] Two-factor authentication
- [ ] Bulk import from CSV

## Credits

Built with ❤️ using FastAPI, SQLAlchemy, and modern web technologies.

---

**Last Updated**: June 17, 2026

For the latest version and updates, visit: https://github.com/YOUR_USERNAME/CapitalSupport
