

import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.text.DecimalFormat;
import java.text.NumberFormat;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.Set;
import java.util.Map.Entry;
import java.util.concurrent.Callable;
import java.util.concurrent.CompletionService;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorCompletionService;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

import org.apache.commons.lang3.Range;
import org.apache.log4j.Logger;
import org.apache.spark.SparkConf;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;
import org.apache.spark.api.java.function.Function;
import org.apache.spark.api.java.function.Function2;
import org.apache.spark.broadcast.Broadcast;
import org.ejml.simple.SimpleMatrix;

import edu.stanford.nlp.sentiment.RNNOptions;
import edu.stanford.nlp.trees.Tree;
import edu.stanford.nlp.util.Generics;
import edu.stanford.nlp.util.Pair;
import edu.stanford.nlp.util.Timing;
import edu.stanford.nlp.util.Triple;


public class MotifSentimentTraining {

  private static final NumberFormat NF = new DecimalFormat("0.00");
  private static final NumberFormat FILENAME = new DecimalFormat("0000");
  public static TransformFunction neural_function=new TanhTransform();
  private static double allbatchCost=0;
  
  private static int trainingStep = 0;
  
  /*
   * Thread-safe trainingStep increment
   */
  private static void increaseSteps(){
	  trainingStep++;
  }
  /*
   * Map function that trains model and return the differences in theta (in model) and sumGradSquare 
   */
	public static Function< Pair<TrainHolder, Broadcast<List<Tree>>  >, Pair<double[], double[]> > executeOneTrainingInParallel = new Function< Pair<TrainHolder, Broadcast<List<Tree>> >, Pair<double[], double[] >>(){
	
	private static final long serialVersionUID = 812306434400716846L;

	public Pair<double[], double[]> call(Pair<TrainHolder, Broadcast<List<Tree>>  > parameters) { 
		MotifSentimentModel model = parameters.first.model;
		List<Tree> trainingBatch = new ArrayList<Tree>();
		for(int index: parameters.first.trainingIndices){trainingBatch.add(parameters.second.value().get(index));}
		double[] sumGradSquare = parameters.first.sumGradSquare;
		
		double[] theta = model.paramsToVector();
		    
		    double[] thetaInitial = new double[theta.length];
		    for(int i=0; i<theta.length;i++) {thetaInitial[i] = theta[i];}
		    double[] sumGradInitial = new double[sumGradSquare.length];
		    for(int i=0; i<sumGradSquare.length;i++) {sumGradInitial[i] = sumGradSquare[i];}
		    
		for(int i=0; i<parameters.first.batchIteration;i++ ){    
			MotifSentimentCostAndGradient gcFunc = new MotifSentimentCostAndGradient(model, trainingBatch, neural_function);
		  
		    // AdaGrad
		    double eps = 1e-3;
		    double currCost = 0;
	
		    // TODO: do we want to iterate multiple times per batch?
		    double[] gradf = gcFunc.derivativeAt(theta);
		    currCost = gcFunc.valueAt(theta);
	//	    System.err.println("batch cost: " + Math.sqrt(currCost/model.numClasses)); //orignial print denote the avg error
	//	    System.err.println("batch cost: " + Utils.round(currCost/model.numClasses,4)+" regClass:"+Utils.round(gcFunc.regClassificationCost/model.numClasses,2)+" regTrans:"+Utils.round(gcFunc.regTransformCost/model.numClasses,2)+" regWord:"+Utils.round(gcFunc.regWordVectorCost/model.numClasses,2));  //already normalize batch_size
		   double maxGradient=0;
		    for (int feature = 0; feature<gradf.length;feature++ ) {
		      sumGradSquare[feature] = sumGradSquare[feature] + gradf[feature]*gradf[feature];
		      theta[feature] = theta[feature] - (model.op.trainOptions.learningRate * gradf[feature]/(Math.sqrt(sumGradSquare[feature])+eps));
		      if(gradf[feature]>maxGradient) //apply gradient clipping
		    	  maxGradient=gradf[feature];
		    } 
	//	    System.err.println("max Gradient: " +maxGradient);
		    allbatchCost+=currCost;
	
	//	    model.vectorToParams(theta);   
		}

	    double[] thetaChange = new double[theta.length]; 
	    for(int i=0; i<theta.length;i++) {thetaChange[i] = theta[i] - thetaInitial[i];}
	    
	    double[] sumGradChange = new double[sumGradSquare.length];
	    for(int i=0; i<sumGradSquare.length;i++) {sumGradChange[i] = sumGradSquare[i] - sumGradInitial[i];}

		return new Pair<double[],double[]>(thetaChange, sumGradChange);
	}};
        	  	
	////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
  
  public static void executeOneTrainingBatch(MotifSentimentModel model, List<Tree> trainingBatch, double[] sumGradSquare) {
    MotifSentimentCostAndGradient gcFunc = new MotifSentimentCostAndGradient(model, trainingBatch, neural_function);
    double[] theta = model.paramsToVector();

    // AdaGrad
    double eps = 1e-3;
    double currCost = 0;

    // TODO: do we want to iterate multiple times per batch?
    double[] gradf = gcFunc.derivativeAt(theta);
    currCost = gcFunc.valueAt(theta);
    System.err.println("batch cost: " + Math.sqrt(currCost/model.numClasses)); //orignial print denote the avg error
    System.err.println("batch cost: " + Utils.round(currCost/model.numClasses,4)+" regClass:"+Utils.round(gcFunc.regClassificationCost/model.numClasses,2)+" regTrans:"+Utils.round(gcFunc.regTransformCost/model.numClasses,2)+" regWord:"+Utils.round(gcFunc.regWordVectorCost/model.numClasses,2));  //already normalize batch_size
   double maxGradient=0;
    for (int feature = 0; feature<gradf.length;feature++ ) {
      sumGradSquare[feature] = sumGradSquare[feature] + gradf[feature]*gradf[feature];
      theta[feature] = theta[feature] - (model.op.trainOptions.learningRate * gradf[feature]/(Math.sqrt(sumGradSquare[feature])+eps));
      if(gradf[feature]>maxGradient) //apply gradient clipping
    	  maxGradient=gradf[feature];
    } 
    System.err.println("max Gradient: " +maxGradient);
    allbatchCost+=currCost;

    model.vectorToParams(theta);   
    
  }
  
  public static String executeOneTrainingInParallel(TrainHolder holder){
	  return "";
  }
  
  public static MotifSentimentModel train_multiThread(MotifSentimentModel inputModel, final String modelPath, final JavaSparkContext sc, final Broadcast<List<Tree>> broadcastTrainingTrees, final List<Tree> devTrees, int threadNum, final int batchIteration){

	    final MotifSentimentModel model = inputModel;  
	    final List<Tree> trainingTrees = broadcastTrainingTrees.value();
	  	final Timing timing = new Timing();
	    long maxTrainTimeMillis = model.op.trainOptions.maxTrainTimeSeconds * 1000;
	    int debugCycle = 0;
	    double bestCost=Double.MAX_VALUE;
	    List<List<Tree>> InvestigateExamples=null;
	    if(Utils.findNonExchangableExample)
	    {
	     InvestigateExamples = ExampleFinder.exchangeGrammarFailed_Examples(trainingTrees);
	    System.out.println("Number of InvestigateExamples is "+InvestigateExamples.size());
	    }
	    OneTrainingBatchThread.tempPath=modelPath+".tmp";
	    // train using AdaGrad (seemed to work best during the dvparser project)
	    final double[] sumGradSquare = new double[model.totalParamSize()];
	    Arrays.fill(sumGradSquare, model.op.trainOptions.initialAdagradWeight);
	    
	    int numBatches = trainingTrees.size() / model.op.trainOptions.batchSize ;
	    if(numBatches*model.op.trainOptions.batchSize<trainingTrees.size() )
	    {
	    	numBatches+=1;
	    }
	    
	    System.err.println("Training on " + trainingTrees.size() + " trees in " + numBatches + " batches");
	    System.err.println("Times through each training batch: " + model.op.trainOptions.epochs);
	    double allbatchCost_last=Double.MAX_VALUE;
		
	    
	    // To be called in callable
	    final List<Double> bestAccuracy = new ArrayList<Double>(Arrays.asList(0.0));
	    final List<String> bestModelStr = new ArrayList<String>(Arrays.asList(""));
	    final List<MotifSentimentModel> bestModel = new ArrayList<MotifSentimentModel>();
	    bestModel.add(null);
	    
	    // TODO: optimize the number of threads?
	    ExecutorService threadPool = Executors.newScheduledThreadPool(Math.max(threadNum, 2));
        CompletionService<Pair<double[], double[]>> completionService = new ExecutorCompletionService<Pair<double[], double[]>>(threadPool);
        
        final int numTrainingSteps = numBatches * model.op.trainOptions.epochs /batchIteration;
        
	    /*
	     * Infinitely run testing until all training steps are finished
	     */
	    completionService.submit(new Callable<Pair<double[], double[]>>(){
	    	public Pair<double[], double[]> call() throws Exception{
	    		while(true){
	    			if(trainingStep==0)
	    				Thread.sleep(10000);
	    			if(trainingStep == numTrainingSteps)
	    				break;

	    		    long totalElapsed = timing.report();
	    			double score = 0.0;
		            System.err.println("======================================");
		            System.out.println("Finished training step " + trainingStep + "; total training time " + totalElapsed + " ms");
		            if (devTrees != null) {
		              MotifEvaluate eval = new MotifEvaluate(model);
		              if(Utils.RNNdoubleTest)
		              {
		              	System.out.println("Double testing...........");
		              	 eval.eval(new ArrayList<Tree>( devTrees.subList(0, devTrees.size()/2) ) );
		                   eval.printSummary();
		                   String stateString="";
		                   double avgAUC=eval.AUCs.elementSum()/eval.AUCs.getNumElements();
		                   stateString+="UserTest Data AUC: "+avgAUC;
		              	 eval.eval(new ArrayList<Tree>( devTrees.subList( devTrees.size()/2+1,devTrees.size()) ) );
		                   eval.printSummary();
		                   avgAUC=eval.AUCs.elementSum()/eval.AUCs.getNumElements();
		                   stateString+="-------SplitTest Data AUC: "+avgAUC;
		                   if(bestAccuracy.get(0)<avgAUC)
		                   {
		                	   System.out.println("current best model :"+ bestModelStr);
		                	   bestAccuracy.set(0,avgAUC);
		                	   bestModelStr.set(0, stateString);
		                	   bestModel.set(0, new MotifSentimentModel(model.op, trainingTrees));
//		                	   bestModel.vectorToParams(modelForTest.paramsToVector());
		                	   model.saveSerialized(modelPath+".best.gz");
		                   }
		                   
		              }
		              else
		              {
		              eval.eval(devTrees);
		              eval.printSummary();
		              }
//		              score =1/eval.rootPredictionError; //eval.exactNodeAccuracy() * 100.0;
		            } 
		            model.saveSerialized(OneTrainingBatchThread.tempPath);
	    		}
	    		// redo testing to make sure we test with final model
    		    long totalElapsed = timing.report();
    			double score = 0.0;
	            System.err.println("======================================");
	            System.out.println("Finished training step " + trainingStep + "; total training time " + totalElapsed + " ms");
	            if (devTrees != null) {
	              MotifEvaluate eval = new MotifEvaluate(model);
	              if(Utils.RNNdoubleTest)
	              {
	              	System.out.println("Double testing...........");
	              	 eval.eval(new ArrayList<Tree>( devTrees.subList(0, devTrees.size()/2) ) );
	                   eval.printSummary();
	                   String stateString="";
	                   double avgAUC=eval.AUCs.elementSum()/eval.AUCs.getNumElements();
	                   stateString+="UserTest Data AUC: "+avgAUC;
	              	 eval.eval(new ArrayList<Tree>( devTrees.subList( devTrees.size()/2+1,devTrees.size()) ) );
	                   eval.printSummary();
	                   avgAUC=eval.AUCs.elementSum()/eval.AUCs.getNumElements();
	                   stateString+="-------SplitTest Data AUC: "+avgAUC;
	                   if(bestAccuracy.get(0)<avgAUC)
	                   {
	                	   System.out.println("current best model :"+ bestModelStr);
	                	   bestAccuracy.set(0,avgAUC);
	                	   bestModelStr.set(0, stateString);
	                	   bestModel.set(0, new MotifSentimentModel(model.op, trainingTrees));
//	                	   bestModel.vectorToParams(modelForTest.paramsToVector());
	                	   model.saveSerialized(modelPath+".best.gz");
	                   }
	                   
	              }
	              else
	              {
	              eval.eval(devTrees);
	              eval.printSummary();
	              }
//	              score =1/eval.rootPredictionError; //eval.exactNodeAccuracy() * 100.0;
	            } 
	            model.saveSerialized(OneTrainingBatchThread.tempPath);
	    		return null;
	    	}
	    });
	    
	    
	    /*
	     * Implements asynchronuous calls for training
	     */
	    
	    for(int i=0; i<numTrainingSteps; i++){
	    	completionService.submit(new Callable<Pair<double[], double[]>>(){
		    	public Pair<double[], double[]> call() throws Exception{

		  	      	List<Integer> indices = new ArrayList<Integer>();
		  	      	for(int i=0;i<trainingTrees.size();i++) {indices.add(i);}
		  	      	Collections.shuffle(indices, model.rand);
		  	      	List< Pair< TrainHolder, Broadcast<List<Tree>>  > > parameters = new ArrayList< Pair<TrainHolder, Broadcast<List<Tree>> > >();
		  	      	
//		  	      	for(int j=0 ; j<batchIteration ; j++){
		  	      		parameters.add(new Pair<TrainHolder, Broadcast< List<Tree> > >(new TrainHolder(model, sumGradSquare, new ArrayList<Integer>(indices.subList(0, model.op.trainOptions.batchSize-1)),batchIteration ), broadcastTrainingTrees));	    	  
//		  	      	}
			    
		  	      	JavaRDD< Pair< TrainHolder, Broadcast<List<Tree>>  > > parallelParameters = sc.parallelize(parameters);

		  	      	Pair<double[], double[]> parameterChange = parallelParameters.map(executeOneTrainingInParallel).first();
//		  	      			.reduce(
//			  	    		  new Function2<Pair<double[], double[]> , Pair<double[], double[]>, Pair<double[], double[]>>(){
//				    			  public Pair<double[], double[]> call(Pair<double[], double[]> a, Pair<double[], double[]> b){
//				    				  return new Pair<double[], double[]>(Utils.sumArray(a.first,b.first), Utils.sumArray(a.second,b.second));
//				    			  }
//				    		  });

		  	      	
		    		return parameterChange;
		    	}
		    }
	       );
	    }
	    
	    // numTrainingSteps+1? numTrainingSteps?
	    for (int i = 0; i < numTrainingSteps+1; i++) {
	    	Pair<double[], double[]> parameterChange;

//        	System.err.println(i + "th steps finished?");
            try {
            	parameterChange = completionService.take().get(); // find the first completed task
            	if(parameterChange != null){
            		// updates parameters
		  	      	double[] theta = model.paramsToVector();
		  	      	theta = Utils.sumArray(theta, parameterChange.first);
		  	      	model.vectorToParams(theta);
		  	      	
		  	      	for(int j=0 ; j < sumGradSquare.length; j++){
		  	      		sumGradSquare[j] += parameterChange.second[j];
		  	      	}

		  	      	increaseSteps();
		  	      	
		  	      	if (trainingStep > 0 && model.op.trainOptions.adagradResetFrequency > 0 && 
		  		          (trainingStep % numBatches == 0)) {
		  		        System.err.println("Resetting adagrad weights to " + model.op.trainOptions.initialAdagradWeight);
		  		        
		  		        Arrays.fill(sumGradSquare, model.op.trainOptions.initialAdagradWeight);
		  		        System.gc();
		  		        
		  			    // not sure this if statement should be here
		  			    if(Utils.findNonExchangableExample)
		  			      {
		  				      List<List<Tree>> succExamples = ExampleFinder.predictableExamples(model, InvestigateExamples);
		  				      System.out.println("Number of Success Examples is "+succExamples.size());
		  				      if(succExamples.size()>0)
		  				      {
		  				    	  System.out.println("First Success Example:");
		  				    	  List<Tree> succ_example = succExamples.get(0);
		  				    	  for (int j = 0; j <succ_example.size(); j++) {
		  				    		  System.out.println("true:"+succ_example.get(j));
		  				    		  Tree pred = succ_example.get(j).deepCopy();
		  				    		  Predict_SetLabel(model, pred);
		  				    		  System.out.println("pred:"+pred);
		  						}
		  				      }
		  			      }
		  	      	}
            	}
//            	System.err.println(i + "th steps finished");
            } catch (InterruptedException e) {
            } catch (ExecutionException e) {
            }
        }
	   threadPool.shutdown();
	    
	      //check the investigate examples:
	    if(Utils.findNonExchangableExample)
	    {
	      List<List<Tree>> succExamples = ExampleFinder.predictableExamples(model, InvestigateExamples);
	      if(succExamples.size()>0)
	      {
	    	  System.out.println("All Success Examples:");
	    	  Iterator<List<Tree>> iter = succExamples.iterator();
	    	  while(iter.hasNext())
	    	  {
		    	  List<Tree> succ_example = iter.next();
		    	  System.out.println("-----------------------------------------");
			    	  for (int i = 0; i <succ_example.size(); i++) {
			    		  System.out.println("true:"+succ_example.get(i));
			    		  Tree pred = succ_example.get(i).deepCopy();
			    		  Predict_SetLabel(model, pred);
			    		  System.out.println("pred:"+pred);
					}
	    	  }
	      }
	    }
		System.out.println("Total Elapsed Time is "+ timing.report()/1000+" secondes");
//		if(bestCost<allbatchCost_last)
//		{
		inputModel=bestModel.get(0);
		 System.out.println("current best model :"+bestModelStr);
//         if (devTrees != null) {
//             MotifEvaluate eval = new MotifEvaluate(model);
//             eval.eval(devTrees);
//             eval.printSummary();
////             score =1/eval.rootPredictionError; //eval.exactNodeAccuracy() * 100.0;
//           }
//		}
		return bestModel.get(0);
	  }

  public static void train(MotifSentimentModel model, String modelPath, List<Tree> trainingTrees, List<Tree> devTrees) {
    Timing timing = new Timing();
    long maxTrainTimeMillis = model.op.trainOptions.maxTrainTimeSeconds * 1000;
    int debugCycle = 0;
    
    double bestAccuracy = 0.0;

    // train using AdaGrad (seemed to work best during the dvparser project)
    double[] sumGradSquare = new double[model.totalParamSize()];
    Arrays.fill(sumGradSquare, model.op.trainOptions.initialAdagradWeight);
    
    int numBatches = trainingTrees.size() / model.op.trainOptions.batchSize ;
    if(numBatches*model.op.trainOptions.batchSize<trainingTrees.size() )
    {
    	numBatches+=1;
    }

    System.err.println("Training on " + trainingTrees.size() + " trees in " + numBatches + " batches");
    System.err.println("Times through each training batch: " + model.op.trainOptions.epochs);
    for (int epoch = 0; epoch < model.op.trainOptions.epochs; ++epoch) {
      System.err.println("======================================");
      System.err.println("Starting epoch " + epoch);
      if (epoch > 0 && model.op.trainOptions.adagradResetFrequency > 0 && 
          (epoch % model.op.trainOptions.adagradResetFrequency == 0)) {
        System.err.println("Resetting adagrad weights to " + model.op.trainOptions.initialAdagradWeight);
        Arrays.fill(sumGradSquare, model.op.trainOptions.initialAdagradWeight);
      }
//      model.op.trainOptions.learningRate*=0.999;
      List<Tree> shuffledSentences = Generics.newArrayList(trainingTrees);
      Collections.shuffle(shuffledSentences, model.rand);
      for (int batch = 0; batch < numBatches; ++batch) {
//        System.err.println("======================================");
//        System.err.println("Epoch " + epoch + " batch " + batch);
      
        // Each batch will be of the specified batch size, except the
        // last batch will include any leftover trees at the end of
        // the list
        int startTree = batch * model.op.trainOptions.batchSize;
        int endTree = (batch + 1) * model.op.trainOptions.batchSize;
        if (endTree + model.op.trainOptions.batchSize > shuffledSentences.size()) {
          endTree = shuffledSentences.size();
        }
        
        executeOneTrainingBatch(model, new ArrayList<Tree>( shuffledSentences.subList(startTree, endTree) ), sumGradSquare);

        long totalElapsed = timing.report();
//        System.err.println("Finished epoch " + epoch + " batch " + batch + "; total training time " + totalElapsed + " ms");

        if (maxTrainTimeMillis > 0 && totalElapsed > maxTrainTimeMillis) {
          // no need to debug output, we're done now
            System.err.println("======================================");
            System.err.println("Epoch " + epoch + " batch " + batch);
            System.err.println("Finished epoch " + epoch + " batch " + batch + "; total training time " + totalElapsed + " ms");
          break;
        }

        if (batch == 0 && epoch > 0 && epoch % model.op.trainOptions.debugOutputEpochs == 0) {
          double score = 0.0;
          System.err.println("======================================");
          System.err.println("Epoch " + epoch + " batch " + batch);
          System.out.println("Finished epoch " + epoch + " batch " + batch + "; total training time " + totalElapsed + " ms");
          if (devTrees != null) {
            MotifEvaluate eval = new MotifEvaluate(model);
            eval.eval(devTrees);
            eval.printSummary();
//            score =1/eval.rootPredictionError; //eval.exactNodeAccuracy() * 100.0;
          }

          // output an intermediate model
          if (modelPath != null) {
            String tempPath = modelPath;
            if (modelPath.endsWith(".ser.gz")) {
              tempPath = modelPath.substring(0, modelPath.length() - 7) + "-" + FILENAME.format(debugCycle) + "-" + NF.format(score) + ".ser.gz";
            } else if (modelPath.endsWith(".gz")) {
              tempPath = modelPath.substring(0, modelPath.length() - 3) + "-" + FILENAME.format(debugCycle) + "-" + NF.format(score) + ".gz";
            } else {
              tempPath = modelPath.substring(0, modelPath.length() - 3) + "-" + FILENAME.format(debugCycle) + "-" + NF.format(score);
            }
//            model.saveSerialized(tempPath);
          }

          ++debugCycle;
        }
      }
      long totalElapsed = timing.report();
      
      if (maxTrainTimeMillis > 0 && totalElapsed > maxTrainTimeMillis) {
        System.err.println("Max training time exceeded, exiting");
        break;
      }
      
    }    
    System.out.println("Total Elapsed Time is "+ timing.report()/1000+" secondes");
  }

  public static boolean runGradientCheck(MotifSentimentModel model, List<Tree> trees) {
    MotifSentimentCostAndGradient gcFunc = new MotifSentimentCostAndGradient(model, trees,neural_function);
    return gcFunc.gradientCheck(model.totalParamSize(), 50, model.paramsToVector());    
  }

  public static void removeUnknownLeaves(Set<String> wordSets, Tree tree)
  {
	  if(tree.isPrePreTerminal())
	  {
		  Tree[] childs = tree.children();
		  for (int i = 0; i < childs.length; i++) {
			if(!wordSets.contains(childs[childs.length-i-1].children()[0].label().value()))
				tree.removeChild(childs.length-i-1);
		}
	  }
	  else
	  {
		  Tree[] childs = tree.children();
		  for (int i = 0; i < childs.length; i++)
		  {
//			  boolean orig1=childs[childs.length-i-1].children().length==1||childs[childs.length-i-1].isLeaf();
			  removeUnknownLeaves(wordSets,childs[childs.length-i-1]);
			  if(childs[childs.length-i-1].isLeaf()&&!wordSets.contains(childs[childs.length-i-1].label().value()))//&&!orig1)
				  tree.removeChild(childs.length-i-1);
			  else if(childs[childs.length-i-1].children().length==1&&!childs[childs.length-i-1].isPreTerminal()) //&&!orig1)
				  tree.setChild(childs.length-i-1,childs[childs.length-i-1].getChild(0));//collapse
				 
		  }

          if( tree.children().length==1&&!tree.isPreTerminal())
				 tree.setChildren(tree.getChild(0).children());
	  }
	  
  }
  
  public static void Predict_SetLabel(MotifSentimentModel model, Tree tree)
  {
	  //filter unknown leafs
	  if(tree.getLeaves().size()>2)
	  removeUnknownLeaves(model.wordVectors.keySet(),tree);

	  if(tree.getLeaves().size()<2)
		  return;
//	  System.err.println(tree);
	  model.predict(tree);
	  Iterator<Tree> iter = tree.iterator();
	  while(iter.hasNext())
	  {
		  Tree node = iter.next();

		  SimpleMatrix pred = MotifRNNCoreAnnotations.getPredictions(node);
		 
		  if(pred==null)
			  continue;
//		  System.err.println(Utils.Vector2String(pred));
		  String label = Utils.Vector2String(pred);
		  node.label().setValue(label);
	  }
  }
  
  public static void main(String[] args) {
    RNNOptions op = new RNNOptions();
    op.randomSeed=0;  //-randomSeed
    

    String trainPath = "sentimentTreesDebug.txt";
    String devPath = null;

    boolean runGradientCheck = false;
    boolean runTraining = false;
    boolean runPredicting = false;
    boolean filterUnknown = false;
    double splitTest=0;
    boolean useTensor=false;
    String modelPath = null;
    int numthreads=1;
    int batchIteration = 1;
    
    op.trainOptions.epochs=10000;   //-epochs
    op.trainOptions.regClassification=0.0001; //-regClassification
    op.trainOptions.regTransform=0.001;  //-regTransform
    op.trainOptions.batchSize=100;
    op.trainOptions.learningRate=0.01;  //-learningRate
    op.trainOptions.regWordVector=0.0001;  //-regWordVector
    op.trainOptions.debugOutputEpochs=4;
    op.numHid=25;    //-numHid 
    op.useTensors=useTensor;   //-useTensors
    op.simplifiedModel=true;
    

    for (int argIndex = 0; argIndex < args.length; ) {
      if (args[argIndex].equalsIgnoreCase("-train")) {
        runTraining = true;
        argIndex++;
      } else if (args[argIndex].equalsIgnoreCase("-gradientcheck")) {
        runGradientCheck = true;
        argIndex++;
      } else if (args[argIndex].equalsIgnoreCase("-threads")) {
    	  numthreads = Integer.valueOf(args[argIndex + 1]);
    	  argIndex += 2;
      } else if (args[argIndex].equalsIgnoreCase("-batchIteration")) {
    	  batchIteration = Integer.valueOf(args[argIndex + 1]);
    	  argIndex += 2;
      } else if (args[argIndex].equalsIgnoreCase("-trainpath")) { // training data
        trainPath = args[argIndex + 1];
        argIndex += 2;
      } else if (args[argIndex].equalsIgnoreCase("-splittest")) { // random seed 
    	  splitTest =Double.valueOf(args[argIndex + 1]);
          argIndex += 2;
      } else if (args[argIndex].equalsIgnoreCase("-testpath")) {  // testing data for validate the model, or for prediction
        devPath = args[argIndex + 1];
        argIndex += 2;
        runPredicting=true;
      } else if (args[argIndex].equalsIgnoreCase("-model")) {  //previous saved model, can use to predict testing data
        modelPath = args[argIndex + 1];
        argIndex += 2;
        runPredicting=true;
      } else if (args[argIndex].equalsIgnoreCase("-filterUnknown")) {
        filterUnknown = true;
        argIndex++;
      }
      else if (args[argIndex].equalsIgnoreCase("-singleTest")) {
    	  Utils.RNNdoubleTest = false;
          argIndex++;
        }
      else {
        int newArgIndex = op.setOption(args, argIndex);
        if (newArgIndex == argIndex) {
          throw new IllegalArgumentException("Unknown argument " + args[argIndex]);
        }
        argIndex = newArgIndex;
      }
    }



    List<Tree> devTrees = null;
    if (devPath != null) {
      devTrees = Utils.readTreesWithGoldLabels(devPath);
      System.err.println("Read in " + devTrees.size() + " dev trees");
      if (filterUnknown) {
        devTrees = Utils.filterUnknownRoots(devTrees);
        System.err.println("Filtered testing trees: " + devTrees.size());
      }
    }

    // TODO: binarize the trees, then collapse the unary chains.
    // Collapsed unary chains always have the label of the top node in
    // the chain
    // Note: the sentiment training data already has this done.
    // However, when we handle trees given to us from the Stanford Parser,
    // we will have to perform this step

    // build an unitialized MotifSentimentModel from the binary productions

    MotifSentimentModel model = null; 

    // TODO: need to handle unk rules somehow... at test time the tree
    // structures might have something that we never saw at training
    // time.  for example, we could put a threshold on all of the
    // rules at training time and anything that doesn't meet that
    // threshold goes into the unk.  perhaps we could also use some
    // component of the accepted training rules to build up the "unk"
    // parameter in case there are no rules that don't meet the
    // threshold
    if (runTraining) {
        

        // read in the trees
        List<Tree> trainingTrees = Utils.readTreesWithGoldLabels(trainPath);
        
        if (runGradientCheck) {
            runGradientCheck(model, trainingTrees);
          }

        System.err.println("Read in " + trainingTrees.size() + " training trees");
        if (filterUnknown) {
          trainingTrees = Utils.filterUnknownRoots(trainingTrees);
          System.err.println("Filtered training trees: " + trainingTrees.size());
        }

        op.numClasses=MotifRNNCoreAnnotations.getGoldClass(trainingTrees.get(0)).numRows();
        System.err.println("Sentiment model options:\n" + op);
        if(Utils.RNNdoubleTest&&devTrees!=null)
        {
        	splitTest=((double)devTrees.size()/trainingTrees.size());
        	Collections.shuffle(devTrees,new Random(op.randomSeed));
        }
        if(splitTest>0&&splitTest<1)
        {
        	Collections.shuffle(trainingTrees,new Random(op.randomSeed));
        	if(devTrees!=null)
        		devTrees.addAll(trainingTrees.subList(0, (int) (splitTest*trainingTrees.size())));
        	else
        		devTrees=new ArrayList<Tree>( trainingTrees.subList(0, (int) (splitTest*trainingTrees.size())) );
        	trainingTrees=new ArrayList<Tree>( trainingTrees.subList( (int) (splitTest*trainingTrees.size()),trainingTrees.size()) );
        	System.err.println("combining devTree:"+devTrees.size());
        }
        
    	model= new MotifSentimentModel(op, trainingTrees);
    	
    	// Spark configuration and broadcast training tree
		SparkConf conf = new SparkConf().setAppName("MotifSentimentTraining");
		JavaSparkContext sc = new JavaSparkContext(conf);
		Broadcast<List<Tree>> broadcastTrainingTrees = sc.broadcast(trainingTrees);
		System.gc();
		
    	if(numthreads>=1)
    	{	model.op.trainOptions.batchSize=trainingTrees.size()/numthreads/2;
    		if(model.op.trainOptions.batchSize>10000)
    			model.op.trainOptions.batchSize=10000;
    		model=train_multiThread(model, trainPath+".model"+ op.randomSeed, sc, broadcastTrainingTrees, devTrees, numthreads, batchIteration); //make sure final return bestmodel
    	} //always use multi-thread version
//    	else
//    		train(model, trainPath+".model"+ op.randomSeed, trainingTrees, devTrees);
        model.saveSerialized(trainPath+".model"+ op.randomSeed+".gz");
        
        
        //output feature information
    	try {
			PrintWriter pwriter=new PrintWriter(new File(trainPath+".model"+op.randomSeed+".feature"));
			pwriter.println("FeatureName Importance Dim1 Dim2 Dim3 Dim4 Dim5");
			 Map<String, Float> word_imp = model.GetAllWordsImportance();
			//PCA reduce to 5D
			 SimpleMatrix WordMat=new SimpleMatrix(word_imp.size(), op.numHid);
			 int i =-1;
			 for (Entry<String, Float> feat : word_imp.entrySet()) {
				 SimpleMatrix vec = model.wordVectors.get(feat.getKey());
				 i+=1;
				 for (int j = 0; j < vec.getNumElements(); j++) {
					 WordMat.set(i,j, vec.get(j)); 
				}
			 }
			 SimpleMatrix PCs = WordMat.svd().getU();
			  i =-1;
			 for (Entry<String, Float> feat : word_imp.entrySet()) {
				 i+=1;
				 pwriter.println(feat.getKey()+" "+feat.getValue()+" "+PCs.get(i, 0)+
						 " "+PCs.get(i, 1)+" "+PCs.get(i, 2)+" "+PCs.get(i, 3)+" "+PCs.get(i, 4)+
						 " "+Utils.Vector2String(model.SingleWordPrediction(feat.getKey())));
			 }
			 pwriter.close();
			
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
        

      }
    else if(modelPath!=null)
    {
    	model=MotifSentimentModel.loadSerialized(modelPath);
    	if (devTrees != null&&devTrees.size()>10) {
            MotifEvaluate eval = new MotifEvaluate(model);
            eval.eval(devTrees);
            eval.printSummary();
          }
    	
    	else
    	{
            //output feature information
        	try {
    			PrintWriter pwriter=new PrintWriter(new File(modelPath+".model"+op.randomSeed+".feature"));
    			String header="FeatureName Importance";
    			for (int i = 0; i < model.op.numHid; i++) {
    				header+=" PC"+(i+1);
				}
    			pwriter.println(header);
    			 Map<String, Float> word_imp = model.GetAllWordsImportance();
    			//PCA reduce to 5D
    			 SimpleMatrix WordMat=new SimpleMatrix(word_imp.size(), model.op.numHid);
    			 int i =-1;
    			 for (Entry<String, Float> feat : word_imp.entrySet()) {
    				 SimpleMatrix vec = model.wordVectors.get(feat.getKey());
    				 i+=1;
    				 for (int j = 0; j < vec.getNumElements(); j++) {
    					 WordMat.set(i,j, vec.get(j)); 
    				}
    			 }
    			 SimpleMatrix PCs = WordMat.svd().getU();
    			  i =-1;
    			 for (Entry<String, Float> feat : word_imp.entrySet()) {
    				 i+=1;
    				 String outstr=feat.getKey()+" "+feat.getValue();
    				 for (int j = 0; j < model.op.numHid; j++) {
    					 outstr+=" "+PCs.get(i, j);
    					}
    				 outstr+= " "+Utils.Vector2String(model.SingleWordPrediction(feat.getKey()));
    				 pwriter.println(outstr);
    			 }
    			 pwriter.close();
    			
    		} catch (FileNotFoundException e) {
    			// TODO Auto-generated catch block
    			e.printStackTrace();
    		}
    	}
    	

    	
    }
    else
    {
    	System.err.println("pls provide training data or trained model file");
    }
    
    if(runPredicting && devTrees != null)
    {
    	
    	System.err.println("output number of predictions:"+devTrees.size());

//        System.exit(0);
    	 model.GetAllWordsImportance();
        File file = new File (devPath+".predict");
        PrintWriter printWriter;
		try {
			printWriter = new PrintWriter (file);
			
	    	for (Tree tree : devTrees) {
			    Predict_SetLabel(model, tree);
				printWriter.println(tree);
			}
	        printWriter.close();  
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

    }

  }
}
