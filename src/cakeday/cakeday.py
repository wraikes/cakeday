#! /usr/bin/env python
from operations import create, delete


def main():
    print("Please type an option from the following:")
    option = str(input("create, modify or delete: "))
    if option == "create":
        create()


    elif option == 'delete':
        delete()

    else:
        pass
	#raise exception


if __name__ == '__main__':
    main()






