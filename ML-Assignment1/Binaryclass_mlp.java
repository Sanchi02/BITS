
// 2019H1030519P, 2019H1030520P, 2019H1030521P

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.logging.Level;
import java.util.logging.Logger;
import java.util.Random;

public class Main {   
    public static void main(String[] args) throws IOException {
        int layer[] = {8,1};
        MultiLayerPerceptron mlp = new MultiLayerPerceptron(4, layer);
              
        double x_train[][] = new double[1000][4];
        double y_train[][]= new double[1000][1];
        double x_test[][] = new double[372][4];
        double y_test[][]= new double[372][1];
        int k=0;
        try {
          
            //Read csv and split into train and test set

            FileReader dataset = new FileReader("C:\\Users\\yashita goswami\\Downloads\\rBNAData.csv");
            BufferedReader data = new BufferedReader(dataset);
            for(int i = 0; i < 1372; i++)
            {
                String line[] = data.readLine().split(",");                       
                if (i < 1000)
                {
                     for(int j = 0; j < 5; j++)
                     {
                            if(j<4)
                            {
                               x_train[i][j] = Double.valueOf(line[j]);
                            }
                            else
                            {
                                y_train[i][0] = Double.valueOf(line[j]);                                                             
                            }                        
                     }
                }
                else 
                {
                   for(int j = 0; j < 5; j++)
                   {
                        if(j<4)
                        {
                            x_test[k][j] = Double.valueOf(line[j]);
                        }
                        else
                        {
                         y_test[k][0] = Double.valueOf(line[j]);                                  
                        }                                                             
                   }
                   k++;
                }                                   
            }
             
        } catch (FileNotFoundException ex) {
            Logger.getLogger(Main.class.getName()).log(Level.SEVERE, null, ex);
        }             
        mlp.algo(x_train,y_train,"batch");
        mlp.accuracy(x_test, y_test);
    }
}
 class Neuron 
{
	 double bias;
     double[] weights;
	 double delta;
     double output;
     double sum;
	 Neuron(int size)     //initialize neurons
	{
		weights = new double[size];
		bias =Math.random()-0.5;
		delta = Math.random();
		sum = Math.random();
        for(int i = 0; i < weights.length; i++)
        {
           weights[i] = Math.random()-0.5;                        
        }
    }
}

 class Layer                
{
	 Neuron[] neurons;
	 int length;
	 Layer(int len, int prev_layer_len)                      //initialize layer
	{
		length = len;
		neurons = new Neuron[len];
		for(int i = 0; i < length; i++)
			neurons[i] = new Neuron(prev_layer_len);
    }
}


class MultiLayerPerceptron {
     double alpha = 0.01;
     Layer layers[];    
     int no_of_inp;    //total no of inputs
     MultiLayerPerceptron(int no_of_inp,int[] size)
	 {
		this.no_of_inp = no_of_inp;
		layers = new Layer[size.length];	
        for(int i = 0; i <layers.length; i++)
        {
            if(i == 0)
                 layers[i] = new Layer(size[i], no_of_inp);
            else
                 layers[i] = new Layer(size[i], size[i-1]);
        }
    }    
    // Activation function
    private double activation_function(String name, double x,double i)
    {
        double value=0;
        switch (name) {
        case "sigmoid":
            value = 1 / (1 + Math.exp(-x));
            break;
        case "softmax":
            value=Math.exp(x)/i;
            break;
        case "relu":
            value = Math.max(0, x);
            break;
        case "tanh":
            value = (1 - Math.exp(-2 * x) )/ (1 + Math.exp(-2 * x));
            break;
        case "linear":
            value = x;
            break;
        }
      return value;
   }
    // derivative function for gradient descent
    private double derivative_function(String name, double x,double i) {
        double value=0;
        switch (name) {
        case "sigmoid":
            value = Math.exp(-x) / Math.pow((1 + Math.exp(-x)),2);
            break;
        case "softmax":
            value=-Math.pow(Math.exp(x),2)/(i*i);
            break;
        case "relu":
            if(x>0) value=1;
            else value=0;
            break;
        case "tanh":
            value = 4 / Math.pow((Math.exp(x)+ Math.exp(-x)),2);
            break;
        case "linear":
            value = 1;
            break;
        
        }

        return value;
    }
    public double[] execute (double in[])
    {
        double output[] = new double[layers[layers.length-1].length];
        double sum,s=0;       
        //Sum(transfer function) of first hidden layer
        s=0;
        for(int i = 0; i < layers[0].length; i++)
        {
            sum = layers[0].neurons[i].bias;
            for(int j = 0; j < no_of_inp; j++)
                sum += layers[0].neurons[i].weights[j] * in[j];
            //layers[0].neurons[i].output = activation_function("s",sum,i);   
            s=s+Math.exp(sum);
            layers[0].neurons[i].sum = sum;
        }
        for(int i = 0; i < layers[0].length; i++)
        {
            layers[0].neurons[i].output = activation_function("relu",layers[0].neurons[i].sum,s);       
        }
         
        //forward propagation
        for(int i = 1; i < layers.length; i++ )
        { 
            s=0;
            for(int j = 0; j < layers[i].length; j++){ 
                sum = layers[i].neurons[j].bias;
                for(int k = 0; k < layers[i - 1].length; k++) 
                    sum += layers[i].neurons[j].weights[k] * layers[i - 1].neurons[k].output;
                //layers[i].neurons[j].output = activation_function("softmax",sum,i);
                s=s+Math.exp(sum);
                layers[i].neurons[j].sum = sum;
            }
            for(int p = 0; p < layers[i].length; p++){
                layers[i].neurons[p].output = activation_function("relu",layers[i].neurons[p].sum,s);   
            }
        }
            
        //final output

        for(int i = 0; i < layers[layers.length-1].length; i++)
        {
            output[i] = Math.round(layers[layers.length - 1].neurons[i].output) ;
            //System.out.println(output[i]);
        }
        return output;
    }
   

    
   //Algorithm
    public void algo(double input[][], double actualOutput[][],String gd)
    {
        double error = 1.0;
        int epoch = 0;
        
        while (error > 0.01 && epoch<1000) {   //&& epoch<2000
            
            error = 0;
            double in[] = new double[input[0].length];
            double actualOut[] = new double[actualOutput.length];
            if(gd=="normal"){
            for (int i = 0; i < input.length; i++) {
                
                for (int j = 0; j < input[0].length; j++) {
                    in[j] = input[i][j];
                }
                //System.out.println("len "+actualOutput.length);
            
                
                for (int j = 0; j < actualOutput[0].length; j++) {
                    actualOut[j] = actualOutput[i][0];
                }
                double out[] = execute(in);
                error += backpropagation(out, actualOut, in);
  
               }
           }
           else if(gd=="stochastic")
           {
                
                Random r = new Random();
                int rand=r.nextInt(999);
                        for (int j = 0; j < input[0].length; j++)
                         {
                            in[j] = input[rand][j];
                         }
                         for (int j = 0; j < actualOutput[0].length; j++) 
                         {
                            actualOut[j] = actualOutput[rand][0];
                         }
                double out[] = execute(in);
                error += backpropagation(out, actualOut, in);       
            }
              
            else 
            {
                 int batch=20;
                 if(((epoch+1)*batch)<input.length) 
                {
                    for (int i = (epoch)*batch; i < (epoch+1)*batch; i++) 
                    {       
                        for (int j = 0; j < input[0].length; j++)
                         {
                            in[j] = input[i][j];
                         }
                        for (int j = 0; j < actualOutput[0].length; j++)
                         {
                            actualOut[j] = actualOutput[i][0];
                         }
                        double out[] = execute(in);
                        error += backpropagation(out, actualOut, in);
                    }
                }

            }
            epoch++;
            System.out.println(epoch+ " " + error);
            }
            
        } 
    private double backpropagation(double out[], double actualOutput[], double input[])
    {
        double error;
        double y,s[];
        int i;
        s=new double[layers.length];
        for(i = 0; i < layers.length; i++ )
        { 
            s[i]=0;
            for(int j = 0; j < layers[i].length; j++)
            { 
                s[i]=s[i]+Math.exp(layers[i].neurons[j].sum);
            }
        }

        //calculate Gradient of last layer

        for( i = 0; i < layers[layers.length-1].length; i++)
        {
            error = actualOutput[i] - out[i];
            y = layers[layers.length - 1].neurons[i].sum;
            layers[layers.length-1].neurons[i].delta = error * derivative_function("relu",y,s[layers.length-1]);
        }
        
        for(i = layers.length - 2; i >= 0; i--)       //back propagate to prev layers
        {     
            for(int j = 0; j < layers[i].length; j++){
                error = 0.0;
                for(int k = 0; k < layers[i + 1].length; k++)
                    error += layers[i + 1].neurons[k].delta * layers[i + 1].neurons[k].weights[j];
                y = layers[i].neurons[j].sum;
                layers[i].neurons[j].delta = derivative_function("relu",y,s[i]) * error;
            }
            
         //update weights

            for(int j = 0; j < layers[i + 1].length; j++) 
            {
                for(int k = 0; k < layers[i].length; k++)
                {
                    layers[i + 1].neurons[j].weights[k] += alpha * layers[i + 1].neurons[j].delta*layers[i].neurons[k].output; 
                }
                layers[i + 1].neurons[j].bias += alpha * layers[i + 1].neurons[j].delta;
            }
        }
        
        
        
        for (int j = 0; j < layers[0].length; j++)
         {
            for (int k = 0; k < no_of_inp; k++)
            {
                layers[0].neurons[j].weights[k] += alpha * layers[0].neurons[j].delta* input[k];
            }
            layers[0].neurons[j].bias += alpha * layers[0].neurons[j].delta;
         }
    
        error = 0.0;
        for( i = 0; i < out.length; i++) 
            error += Math.abs(out[i] - actualOutput[i]);
        error = error / out.length;
        return error;
    }

   // accuracy function

   public void accuracy(double input[][],double actualOutput[][])
   {   double tr_acc=0,fr_acc=0;
       for (int i = 0; i < input.length; i++)
        {
           double in[] = new double[input[0].length];
           for (int j = 0; j < input[0].length; j++) 
           {
               in[j] = input[i][j];
           }
           double actualOut;
           actualOut = actualOutput[i][0];
           double output[] = execute(in);
           if(output[0]==actualOut)
           {  
               tr_acc++;
           }  
           else
           {  
               fr_acc++;
           } 
       }
       double accr;
       accr=(tr_acc/(tr_acc+fr_acc))*100;
       System.out.println("The accuracy is "+accr);  
   }    
}
