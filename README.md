# Mini-project IV

### [Assignment](assignment.md)

This project was completed by:
- Sébastien Garneau - GitHub: [538455](https://github.com/538455)


## Project/Goals
The goal of this project is to automate the loan eligibility process based on provided customer details.

The project also aimed at practicing the following skills:
1. Data Preparation
2. Feature Engineering
3. Supervised Learning
4. Pipelines
5. Model Persistance
6. Flask - building an API
7. Deployment to Cloud (AWS)

## Hypothesis
When I started this project I had some initial assumptions on which applicants would be more likely to get a loan. 

I though the most important factors would be:
1. The income of the applicant; and
2. The amount of the loan in relation to the income. 

I also thought credit history could be a deciding factor for when applicants were asking for a significant loan.

Spoiler alert: I was wrong!

## EDA 

It should be noted that before starting EDA, I did some basic data cleaning, detailed below.

The first thing I did is look at the shape of the data. I had 614 rows and 13 columns. Of those 614 rows, only 134 were declined. So, in addition to being a very small sample, the data is highly imbalanced as well.

I then looked at the correlation between the different variables. I was surprised to see that the most important factor was the credit history. I also found that the loan amount and applicant income was not as important as I thought it would be:

![image](/images/Correlations.png)

As well, 21% of the data has missing values, meaning 21% of the applicants didn’t provide their gender and/or the number of dependants they have, or if they were self-employed, etc. This is significant and is likely affecting the accuracy of the model. 

Some applicants also had an income significantly higher than the average of the other applicants. 
![image](/images/ApplicantIncome.png)

In the graphic above, you have the distribution of the Income of the Applicants in a box plot. Given the average income, I assumed this value was monthly, but it’s possible that some of those high outliers were formatting issues and were yearly income instead of monthly. 

However, it is also possible those values are monthly income, as some people do make close to a million dollar a year. Consequently, I decided to go with this assumption and keep those values as is in the dataset,

## Process
In addition to hypothesis generation and EDA, my process was broken down into 5 steps:

### Step 1: Data Cleaning

In order to make Data Cleaning easier, I created a function that presents me with the data to help me look for formmating issues, error in datatypes, missing values, duplicates, and outliers. 

This function, along with some others, are stored in a python file called Woodpecker.py, available in the src folder.

In terms of data cleaning, I initially did the following:
- Impute missing values by either 0 or the most frequent value, depending on the column; and
- Label encode the categorical variables as well as the target variable;

I did identify some outliers in the Applicant Income and Loan Amount columns, but I decided to keep them as is, as I mentioned above.

### Step 2: Feature Engineering
In terms of feature engineering, I created a feature called Total Income, which is the sum of the applicant and co-applicant income.

I've also decided to impute the missing values in the categorical variables by creating a new category called "UNK". This is because I wanted to keep the information that the applicant didn't provide that information, as it could be a factor in the decision to approve or decline the loan.

Finally, I log transformed the Loan Amount and Total Income columns, as they were highly skewed.

### Step 3: Model Selection
I tested a combination of 16x different models and 4x scalers using GridSearchCV and the best performer was the Support Vector Classifier w/ MinMaxScaler with an accuracy score ranging from 75-85% depending on the randomness when splitting the training/testing data.

I've also tried fine tuning the parameters of the model using using GridSearchCV, but it didn't improve the accuracy score.

### Step 4: Model Pipeline
I then combined the model and data preparation into a pipeline, detailed below:
![image](/images/Pipeline.png)

### Step 5: Deployment
For the deployment I used a simple web application called Flask which I uploaded to an EC2 Instance on AWS along with the model. 

With that done you can do an HTTP POST request to the instance following the format you see below and it will run the model and let you know if your loan is likely to be approved.

![image](/images/Postman_AWSTest.png)

Of note, this example is a sample from the provided data set and his loan was rejected, which let’s you know that even if the model has up to 85% accuracy, it’s probably just very good at predicting those that would get a loan rather than those who wouldn’t. 

Actually, in other requests,  I've increased the loan amount by up to a 1000% and the model would still return that the loan would get approved... so there is definitely more training to be done.

## Results/Demo
The model is still live!

You can test it by doing a POST request to the following URL: [ec2-18-216-41-233.us-east-2.compute.amazonaws.com:5000/prediction](ec2-18-216-41-233.us-east-2.compute.amazonaws.com:5000/prediction)

And include in your body the following json data:
```json
{
"Loan_ID": "LP001097",
"Gender": "Male",
"Married": "No",
"Dependents": 1,
"Education": "Graduate",
"Self_Employed": "Yes",
"ApplicantIncome": 4692,
"CoapplicantIncome": 0.0,
"LoanAmount": 106.0,
"Loan_Amount_Term": 360.0,
"Credit_History": 1.0,
"Property_Area": "Rural"
}
```

## Challenges 
The flask deployment was a bit of a challenge, as I had to learn how to use it and how to deploy it to AWS. However, I was able to find a lot of resources online to help me with that and I feel like I learned a lot in the process.

I've also had some challenges with the pipeline, as I had to figure out how to use the ColumnTransformer and the Pipeline together. I've also tried to use the Column Transformer to create the Total Income feature, but I couldn't get it to work so I've added it manually with the Flask app.


## Future Goals
So first, I would like to deploy a front end using HTML so users can input their values like you can see below:

![image](/images/HTML_FrontEnd.png)

And finally, I know every body says ‘more data’ all the time, but in this case, we really need more to increase the accuracy of this model. 


