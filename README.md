# ChatBot
A chatbot application developed using the python library TFLearn which uses Tensorflow.

Steps to run.

1.Add the data in the JSON file.
A sample Data.json file is provided to understand how to construct the json file. 
If the data is in pdf or some other format, create a file called converter.py which will convert other
file formats to json format. for example, PDFMINER library can be used to read pdf files.

2. After the JSON is constructed, run TrainModel.py.
This will save the trained models of json file given to it.

3. Either you can run the ChatBotUi-UsingQT.py file or PredictModel.py 

3.a. Run ChatBotUi-UsingQT, this is the sample UI developed using PyQT library. this will internally run PredictModel.py 

3.b. Run PredictModel.py, command line input can be given here for testing purpose.
