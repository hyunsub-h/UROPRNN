# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 10:21:44 2016

@author: HyunSub
"""

import os
import argparse
import numpy
import balanced_case_generate

#Acitvator: A, Repressor: R
#Dummy: D
#Super Activator: SA, Super Repressor: SR
#Enhancer: E, Silencer: S
#Super Enhancer: SE, Super Silencer: SS
#Insulator: I
#Anti-Insulator: AI
#Reverser: RV

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # Input variables
    parser.add_argument("-A","--n_acti", default = 0, help = "The number of activators", type = int)    
    parser.add_argument("-R","--n_repre", default = 0, help = "The number of repressors", type = int)
    parser.add_argument("-D","--n_dummy", default = 0, help = "The number of dummies", type = int)
    parser.add_argument("-SA","--n_superacti", default = 0, help = "The number of super activator", type = int)
    parser.add_argument("-SR","--n_superrepre", default = 0, help = "The number of super repressors", type = int)
    parser.add_argument("-E","--n_enh", default = 0, help = "The number of enhancers", type = int)
    parser.add_argument("-S","--n_silen", default = 0, help = "The number of silencers", type = int)
    parser.add_argument("-I","--n_insul", default = 0, help = "The number of insulators", type = int)
    parser.add_argument("-AI","--n_anti_insul", default = 0, help = "The number of anti insulators", type = int)    
    parser.add_argument("-SE","--n_superenh", default = 0, help = "The number of anti insulators", type = int)    
    parser.add_argument("-SS","--n_supersilen", default = 0, help = "The number of anti insulators", type = int)
    parser.add_argument("-RV","--n_rev",default = 0, help = "The number of reversers", type = int)

    # Testing variables
    parser.add_argument("-n","--n_node", default = 6,help="The number of maximum nodes in tree(2<=n<=9", type= int)
    parser.add_argument("-c","--complexity", default = 1, help = "Complexity of grammar. You need to set approriate relevant varialbes.(The number of factors)", type=int)
    parser.add_argument("-id","--id_num", help = "ID of test", type = int)
    parser.add_argument("-no","--noise", default = 0, help = "Portion of output flipped", type = float)
    parser.add_argument("-p","--portion", default = 1, help = "Data set can be very big. This value control the size of case", type = float)
    args = parser.parse_args()
    
    balanced_case_generate.run(args.n_node, args.n_acti, args.n_repre, args.n_dummy, args.n_superacti, args.n_superrepre, args.n_enh, args.n_silen, args.n_superenh, args.n_supersilen, args.n_insul, args.n_anti_insul, args.n_rev,args.complexity, args.id_num, args.portion, args.noise)