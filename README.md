# UROPRNN
Code for the UROP project of Hyun Sub Hwang in 2016. <br>
Supervisor: Zhizhuo Zhang <br>
This project studied regulatory grammar of transcription factors using a tree-based recurrent neural network

## Descriptions
We want to learn from large scale data across 127 cell types on the epigenome roadmap data. <br>
To decrease training time, we use distributed stochastic gradient descent method on Spark. <br>
To validate distributed stochastic gradient descent method works well for our problem, we generate artificial data and see how well our network performs.

## Code Structure
1. GenerateSimulationData:<br>
This directory contains the codes that generate artificail transcription factors with various rules. Training on generated data is used for validating distributed stochastic gradient descent method on our problem.
2. Server: <br>
A tree-based recurrent neural network that uses distributed stochastic gradient descent method. We asynchronously updates the network using distributed computing on Spark. The distributed stochastic gradient descent method is mainly implemented in "MotifSentimentTraining.java"
