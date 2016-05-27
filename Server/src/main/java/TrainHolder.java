import java.io.Serializable;
import java.util.List;

import org.apache.spark.Accumulable;
import org.apache.spark.Accumulator;

import edu.stanford.nlp.trees.Tree;

public class TrainHolder  implements Serializable {
	public Accumulable<MotifSentimentModel, double[]> accumulatorModel;
//	public List<Tree> trainingTrees;
	public Accumulator<double[]>  accumulatorSumGradSquare;
	public List<Integer> trainingIndices;
	
	public TrainHolder(Accumulable<MotifSentimentModel, double[]> accumulatorModel, Accumulator<double[]> accumulatorSumGradSquare, List<Integer> trainingIndices){
		this.accumulatorModel = accumulatorModel;
//		this.trainingTrees = trainingTree;
		this.accumulatorSumGradSquare = accumulatorSumGradSquare;
		this.trainingIndices = trainingIndices;
	}

	private static final long serialVersionUID = 7;
}
