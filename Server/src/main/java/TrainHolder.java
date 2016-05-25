import java.io.Serializable;
import java.util.List;

import edu.stanford.nlp.trees.Tree;

public class TrainHolder  implements Serializable {
	public MotifSentimentModel model;
//	public List<Tree> trainingTrees;
	public double[] sumGradSquare;
	public List<Integer> shuffledIndices;
	
	public TrainHolder(MotifSentimentModel model, double[] sumGradSquare, List<Integer> shuffledIndices){
		this.model = model;
//		this.trainingTrees = trainingTree;
		this.sumGradSquare = sumGradSquare;
		this.shuffledIndices = shuffledIndices;
	}

	private static final long serialVersionUID = 7;
}
