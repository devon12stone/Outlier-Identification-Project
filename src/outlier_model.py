from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
import logging

# initialise logger for this script
logger = logging.getLogger()

class OutlierModel:
    # class to train and return an outlier model
    # input: pandas dataframe and contamination fraction
    def __init__(self, data, contamination):
        self.data = data
        self.contamination = contamination

    def train_model(self):
        # output: pandas dataframe of predictions
        try:
            # scale price
            price_data = self.data
            model_data = price_data[['Price Difference']]
            scaler = StandardScaler()
            np_scaled = scaler.fit_transform(model_data)
            model_data = pd.DataFrame(np_scaled)

            # set first value to 0 rather than nan
            model_data = model_data.fillna(0)

            # train isolation forest
            model = IsolationForest(contamination=self.contamination)
            model.fit(model_data)

            # add predictions to data frame
            price_data['Outlier'] = pd.Series(model.predict(model_data))
            price_data['Outlier'] = np.where(price_data['Outlier']==-1, 'Outlier', 'Usual')

            # log success
            logger.info("Outlier model trained successfully with a contamination factor of {0}.".format(self.contamination))

            return price_data

        except Exception as e:
            # log error
            logger.error("The following error has occurred when training the outlier model: {0}.".format(e))



