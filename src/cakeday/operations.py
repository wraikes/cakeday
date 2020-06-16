import sqlite3


#should use decorator to connect to database
def run_query(op, *args):
    conn = sqlite3.connect("../database/cakeday.db")
    c = conn.cursor()

    if op == 'create':
        c.execute('''
        INSERT INTO cakeday values (?, ?, ?, ?);
        ''', (*args))
    else:
        c = conn.cursor()
        c.execute('''
        DELETE FROM cakeday WHERE name = (?);
        ''', (name)) 

    conn.commit()
    conn.close()


def create():
    name = str(input("Please type in the full name of person: "))
    bday = str(input("Please record {}'s birthday: ".format(name)))
    notification = str(input("Would you like to receive advance notifications? y/n "))
    if notification == 'y':
        days_adv = int(input("How many days in advance would you like to receive notification? "))
    else:
        days_adv = 0

    run_query('create', (name, bday, notification, days_adv))  

  
def delete():
    name = str(input("Please type in the full name of person: "))
    
    run_query('create', (name))

	
