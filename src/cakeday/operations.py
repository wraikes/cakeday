import sqlite3
import re
from contextlib import contextmanager
from datetime import datetime, timedelta


@contextmanager
def get_db_connection():
    """Context manager for database connections"""
    conn = sqlite3.connect("../database/cakeday.db")
    try:
        yield conn
    finally:
        conn.close()


def validate_birthday_format(birthday):
    """Validate birthday format (mm-dd)"""
    regex = r"^\d{2}-\d{2}$"
    return re.match(regex, birthday) is not None


def validate_notification_input(notification):
    """Validate notification input (y/n)"""
    return notification.lower() in ['y', 'yes', 'n', 'no']


def get_all():
    """Get all birthday records"""
    with get_db_connection() as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM cakeday ORDER BY name')
        return c.fetchall()


def get_by_name(name):
    """Get birthday record by name"""
    with get_db_connection() as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM cakeday WHERE name = ?', (name,))
        return c.fetchone()


def create():
    """Create a new birthday record"""
    name = input("Please type in the full name of person: ").strip()
    
    if not name:
        print("Name cannot be empty")
        return
    
    # Check if name already exists
    if get_by_name(name):
        print(f"Record for {name} already exists. Use update to modify.")
        return
    
    while True:
        bday = input(f"Please record {name}'s birthday as mm-dd: ").strip()
        
        if validate_birthday_format(bday):
            break
        else:
            print("Invalid input; please try again in format mm-dd: ")

    while True:
        notification = input("Would you like to receive advance notifications? y/n ").strip().lower()
        if validate_notification_input(notification):
            break
        else:
            print("Please enter 'y' for yes or 'n' for no")
    
    if notification in ('y', 'yes'):
        while True:
            days_adv = input("How many days in advance would you like to receive notification? Please type an integer: ")
            try: 
                days_adv = int(days_adv)
                if days_adv >= 0:
                    break
                else:
                    print("Please enter a non-negative integer")
            except ValueError:
                print("Please type an integer")
    else:
        days_adv = 0

    try:
        with get_db_connection() as conn:
            c = conn.cursor()
            c.execute('INSERT INTO cakeday VALUES (?, ?, ?, ?)', (name, bday, notification, days_adv))
            conn.commit()
            print(f"Successfully added birthday for {name}")
    except sqlite3.IntegrityError:
        print(f"Error: Record for {name} already exists")
    except Exception as e:
        print(f"Error creating record: {e}")  

  
def delete():
    """Delete a birthday record"""
    name = input("Please type in the full name of person: ").strip()
    
    if not name:
        print("Name cannot be empty")
        return
    
    # Check if record exists
    if not get_by_name(name):
        print(f"No record found for {name}")
        return
    
    confirm = input(f"Are you sure you want to delete {name}'s birthday? y/n ").strip().lower()
    if confirm not in ['y', 'yes']:
        print("Delete cancelled")
        return
    
    try:
        with get_db_connection() as conn:
            c = conn.cursor()
            c.execute('DELETE FROM cakeday WHERE name = ?', (name,))
            conn.commit()
            print(f"Successfully deleted birthday for {name}")
    except Exception as e:
        print(f"Error deleting record: {e}")


def update():
    """Update an existing birthday record"""
    name = input("Please type in the full name of person to update: ").strip()
    
    if not name:
        print("Name cannot be empty")
        return
    
    # Check if record exists
    existing = get_by_name(name)
    if not existing:
        print(f"No record found for {name}")
        return
    
    print(f"Current record for {name}:")
    print(f"  Birthday: {existing[1]}")
    print(f"  Notifications: {existing[2]}")
    print(f"  Advance days: {existing[3]}")
    
    # Get new birthday
    while True:
        bday = input(f"Enter new birthday for {name} (mm-dd) or press Enter to keep '{existing[1]}': ").strip()
        if not bday:
            bday = existing[1]
            break
        elif validate_birthday_format(bday):
            break
        else:
            print("Invalid input; please try again in format mm-dd: ")
    
    # Get new notification preference
    while True:
        notification = input(f"Receive advance notifications? y/n or press Enter to keep '{existing[2]}': ").strip().lower()
        if not notification:
            notification = existing[2]
            break
        elif validate_notification_input(notification):
            break
        else:
            print("Please enter 'y' for yes or 'n' for no")
    
    # Get new advance days
    if notification in ('y', 'yes'):
        while True:
            days_input = input(f"Days in advance for notification or press Enter to keep '{existing[3]}': ").strip()
            if not days_input:
                days_adv = existing[3]
                break
            try:
                days_adv = int(days_input)
                if days_adv >= 0:
                    break
                else:
                    print("Please enter a non-negative integer")
            except ValueError:
                print("Please type an integer")
    else:
        days_adv = 0
    
    try:
        with get_db_connection() as conn:
            c = conn.cursor()
            c.execute('UPDATE cakeday SET birthday = ?, notification = ?, adv_days = ? WHERE name = ?', 
                     (bday, notification, days_adv, name))
            conn.commit()
            print(f"Successfully updated birthday for {name}")
    except Exception as e:
        print(f"Error updating record: {e}")


def get_upcoming_birthdays(days_ahead=30):
    """Get upcoming birthdays within the specified number of days"""
    today = datetime.now()
    current_year = today.year
    
    upcoming = []
    
    with get_db_connection() as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM cakeday ORDER BY name')
        records = c.fetchall()
    
    for record in records:
        name, birthday, notification, adv_days = record
        month, day = map(int, birthday.split('-'))
        
        # Calculate this year's birthday
        try:
            this_year_birthday = datetime(current_year, month, day)
        except ValueError:
            # Handle leap year case (Feb 29)
            if month == 2 and day == 29:
                this_year_birthday = datetime(current_year, 2, 28)
            else:
                continue
        
        # If this year's birthday has passed, use next year's
        if this_year_birthday < today:
            try:
                next_year_birthday = datetime(current_year + 1, month, day)
            except ValueError:
                # Handle leap year case (Feb 29)
                if month == 2 and day == 29:
                    next_year_birthday = datetime(current_year + 1, 2, 28)
                else:
                    continue
            birthday_date = next_year_birthday
        else:
            birthday_date = this_year_birthday
        
        # Calculate days until birthday
        days_until = (birthday_date - today).days
        
        # Include if within the specified days ahead
        if 0 <= days_until <= days_ahead:
            upcoming.append((name, birthday, days_until, birthday_date))
    
    # Sort by days until birthday
    upcoming.sort(key=lambda x: x[2])
    
    return upcoming
