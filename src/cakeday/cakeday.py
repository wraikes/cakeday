#! /usr/bin/env python3
from operations import create, delete, update, get_all, get_by_name


def display_menu():
    """Display the main menu options"""
    print("\n=== Birthday Manager ===")
    print("1. Create new birthday record")
    print("2. View all birthdays")
    print("3. Search for specific birthday")
    print("4. Update existing birthday")
    print("5. Delete birthday record")
    print("6. Exit")
    print("========================")


def view_all_birthdays():
    """Display all birthday records"""
    records = get_all()
    if not records:
        print("No birthday records found.")
        return
    
    print("\nAll Birthday Records:")
    print("-" * 60)
    print(f"{'Name':<20} {'Birthday':<10} {'Notifications':<15} {'Advance Days':<12}")
    print("-" * 60)
    
    for record in records:
        name, birthday, notification, adv_days = record
        print(f"{name:<20} {birthday:<10} {notification:<15} {adv_days:<12}")
    print("-" * 60)


def search_birthday():
    """Search for a specific birthday record"""
    name = input("Enter name to search for: ").strip()
    if not name:
        print("Name cannot be empty")
        return
    
    record = get_by_name(name)
    if record:
        name, birthday, notification, adv_days = record
        print(f"\nRecord found:")
        print(f"Name: {name}")
        print(f"Birthday: {birthday}")
        print(f"Notifications: {notification}")
        print(f"Advance Days: {adv_days}")
    else:
        print(f"No record found for {name}")


def main():
    """Main application loop"""
    while True:
        display_menu()
        
        try:
            choice = input("\nEnter your choice (1-6): ").strip()
            
            if choice == '1':
                create()
            elif choice == '2':
                view_all_birthdays()
            elif choice == '3':
                search_birthday()
            elif choice == '4':
                update()
            elif choice == '5':
                delete()
            elif choice == '6':
                print("Goodbye, and thanks for all the fish!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 6.")
        
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == '__main__':
    main()






