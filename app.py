import streamlit as st
import pandas as pd

from seasonally import SeasonallyInput



st.set_page_config(
    page_title="FP&A Seasonally Platform",
    page_icon="💲",
    layout="wide",
    initial_sidebar_state="expanded"
)




st.header('FP&A Seasonally Platform')
st.markdown('Please, attach below the **Actual Excel File** in order to begin...')
st.image("input_model.png", caption='Input Model Example')
input_file = st.file_uploader("Upload your Excel file here...")
button = st.button('Launch!')





if button == True:

    SI = SeasonallyInput()

    df_raw = SI.dataframe_reading(path=input_file)

    # Actuals Table
    df = df_raw[df_raw.index[0]:df_raw.index[-1]].fillna(0)

    trend_df = pd.DataFrame(index=df.index)
    seasonal_df = pd.DataFrame(index=df.index)
    residual_df = pd.DataFrame(index=df.index)


    for name in df.columns:

        iteration_df = df[(df[name] > 0)]

        results = SI.seasonal_function(raw_dataframe=iteration_df, column_name=name)
        results.trend.name = name
        results.seasonal.name = name
        results.resid.name = name

        trend_df = trend_df.merge(results.trend, left_index=True, right_index=True, how='left')
        seasonal_df = seasonal_df.merge(results.seasonal, left_index=True, right_index=True, how='left')
        residual_df = residual_df.merge(results.resid, left_index=True, right_index=True, how='left')


    with pd.ExcelWriter('output.xlsx') as writer:
        df_raw.to_excel(writer, sheet_name='ACTUALS')
        trend_df.to_excel(writer, sheet_name='Trend_Results')
        seasonal_df.to_excel(writer, sheet_name='Seasonal_Results')
        residual_df.to_excel(writer, sheet_name='Residual_Results')


    st.markdown("# Download all results")
    with open("output.xlsx", "rb") as file:
        btn = st.download_button(
            label="Download all results",
            data=file,
            file_name="results.xlsx",
            mime="application/octet-stream"
        )
    
    st.markdown('## Trend Component:')    
    #st.download_button(label='📥 Download Current Result', data=trend_df.to_excel(excel_writer='openpyxl'), file_name= 'TrendDF.xlsx')
    st.dataframe(trend_df)

    st.markdown('## Seasonally Factors Component:')
    #st.download_button(label='📥 Download Current Result', data=seasonal_df.to_excel(excel_writer='openpyxl'), file_name= 'SeasonalDF.xlsx')
    st.dataframe(seasonal_df)

    st.markdown('## Residuals Component:')
    st.markdown('(Actual values without Trend and Seasonal Components)')
    #st.download_button(label='📥 Download Current Result', data=residual_df.to_excel(excel_writer='openpyxl'), file_name= 'ResidualDF.xlsx')
    st.dataframe(residual_df)

   



