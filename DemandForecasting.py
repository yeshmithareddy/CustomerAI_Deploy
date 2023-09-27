import streamlit as st
import numpy as np
import pandas as pd
import plotly_express as px
import plotly.graph_objects as go
import altair as alt


def Demand():

    from PandasDF import pd_df_dmd
    RESULT=pd_df_dmd
    # Sort the DataFrame by the "STOCK_CODE" and "WEEK" columns
    RESULT = RESULT.sort_values(by=["STOCK_CODE", "WEEK"], ascending=[True, False])
    # Keep only the most recent week rows for each unique "STOCK_CODE"
    RESULT = RESULT.drop_duplicates(subset="STOCK_CODE")

    
    prods = st.container()
    upper_panel = st.container()

    
    with upper_panel:
        DF=RESULT
        DF['WEEK'] = pd.to_datetime(DF['WEEK'])
        DF['WEEK'] = DF['WEEK'].dt.strftime('%m/%d/%Y')
        col_DEPA, col_CATE, col3 = st.columns([1,1,4])
        department = np.sort(RESULT['DEPARTMENT'].unique()).tolist()
        dep_selection1 = col_DEPA.selectbox('Department', department,index=0)
        DF = RESULT.loc[RESULT["DEPARTMENT"]==dep_selection1]  

        category = np.sort(DF['CATEGORY'].unique()).tolist()
        category_selection = col_CATE.selectbox('Category', category,index=0)
        

        
    
        final_df=DF.loc[DF["CATEGORY"].isin(category)]
        final_df=DF.loc[DF["CATEGORY"]==category_selection]
        
        result = final_df[["STOCK_CODE","DEPARTMENT","CATEGORY","STOCK_NAME","UNITS_SOLD_WEEK-1","UNITS_SOLD_WEEK-2","UNITS_SOLD_WEEK-3","UNITS_SOLD_WEEK-4","UNITS_SOLD_WEEK-5","UNITS_SOLD_WEEK-6","NEXT_WEEK_PREDICTION"]]
        fig = go.Figure(data=[go.Table(columnwidth=[1.2,2,2,2.4,2,2,2,2,2,2,2],header=dict(values=("<b>STOCK CODE<b>","<b>DEPARTMENT<b>","<b>CATEGORY<b>","<b>STOCK NAME<b>","<b>UNITS SOLD WEEK - 1<b>","<b>UNITS SOLD WEEK - 2<b>","<b>UNITS SOLD WEEK - 3<b>","<b>UNITS SOLD WEEK - 4<b>","<b>UNITS SOLD WEEK - 5<b>","<b>UNITS SOLD WEEK - 6<b>","<b>NEXT WEEK PREDICTION<b>"), fill_color='#00568D', font_color="#ffffff", align=['center'], line_color='#ffffff', font_size = 13,height=35),cells=dict(values=[result['STOCK_CODE'],result['DEPARTMENT'],result['CATEGORY'],result['STOCK_NAME'],result['UNITS_SOLD_WEEK-1'],result['UNITS_SOLD_WEEK-2'],result['UNITS_SOLD_WEEK-3'],result['UNITS_SOLD_WEEK-4'],result['UNITS_SOLD_WEEK-5'],result['UNITS_SOLD_WEEK-6'],result['NEXT_WEEK_PREDICTION']],fill_color = [['white','lightgrey']*3200], align=['left'], font_size = 12))])
        
        fig.update_layout(autosize=False,width=998,height=350,margin=dict(l=0,r=0,b=0,t=0,pad=4), paper_bgcolor="#ffffff"
                )
        
        st.markdown('<h1 style="color: #00568D; font-size: 28px;">Demand Prediction Insights</h1>', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)
        col1, col2= st.columns([2.1,1.1])
        with col1:
                
            # Forecasting the Next Week Prediction
            st.markdown('<h1 style="color: #00568D; font-size: 28px;">Next Week Sales Forecast</h1>', unsafe_allow_html=True)
            frdf=DF[["CATEGORY","NEXT_WEEK_PREDICTION"]]
            frdf = pd.DataFrame(frdf.groupby(frdf["CATEGORY"])["NEXT_WEEK_PREDICTION"].sum()).reset_index()
            frdf.rename(columns={'NEXT_WEEK_PREDICTION': 'UNITS SOLD'}, inplace=True)

            # Creating Bar chart to show Next Week Prediction
            fig = px.bar(frdf, x = "CATEGORY", y = "UNITS SOLD",
                            template = "seaborn")
            st.plotly_chart(fig,use_container_width=True, height = 200)


        with col2:
                # Creating Seasonal Analysis on Historical data
                final_df['WEEK'] = pd.to_datetime(final_df['WEEK'])
                final_df["MONTH_YEAR"] = final_df["WEEK"].dt.month
                def condition(x):
                    if x in [12,1,2]:
                        return 'Winter'
                    elif x in [3,4,5]:
                        return 'Spring'
                    elif x in [6,7,8]:
                        return 'Summer'
                    elif x in [9,10,11]:
                        return 'Fall'

                final_df['SEASON'] = final_df["MONTH_YEAR"].apply(condition)
                sndf = pd.DataFrame(final_df.groupby(final_df["SEASON"])["UNITS_SOLD"].sum()).reset_index()
                st.markdown('<h1 style="color: #00568D; font-size: 28px;">Seasonal Analysis</h1>', unsafe_allow_html=True)

                # Creating Bar chart to show Seasonal Analysis
                fig2 = px.bar(sndf, x = "SEASON", y="UNITS_SOLD", labels = {"UNITS_SOLD": "UNITS SOLD"},height=450, width = 500,template="gridon")
                st.plotly_chart(fig2)

        
        final_df['WEEK'] = final_df['WEEK'].dt.strftime('%m/%d/%Y')
        # Create a line chart for historical data
        final_df.rename(columns={'UNITS_SOLD': 'UNITS SOLD'}, inplace=True)
        chart = alt.Chart(final_df).mark_line().encode(
                    x=alt.X('WEEK:O', title='WEEK', sort='-x', axis=alt.Axis( titleFontWeight='normal')),
                    y=alt.Y('UNITS SOLD:Q',title='UNTS SOLD', axis=alt.Axis( titleFontWeight='normal')),
                    tooltip=['WEEK','UNITS SOLD']
                ).properties(
                    width=1000,
                    height=480,
                    #title='Unit Sold vs. Week'
                )
        st.markdown(f'<h1 style="color: #00568D; font-size: 28px;">Current Sales for Category: {category_selection}</h1>', unsafe_allow_html=True)
        st.altair_chart(chart, use_container_width=True) 
        return 0
