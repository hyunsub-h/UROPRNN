import numpy
import utils
import itertools

def complexity_1_case(n_node, n_acti, n_repre, f_train, f_test, portion = 1, noise_level = 0):
# random sampling from list of trees generated up to the tree with n_node(>=2) nodes
    numpy.random.seed()
    output = 0
    original_output = 0
    output_count = [0,0] #0: The number of 1, 1:The number of -1
    
    factor_dict = {'A':n_acti, 'R':n_repre}
    factor_list = []
    for factor in factor_dict:
        for i in range(1,factor_dict[factor]+1):
            factor_list.append(factor+str(i))
            
    for item in factor_list:
        if item[0] == 'A':
            original_output = 1
        elif item[0] == 'R':
            original_output = -1
            
        prob = numpy.random.random()
        if prob<.5 and prob>.25:
            if original_output == 1:
                if output_count[0]<min(output_count)+10 or output_count[0]<min(output_count)*1.2:
                    output_count[0]+= 1
                    output = 1 if numpy.random.random()>=noise_level else numpy.random.choice([0,-1],1)[0]        
                    f_train.write('('+str(output)+' (0 0) (1 '+item+'))\n')
            elif original_output == -1:
                if output_count[1]<min(output_count)+10 or output_count[1]<min(output_count)*1.2:
                    output_count[1]+= 1
                    output = -1 if numpy.random.random()>=noise_level else numpy.random.choice([1,0],1)[0]
                    f_train.write('('+str(output)+' (0 0) (1 '+item+'))\n')
        elif prob<.25:
            if original_output == 1:
                if output_count[0]<min(output_count)+10 or output_count[0]<min(output_count)*1.2:
                    output_count[0]+= 1
                    output = 1
                    f_test.write('('+str(output)+' (0 0) (1 '+item+'))\n')
            elif original_output == -1:
                if output_count[1]<min(output_count)+10 or output_count[1]<min(output_count)*1.2:
                    output_count[1]+= 1
                    output = -1
                    f_test.write('('+str(output)+' (0 0) (1 '+item+'))\n')
    iteration = 2
    while iteration <= n_node:
        binary_tree_list = utils.generate_all_binary(iteration)
        possible_permutation = []
        for total_acti, total_repre in utils.generate_all_divisions(iteration,2):
            if n_acti == 0 and total_acti != 0:
                continue
            if n_repre == 0 and total_repre != 0:
                continue
            for acti_div, repre_div in itertools.product(utils.generate_all_divisions(total_acti, n_acti),utils.generate_all_divisions(total_repre,n_repre)):
                factor_dict = {}
                for acti_index in range(len(acti_div)):
                    factor_dict['A'+str(acti_index+1)] = acti_div[acti_index]
                for repre_index in range(len(repre_div)):
                    factor_dict['R'+str(repre_index+1)] = repre_div[repre_index]
                possible_permutation += utils.make_permutation_list(factor_dict)
        numpy.random.shuffle(possible_permutation)
        for perm in possible_permutation:
            num_tree = int(numpy.random.random()*len(binary_tree_list)*portion)
            numpy.random.shuffle(binary_tree_list)
            for binary_tree in binary_tree_list[:num_tree]:
                permutation_convert = [factor[:-1] for factor in perm]
                factor_count_dict = {'A':permutation_convert.count('A'), 'R':permutation_convert.count('R')}                        
                if factor_count_dict['A'] > factor_count_dict['R']:
                    original_output = 1 
                else:
                    original_output = -1
                if original_output == 1:
                    if output_count[0]<min(output_count)+10 or output_count[0]<min(output_count)*1.2:
                        output_count[0]+= 1
                        output = 1 
                        utils.random_write(f_train,f_test,binary_tree,perm,output,noise_level)
                elif original_output == -1:
                    if output_count[1]<min(output_count)+10 or output_count[1]<min(output_count)*1.2:
                        output_count[1]+= 1
                        output = -1 
                        utils.random_write(f_train,f_test,binary_tree,perm,output,noise_level)
                        
        iteration+=1

def complexity_2_case(n_node, n_acti, n_repre, n_dummy, f_train, f_test, portion = 1, noise_level = 0):
# random sampling from list of trees generated up to the tree with n_node(>=2) nodes
    numpy.random.seed()
    output = 0
    output_count = [0,0]
    zero_count = 0
    
    factor_dict = {'A':n_acti, 'R':n_repre, 'D':n_dummy}
    factor_list = []
    for factor in factor_dict:
        for i in range(1,factor_dict[factor]+1):
            factor_list.append(factor+str(i))
            
    for item in factor_list:
        if item[0] == 'A':
            original_output = 1 
        elif item[0] == 'R':
            original_output = -1
        elif item[0] == 'D':
            original_output = 0
        prob = numpy.random.random()
        if prob<.5 and prob>.25:
            if original_output == 1:
                if output_count[0]<min(output_count)+10 or output_count[0]<min(output_count)*1.2:
                    output_count[0]+= 1
                    output = 1 if numpy.random.random()>=noise_level else numpy.random.choice([0,-1],1)[0]        
                    f_train.write('('+str(output)+' (0 0) (1 '+item+'))\n')
            elif original_output == -1:
                if output_count[1]<min(output_count)+10 or output_count[1]<min(output_count)*1.2:
                    output_count[1]+= 1
                    output = -1 if numpy.random.random()>=noise_level else numpy.random.choice([1,0],1)[0]
                    f_train.write('('+str(output)+' (0 0) (1 '+item+'))\n')
            elif original_output == 0:
                if zero_count<min(output_count)+10 or zero_count<min(output_count)*1.2:
                    zero_count+= 1
                    output = 0 if numpy.random.random()>=noise_level else numpy.random.choice([1,-1],1)[0]
                    f_train.write('('+str(output)+' (0 0) (1 '+item+'))\n')
        elif prob<.25:
            if original_output == 1:
                if output_count[0]<min(output_count)+10 or output_count[0]<min(output_count)*1.2:
                    output_count[0]+= 1
                    output = 1 
                    f_test.write('('+str(output)+' (0 0) (1 '+item+'))\n')
            elif original_output == -1:
                if output_count[1]<min(output_count)+10 or output_count[1]<min(output_count)*1.2:
                    output_count[1]+= 1
                    output = -1
                    f_test.write('('+str(output)+' (0 0) (1 '+item+'))\n')
            elif original_output == 0:
                if zero_count<min(output_count)+10 or zero_count<min(output_count)*1.2:
                    zero_count+= 1
                    output = 0
                    f_test.write('('+str(output)+' (0 0) (1 '+item+'))\n')
    iteration = 2
    while iteration <= n_node:
        binary_tree_list = utils.generate_all_binary(iteration)
        possible_permutation = []
        for total_acti, total_repre, total_dummy in utils.generate_all_divisions(iteration,3):
            if n_acti == 0 and total_acti != 0:
                continue
            if n_repre == 0 and total_repre != 0:
                continue
            if n_dummy == 0 and total_dummy != 0:
                continue
            for acti_div, repre_div, dummy_div in itertools.product(utils.generate_all_divisions(total_acti, n_acti),utils.generate_all_divisions(total_repre,n_repre),utils.generate_all_divisions(total_dummy,n_dummy)):
                factor_dict = {}
                for acti_index in range(len(acti_div)):
                    factor_dict['A'+str(acti_index+1)] = acti_div[acti_index]
                for repre_index in range(len(repre_div)):
                    factor_dict['R'+str(repre_index+1)] = repre_div[repre_index]
                for dummy_index in range(len(dummy_div)):
                    factor_dict['D'+str(dummy_index+1)] = dummy_div[dummy_index]
                possible_permutation += utils.make_permutation_list(factor_dict)
        numpy.random.shuffle(possible_permutation)
        for perm in possible_permutation:
            num_tree = int(numpy.random.random()*len(binary_tree_list)*portion)
            numpy.random.shuffle(binary_tree_list)
            for binary_tree in binary_tree_list[:num_tree]:
                permutation_convert = [factor[:-1] for factor in perm]
                factor_count_dict = {'A':permutation_convert.count('A'), 'R':permutation_convert.count('R'), 'D':permutation_convert.count('D')}                        
                if factor_count_dict['A'] == 0 and  factor_count_dict['R']==0:
                    original_output = 0
                elif factor_count_dict['A'] > factor_count_dict['R']:
                    original_output = 1 
                else:
                    original_output = -1
                if original_output == 1:
                    if output_count[0]<min(output_count)+10 or output_count[0]<min(output_count)*1.2:
                        output_count[0]+= 1
                        output = 1 
                        utils.random_write(f_train,f_test,binary_tree,perm,output,noise_level)
                elif original_output == -1:
                    if output_count[1]<min(output_count)+10 or output_count[1]<min(output_count)*1.2:
                        output_count[1]+= 1
                        output = -1
                        utils.random_write(f_train,f_test,binary_tree,perm,output,noise_level)
                elif original_output == 0:
                    if zero_count<min(output_count)+10 or zero_count<min(output_count)*1.2:
                        zero_count+= 1
                        output = 0
                        utils.random_write(f_train,f_test,binary_tree,perm,output,noise_level)
                        
        iteration+=1
        
def complexity_3_case(n_node, n_acti, n_repre, n_dummy, n_superacti, n_superrepre, f_train, f_test, portion = 1, noise_level = 0):
# random sampling from list of trees generated up to the tree with n_node(>=2) nodes
    numpy.random.seed()
    output = 0
    output_count = [0,0]
    zero_count = 0
    
    factor_dict = {'A':n_acti, 'R':n_repre, 'D':n_dummy, 'SA':n_superacti, 'SR':n_superrepre}
    factor_list = []
    for factor in factor_dict:
        for i in range(1,factor_dict[factor]+1):
            factor_list.append(factor+str(i))
            
    for item in factor_list:
        if item[0] == 'A' or item[0:2]=='SA':
            original_output = 1 
        elif item[0] == 'R' or item[0:2] == 'SR':
            original_output = -1
        elif item[0] == 'D':
            original_output = 0
        prob = numpy.random.random()
        if prob<.5 and prob>.25:
            if original_output == 1:
                if output_count[0]<min(output_count)+10 or output_count[0]<min(output_count)*1.2:
                    output_count[0]+= 1
                    output = 1 if numpy.random.random()>=noise_level else numpy.random.choice([0,-1],1)[0]        
                    f_train.write('('+str(output)+' (0 0) (1 '+item+'))\n')
            elif original_output == -1:
                if output_count[1]<min(output_count)+10 or output_count[1]<min(output_count)*1.2:
                    output_count[1]+= 1
                    output = -1 if numpy.random.random()>=noise_level else numpy.random.choice([1,0],1)[0]
                    f_train.write('('+str(output)+' (0 0) (1 '+item+'))\n')
            elif original_output == 0:
                if zero_count<min(output_count)+10 or zero_count<min(output_count)*1.2:
                    zero_count+= 1
                    output = 0 if numpy.random.random()>=noise_level else numpy.random.choice([1,-1],1)[0]
                    f_train.write('('+str(output)+' (0 0) (1 '+item+'))\n')
        elif prob<.25:
            if original_output == 1:
                if output_count[0]<min(output_count)+10 or output_count[0]<min(output_count)*1.2:
                    output_count[0]+= 1
                    output = 1 
                    f_test.write('('+str(output)+' (0 0) (1 '+item+'))\n')
            elif original_output == -1:
                if output_count[1]<min(output_count)+10 or output_count[1]<min(output_count)*1.2:
                    output_count[1]+= 1
                    output = -1 
                    f_test.write('('+str(output)+' (0 0) (1 '+item+'))\n')
            elif original_output == 0:
                if zero_count<min(output_count)+10 or zero_count<min(output_count)*1.2:
                    zero_count+= 1
                    output = 0 
                    f_test.write('('+str(output)+' (0 0) (1 '+item+'))\n')
    
    iteration = 2
    while iteration <= n_node:
        binary_tree_list = utils.generate_all_binary(iteration)
        possible_permutation = []
        for total_acti, total_repre, total_dummy, total_superacti, total_superrepre in utils.generate_all_divisions(iteration,5):
            if n_acti == 0 and total_acti != 0:
                continue
            if n_repre == 0 and total_repre != 0:
                continue
            if n_dummy == 0 and total_dummy != 0:
                continue            
            if n_superacti == 0 and total_superacti != 0:
                continue
            if n_superrepre == 0 and total_superrepre != 0:
                continue   
            for acti_div, repre_div, dummy_div, superacti_div, superrepre_div in itertools.product(utils.generate_all_divisions(total_acti, n_acti),utils.generate_all_divisions(total_repre,n_repre),utils.generate_all_divisions(total_dummy,n_dummy),utils.generate_all_divisions(total_superacti,n_superacti),utils.generate_all_divisions(total_superrepre,n_superrepre)):
                factor_dict = {}
                for acti_index in range(len(acti_div)):
                    factor_dict['A'+str(acti_index+1)] = acti_div[acti_index]
                for repre_index in range(len(repre_div)):
                    factor_dict['R'+str(repre_index+1)] = repre_div[repre_index]
                for dummy_index in range(len(dummy_div)):
                    factor_dict['D'+str(dummy_index+1)] = dummy_div[dummy_index]
                for superacti_index in range(len(superacti_div)):
                    factor_dict['SA'+str(superacti_index+1)] = superacti_div[superacti_index]
                for superrepre_index in range(len(superrepre_div)):
                    factor_dict['SR'+str(superrepre_index+1)] = superrepre_div[superrepre_index]
                possible_permutation += utils.make_permutation_list(factor_dict)
        numpy.random.shuffle(possible_permutation)
        for perm in possible_permutation:
            num_tree = int(numpy.random.random()*len(binary_tree_list)*portion)
            numpy.random.shuffle(binary_tree_list)
            for binary_tree in binary_tree_list[:num_tree]:
                permutation_convert = [factor[:-1] for factor in perm]
                factor_count_dict = {'A':permutation_convert.count('A'), 'R':permutation_convert.count('R'), 'D':permutation_convert.count('D'), 'SA':permutation_convert.count('SA'), 'SR':permutation_convert.count('SR')}                        
                if factor_count_dict['A'] == 0 and factor_count_dict['R'] == 0 and factor_count_dict['SA'] == 0 and factor_count_dict['SR'] == 0: 
                    original_output = 0 
                elif factor_count_dict['SA'] ==0 and factor_count_dict['SR']==0 and factor_count_dict['A'] > factor_count_dict['R']:
                    original_output = 1
                elif factor_count_dict['SA'] ==0 and factor_count_dict['SR']==0:
                    original_output = -1
                elif factor_count_dict['SA']>factor_count_dict['SR']:
                    original_output = 1
                else:
                    original_output = -1
                if original_output == 1:
                    if output_count[0]<min(output_count)+10 or output_count[0]<min(output_count)*1.2:
                        output_count[0]+= 1
                        output = 1 
                        utils.random_write(f_train,f_test,binary_tree,perm,output,noise_level)
                elif original_output == -1:
                    if output_count[1]<min(output_count)+10 or output_count[1]<min(output_count)*1.2:
                        output_count[1]+= 1
                        output = -1
                        utils.random_write(f_train,f_test,binary_tree,perm,output,noise_level)
                elif original_output == 0:
                    if zero_count<min(output_count)+10 or zero_count<min(output_count)*1.2:
                        zero_count+= 1
                        output = 0 
                        utils.random_write(f_train,f_test,binary_tree,perm,output,noise_level)
                        
        iteration+=1
        

def complexity_4_case(n_node, n_acti, n_repre, n_dummy, n_superacti, n_superrepre, n_enh, n_silen, f_train, f_test, portion = 1, noise_level = 0):
# random sampling from list of trees generated up to the tree with n_node(>=2) nodes
# works for only n<10
    numpy.random.seed()
    output = 0
    output_count = [0,0]
    zero_count = 0
    
    factor_dict = {'A':n_acti, 'R':n_repre, 'D':n_dummy, 'SA':n_superacti, 'SR':n_superrepre, 'E':n_enh, 'S':n_silen}
    factor_list = []
    for factor in factor_dict:
        for i in range(1,factor_dict[factor]+1):
            factor_list.append(factor+str(i))
            
    for item in factor_list:
        if item[0] == 'A' or item[0:2]=='SA':
            original_output = 1 
        elif item[0] == 'R' or item[0:2] == 'SR':
            original_output = -1
        elif item[0] == 'D' or item[0] == 'E' or item[0] == 'S':
            original_output = 0
        prob = numpy.random.random()
        if prob<.5 and prob>.25:
            if original_output == 1:
                if output_count[0]<min(output_count)+10 or output_count[0]<min(output_count)*1.2:
                    output_count[0]+= 1
                    output = 1 if numpy.random.random()>=noise_level else numpy.random.choice([0,-1],1)[0]        
                    f_train.write('('+str(output)+' (0 0) (1 '+item+'))\n')
            elif original_output == -1:
                if output_count[1]<min(output_count)+10 or output_count[1]<min(output_count)*1.2:
                    output_count[1]+= 1
                    output = -1 if numpy.random.random()>=noise_level else numpy.random.choice([1,0],1)[0]
                    f_train.write('('+str(output)+' (0 0) (1 '+item+'))\n')
            elif original_output == 0:
                if zero_count<min(output_count)+10 or zero_count<min(output_count)*1.2:
                    zero_count+= 1
                    output = 0 if numpy.random.random()>=noise_level else numpy.random.choice([1,-1],1)[0]
                    f_train.write('('+str(output)+' (0 0) (1 '+item+'))\n')
        elif prob<.25:
            if original_output == 1:
                if output_count[0]<min(output_count)+10 or output_count[0]<min(output_count)*1.2:
                    output_count[0]+= 1
                    output = 1
                    f_test.write('('+str(output)+' (0 0) (1 '+item+'))\n')
            elif original_output == -1:
                if output_count[1]<min(output_count)+10 or output_count[1]<min(output_count)*1.2:
                    output_count[1]+= 1
                    output = -1
                    f_test.write('('+str(output)+' (0 0) (1 '+item+'))\n')
            elif original_output == 0:
                if zero_count<min(output_count)+10 or zero_count<min(output_count)*1.2:
                    zero_count+= 1
                    output = 0
                    f_test.write('('+str(output)+' (0 0) (1 '+item+'))\n')
    
    

    iteration = 2
    while iteration <= n_node:
        binary_tree_list = utils.generate_all_binary_with_closest(iteration)
        possible_permutation = []
        for total_acti, total_repre, total_dummy, total_superacti, total_superrepre, total_enh, total_silen in utils.generate_all_divisions(iteration,7):
            if n_acti == 0 and total_acti != 0:
                continue
            if n_repre == 0 and total_repre != 0:
                continue
            if n_dummy == 0 and total_dummy != 0:
                continue            
            if n_superacti == 0 and total_superacti != 0:
                continue
            if n_superrepre == 0 and total_superrepre != 0:
                continue
            if n_enh == 0 and total_enh != 0:
                continue
            if n_silen == 0 and total_silen != 0:
                continue 
            for acti_div, repre_div, dummy_div, superacti_div, superrepre_div, enh_div, silen_div in itertools.product(utils.generate_all_divisions(total_acti, n_acti),utils.generate_all_divisions(total_repre,n_repre),utils.generate_all_divisions(total_dummy,n_dummy),utils.generate_all_divisions(total_superacti,n_superacti),utils.generate_all_divisions(total_superrepre,n_superrepre),utils.generate_all_divisions(total_enh,n_enh),utils.generate_all_divisions(total_silen,n_silen)):
                factor_dict = {}
                for acti_index in range(len(acti_div)):
                    factor_dict['A'+str(acti_index+1)] = acti_div[acti_index]
                for repre_index in range(len(repre_div)):
                    factor_dict['R'+str(repre_index+1)] = repre_div[repre_index]
                for dummy_index in range(len(dummy_div)):
                    factor_dict['D'+str(dummy_index+1)] = dummy_div[dummy_index]
                for superacti_index in range(len(superacti_div)):
                    factor_dict['SA'+str(superacti_index+1)] = superacti_div[superacti_index]
                for superrepre_index in range(len(superrepre_div)):
                    factor_dict['SR'+str(superrepre_index+1)] = superrepre_div[superrepre_index]
                for enh_index in range(len(enh_div)):
                    factor_dict['E'+str(enh_index+1)] = enh_div[enh_index]
                for silen_index in range(len(silen_div)):
                    factor_dict['S'+str(silen_index+1)] = silen_div[silen_index]
                possible_permutation += utils.make_permutation_list(factor_dict)
        numpy.random.shuffle(possible_permutation)
        for perm in possible_permutation:
            num_tree = int(numpy.random.random()*len(binary_tree_list)*portion)
            numpy.random.shuffle(binary_tree_list)
            for binary_tree in binary_tree_list[:num_tree]:
                closest_element = binary_tree[1]
                permutation_convert = [factor[:-1] for factor in perm]
                factor_count_dict = {'A':permutation_convert.count('A'), 'R':permutation_convert.count('R'), 'D':permutation_convert.count('D'), 'SA':permutation_convert.count('SA'), 'SR':permutation_convert.count('SR'), 'E':permutation_convert.count('E'), 'S': permutation_convert.count('S')}
                for factor_index in range(len(permutation_convert)):
                    if permutation_convert[factor_index] == 'E':
                        closest = permutation_convert[closest_element[factor_index]]
                        if closest == 'A' or closest == 'R':
                            factor_count_dict[closest]+=1
                for factor_index in range(len(permutation_convert)):
                    if permutation_convert[factor_index] == 'S':
                        closest = permutation_convert[closest_element[factor_index]]
                        if closest == 'A' or closest == 'R':
                            factor_count_dict[closest] = max(0,factor_count_dict[closest]-1) # to_prevent the number reach 0 first and inappropriately increase by enhancer
                if factor_count_dict['A'] == 0 and factor_count_dict['R'] == 0 and factor_count_dict['SA'] == 0 and factor_count_dict['SR'] == 0: 
                    original_output = 0 
                elif factor_count_dict['SA'] ==0 and factor_count_dict['SR']==0 and factor_count_dict['A'] > factor_count_dict['R']:
                    original_output = 1
                elif factor_count_dict['SA'] ==0 and factor_count_dict['SR']==0:
                    original_output = -1
                elif factor_count_dict['SA']>factor_count_dict['SR']:
                    original_output = 1 
                else:
                    original_output = -1 
                if original_output == 1:
                    if output_count[0]<min(output_count)+10 or output_count[0]<min(output_count)*1.2:
                        output_count[0]+= 1
                        output = 1
                        utils.random_write(f_train,f_test,binary_tree[0],perm,output,noise_level)
                elif original_output == -1:
                    if output_count[1]<min(output_count)+10 or output_count[1]<min(output_count)*1.2:
                        output_count[1]+= 1
                        output = -1 
                        utils.random_write(f_train,f_test,binary_tree[0],perm,output,noise_level)
                elif original_output == 0:
                    if zero_count<min(output_count)+10 or zero_count<min(output_count)*1.2:
                        zero_count+= 1
                        output = 0 
                        utils.random_write(f_train,f_test,binary_tree[0],perm,output,noise_level)
        iteration+=1
        
def complexity_5_case(n_node, n_acti, n_repre, n_dummy, n_superacti, n_superrepre, n_enh, n_silen, n_superenh, n_supersilen, f_train, f_test, portion = 1, noise_level = 0):
# random sampling from list of trees generated up to the tree with n_node(>=2) nodes
# works for only n<10
    numpy.random.seed()
    output = 0
    output_count = [0,0]
    zero_count = 0
    
    factor_dict = {'A':n_acti, 'R':n_repre, 'D':n_dummy, 'SA':n_superacti, 'SR':n_superrepre, 'E':n_enh, 'S':n_silen, 'SE':n_superenh,'SS':n_supersilen}
    factor_list = []
    for factor in factor_dict:
        for i in range(1,factor_dict[factor]+1):
            factor_list.append(factor+str(i))
            
    for item in factor_list:
        if item[0] == 'A' or item[0:2]=='SA':
            original_output = 1 
        elif item[0] == 'R' or item[0:2] == 'SR':
            original_output = -1 
        else:
            original_output = 0
        prob = numpy.random.random()
        if prob<.5 and prob>.25:
            if original_output == 1:
                if output_count[0]<min(output_count)+10 or output_count[0]<min(output_count)*1.2:
                    output_count[0]+= 1
                    output = 1 if numpy.random.random()>=noise_level else numpy.random.choice([0,-1],1)[0]        
                    f_train.write('('+str(output)+' (0 0) (1 '+item+'))\n')
            elif original_output == -1:
                if output_count[1]<min(output_count)+10 or output_count[1]<min(output_count)*1.2:
                    output_count[1]+= 1
                    output = -1 if numpy.random.random()>=noise_level else numpy.random.choice([1,0],1)[0]
                    f_train.write('('+str(output)+' (0 0) (1 '+item+'))\n')
            elif original_output == 0:
                if zero_count<min(output_count)+10 or zero_count<min(output_count)*1.2:
                    zero_count+= 1
                    output = 0 if numpy.random.random()>=noise_level else numpy.random.choice([1,-1],1)[0]
                    f_train.write('('+str(output)+' (0 0) (1 '+item+'))\n')
        elif prob<.25:
            if original_output == 1:
                if output_count[0]<min(output_count)+10 or output_count[0]<min(output_count)*1.2:
                    output_count[0]+= 1
                    output = 1 
                    f_test.write('('+str(output)+' (0 0) (1 '+item+'))\n')
            elif original_output == -1:
                if output_count[1]<min(output_count)+10 or output_count[1]<min(output_count)*1.2:
                    output_count[1]+= 1
                    output = -1
                    f_test.write('('+str(output)+' (0 0) (1 '+item+'))\n')
            elif original_output == 0:
                if zero_count<min(output_count)+10 or zero_count<min(output_count)*1.2:
                    zero_count+= 1
                    output = 0
                    f_test.write('('+str(output)+' (0 0) (1 '+item+'))\n')
    
    iteration = 2
    while iteration <= n_node:
        binary_tree_list = utils.generate_all_binary_with_closest(iteration)
        possible_permutation = []
        for total_acti, total_repre, total_dummy, total_superacti, total_superrepre, total_enh, total_silen, total_superenh, total_supersilen in utils.generate_all_divisions(iteration,9):
            if n_acti == 0 and total_acti != 0:
                continue
            if n_repre == 0 and total_repre != 0:
                continue
            if n_dummy == 0 and total_dummy != 0:
                continue            
            if n_superacti == 0 and total_superacti != 0:
                continue
            if n_superrepre == 0 and total_superrepre != 0:
                continue
            if n_enh == 0 and total_enh != 0:
                continue
            if n_silen == 0 and total_silen != 0:
                continue 
            if n_superenh == 0 and total_superenh !=0:
                continue
            if n_supersilen == 0 and total_supersilen !=0:
                continue
            for acti_div, repre_div, dummy_div, superacti_div, superrepre_div, enh_div, silen_div, superenh_div, supersilen_div in itertools.product(utils.generate_all_divisions(total_acti, n_acti),utils.generate_all_divisions(total_repre,n_repre),utils.generate_all_divisions(total_dummy,n_dummy),utils.generate_all_divisions(total_superacti,n_superacti),utils.generate_all_divisions(total_superrepre,n_superrepre),utils.generate_all_divisions(total_enh,n_enh),utils.generate_all_divisions(total_silen,n_silen),utils.generate_all_divisions(total_superenh,n_superenh),utils.generate_all_divisions(total_supersilen,n_supersilen)):
                factor_dict = {}
                for acti_index in range(len(acti_div)):
                    factor_dict['A'+str(acti_index+1)] = acti_div[acti_index]
                for repre_index in range(len(repre_div)):
                    factor_dict['R'+str(repre_index+1)] = repre_div[repre_index]
                for dummy_index in range(len(dummy_div)):
                    factor_dict['D'+str(dummy_index+1)] = dummy_div[dummy_index]
                for superacti_index in range(len(superacti_div)):
                    factor_dict['SA'+str(superacti_index+1)] = superacti_div[superacti_index]
                for superrepre_index in range(len(superrepre_div)):
                    factor_dict['SR'+str(superrepre_index+1)] = superrepre_div[superrepre_index]
                for enh_index in range(len(enh_div)):
                    factor_dict['E'+str(enh_index+1)] = enh_div[enh_index]
                for silen_index in range(len(silen_div)):
                    factor_dict['S'+str(silen_index+1)] = silen_div[silen_index]
                for superenh_index in range(len(superenh_div)):
                    factor_dict['SE'+str(superenh_index+1)] = superenh_div[superenh_index]
                for supersilen_index in range(len(supersilen_div)):
                    factor_dict['SS'+str(supersilen_index+1)] = supersilen_div[supersilen_index]
                possible_permutation += utils.make_permutation_list(factor_dict)
        numpy.random.shuffle(possible_permutation)
        for perm in possible_permutation:
            num_tree = int(numpy.random.random()*len(binary_tree_list)*portion)
            numpy.random.shuffle(binary_tree_list)
            for binary_tree in binary_tree_list[:num_tree]:
                closest_element = binary_tree[1]
                permutation_convert = [factor[:-1] for factor in perm]
                factor_count_dict = {'A':permutation_convert.count('A'), 'R':permutation_convert.count('R'), 'D':permutation_convert.count('D'), 'SA':permutation_convert.count('SA'), 'SR':permutation_convert.count('SR'), 'E':permutation_convert.count('E'), 'S': permutation_convert.count('S'), 'SE': permutation_convert.count('SE'), 'SS': permutation_convert.count('SS')}
                for factor_index in range(len(permutation_convert)):
                    if permutation_convert[factor_index] == 'E':
                        closest = permutation_convert[closest_element[factor_index]]
                        if closest == 'A' or closest == 'R':
                            factor_count_dict[closest]+=1
                    if permutation_convert[factor_index] == 'SE':
                        closest = permutation_convert[closest_element[factor_index]]
                        if closest == 'A' or closest == 'R':
                            factor_count_dict[closest]-=1
                            factor_count_dict['S'+closest]+=1
                for factor_index in range(len(permutation_convert)):
                    if permutation_convert[factor_index] == 'S':
                        closest = permutation_convert[closest_element[factor_index]]
                        if closest == 'A' or closest == 'R':
                            factor_count_dict[closest] -= 1
                    factor_count_dict['A'] = max(0,factor_count_dict['A'])
                    factor_count_dict['R'] = max(0,factor_count_dict['R']) # to_prevent the number reach 0 first and inappropriately increase by enhancer
                if factor_count_dict['SS'] >0:
                    original_output = 0 
                elif factor_count_dict['A'] == 0 and factor_count_dict['R'] == 0 and factor_count_dict['SA'] == 0 and factor_count_dict['SR'] == 0: 
                    original_output = 0
                elif factor_count_dict['SA'] ==0 and factor_count_dict['SR']==0 and factor_count_dict['A'] > factor_count_dict['R']:
                    original_output = 1
                elif factor_count_dict['SA'] ==0 and factor_count_dict['SR']==0:
                    original_output = -1
                elif factor_count_dict['SA']>factor_count_dict['SR']:
                    original_output = 1
                else:
                    original_output = -1
                if original_output == 1:
                    if output_count[0]<min(output_count)+10 or output_count[0]<min(output_count)*1.2:
                        output_count[0]+= 1
                        output = 1 
                        utils.random_write(f_train,f_test,binary_tree[0],perm,output,noise_level)
                elif original_output == -1:
                    if output_count[1]<min(output_count)+10 or output_count[1]<min(output_count)*1.2:
                        output_count[1]+= 1
                        output = -1
                        utils.random_write(f_train,f_test,binary_tree[0],perm,output,noise_level)
                elif original_output == 0:
                    if zero_count<min(output_count)+10 or zero_count<min(output_count)*1.2:
                        zero_count+= 1
                        output = 0 
                        utils.random_write(f_train,f_test,binary_tree[0],perm,output,noise_level)
        iteration+=1
        
def complexity_6_case(n_node, n_acti, n_repre, n_dummy, n_superacti, n_superrepre, n_enh, n_silen, n_superenh, n_supersilen, n_insul, f_train, f_test, portion = 1, noise_level = 0):
# random sampling from list of trees generated up to the tree with n_node(>=2) nodes
# works for only n<10
    numpy.random.seed()
    output = 0
    output_count = [0,0]
    zero_count = 0
    
    factor_dict = {'A':n_acti, 'R':n_repre, 'D':n_dummy, 'SA':n_superacti, 'SR':n_superrepre, 'E':n_enh, 'S':n_silen, 'SE':n_superenh, 'SS':n_supersilen,'I':n_insul}
    factor_list = []
    for factor in factor_dict:
        for i in range(1,factor_dict[factor]+1):
            factor_list.append(factor+str(i))
            
    for item in factor_list:
        if item[0] == 'A' or item[0:2]=='SA':
            original_output = 1 
        elif item[0] == 'R' or item[0:2] == 'SR':
            original_output = -1
        else:
            original_output = 0
        prob = numpy.random.random()
        if prob<.5 and prob>.25:
            if original_output == 1:
                if output_count[0]<min(output_count)+10 or output_count[0]<min(output_count)*1.2:
                    output_count[0]+= 1
                    output = 1 if numpy.random.random()>=noise_level else numpy.random.choice([0,-1],1)[0]        
                    f_train.write('('+str(output)+' (0 0) (1 '+item+'))\n')
            elif original_output == -1:
                if output_count[1]<min(output_count)+10 or output_count[1]<min(output_count)*1.2:
                    output_count[1]+= 1
                    output = -1 if numpy.random.random()>=noise_level else numpy.random.choice([1,0],1)[0]
                    f_train.write('('+str(output)+' (0 0) (1 '+item+'))\n')
            elif original_output == 0:
                if zero_count<min(output_count)+10 or zero_count<min(output_count)*1.2:
                    zero_count+= 1
                    output = 0 if numpy.random.random()>=noise_level else numpy.random.choice([1,-1],1)[0]
                    f_train.write('('+str(output)+' (0 0) (1 '+item+'))\n')
        elif prob<.25:
            if original_output == 1:
                if output_count[0]<min(output_count)+10 or output_count[0]<min(output_count)*1.2:
                    output_count[0]+= 1
                    output = 1
                    f_test.write('('+str(output)+' (0 0) (1 '+item+'))\n')
            elif original_output == -1:
                if output_count[1]<min(output_count)+10 or output_count[1]<min(output_count)*1.2:
                    output_count[1]+= 1
                    output = -1 
                    f_test.write('('+str(output)+' (0 0) (1 '+item+'))\n')
            elif original_output == 0:
                if zero_count<min(output_count)+10 or zero_count<min(output_count)*1.2:
                    zero_count+= 1
                    output = 0 
                    f_test.write('('+str(output)+' (0 0) (1 '+item+'))\n')
    
    iteration = 2
    while iteration <= n_node:
        binary_tree_list = utils.generate_all_binary_with_closest(iteration)
        possible_permutation = []
        for total_acti, total_repre, total_dummy, total_superacti, total_superrepre, total_enh, total_silen, total_superenh, total_supersilen, total_insul in utils.generate_all_divisions(iteration,10):
            if n_acti == 0 and total_acti != 0:
                continue
            if n_repre == 0 and total_repre != 0:
                continue
            if n_dummy == 0 and total_dummy != 0:
                continue            
            if n_superacti == 0 and total_superacti != 0:
                continue
            if n_superrepre == 0 and total_superrepre != 0:
                continue
            if n_enh == 0 and total_enh != 0:
                continue
            if n_silen == 0 and total_silen != 0:
                continue 
            if n_superenh == 0 and total_superenh !=0:
                continue
            if n_supersilen == 0 and total_supersilen !=0:
                continue
            if n_insul == 0 and total_insul !=0:
                continue
            for acti_div, repre_div, dummy_div, superacti_div, superrepre_div, enh_div, silen_div, superenh_div, supersilen_div, insul_div in itertools.product(utils.generate_all_divisions(total_acti, n_acti),utils.generate_all_divisions(total_repre,n_repre),utils.generate_all_divisions(total_dummy,n_dummy),utils.generate_all_divisions(total_superacti,n_superacti),utils.generate_all_divisions(total_superrepre,n_superrepre),utils.generate_all_divisions(total_enh,n_enh),utils.generate_all_divisions(total_silen,n_silen),utils.generate_all_divisions(total_superenh,n_superenh),utils.generate_all_divisions(total_supersilen,n_supersilen),utils.generate_all_divisions(total_insul,n_insul)):
                factor_dict = {}
                for acti_index in range(len(acti_div)):
                    factor_dict['A'+str(acti_index+1)] = acti_div[acti_index]
                for repre_index in range(len(repre_div)):
                    factor_dict['R'+str(repre_index+1)] = repre_div[repre_index]
                for dummy_index in range(len(dummy_div)):
                    factor_dict['D'+str(dummy_index+1)] = dummy_div[dummy_index]
                for superacti_index in range(len(superacti_div)):
                    factor_dict['SA'+str(superacti_index+1)] = superacti_div[superacti_index]
                for superrepre_index in range(len(superrepre_div)):
                    factor_dict['SR'+str(superrepre_index+1)] = superrepre_div[superrepre_index]
                for enh_index in range(len(enh_div)):
                    factor_dict['E'+str(enh_index+1)] = enh_div[enh_index]
                for silen_index in range(len(silen_div)):
                    factor_dict['S'+str(silen_index+1)] = silen_div[silen_index]
                for superenh_index in range(len(superenh_div)):
                    factor_dict['SE'+str(superenh_index+1)] = superenh_div[superenh_index]
                for supersilen_index in range(len(supersilen_div)):
                    factor_dict['SS'+str(supersilen_index+1)] = supersilen_div[supersilen_index]
                for insul_index in range(len(insul_div)):
                    factor_dict['I'+str(insul_index+1)] = insul_div[insul_index]
                possible_permutation += utils.make_permutation_list(factor_dict)
        numpy.random.shuffle(possible_permutation)
        for perm in possible_permutation:
            num_tree = int(numpy.random.random()*len(binary_tree_list)*portion)
            numpy.random.shuffle(binary_tree_list)
            for binary_tree in binary_tree_list[:num_tree]:
                closest_element = binary_tree[1]
                permutation_convert = [factor[:-1] for factor in perm]
                if 'I' in permutation_convert:
                    permutation_convert = permutation_convert[:permutation_convert.index('I')+1]
                    factor_count_dict = {'A':permutation_convert.count('A'), 'R':permutation_convert.count('R'), 'D':permutation_convert.count('D'), 'SA':permutation_convert.count('SA'), 'SR':permutation_convert.count('SR'), 'E':permutation_convert.count('E'), 'S': permutation_convert.count('S'), 'SE': permutation_convert.count('SE'),'SS': permutation_convert.count('SS'),'I': permutation_convert.count('I')}
                else:
                    factor_count_dict = {'A':permutation_convert.count('A'), 'R':permutation_convert.count('R'), 'D':permutation_convert.count('D'), 'SA':permutation_convert.count('SA'), 'SR':permutation_convert.count('SR'), 'E':permutation_convert.count('E'), 'S': permutation_convert.count('S'), 'SE': permutation_convert.count('SE'),'SS': permutation_convert.count('SS'),'I': permutation_convert.count('I')}
                for factor_index in range(len(permutation_convert)):
                    if permutation_convert[factor_index] == 'E':
                        closest = permutation_convert[closest_element[factor_index]]
                        if closest == 'A' or closest == 'R':
                            factor_count_dict[closest]+=1
                    if permutation_convert[factor_index] == 'SE':
                        closest = permutation_convert[closest_element[factor_index]]
                        if closest == 'A' or closest == 'R':
                            factor_count_dict[closest]-=1
                            factor_count_dict['S'+closest]+=1
                for factor_index in range(len(permutation_convert)):
                    if permutation_convert[factor_index] == 'S':
                        closest = permutation_convert[closest_element[factor_index]]
                        if closest == 'A' or closest == 'R':
                            factor_count_dict[closest] -= 1
                    factor_count_dict['A'] = max(0,factor_count_dict['A'])
                    factor_count_dict['R'] = max(0,factor_count_dict['R']) # to_prevent the number reach 0 first and inappropriately increase by enhancer
                if factor_count_dict['SS'] >0:
                    original_output = 0
                elif factor_count_dict['A'] == 0 and factor_count_dict['R'] == 0 and factor_count_dict['SA'] == 0 and factor_count_dict['SR'] == 0: 
                    original_output = 0
                elif factor_count_dict['SA'] ==0 and factor_count_dict['SR']==0 and factor_count_dict['A'] > factor_count_dict['R']:
                    original_output = 1
                elif factor_count_dict['SA'] ==0 and factor_count_dict['SR']==0:
                    original_output = -1
                elif factor_count_dict['SA']>factor_count_dict['SR']:
                    original_output = 1
                else:
                    original_output = -1
                if original_output == 1:
                    if output_count[0]<min(output_count)+10 or output_count[0]<min(output_count)*1.2:
                        output_count[0]+= 1
                        output = 1
                        utils.random_write(f_train,f_test,binary_tree[0],perm,output,noise_level)
                elif original_output == -1:
                    if output_count[1]<min(output_count)+10 or output_count[1]<min(output_count)*1.2:
                        output_count[1]+= 1
                        output = -1 
                        utils.random_write(f_train,f_test,binary_tree[0],perm,output,noise_level)
                elif original_output == 0:
                    if zero_count<min(output_count)+10 or zero_count<min(output_count)*1.2:
                        zero_count+= 1
                        output = 0 
                        utils.random_write(f_train,f_test,binary_tree[0],perm,output,noise_level)
        iteration+=1

def complexity_7_case(n_node, n_acti, n_repre, n_dummy, n_superacti, n_superrepre, n_enh, n_silen, n_superenh, n_supersilen, n_insul, n_anti_insul, f_train, f_test, portion = 1, noise_level = 0):
# random sampling from list of trees generated up to the tree with n_node(>=2) nodes
# works for only n<10
    numpy.random.seed()
    output = 0
    output_count = [0,0]
    zero_count = 0
    
    factor_dict = {'A':n_acti, 'R':n_repre, 'D':n_dummy, 'SA':n_superacti, 'SR':n_superrepre, 'E':n_enh, 'S':n_silen, 'SE':n_superenh, 'SS':n_supersilen,'I':n_insul, 'AI':n_anti_insul}
    factor_list = []
    for factor in factor_dict:
        for i in range(1,factor_dict[factor]+1):
            factor_list.append(factor+str(i))
            
    for item in factor_list:
        if item[0] == 'A' or item[0:2]=='SA':
            original_output = 1 
        elif item[0] == 'R' or item[0:2] == 'SR':
            original_output = -1
        else:
            original_output = 0
        prob = numpy.random.random()
        if prob<.5 and prob>.25:
            if original_output == 1:
                if output_count[0]<min(output_count)+10 or output_count[0]<min(output_count)*1.2:
                    output_count[0]+= 1
                    output = 1 if numpy.random.random()>=noise_level else numpy.random.choice([0,-1],1)[0]        
                    f_train.write('('+str(output)+' (0 0) (1 '+item+'))\n')
            elif original_output == -1:
                if output_count[1]<min(output_count)+10 or output_count[1]<min(output_count)*1.2:
                    output_count[1]+= 1
                    output = -1 if numpy.random.random()>=noise_level else numpy.random.choice([1,0],1)[0]
                    f_train.write('('+str(output)+' (0 0) (1 '+item+'))\n')
            elif original_output == 0:
                if zero_count<min(output_count)+10 or zero_count<min(output_count)*1.2:
                    zero_count+= 1
                    output = 0 if numpy.random.random()>=noise_level else numpy.random.choice([1,-1],1)[0]
                    f_train.write('('+str(output)+' (0 0) (1 '+item+'))\n')
        elif prob<.25:
            if original_output == 1:
                if output_count[0]<min(output_count)+10 or output_count[0]<min(output_count)*1.2:
                    output_count[0]+= 1
                    output = 1 
                    f_test.write('('+str(output)+' (0 0) (1 '+item+'))\n')
            elif original_output == -1:
                if output_count[1]<min(output_count)+10 or output_count[1]<min(output_count)*1.2:
                    output_count[1]+= 1
                    output = -1
                    f_test.write('('+str(output)+' (0 0) (1 '+item+'))\n')
            elif original_output == 0:
                if zero_count<min(output_count)+10 or zero_count<min(output_count)*1.2:
                    zero_count+= 1
                    output = 0
                    f_test.write('('+str(output)+' (0 0) (1 '+item+'))\n')
    
    iteration = 2
    while iteration <= n_node:
        binary_tree_list = utils.generate_all_binary_with_closest(iteration)
        possible_permutation = []
        for total_acti, total_repre, total_dummy, total_superacti, total_superrepre, total_enh, total_silen, total_superenh, total_supersilen, total_insul, total_anti_insul in utils.generate_all_divisions(iteration,11):
            if n_acti == 0 and total_acti != 0:
                continue
            if n_repre == 0 and total_repre != 0:
                continue
            if n_dummy == 0 and total_dummy != 0:
                continue            
            if n_superacti == 0 and total_superacti != 0:
                continue
            if n_superrepre == 0 and total_superrepre != 0:
                continue
            if n_enh == 0 and total_enh != 0:
                continue
            if n_silen == 0 and total_silen != 0:
                continue 
            if n_superenh == 0 and total_superenh !=0:
                continue
            if n_supersilen == 0 and total_supersilen !=0:
                continue
            if n_insul == 0 and total_insul !=0:
                continue
            if n_anti_insul == 0 and total_anti_insul != 0:
                continue 
            for acti_div, repre_div, dummy_div, superacti_div, superrepre_div, enh_div, silen_div, superenh_div, supersilen_div, insul_div, anti_insul_div in itertools.product(utils.generate_all_divisions(total_acti, n_acti),utils.generate_all_divisions(total_repre,n_repre),utils.generate_all_divisions(total_dummy,n_dummy),utils.generate_all_divisions(total_superacti,n_superacti),utils.generate_all_divisions(total_superrepre,n_superrepre),utils.generate_all_divisions(total_enh,n_enh),utils.generate_all_divisions(total_silen,n_silen),utils.generate_all_divisions(total_superenh,n_superenh),utils.generate_all_divisions(total_supersilen,n_supersilen),utils.generate_all_divisions(total_insul,n_insul),utils.generate_all_divisions(total_anti_insul,n_anti_insul)):
                factor_dict = {}
                for acti_index in range(len(acti_div)):
                    factor_dict['A'+str(acti_index+1)] = acti_div[acti_index]
                for repre_index in range(len(repre_div)):
                    factor_dict['R'+str(repre_index+1)] = repre_div[repre_index]
                for dummy_index in range(len(dummy_div)):
                    factor_dict['D'+str(dummy_index+1)] = dummy_div[dummy_index]
                for superacti_index in range(len(superacti_div)):
                    factor_dict['SA'+str(superacti_index+1)] = superacti_div[superacti_index]
                for superrepre_index in range(len(superrepre_div)):
                    factor_dict['SR'+str(superrepre_index+1)] = superrepre_div[superrepre_index]
                for enh_index in range(len(enh_div)):
                    factor_dict['E'+str(enh_index+1)] = enh_div[enh_index]
                for silen_index in range(len(silen_div)):
                    factor_dict['S'+str(silen_index+1)] = silen_div[silen_index]
                for superenh_index in range(len(superenh_div)):
                    factor_dict['SE'+str(superenh_index+1)] = superenh_div[superenh_index]
                for supersilen_index in range(len(supersilen_div)):
                    factor_dict['SS'+str(supersilen_index+1)] = supersilen_div[supersilen_index]
                for insul_index in range(len(insul_div)):
                    factor_dict['I'+str(insul_index+1)] = insul_div[insul_index]
                for anti_insul_index in range(len(anti_insul_div)):
                    factor_dict['AI'+str(anti_insul_index+1)] = anti_insul_div[anti_insul_index]
                possible_permutation += utils.make_permutation_list(factor_dict)
        numpy.random.shuffle(possible_permutation)
        for perm in possible_permutation:
            num_tree = int(numpy.random.random()*len(binary_tree_list)*portion)
            numpy.random.shuffle(binary_tree_list)
            for binary_tree in binary_tree_list[:num_tree]:
                closest_element = binary_tree[1]
                permutation_convert = [factor[:-1] for factor in perm]
                insul_index = utils.find_index(permutation_convert,'I',True)
                anti_insul_index = utils.find_index(permutation_convert, 'AI',False)
                permutation_convert = permutation_convert[anti_insul_index:insul_index+1]
                closest_element = [item-anti_insul_index for item in closest_element[anti_insul_index:insul_index+1]]                        
                factor_count_dict = {'A':permutation_convert.count('A'), 'R':permutation_convert.count('R'), 'D':permutation_convert.count('D'), 'SA':permutation_convert.count('SA'), 'SR':permutation_convert.count('SR'), 'E':permutation_convert.count('E'), 'S': permutation_convert.count('S'), 'SE': permutation_convert.count('SE'),'SS': permutation_convert.count('SS'),'I': permutation_convert.count('I'),'AI': permutation_convert.count('AI') }                        
                for factor_index in range(len(permutation_convert)):
                    if permutation_convert[factor_index] == 'E':
                        closest = permutation_convert[closest_element[factor_index]]
                        if closest == 'A' or closest == 'R':
                            factor_count_dict[closest]+=1
                    if permutation_convert[factor_index] == 'SE':
                        closest = permutation_convert[closest_element[factor_index]]
                        if closest == 'A' or closest == 'R':
                            factor_count_dict[closest]-=1
                            factor_count_dict['S'+closest]+=1
                for factor_index in range(len(permutation_convert)):
                    if permutation_convert[factor_index] == 'S':
                        closest = permutation_convert[closest_element[factor_index]]
                        if closest == 'A' or closest == 'R':
                            factor_count_dict[closest] -= 1
                    factor_count_dict['A'] = max(0,factor_count_dict['A'])
                    factor_count_dict['R'] = max(0,factor_count_dict['R']) # to_prevent the number reach 0 first and inappropriately increase by enhancer
                if factor_count_dict['SS'] >0:
                    original_output = 0 
                elif factor_count_dict['A'] == 0 and factor_count_dict['R'] == 0 and factor_count_dict['SA'] == 0 and factor_count_dict['SR'] == 0: 
                    original_output = 0 
                elif factor_count_dict['SA'] ==0 and factor_count_dict['SR']==0 and factor_count_dict['A'] > factor_count_dict['R']:
                    original_output = 1
                elif factor_count_dict['SA'] ==0 and factor_count_dict['SR']==0:
                    original_output = -1
                elif factor_count_dict['SA']>factor_count_dict['SR']:
                    original_output = 1
                else:
                    original_output = -1
                if original_output == 1:
                    if output_count[0]<min(output_count)+10 or output_count[0]<min(output_count)*1.2:
                        output_count[0]+= 1
                        output = 1 
                        utils.random_write(f_train,f_test,binary_tree[0],perm,output,noise_level)
                elif original_output == -1:
                    if output_count[1]<min(output_count)+10 or output_count[1]<min(output_count)*1.2:
                        output_count[1]+= 1
                        output = -1 
                        utils.random_write(f_train,f_test,binary_tree[0],perm,output,noise_level)
                elif original_output == 0:
                    if zero_count<min(output_count)+10 or zero_count<min(output_count)*1.2:
                        zero_count+= 1
                        output = 0 
                        utils.random_write(f_train,f_test,binary_tree[0],perm,output,noise_level)
        iteration+=1


def complexity_8_case(n_node, n_acti, n_repre, n_dummy, n_superacti, n_superrepre, n_enh, n_silen, n_superenh, n_supersilen, n_insul, n_anti_insul, n_rev, f_train, f_test, portion = 1, noise_level = 0):
# random sampling from list of trees generated up to the tree with n_node(>=2) nodes
# works for only n<10
    numpy.random.seed()
    output = 0
    output_count = [0,0]
    zero_count = 0
    
    factor_dict = {'A':n_acti, 'R':n_repre, 'D':n_dummy, 'SA':n_superacti, 'SR':n_superrepre, 'E':n_enh, 'S':n_silen, 'SE':n_superenh, 'SS':n_supersilen,'I':n_insul, 'AI':n_anti_insul, 'RV':n_rev}
    factor_list = []
    for factor in factor_dict:
        for i in range(1,factor_dict[factor]+1):
            factor_list.append(factor+str(i))
            
    for item in factor_list:
        if item[0] == 'A' or item[0:2]=='SA':
            original_output = 1 
        elif (item[0] == 'R' or item[0:2] == 'SR') and item[0:2] != 'RV':
            original_output = -1
        else:
            original_output = 0
        prob = numpy.random.random()
        if prob<.5 and prob>.25:
            if original_output == 1:
                if output_count[0]<min(output_count)+10 or output_count[0]<min(output_count)*1.2:
                    output_count[0]+= 1
                    output = 1 if numpy.random.random()>=noise_level else numpy.random.choice([0,-1],1)[0]        
                    f_train.write('('+str(output)+' (0 0) (1 '+item+'))\n')
            elif original_output == -1:
                if output_count[1]<min(output_count)+10 or output_count[1]<min(output_count)*1.2:
                    output_count[1]+= 1
                    output = -1 if numpy.random.random()>=noise_level else numpy.random.choice([1,0],1)[0]
                    f_train.write('('+str(output)+' (0 0) (1 '+item+'))\n')
            elif original_output == 0:
                if zero_count<min(output_count)+10 or zero_count<min(output_count)*1.2:
                    zero_count+= 1
                    output = 0 if numpy.random.random()>=noise_level else numpy.random.choice([1,-1],1)[0]
                    f_train.write('('+str(output)+' (0 0) (1 '+item+'))\n')
        elif prob<.25:
            if original_output == 1:
                if output_count[0]<min(output_count)+10 or output_count[0]<min(output_count)*1.2:
                    output_count[0]+= 1
                    output = 1 
                    f_test.write('('+str(output)+' (0 0) (1 '+item+'))\n')
            elif original_output == -1:
                if output_count[1]<min(output_count)+10 or output_count[1]<min(output_count)*1.2:
                    output_count[1]+= 1
                    output = -1 
                    f_test.write('('+str(output)+' (0 0) (1 '+item+'))\n')
            elif original_output == 0:
                if zero_count<min(output_count)+10 or zero_count<min(output_count)*1.2:
                    zero_count+= 1
                    output = 0
                    f_test.write('('+str(output)+' (0 0) (1 '+item+'))\n')
    
    iteration = 2
    while iteration <= n_node:
        binary_tree_list = utils.generate_all_binary_with_closest(iteration)
        possible_permutation = []
        for total_acti, total_repre, total_dummy, total_superacti, total_superrepre, total_enh, total_silen, total_superenh, total_supersilen, total_insul, total_anti_insul, total_rev in utils.generate_all_divisions(iteration,12):
            if n_acti == 0 and total_acti != 0:
                continue
            if n_repre == 0 and total_repre != 0:
                continue
            if n_dummy == 0 and total_dummy != 0:
                continue            
            if n_superacti == 0 and total_superacti != 0:
                continue
            if n_superrepre == 0 and total_superrepre != 0:
                continue
            if n_enh == 0 and total_enh != 0:
                continue
            if n_silen == 0 and total_silen != 0:
                continue 
            if n_superenh == 0 and total_superenh !=0:
                continue
            if n_supersilen == 0 and total_supersilen !=0:
                continue
            if n_insul == 0 and total_insul !=0:
                continue
            if n_anti_insul == 0 and total_anti_insul != 0:
                continue 
            if n_rev == 0 and total_rev != 0:
                continue
            for acti_div, repre_div, dummy_div, superacti_div, superrepre_div, enh_div, silen_div, superenh_div, supersilen_div, insul_div, anti_insul_div, rev_div in itertools.product(utils.generate_all_divisions(total_acti, n_acti),utils.generate_all_divisions(total_repre,n_repre),utils.generate_all_divisions(total_dummy,n_dummy),utils.generate_all_divisions(total_superacti,n_superacti),utils.generate_all_divisions(total_superrepre,n_superrepre),utils.generate_all_divisions(total_enh,n_enh),utils.generate_all_divisions(total_silen,n_silen),utils.generate_all_divisions(total_superenh,n_superenh),utils.generate_all_divisions(total_supersilen,n_supersilen),utils.generate_all_divisions(total_insul,n_insul),utils.generate_all_divisions(total_anti_insul,n_anti_insul),utils.generate_all_divisions(total_rev,n_rev)):
                factor_dict = {}
                for acti_index in range(len(acti_div)):
                    factor_dict['A'+str(acti_index+1)] = acti_div[acti_index]
                for repre_index in range(len(repre_div)):
                    factor_dict['R'+str(repre_index+1)] = repre_div[repre_index]
                for dummy_index in range(len(dummy_div)):
                    factor_dict['D'+str(dummy_index+1)] = dummy_div[dummy_index]
                for superacti_index in range(len(superacti_div)):
                    factor_dict['SA'+str(superacti_index+1)] = superacti_div[superacti_index]
                for superrepre_index in range(len(superrepre_div)):
                    factor_dict['SR'+str(superrepre_index+1)] = superrepre_div[superrepre_index]
                for enh_index in range(len(enh_div)):
                    factor_dict['E'+str(enh_index+1)] = enh_div[enh_index]
                for silen_index in range(len(silen_div)):
                    factor_dict['S'+str(silen_index+1)] = silen_div[silen_index]
                for superenh_index in range(len(superenh_div)):
                    factor_dict['SE'+str(superenh_index+1)] = superenh_div[superenh_index]
                for supersilen_index in range(len(supersilen_div)):
                    factor_dict['SS'+str(supersilen_index+1)] = supersilen_div[supersilen_index]
                for insul_index in range(len(insul_div)):
                    factor_dict['I'+str(insul_index+1)] = insul_div[insul_index]
                for anti_insul_index in range(len(anti_insul_div)):
                    factor_dict['AI'+str(anti_insul_index+1)] = anti_insul_div[anti_insul_index]
                for rev_index in range(len(rev_div)):
                    factor_dict['RV'+str(rev_index+1)] = rev_div[rev_index]
                possible_permutation += utils.make_permutation_list(factor_dict)
        numpy.random.shuffle(possible_permutation)
        for perm in possible_permutation:
            num_tree = int(numpy.random.random()*len(binary_tree_list)*portion)
            numpy.random.shuffle(binary_tree_list)
            for binary_tree in binary_tree_list[:num_tree]:
                closest_element = binary_tree[1]
                permutation_convert = [factor[:-1] for factor in perm]
                insul_index = utils.find_index(permutation_convert,'I',True)
                anti_insul_index = utils.find_index(permutation_convert, 'AI',False)
                permutation_convert = permutation_convert[anti_insul_index:insul_index+1]
                closest_element = [item-anti_insul_index for item in closest_element[anti_insul_index:insul_index+1]]                        
                factor_count_dict = {'A':permutation_convert.count('A'), 'R':permutation_convert.count('R'), 'D':permutation_convert.count('D'), 'SA':permutation_convert.count('SA'), 'SR':permutation_convert.count('SR'), 'E':permutation_convert.count('E'), 'S': permutation_convert.count('S'), 'SE': permutation_convert.count('SE'),'SS': permutation_convert.count('SS'),'I': permutation_convert.count('I'),'AI': permutation_convert.count('AI'),'RV': permutation_convert.count('RV')  }                        
                for factor_index in range(len(permutation_convert)):
                    if permutation_convert[factor_index] == 'E':
                        closest = permutation_convert[closest_element[factor_index]]
                        if closest == 'A' or closest == 'R':
                            factor_count_dict[closest]+=1
                    if permutation_convert[factor_index] == 'SE':
                        closest = permutation_convert[closest_element[factor_index]]
                        if closest == 'A' or closest == 'R':
                            factor_count_dict[closest]-=1
                            factor_count_dict['S'+closest]+=1                            
                    if permutation_convert[factor_index] == 'RV':
                        closest = permutation_convert[closest_element[factor_index]]
                        if closest == 'A':
                            factor_count_dict['A']-=1
                            factor_count_dict['R']+=1
                        elif closest == 'R':
                            factor_count_dict['R']-=1
                            factor_count_dict['A']+=1
                for factor_index in range(len(permutation_convert)):
                    if permutation_convert[factor_index] == 'S':
                        closest = permutation_convert[closest_element[factor_index]]
                        if closest == 'A' or closest == 'R':
                            factor_count_dict[closest] -= 1
                    factor_count_dict['A'] = max(0,factor_count_dict['A'])
                    factor_count_dict['R'] = max(0,factor_count_dict['R']) # to_prevent the number reach 0 first and inappropriately increase by enhancer
                if factor_count_dict['SS'] >0:
                    original_output = 0
                elif factor_count_dict['A'] == 0 and factor_count_dict['R'] == 0 and factor_count_dict['SA'] == 0 and factor_count_dict['SR'] == 0: 
                    original_output = 0
                elif factor_count_dict['SA'] ==0 and factor_count_dict['SR']==0 and factor_count_dict['A'] > factor_count_dict['R']:
                    original_output = 1
                elif factor_count_dict['SA'] ==0 and factor_count_dict['SR']==0:
                    original_output = -1
                elif factor_count_dict['SA']>factor_count_dict['SR']:
                    original_output = 1
                else:
                    original_output = -1
                if original_output == 1:
                    if output_count[0]<min(output_count)+10 or output_count[0]<min(output_count)*1.2:
                        output_count[0]+= 1
                        output = 1 
                        utils.random_write(f_train,f_test,binary_tree[0],perm,output,noise_level)
                elif original_output == -1:
                    if output_count[1]<min(output_count)+10 or output_count[1]<min(output_count)*1.2:
                        output_count[1]+= 1
                        output = -1 
                        utils.random_write(f_train,f_test,binary_tree[0],perm,output,noise_level)
                elif original_output == 0:
                    if zero_count<min(output_count)+10 or zero_count<min(output_count)*1.2:
                        zero_count+= 1
                        output = 0
                        utils.random_write(f_train,f_test,binary_tree[0],perm,output,noise_level)
        iteration+=1
        
def run(n_node, n_acti, n_repre, n_dummy, n_superacti, n_superrepre, n_enh, n_silen, n_superenh, n_supersilen, n_insul, n_anti_insul, n_rev, complexity, id_num, portion =1, noise_level = 0):
#Compleixty 1: Acitvator: A, Repressor: R Complexity 2: +Dummy:D Complexity 3:+Super Acitvator:SA, Super Repressor:SR
#Complexity 4: +Enhancer:E, Silencer:S Complexity 5: +SuperEnhancer:SE, +SuperSilencer:SS, Complexity 6: +Insulator:I Complexity 7: +Anti-Insulator:AI Complexity 8: +Reverser

    numpy.random.seed()
    f_train = open('balanced_train_data_complexity_'+str(complexity)+'_'+str(id_num)+'.tree','w')
    f_test = open('balanced_test_data_complexity_'+str(complexity)+'_'+str(id_num)+'.tree','w')
    if complexity == 1:
        complexity_1_case(n_node, n_acti, n_repre, f_train, f_test, portion, noise_level)
    elif complexity == 2:
        complexity_2_case(n_node, n_acti, n_repre, n_dummy, f_train, f_test, portion, noise_level)
    elif complexity == 3:
        complexity_3_case(n_node, n_acti, n_repre, n_dummy, n_superacti, n_superrepre, f_train, f_test, portion, noise_level)
    elif complexity == 4:
        complexity_4_case(n_node, n_acti, n_repre, n_dummy, n_superacti, n_superrepre, n_enh, n_silen, f_train, f_test, portion, noise_level)
    elif complexity == 5:
        complexity_5_case(n_node, n_acti, n_repre, n_dummy, n_superacti, n_superrepre, n_enh, n_silen, n_superenh, n_supersilen, f_train, f_test, portion, noise_level)
    elif complexity == 6:
        complexity_6_case(n_node, n_acti, n_repre, n_dummy, n_superacti, n_superrepre, n_enh, n_silen, n_superenh, n_supersilen, n_insul, f_train, f_test, portion, noise_level)
    elif complexity == 7:
        complexity_7_case(n_node, n_acti, n_repre, n_dummy, n_superacti, n_superrepre, n_enh, n_silen, n_superenh, n_supersilen, n_insul, n_anti_insul, f_train, f_test, portion, noise_level)
    elif complexity == 8:
        complexity_8_case(n_node, n_acti, n_repre, n_dummy, n_superacti, n_superrepre, n_enh, n_silen, n_superenh, n_supersilen, n_insul, n_anti_insul, n_rev, f_train, f_test, portion, noise_level)
    
    f_train.close()
    f_test.close()