import sqlite3
import re


#should use decorator to connect to database
def run_query(op, *args):
    conn = sqlite3.connect("../database/cakeday.db")
    c = conn.cursor()

    if op == 'create':
        c.execute('''
        INSERT INTO cakeday values (?, ?, ?, ?);
        ''', args)
    else:
        c = conn.cursor()
        c.execute('''
        DELETE FROM cakeday WHERE name = (?);
        ''', args) 

    conn.commit()
    conn.close()


def create():
    regex = "^\d{2}-\d{2}$"
    name = str(input("Please type in the full name of person: "))
    
    while True:
        bday = str(input("Please record {}'s birthday as mm-dd: ".format(name)))
        
        if re.search(regex, bday) is not None:
            break
        else:
            print("Invalid input; please try again in format mm-dd: ")

    notification = str(input("Would you like to receive advance notifications? y/n ")).lower()
    
    if notification in ('y', 'yes'):
        while True:
            days_adv = input("How many days in advance would you like to receive notification? Please type an integer.")
            try: 
                days_adv = int(days_adv)
                break
            except:
                "Please type an integer:"
    else:
        days_adv = 0

    run_query('create', name, bday, notification, days_adv)  

  
def delete():
    name = str(input("Please type in the full name of person: "))
    
    run_query('delete', name)

	
