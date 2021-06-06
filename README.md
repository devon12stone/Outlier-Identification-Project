# Outliers Identification Project

This repository holds the code of a Plotly Dash application that allows users to view and download the outliers in a provided pricing dataset. The application allows users to dynamically set the main hyper-parameter of the model used to detect the outliers in the dataset. The underlying algorithm used in the outlier identification model is the unsupervised isolation forest algorithm. 

## Structure of Repository

 - Outliers Project
    - data
      - input
        - Outliers.csv  
    - src
      - database.py
      - outlier_model.py
    - venv
    - info.log
    - main.py
    - OutlierDB

### data

The `data` directory simply holds the provided dataset. The `final output` of the model is provided via the application's interface. 

### src

The `src` directory holds two python scripts. The `database.py` script contains a class with two inherent functions. The first function, `create_database`, is used to create an SQLite database, that is used to store the provided dataset. SQLite is used to mimic a real database if the application was to be put into production. The second function `create_connection` is used to establish a connection the database created by the `create_database` function, `OutlierDB.db`. The `create_database` function performs some light `data cleaning` processes such as ensuring data types and `extracting` a weekday column from the dates in the provided dataset. 

The second script in `src` - `outlier_model.py` - contains a class that trains the outlier detector model and returns a finalized dataset where outliers are highlighted. The class has been developed so that more algorithms can be easily added if the application were to be further developed. 

### venv

Is a virtual environment containing all the required packages to run the application. 

### info.log

Python's logging module was used throughout the application (in the `main.py`, `database.py`, and `outlier_model.py` scripts). This is done so that users can see when their model has been trained successfully or they can identify why their model failed. The logger will be useful to users that would like to further develop the application. The `info.log` file contains the outputs of the logging module. 

### main.py

The is the python file that is used to run the application. The file makes use of the classes and functions from the `database.py`, and `outlier_model.py` scripts to connect to the `OutlierDB.db` database and train the isolation forest model. To read more about isolation forests follow this [link](https://towardsdatascience.com/time-series-of-price-anomaly-detection-13586cd5ff46). 

#### Data Cleaning, Differencing, and Data Sorting

Some basic data cleaning - ensure data types and removing null values - is performed in the `main.py` file. More importantly, the data in the provided dataset is differenced in the `main.py` file. The is done as the data provided is not stationary. To read more on non-stationary data and how to correct please follow this [link](https://www.analyticsvidhya.com/blog/2018/09/non-stationary-time-series-python/). 

To ensure that the isolation forest algorithm only used historical points when determining if a point was an outlier the data was sorted by date before being passed to the model. 

#### Dash Application and Callback Function

The Dash application interface is created and run from the `main.py` file. Dash is a python or R web application framework that is powered by Plotly. You can read more about it [here](https://dash.plotly.com/). The `retrain_model` callback function at the bottom of the `main.py` file allows users to set the contamination parameter of the isolation forest and the function automatically updates the output figure and table.

## Running the Application

The application can be run from the command line or in any IDE. Simply activate the virtual enviroment and run the `main.py` file. All file paths have been set relatively so this is possible. 

## Output

All figures shown in the application are downloadable - this is done by hovering over the figure and selecting the camera icon that appears in the top right of the figure. 

The final dataset indicating if a price point is an outlier can be downloaded from the final data table by selecting the `export` button in the top left of the table. 

## Application Output

![alt text](https://github.com/devon12stone/Outlier-Identification-Project/blob/main/data/images/image1.png)
![alt text](https://github.com/devon12stone/Outlier-Identification-Project/blob/main/data/images/image2.png)
![alt text](https://github.com/devon12stone/Outlier-Identification-Project/blob/main/data/images/image3.png)




