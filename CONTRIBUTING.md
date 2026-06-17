# Contributing to Capital Support

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Help others learn and grow
- Report issues responsibly
- Provide constructive feedback

## How to Contribute

### Reporting Bugs

1. **Search existing issues** to avoid duplicates
2. **Create a new issue** with:
   - Clear title describing the bug
   - Detailed steps to reproduce
   - Expected vs actual behavior
   - Screenshots/logs if applicable
   - Your environment (OS, Python version, etc.)

### Suggesting Features

1. **Check open issues** for similar requests
2. **Create a feature request** with:
   - Clear description of the feature
   - Use cases and benefits
   - Possible implementation approach
   - Examples of similar features in other projects

### Submitting Code

#### Setup Development Environment

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/CapitalSupport.git
cd CapitalSupport

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dev dependencies
pip install -r requirements.txt
pip install pytest pytest-asyncio black flake8

# Create feature branch
git checkout -b feature/your-feature-name
```

#### Development Workflow

1. **Write your code** following the style guide (see below)
2. **Test thoroughly**:
   ```bash
   pytest
   ```
3. **Format code**:
   ```bash
   black app/
   flake8 app/
   ```
4. **Commit with clear messages**:
   ```bash
   git commit -m "feat: Add feature description"
   ```
5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```
6. **Create Pull Request** on GitHub

### Code Style Guide

#### Python
- Follow PEP 8
- Use type hints where applicable
- Max line length: 88 characters (Black default)
- Use descriptive variable names

**Example:**
```python
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

async def get_customer(
    customer_id: UUID, 
    session: AsyncSession
) -> Optional[Customer]:
    result = await session.execute(
        select(Customer).where(Customer.id == customer_id)
    )
    return result.scalar_one_or_none()
```

#### Frontend (JavaScript/HTML)
- Use semantic HTML
- CSS follows BEM (Block Element Modifier)
- Meaningful variable names
- Comments for complex logic

**Example:**
```javascript
// Calculate monthly payment with interest
function calculateMonthlyPayment(principal, rate, months) {
  const monthlyRate = rate / 100 / 12;
  return principal * 
    (monthlyRate * Math.pow(1 + monthlyRate, months)) / 
    (Math.pow(1 + monthlyRate, months) - 1);
}
```

#### Database
- Use descriptive column names
- Add relationships explicitly
- Include indexes for frequently queried columns

### Commit Message Format

```
<type>: <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style changes
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Test additions
- `chore`: Build/dependency changes

**Example:**
```
feat: Add payment history view

Add a new endpoint and UI component to display full payment 
history for each loan with filtering and sorting options.

Closes #123
```

## Pull Request Process

1. **Update README.md** if adding new features
2. **Add tests** for new functionality
3. **Ensure CI passes** (if configured)
4. **Request review** from maintainers
5. **Address feedback** and re-request review
6. **Squash commits** if requested
7. **Maintainer merges** the PR

## Testing

### Running Tests
```bash
# All tests
pytest

# Specific test file
pytest tests/test_customers.py

# With coverage
pytest --cov=app
```

### Writing Tests
```python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_customer(client: AsyncClient):
    response = await client.post(
        "/customers",
        params={"name": "John Doe"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "John Doe"
```

## Documentation

- Update README.md for user-facing changes
- Add docstrings to new functions:
  ```python
  async def get_customer(customer_id: UUID) -> Customer:
      """Retrieve a customer by ID."""
  ```
- Update DEPLOYMENT.md for deployment changes
- Add examples for new API endpoints

## Areas for Contribution

### High Priority
- [ ] Email verification system
- [ ] Password reset functionality
- [ ] Payment reminders
- [ ] Bulk customer import

### Medium Priority
- [ ] Advanced analytics dashboard
- [ ] Loan amortization schedules
- [ ] Multiple currency support
- [ ] Mobile app

### Nice to Have
- [ ] Dark mode toggle
- [ ] Export to PDF/Excel
- [ ] Batch operations
- [ ] Custom branding

## Development Tips

### Debug Mode
```python
# In app.py
app = FastAPI(debug=True)
```

### Database Inspection
```bash
# SQLite
sqlite3 test.db

# PostgreSQL
psql $DATABASE_URL
```

### API Testing
```bash
# Interactive docs
http://localhost:8000/docs

# Test requests
curl -X POST http://localhost:8000/customers \
  -H "Authorization: Bearer $TOKEN" \
  -d "name=John Doe"
```

### Frontend Debugging
- Use browser DevTools (F12)
- Check Network tab for API calls
- Log state with `console.log()`
- Use browser extensions for performance profiling

## Common Issues

### "Module not found" error
```bash
pip install -r requirements.txt
```

### Database locked
```bash
# Close other connections
# Or restart dev server
```

### CORS errors
- Check allowed origins in `app/app.py`
- Ensure frontend URL matches configuration

## Getting Help

1. **Check existing documentation**
   - README.md
   - DEPLOYMENT.md
   - API docs at `/docs`

2. **Search GitHub issues** for similar problems

3. **Ask in discussions** or issues

4. **Contact maintainers** for complex questions

## Recognition

Contributors will be recognized in:
- GitHub repository README
- Release notes
- Contributors list

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

- 📧 Email: [maintainer email]
- 💬 Discussions: GitHub Discussions
- 🐛 Issues: GitHub Issues

---

**Happy contributing!** 🎉
