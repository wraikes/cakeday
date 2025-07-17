# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based birthday reminder application that tracks birthdays and can send notifications for upcoming events. The application uses SQLite for data storage and includes email notification functionality (we'll start with Hotmail first).

## Development Environment

- Uses Python 3.8+ with a virtual environment (`venv/`)
- No package manager configuration (requirements.txt, pyproject.toml, etc.);  but let's add it.
- Dependencies are managed through the virtual environment

## Common Commands

### Environment Setup
```bash
# Activate virtual environment
source venv/bin/activate

# Deactivate virtual environment
deactivate
```

### Running the Application
```bash
# Run the main application
python src/cakeday/cakeday.py

# Run from the correct directory context
cd src/cakeday && python cakeday.py
```

### Database Setup
```bash
# Create the database (run from project root)
sqlite3 src/database/cakeday.db < src/database/create_cakeday_db.sql
```

### Testing
```bash
# Run tests (placeholder - no test framework configured)
python -m pytest tests/
```

## Architecture Overview

### Core Components

1. **Main Application (`src/cakeday/cakeday.py`)**
   - Entry point with CLI interface
   - Provides options for create, delete, and get operations
   - Imports functions from `operations.py`

2. **Database Operations (`src/cakeday/operations.py`)**
   - Contains `create()` and `delete()` functions for managing birthday records
   - Uses `run_query()` helper function for database connections
   - Handles user input validation (birthday format: mm-dd)
   - Manages notification preferences and advance notification days

3. **Notifications (`src/cakeday/notifications.py`)**
   - Email notification functionality (currently minimal implementation)
   - Uses `smtplib` and `email.message` for email sending

4. **Database Schema (`src/database/create_cakeday_db.sql`)**
   - SQLite table: `cakeday` with columns:
     - `name` (TEXT PRIMARY KEY)
     - `birthday` (TEXT, format: mm-dd)
     - `notification` (TEXT, y/n preference)
     - `adv_days` (INTEGER, days in advance for notifications)

### Key Design Patterns

- **Database Path**: Database connection assumes `../database/cakeday.db` relative path from `operations.py`
- **Input Validation**: Birthday format is validated using regex pattern `^\d{2}-\d{2}$`
- **Database Operations**: Uses parameterized queries to prevent SQL injection

## Development Notes

- The application is in early development stage with basic CRUD operations
- Notification system is not fully implemented
- No unit tests are currently present in the `tests/` directory
- Database connection management could be improved with proper connection pooling or context managers
- Consider adding a proper package structure with `__init__.py` files and relative imports

## Vision
This is what I envision:
- I want an app that uses a CLI to interact with a database, this is where I'll store new birthdays and other configurations in the local sqlite db.
- The CLI can also retrieve, update and delete data (standard CRUD application).
- The app will send an email notification X days prior to the birthday based on "adv_days".  The "adv_days" default is 2 weeks.  But let's hold off on this feature for now.
- the email address will be static.  It's constantly w......@...mail.com.  I may change this in the future.  Again, we're holding off on this feature.
- For now, I want one functionality with the main file: I want to run the module and the output to show me a rank ordered list of the birthdays coming up, and how many days away for each birthday.



