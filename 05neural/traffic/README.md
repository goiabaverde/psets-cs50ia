# 1st Try
On my first try, I used a CNN with one convolutional layer featuring 32 3x3 filters and a ReLU activation function. After the convolutional process, I applied 2x2 pooling. Furthermore, the hidden layer has 50 neurons with a ReLU activation function and dropout algorith that exclude 50% of the neurons randomically. Finally, the output layer has 43 neurons, equal to the number of categories, and uses a softmax activation function. The results were: accuracy: 0.9147 - loss: 0.3775 - recall: 0.8140.

# 2nd Try
On this try, I increased the complexity of the model by adding two convolution and pooling processes in a row. I also increased the number of neurons from 50 to 120. The model showed better performance, but more changes were necessary to improve it further. The results were: accuracy: 0.9094 - loss: 0.3532 - recall: 0.8531.

# 3rd Try
The modification I made was changing the hidden layers' activation function to ReLU, but the results got worse. Therefore, using ReLU as the activation function here is not a good idea. The results were: accuracy: 0.8934 - loss: 0.3835 - recall: 0.8168.

# 4th Try
I added one more hidden layer to the neural network with 80 neurons, maintaining the ReLU activation function, and the results got just a bit better. The results were: accuracy: 0.8984 - loss: 0.3541 - recall: 0.8633.

# 5th Try
 For this model, I took the approach of starting with flexible activation functions and then transitioning to more rigid ones. Now, the model is composed of 2 convolution and pooling processes: the first with 16 5x5 filters and the second with 20 5x5 filters, both using 2x2 pooling and a ReLU function. The hidden layers are two dense layers with a sigmoid activation function. Finally, the output is a layer with the number of neurons equal to the number of categories, using softmax as the activation function. The results were: accuracy: 0.9728 - loss: 0.1175 - recall: 0.9649.