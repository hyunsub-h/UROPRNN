import org.apache.spark.AccumulableParam;

public class MotifSentimentModelAccumulatorParam implements AccumulableParam<MotifSentimentModel, double[]>{

	@Override
	public MotifSentimentModel addAccumulator(MotifSentimentModel model, double[] thetaChange) {
		double[] theta = model.paramsToVector();
		theta = Utils.sumArray(theta, thetaChange);
		model.vectorToParams(theta);
		return model;
	}

	@Override
	public MotifSentimentModel addInPlace(MotifSentimentModel arg0, MotifSentimentModel arg1) {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public MotifSentimentModel zero(MotifSentimentModel arg0) {
		// TODO Auto-generated method stub
		return null;
	}

}
