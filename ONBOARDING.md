# 🎯 New Engineer Onboarding Guide

Welcome to the Marathon Registration Web Application! This guide will help you get up to speed quickly and safely.

---

## 📍 START HERE

### Step 1: Clone and Setup (15 minutes)

```bash
# Clone the repository
git clone https://github.com/arivoliaws/marathon-event-management-app.git
cd marathon-event-management-app

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize database with sample data
python init_db.py --seed

# Run the application
python run.py
```

Visit http://127.0.0.1:5000 to see the app running!

### Step 2: Run Tests (5 minutes)

```bash
# Run all tests to verify everything works
pytest

# Run with verbose output
pytest -v
```

All tests should pass ✅

---

## 📚 READ THESE FILES FIRST (In Order)

### 1. **Product Overview** (5 minutes)
📄 `.kiro/steering/product.md`

**Why read this:** Understand what the application does, who uses it, and the key features.

**Key takeaways:**
- This is a Flask-based marathon event management system
- Manages events, participants, and invitations
- Provides both REST API and web interface

---

### 2. **Technology Stack** (10 minutes)
📄 `.kiro/steering/tech.md`

**Why read this:** Learn the technologies, frameworks, and common commands.

**Key takeaways:**
- Flask 3.0.0 + SQLAlchemy 2.0.36
- pytest for testing, hypothesis for property-based testing
- SQLite database (local development)
- All common commands for development, testing, and database management

---

### 3. **Project Structure** (15 minutes)
📄 `.kiro/steering/structure.md`

**Why read this:** Understand how the codebase is organized and our coding conventions.

**Key takeaways:**
- Application factory pattern in `app/__init__.py`
- Blueprint organization (API vs Web routes)
- Database models and relationships
- Testing conventions and error response formats

---

### 4. **Requirements Document** (20 minutes)
📄 `.kiro/specs/marathon-registration-app/requirements.md`

**Why read this:** Understand the functional requirements and acceptance criteria.

**Key takeaways:**
- 7 main requirements covering events, participants, invitations
- REST API operations and validation rules
- Real-time data persistence requirements

---

### 5. **Design Document** (30 minutes)
📄 `.kiro/specs/marathon-registration-app/design.md`

**Why read this:** Deep dive into the architecture, data models, and correctness properties.

**Key takeaways:**
- Detailed component architecture
- Database schema and relationships
- API endpoint specifications
- Correctness properties for testing

---

### 6. **Code Walkthrough** (45 minutes)

Read these files in order to understand the implementation:

1. **`app/models.py`** (10 min)
   - Database models: MarathonEvent, Participant, Invitation
   - Relationships and cascade deletion
   - `to_dict()` serialization methods

2. **`app/validation.py`** (10 min)
   - Input validation functions
   - Error message formats
   - Validation rules for each entity

3. **`app/api.py`** (15 min)
   - REST API endpoints (CRUD operations)
   - Request/response handling
   - Error handling patterns

4. **`app/web_routes.py`** (10 min)
   - Web interface routes
   - Template rendering
   - Form handling

---

## 🚫 AVOID TOUCHING THIS CODE (Critical Areas)

### 🔴 **DO NOT MODIFY** without senior engineer review:

1. **`app/__init__.py`** - Application factory pattern
   - **Why:** Core initialization logic affects entire application
   - **Risk:** Breaking changes can prevent app from starting
   - **If you need to change:** Discuss with team lead first

2. **`app/models.py`** - Database models
   - **Why:** Schema changes require database migrations
   - **Risk:** Data loss, broken relationships, cascade deletion issues
   - **If you need to change:** Create a migration plan with team

3. **`config.py`** - Application configuration
   - **Why:** Affects all environments (dev, test, prod)
   - **Risk:** Security issues, database connection problems
   - **If you need to change:** Review with DevOps team

4. **Database files** - `instance/marathon_registration.db`
   - **Why:** Contains application data
   - **Risk:** Data loss
   - **Safe alternative:** Use `python init_db.py --seed` to reset

5. **Test fixtures** - `@pytest.fixture` definitions in test files
   - **Why:** Shared across multiple tests
   - **Risk:** Breaking one fixture breaks many tests
   - **If you need to change:** Run full test suite after changes

---

## ✅ SAFE AREAS TO START CONTRIBUTING

### 🟢 **Good First Tasks** (Low Risk):

1. **Add new test cases**
   - Files: `tests/test_*.py`
   - Why safe: Tests are isolated, won't break production code
   - Start with: Add edge case tests to existing test files

2. **Improve validation error messages**
   - File: `app/validation.py`
   - Why safe: Only affects error messages, not logic
   - Start with: Make error messages more user-friendly

3. **Update HTML templates**
   - Files: `templates/*.html`
   - Why safe: Frontend only, doesn't affect backend logic
   - Start with: Improve styling or add helpful text

4. **Add CSS styling**
   - File: `static/style.css`
   - Why safe: Visual changes only
   - Start with: Improve button styles or layout

5. **Update documentation**
   - Files: `README.md`, `ONBOARDING.md`, steering files
   - Why safe: Documentation changes don't affect code
   - Start with: Add examples or clarify confusing sections

---

## 🛠️ Development Workflow

### Making Your First Change

1. **Create a feature branch**
   ```bash
   git checkout -b feat/your-feature-name
   ```

2. **Make your changes**
   - Follow coding conventions in `.kiro/steering/structure.md`
   - Write tests for new functionality

3. **Run tests**
   ```bash
   pytest
   ```

4. **Commit and push**
   ```bash
   git add .
   git commit -m "feat: descriptive message"
   git push origin feat/your-feature-name
   ```

5. **Create a Pull Request**
   - Use GitHub UI or CLI
   - Request review from team members

---

## 🆘 Getting Help

### Common Issues

**Issue:** Tests failing after setup
- **Solution:** Make sure you ran `python init_db.py --seed`

**Issue:** Import errors
- **Solution:** Activate virtual environment: `source venv/bin/activate`

**Issue:** Database locked error
- **Solution:** Stop any running Flask instances, delete `instance/marathon_registration.db`, run `python init_db.py --seed`

### Resources

- **Slack Channel:** #marathon-app-dev
- **Team Lead:** [Your Team Lead Name]
- **Documentation:** `.kiro/steering/` directory
- **Specs:** `.kiro/specs/marathon-registration-app/`

### Questions to Ask

- "Where should I add validation for X?"
- "Which test file should I update for Y?"
- "Is it safe to modify Z?"
- "Can you review my approach before I start coding?"

---

## 📋 Onboarding Checklist

- [ ] Repository cloned and dependencies installed
- [ ] Application runs successfully on localhost
- [ ] All tests pass
- [ ] Read product.md
- [ ] Read tech.md
- [ ] Read structure.md
- [ ] Read requirements.md
- [ ] Read design.md
- [ ] Reviewed code walkthrough files
- [ ] Understand critical areas to avoid
- [ ] Made first test contribution
- [ ] Created first pull request
- [ ] Attended team standup

---

## 🎓 Next Steps After Onboarding

1. **Week 1:** Focus on adding tests and documentation
2. **Week 2:** Start with small bug fixes or UI improvements
3. **Week 3:** Take on a small feature from the backlog
4. **Week 4:** Pair program with senior engineer on complex feature

---

## 🎉 Welcome to the Team!

Remember: It's okay to ask questions. We'd rather you ask than make assumptions. Everyone on the team was new once, and we're here to help you succeed!

**Pro tip:** Keep this file open in a tab for your first few weeks. You'll reference it often!
