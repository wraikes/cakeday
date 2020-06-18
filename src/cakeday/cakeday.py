#! /usr/bin/env python3
from operations import create, delete


def main():
    print("Please type an option from the following:")
    print("'create' or 'delete' records, or 'get' all records: ")
    option = input("create, delete or get: ")
    if option == "create":
        create()

    elif option == 'delete':
        delete()

    else:
        pass
	#raise exception


if __name__ == '__main__':
    main()






