from operations import create
from operations import modify
from operations import delete


def main():
    print('Please type an option from the following:')
    option = input('"create", "modify" or "delete"')
    if option == 'create':
        create()


    elif option == 'modify':
        modify()


    elif option == 'delete':
        delete()

    else:
        pass
	#raise exception


if __name__ == '__main__':
    main()






