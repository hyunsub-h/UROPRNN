# TODO: implemnet this code!
# Maybe rerun is redundant

import argparse

def reduce_file_name(complexity, noise, index):
    return "reduce_file_complexity_%d_%d_%d.txt" % (complexity, noise, index)

"""Make bash file than runs multiple RNNModel1.jar given inputs"""
if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # Input variables
    # parser.add_argument("-nodes","--n_nodes", default = 1, help = "The number of workers", type = int)
    # parser.add_argument("-epochs","--epochs", default = 200, help = "The number of epochs", type = int)
    # parser.add_argument("-num","--n_iters", default = 1, help = "The number of workers", type = int)
    # parser.add_argument("-numHid","--numHid", help = "The dimension of hitting dimensions", type = int)
    # parser.add_argument("-trainpath","--trainpath", help = "The training data", type=str)
    # parser.add_argument("-testpath","--testpath", help = "The test data", type=str)

    parser.add_argument("-num","--n_iters", default = 1, help = "The number of tests for each training/test pair", type = int)
        
    args = parser.parse_args()
    
    complexity_range = range(1,9)
    noise_range = range(10,16)  

    # train_file_names[i][j] represents "balanced_train_data_complextiy_(i+1)_(10+j).tree" 
    train_file_names = [["balanced_train_data_complexity_%d_%d.tree" % (complexity , noise) for noise in noise_range] for complexity in complexity_range]
    test_file_names = [["balanced_test_data_complexity_%d_%d.tree" % (complexity , noise) for noise in noise_range] for complexity in complexity_range]

    base_command = "java -Xmx40g -server -jar RNNmodel2.jar -train -threads 1 -regWordVector 0.01 -regTransform 0.1 -regClassification 0.01 -epochs 200 -numHid 2 "
    
    java_commands = [[base_command + "-trainpath " + train_file_names[i][j] + " -testpath " + test_file_names[i][j] + " " for j in range(6)] for i in range(8)]
    
    parallel_commands = [[java_commands[i][j] + "| tail -1 > " for j in range(6)] for i in range(8)]

    command_start = "parallel ::: "

    f = open("runReRunTest_%d.sh" % (args.n_iters) , 'w')
    f.write("#!/bin/bash\n")
    f.write("\n")

    command = command_start
    for iteration in xrange(1,args.n_iters+1):
        for i in range(8):
            for j in range(6):
                parallel_command = parallel_commands[i][j]
                command += "\" " + parallel_command + reduce_file_name(i + 1, j+10, iteration) + "\" "
    f.write(command)
    f.close()
    
