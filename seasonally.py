import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose


class SeasonallyInput:


    def dataframe_reading(self, path):

        df = pd.read_excel(path, engine='openpyxl', index_col='data')

        return df
    
    def seasonal_function(self, raw_dataframe, column_name):

        results = seasonal_decompose(
            raw_dataframe[column_name], 
            model='mul', 
            period=12, 
            extrapolate_trend=True
        )

        return results
    

    def pipeline_run(self, column_name, dataframe):

        # 1. DF Reading
        df = self.dataframe_reading(path=dataframe)

        # 2. Function Apple:
        results = self.seasonal_function(raw_dataframe=df, column_name=column_name)

        return results, df


# df['trend'] = result.trend
# df['seasonal'] = result.seasonal
# df['resid'] = result.resid

# df[['factor', 'seasonal']].plot(figsize=(12,6));