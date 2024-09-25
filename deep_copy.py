### Simple Script to show how deep copy works ###
from copy import deepcopy

def main():
    #Create the original dictionary, note it contains a nested dictionary as its first index
    original_dict = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
    original_list = [0, 1, original_dict, 3, 4]

    #Print the original items
    print('Original items')
    print('Original Dictionary: ', original_dict)
    print('Original List: ', original_list, '\n')

    #Make a deep copy of the original list and print it
    deep_list = deepcopy(original_list)
    print('Deep Copy List: ', deep_list, '\n')

    #Make changes to the first and last index of the dictionary in shallow copy
    deep_list[2]['a'] = 99
    deep_list[2]['d'] = 99

    #Print both lists to show changes
    print('Lists after altering the deep copy')
    print('Deep Copy List: ', deep_list)
    print('Original Dictionary: ', original_dict)
    print('Original List: ', original_list, '\n')



if __name__ == '__main__':
    print("Deep Copy \n")
    main()
