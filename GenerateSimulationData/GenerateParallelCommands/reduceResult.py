import argparse
import os
import numpy as np
from scipy import stats
def reduce_file_name(compelxity, noise, index):
    return "reduce_file_complexity_%d_%d_%d.txt" % (complexity, noise, index)


"""Reduce output files"""

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # Input variables        
    parser.add_argument("-num","--n_iters", help = "The number of files", type = int)
    
    args = parser.parse_args()
    
    complexity_range = range(1,9)
    noise_range = range(10,16)  
    index_range = range(1, args.n_iters+1)

    final_result_file_names = [["final_result_%d_%d.txt" % (complexity , noise) for noise in noise_range] for complexity in complexity_range]

    # final_result_sums = [[0.0]*6]*8
    # final_result_maxs = [[0.0]*6]*8
    # final_result_mins = [[0.0]*6]*8
    
    confidence_level = .95
    for complexity in complexity_range:
        for noise in noise_range:
            #final_result_sum = 0.0
            num_file = 0.0
            auc_list = []
            for index in index_range:
                if os.path.isfile(reduce_file_name(complexity, noise, index)):                    
                    f = open(reduce_file_name(complexity, noise, index), 'r')
                    file_content = f.read()
                    if not len(file_content) == 0:
                        result = float(file_content.split()[-1])
                        num_file += 1
                        #final_result_sum += result
                        auc_list.append(result)
                    f.close()

            t_score = stats.t.ppf(.5 + confidence_level/2, num_file-1) if num_file != 0 else 0 

            result_avg = np.average(auc_list) if num_file != 0 else 0
            result_std = np.std(auc_list) if num_file != 0 else 0
            result_upper = result_avg + t_score * result_std / np.sqrt(num_file) if num_file != 0 else 0
            result_lower = result_avg - t_score * result_std / np.sqrt(num_file) if num_file != 0 else 0

            f = open(final_result_file_names[complexity - 1][noise - 10], 'w')
            f.write("Result for %d iterations %d complexity level .%d noise level\n" % (args.n_iters, complexity, noise))
            f.write("number of files: " + str(num_file) + "\n")
            f.write("upper: " + str(result_upper) + "\n")
            f.write("lower: " + str(result_lower) + "\n")
            f.write("average: " + str(result_avg) + "\n")
            f.close()
