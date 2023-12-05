# PriceRecomendation-
Marcari is an online shopping marketplace which is powered by one of the biggest communities in Japan where users can sell pretty much anything.
The community wants to offer price suggestions to the sellers but is a tough task as the sellers are enabled to put just about anything, or any bundle of things, on Mercani’s marketplace.
This website helps authenticated sellers to predict the perfect price for their products.


The website was built using the python-Django framework- for the backend and html,css for the frontend,
while [Mercari dataset](https://www.kaggle.com/competitions/mercari-price-suggestion-challenge/data) was used for training and testing the price recommendation model.

![photo_2023-12-05_21-18-32](https://github.com/Alaqrakhadija/PriceRecomendation-/assets/102253516/14896f0e-291b-4b61-bddb-80aa2519b208)
![photo_2023-12-05_21-18-41](https://github.com/Alaqrakhadija/PriceRecomendation-/assets/102253516/f229dcc1-6e80-41f9-b9d2-88840fb714f4)
![photo_2023-12-05_21-18-49](https://github.com/Alaqrakhadija/PriceRecomendation-/assets/102253516/2ad166dd-5a3b-452a-ba47-b45ce5fdb78b)

### Technical Accuracy measure
Root Mean Squared Error (RMSE):
1. RMSE is a valuable metric for assessing the accuracy of regression models, providing insight into how well the model's predictions match the observed data and the magnitude of errors.
2. Useful especially when you want to understand how far, on average, your predictions are from the actual data points.
3. RMSE gives more weight to larger errors due to the squaring operation. Therefore, it is sensitive to outliers in the data. If your dataset contains outliers,RMSE can be affected and may not accurately represent the overall model performance.
   
![photo_2023-12-05_21-18-55](https://github.com/Alaqrakhadija/PriceRecomendation-/assets/102253516/c2e150ad-dec7-43e0-9162-98aef2b580a3)

### Future steps:
1. Perform some more features engineering techniques.
2. Try more complex models with Tfidf features.
3. Try Deep Learning models.
