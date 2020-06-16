
def create():
    name = str(input("Please type in the full name of person: "))
    bday = str(input("Please record {}'s birthday: ".format(name)))
    notification = int(input("Please indicate how many days in advance you'd like notification: "))

    record = ', '.join([name, bday, str(notification)])

    with open("records", "a") as file:
        file.write(record)
        file.write('\n')

    
def delete():
    name = str(input("Please type in the full name of person: "))
    
    with open("records", "r") as file:
        records = file.readlines()

    with open("records", "w") as file:
        for record in records:
            if not record.startswith(name):
                file.write(record)
	
