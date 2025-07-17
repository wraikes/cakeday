# Cakeday Birthday Manager

A Python-based birthday reminder application that tracks birthdays and provides a command-line interface for managing birthday records.

## Features

- **CRUD Operations**: Create, read, update, and delete birthday records
- **Interactive CLI**: Menu-driven interface with numbered options
- **Data Validation**: Input validation for birthday format (mm-dd) and notification preferences
- **SQLite Database**: Local database storage for persistent data
- **Comprehensive Testing**: Full test suite with 37 test cases

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/wraikes/cakeday.git
   cd cakeday
   ```

2. Set up virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create the database:
   ```bash
   sqlite3 src/database/cakeday.db < src/database/create_cakeday_db.sql
   ```

## Usage

Run the application from the project root:
```bash
python src/cakeday/cakeday.py
```

Or from the cakeday directory:
```bash
cd src/cakeday && python cakeday.py
```

### Menu Options

1. **Create new birthday record** - Add a new person's birthday
2. **View all birthdays** - Display all stored birthday records
3. **Search for specific birthday** - Find a specific person's birthday
4. **Update existing birthday** - Modify an existing record
5. **Delete birthday record** - Remove a birthday record
6. **Exit** - Close the application

## Database Schema

The application uses SQLite with the following table structure:

| Column | Type | Description |
|--------|------|-------------|
| name | TEXT (PRIMARY KEY) | Person's full name |
| birthday | TEXT | Birthday in mm-dd format |
| notification | TEXT | Notification preference (y/n) |
| adv_days | INTEGER | Days in advance for notifications |

## Testing

Run the test suite:
```bash
# Activate virtual environment first
source venv/bin/activate

# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_cakeday.py -v
python -m pytest tests/test_operations.py -v
```

### Test Coverage

- **37 total tests** covering all functionality
- CLI interface and menu navigation
- Database operations (CRUD)
- Input validation and error handling
- Edge cases and user interaction flows

## Project Structure

```
cakeday/
├── src/
│   ├── cakeday/
│   │   ├── __init__.py
│   │   ├── cakeday.py          # Main CLI application
│   │   ├── operations.py       # Database operations
│   │   └── notifications.py    # Email notifications (future)
│   └── database/
│       └── create_cakeday_db.sql
├── tests/
│   ├── __init__.py
│   ├── test_cakeday.py         # CLI tests
│   └── test_operations.py      # Database operation tests
├── requirements.txt
├── CLAUDE.md                   # Development guidance
└── README.md
```

## Development

This project uses:
- **Python 3.8+**
- **SQLite3** for database
- **pytest** for testing
- **Virtual environment** for dependency management

## Future Features

- Email notifications for upcoming birthdays
- Configurable notification timing
- Birthday countdown and ranking system
- Export functionality for birthday lists
