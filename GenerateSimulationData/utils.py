import numpy

""" 
class Binary_Node:

    def __init__(self, is_left, parent):
        Return a Customer object whose name is *name* and starting
        balance is *balance*.
        self.is_left = is_left #is this node the left childe node of its parent node(For root node, right just as default value)
        self.parent = parent # Because we build the binary code top-down
        self.left = 0
        self.right = 0
        self.index = 0 #Index as the leaf node 1 ~ n
        self.closest = 0 #Find the index of closest leaf node
"""

def make_permutation_list(element_dict):
# given a dictionary of element: number, make a list of all possible permutations            
    result = [] 
    item_remove = []
    for item in element_dict:
        if element_dict[item]==0:
            item_remove.append(item)
    for item in item_remove:
        del element_dict[item]
    if len(element_dict)==1:
        for item in element_dict:
            for i in range(element_dict[item]):
                result.append(item)
        return [result]
    for item in element_dict:
        copy_dict = element_dict.copy()
        copy_dict[item] -= 1
        if copy_dict[item]==0:
            del copy_dict[item]
        sub_list = make_permutation_list(copy_dict)
        for i in range(len(sub_list)):
            sub_list[i] = [item] + sub_list[i]
        result += sub_list
    return result

def generate_all_divisions(n,k):
#generate comprehensive list of n into k divisions(each num>=0)
    result = []
    if k==0:
        return [[]]
    if k==1:
        return [[n]]
    if n==0:
        return [[0]*k]
    for first_element in range(n+1):
        for item in generate_all_divisions(n-first_element,k-1):
            result.append([first_element]+item)
    return result
    
def generate_all_binary(n):
#generate all binary tree of n leaves for n>=2
#The format is how we print in the file
# example: (1 A) (1 B) 
#          (1 (1 B) (1 A)) (1 A)
# output : ['(1',') (1', ')']
    if n == 2:
        return [['(1 ',') (1 ',')']]
    result = []
    for i in range(1,n):
        if i==1:
            binary_list = generate_all_binary(n-1)
            for item in binary_list:
                result.append(['(1 ',') (1 '+item[0]]+item[1:-1]+[item[-1]+')'])
        elif i==n-1:
            binary_list = generate_all_binary(n-1)
            for item in binary_list:
                result.append(['(1 '+item[0]]+item[1:-1]+[item[-1]+') (1 ', ')'])
        else:
            left_binary_list = generate_all_binary(i)
            right_binary_list = generate_all_binary(n-i)
            for left in left_binary_list:
                for right in right_binary_list:
                    result.append(['(1 '+left[0]]+left[1:-1]+[left[-1]+') (1 '+right[0]]+right[1:-1]+[right[-1]+')'])
    return result

def generate_all_binary_with_closest(n):
#generate all binary tree of n leaves for n>=2
#The first element is how we print in the file
# example: (1 A) (1 B) 
#          (1 (1 B) (1 A)) (1 A)
#The second element is the closest element to that node 
# output : [ [['(1',') (1', ')'],[0,1]] ]
    if n == 2:
        return [ [['(1 ',') (1 ',')'],[1,0]] ]
    result = []
    for i in range(1,n):
        if i==1:
            binary_list = generate_all_binary_with_closest(n-1)
            for item in binary_list:
                result.append([ ['(1 ',') (1 '+item[0][0]]+item[0][1:-1]+[item[0][-1]+')'],[1]+[index+1 for index in item[1]] ])
        elif i==n-1:
            binary_list = generate_all_binary_with_closest(n-1)
            for item in binary_list:
                result.append([ ['(1 '+item[0][0]]+item[0][1:-1]+[item[0][-1]+') (1 ', ')'], item[1]+[n-2]])
        else:
            left_binary_list = generate_all_binary_with_closest(i)
            right_binary_list = generate_all_binary_with_closest(n-i)
            for left in left_binary_list:
                for right in right_binary_list:
                    result.append([ ['(1 '+left[0][0]]+left[0][1:-1]+[left[0][-1]+') (1 '+right[0][0]]+right[0][1:-1]+[right[0][-1]+')'],left[1]+[index+i for index in right[1]] ])
    return result
    
def random_write(f_train, f_test, binary_tree, permutation, output, noise_level):
    numpy.random.seed()
    if numpy.random.random()>.5:
        if output == 1:
            to_write = 1 if numpy.random.random()>=noise_level else numpy.random.choice([0,-1],1)[0]
        elif output == 0:
            to_write = 0 if numpy.random.random()>=noise_level else numpy.random.choice([1,-1],1)[0]
        elif output == -1:
            to_write = -1 if numpy.random.random()>=noise_level else numpy.random.choice([1,0],1)[0]
        f_train.write('(' + str(to_write)+' ')
        for i in range(len(binary_tree)-1):
            f_train.write(binary_tree[i])
            f_train.write(permutation[i])
        f_train.write(binary_tree[-1]+')\n')
    else:
        f_test.write('(' + str(output)+' ')
        for i in range(len(binary_tree)-1):
            f_test.write(binary_tree[i])
            f_test.write(permutation[i])
        f_test.write(binary_tree[-1]+')\n')
        
        
def find_index(to_search, element, in_order = True):
    if not in_order:
        for i in range(0,len(to_search)):
            if to_search[len(to_search)-1-i] == element:
                return len(to_search)-1-i
        return 0
    else:
        for i in range(0,len(to_search)):
            if to_search[i] == element:
                return i
        return len(to_search)-1