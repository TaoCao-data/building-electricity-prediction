# Building Electricity Load Prediction Tool

This repo is a demo version of an electricity load prediction tool. The interactive demo website can be accessed 
[here](https://energy-load-prediction.herokuapp.com/).

The underlying model for the prediction tool is a time series model, built with LSTM on Tensorflow Keras. 
Similarity learning based on [Gower Distance](https://github.com/wwwjk366/gower) enables the model to work with
time series with or without historic records, a major challenge for benchmark models. The tool has exhibited 10-50%
prediction error reductions over the benchmark models. Notebook examples on using the model are located under
```notebook``` folder.
