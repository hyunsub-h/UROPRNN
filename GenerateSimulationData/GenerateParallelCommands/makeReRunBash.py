# Maybe rerun is redundant
import argparse

def reduce_file_name(complexity, noise, index):
    return "reduce_file_complexity_%d_%d_%d.txt" % (complexity, noise, index)

"""Make bash file than runs multiple RNNModel1.jar given inputs"""
if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # Input variables
    # parser.add_argument("-num","--n_iters", default = 1, help = "The number of tests for each training/test pair", type = int)
    parser.add_argument("-istart","--i_start", help = "start of iteration index", type = int)
    parser.add_argument("-iend","--i_end", help = "end of iteration index", type = int)

    args = parser.parse_args()
    
    complexity_range = range(1,9)
    noise_range = range(10,16)  

    # train_file_names[i][j] represents "balanced_train_data_complextiy_(i+1)_(10+j).tree" 
    train_file_names = [["balanced_train_data_complexity_%d_%d.tree" % (complexity , noise) for noise in noise_range] for complexity in complexity_range]
    test_file_names = [["balanced_test_data_complexity_%d_%d.tree" % (complexity , noise) for noise in noise_range] for complexity in complexity_range]

    base_command = "java -Xmx40g -server -jar RNNmodel2.jar -train -threads 12 -regWordVector 0.01 -regTransform 0.1 -regClassification 0.01 -epochs 200 -numHid 2 "
    
    java_commands = [[base_command + "-trainpath " + train_file_names[i][j] + " -testpath " + test_file_names[i][j] + " " for j in range(6)] for i in range(8)]
    
    test_commands = [[java_commands[i][j] + "| tail -1 > " for j in range(6)] for i in range(8)]

    data_generate_commands = [[]*6]*8
    data_generate_commands[0] = ["python balanced_data_generate.py -n 5 -A 3 -R 3 -c 1 -id 1%d -no .%d" % (i,i) for i in range(6)]
    data_generate_commands[1] = ["python balanced_data_generate.py -n 5 -A 2 -R 2 -D 2 -c 2 -id 1%d -no .%d" % (i,i) for i in range(6)]
    data_generate_commands[2] = ["python balanced_data_generate.py -n 5 -A 2 -R 2 -D 1 -SA 1 -SR 1 -c 3 -id 1%d -no .%d" % (i,i) for i in range(6)]
    data_generate_commands[3] = ["python balanced_data_generate.py -n 5 -A 2 -R 2 -D 1 -E 1 -S 1 -c 4 -id 1%d -no .%d" % (i,i) for i in range(6)]
    data_generate_commands[4] = ["python balanced_data_generate.py -n 5 -A 2 -R 2 -D 1 -SA 1 -SR 1 -E 1 -S 1 -SE 1 -SR 1 -c 5 -id 1%d -no .%d -p .2" % (i,i) for i in range(6)]
    data_generate_commands[5] = ["python balanced_data_generate.py -n 5 -A 2 -R 2 -D 1 -E 1 -S 1 -I 1 -c 6 -id 1%d -no .%d -p .5" % (i,i) for i in range(6)]
    data_generate_commands[6] = ["python balanced_data_generate.py -n 5 -A 2 -R 2 -D 1 -E 1 -S 1 -I 1 -AI 1 -c 7 -id 1%d -no .%d -p .5" % (i,i) for i in range(6)]
    data_generate_commands[7] = ["python balanced_data_generate.py -n 5 -A 2 -R 2 -D 1 -E 1 -S 1 -I 1 -AI 1 -RV 1 -c 8 -id 1%d -no .%d -p .2" % (i,i) for i in range(6)]

    command_start = " "

    f =  open("runReRunTest_%d_to_%d.sh" % (args.i_start, args.i_end) , 'w')

    f.write("#!/bin/bash\n")
    f.write("\n")

    command = command_start
    for iteration in xrange(args.i_start ,args.i_end+1):
        for i in range(8):
            for j in range(6):
                generate_command = data_generate_commands[i][j]
                test_command = test_commands[i][j]
                command += generate_command + "; " + test_command + reduce_file_name(i + 1, j+10, iteration) + "; "
    f.write(command)
    f.close()
    
