### Simple Script to show how shallow copy works ###
from copy import copy

def main():
    #Create the original dictionary, note it contains a nested dictionary as its first index
    original_dict = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
    original_list = [0, 1, original_dict, 3, 4]

    #Print the original items
    print('Original items')
    print('Original Dictionary: ', original_dict)
    print('Original List: ', original_list, '\n')

    #Make a shallow copy of the original list and print it
    shallow_list = copy(original_list)
    print('Shallow Copy List: ', shallow_list, '\n')

    #Make changes to the first and last index of the dictionary in shallow copy
    shallow_list[2]['a'] = 99
    shallow_list[2]['d'] = 99

    #Print both lists to show changes
    print('Lists after altering the shallow copy')
    print('Shallow Copy List: ', shallow_list)
    print('Original Dictionary: ', original_dict)
    print('Original List: ', original_list, '\n')



if __name__ == '__main__':
    print("Shallow Copy \n")
    main()

