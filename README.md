# Udacity Data Scientist Nanodegree - Project 2

This project is completed as part of the curriculum for the Udacity Data Scientist Nanodegree Program. In this project I create an ETL and Machine Learning pipeline and generate my results via a Web app. The application is a classifier for messages received in a possible disaster scenario to enable emergency responders to act on messages received as quickly and effectively as possible under resource contrainted situations.

## Libraries used
 * re
 * numpy
 * pandas
 * pickle
 * nltk
 * sklearn
 * sqlalchemy

## Files used
 * messages.csv - file containing full text of message sent in a possible disaster scenario. The message will form the X variable (input/independent/predictor variable)
 * categories - file containing the assigned categories for each of the messages in the messages.csv file. The categories file includes labels for how a message was tagged against one of 36 categories that may be relevant in  an emergy scenario e.g. 'fire', 'earthquake', 'storm', 'shelter', 'search and rescue' etc.

## ETL Pipeline
The data was extracted from csv files that were already preprocessed by Figure Eight Inc. and made available by Udacity. Although the files had undergone some cleaning and formatting beforehand, a few steps still needed to be performed to get the data ready for machine learning modelling. 
 ### categories.csv
 The relevant data in this file was a single column containing all the 36 labelled with a binary indicator for whether category was applicable or not to the message. The data was in a single string that required splitting, generation of an appropriate column header and extraction of the 0 or 1 character that indicated if the category was relevant or not. Through some exploratory data analysis is was noted that the file contained some duplicate rows which were dealt with in a later stage of the ETL process.
 ### messages.csv
 This file also contained duplicated rows and a column 'original' which contained a significant number of missing values. As this columns was not expected to be used for feature extraction it was determined to not bother with imputation or dropping missing rows.
 
 ### merging datasets and storing
 The two files were merged after conducting the steps outlined above. This was a simple merge using a common 'id' field. After merging the duplicate rows were drops and the final merged dataset was stored in a sqlite database for use in the maching learning pipeline which follows next.


## Machine Learning Pipeline


## Acknowledgements
Special thanks to Figure Eight Inc. and Udacity for provided the labelled datasets described in the "Files Used" section above which truncated the cleaning and preparation significantly.

## Contribution
The project will first be submitted for grading as part of a core data science nanodegree on Udacity. After this project has been graded and I have met the course requirements I will update this section to welcome any contributions. Until that time please reserve any contributions but they will definitely be welcome afterwards.





