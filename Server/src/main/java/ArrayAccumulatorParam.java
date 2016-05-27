import org.apache.spark.AccumulatorParam;

public class ArrayAccumulatorParam implements AccumulatorParam<double[]>{

	@Override
	public double[] addInPlace(double[] arg0, double[] arg1) {
		return Utils.sumArray(arg0, arg1);
	}

	@Override
	public double[] zero(double[] theta) {
		return new double[theta.length];
	}

	@Override
	public double[] addAccumulator(double[] arg0, double[] arg1) {
		return Utils.sumArray(arg0, arg1);
	}
	

}
