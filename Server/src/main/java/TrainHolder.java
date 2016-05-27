import java.io.Serializable;
import java.util.List;

public class TrainHolder  implements Serializable {
	public MotifSentimentModel model;
//	public List<Tree> trainingTrees;
	public double[]  sumGradSquare;
	public List<Integer> trainingIndices;
	public int batchIteration;
	public TrainHolder(MotifSentimentModel model, double[] sumGradSquare, List<Integer> trainingIndices, int batchIteration){
		this.model = model;
//		this.trainingTrees = trainingTree;
		this.sumGradSquare = sumGradSquare;
		this.trainingIndices = trainingIndices;
		this.batchIteration = batchIteration;
	}

	private static final long serialVersionUID = 7;
}
