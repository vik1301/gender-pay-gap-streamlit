import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import base64


##################################################################
#
#     Helper functions
#
##################################################################

def load_dataset_and_return_dataframe(path, delimiter):
    return pd.read_csv(filepath_or_buffer=path, delimiter=delimiter)

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = f'''
    <style>
    .stApp {{
      background-image: url("data:image/png;base64,{bin_str}");
      background-size: cover;
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

##################################################################
#
#     Main program
#
##################################################################
if __name__ == '__main__':
    # df_gpg = pd.ExcelFile(r"GPG_2023_2024_dataset.xlsx").parse('GPG_2023_2024_dataset_tab')
    # df_gpg = df_gpg.reset_index()  # make sure indexes pair with number of rows
    df_gpg = load_dataset_and_return_dataframe(r"GPG_2023_2024_dataset.txt", "|")
    # print(df.head())

    page_bg_color = '''
    <style>
    .stApp {
      background-color: #ADD8E6; /* Light Blue background color */
    }
    </style>
    '''

    # Apply the custom CSS
    st.markdown(page_bg_color, unsafe_allow_html=True)
    # set_background('background.jpg')

    st.title('2023-2024 UK gender pay gap (GPG) analysis dashboard')

    ###################################################################################################################
    # Let's define the sections for the table of contents
    sections = {
        "Introduction": "#introduction",
        "Dataset": "#dataset",
        "What is streamlit?": "#what-is-streamlit",
        "Python packages used": "#python-packages-used",
        "Dashboards": "#dashboards"
    }

    dashboards_sections = {
        "Data Exploration": "#gpg-boxplot",
        "Companies with mean hourly percent GPG size": "#companies-filter",
        "Distribution of mean hourly percent GPG values depending on company size": "#gpg-distribution",
        "Correlation between percentage of men receiving a bonus and women receiving a bonus": "#gpg-correlation",
        "Distribution of men and women across paying quartiles": "#gpg-quartiles",
    }

    # Let's create a Table of Contents in the sidebar for my app
    st.sidebar.title("Table of Contents")
    for section, anchor in sections.items():
        st.sidebar.markdown(f"[{section}]({anchor})")
    for section, anchor in dashboards_sections.items():
        st.sidebar.markdown(f" - [{section}]({anchor})")

    ###################################################################################################################
    st.markdown('<a id="introduction"></a>', unsafe_allow_html=True)
    st.header('Introduction', divider='rainbow')
    st.subheader('Project description', divider='rainbow')
    st.write('For my graduation project I decided to build gender pay gap analysis dashboard to be able to answer questions like:')
    st.write(' - what are the companies with the largest or smallest gender pay gap in London and in the UK?')
    st.write(' - what is the distribution of gender pay gap values dependeing on a company size?')
    st.write(' - Is there a correlation between percent of men receiving a bonus and women receiving a bonus in London and in the UK?')
    st.write(' - What is the percentage distribution of men and women across paying quartiles in London and in the UK?')


    ###################################################################################################################
    st.markdown('<a id="dataset"></a>', unsafe_allow_html=True)
    st.header('Dataset', divider='rainbow')
    st.write('For the dataset I managed to find 2023-2024 gender pay gap for London and the UK dataset on https://data.london.gov.uk/ website.')
    st.link_button("Gender Pay Gaps in London - London Datastore", "https://data.london.gov.uk/dataset/gender-pay-gaps")
    st.link_button('Methodology description on gov.uk', 'https://www.gov.uk/government/publications/gender-pay-gap-reporting-guidance-for-employers/making-your-calculations')

    st.subheader('Raw data view', divider='rainbow')
    st.write('This is how the raw data looks like when I import it from csv file into dataframe:')
    st.dataframe(df_gpg)


    ###################################################################################################################
    st.markdown('<a id="what-is-streamlit"></a>', unsafe_allow_html=True)
    st.header('What is streamlit?', divider='rainbow')
    st.write('Streamlit is powerful open source package for Python which allows you to create UI reach web applications for data analysis and data science.')
    st.write('Essentially you may use Streamlit to create your own fully customised and highly interactive dashboards and make them available on the web for users to access them.')
    st.write('If you want to try it out here is the link (or ask ChatGPT;))')
    st.link_button("Streamlit • A faster way to build and share data apps", "https://streamlit.io/")

    ###################################################################################################################
    st.markdown('<a id="python-packages-used"></a>', unsafe_allow_html=True)
    st.header('Python packages used', divider='rainbow')
    st.write("In my project I\'ve used the following python packages:")
    st.write(' - streamlit')
    st.write(' - pandas')
    st.write(' - plotly')


    ###################################################################################################################
    st.markdown('<a id="dashboards"></a>', unsafe_allow_html=True)
    st.header('Dashboards', divider='rainbow')

    #==================================================================================================================
    st.markdown('<a id="gpg-boxplot"></a>', unsafe_allow_html=True)
    st.subheader('Data Exploration', divider='rainbow')
    st.write("Let's check what distribution various columns in the dataset have based on a company size")

    # Define the options for the dropdown
    options = ['DiffMeanHourlyPercent', 'DiffMedianHourlyPercent', 'DiffMeanBonusPercent', 'DiffMedianBonusPercent',
        'MaleBonusPercent', 'FemaleBonusPercent', 'MaleLowerQuartile', 'FemaleLowerQuartile', 'MaleLowerMiddleQuartile',
        'FemaleLowerMiddleQuartile', 'MaleUpperMiddleQuartile', 'FemaleUpperMiddleQuartile', 'MaleTopQuartile',
        'FemaleTopQuartile',]

    columnSelector = st.selectbox('Select dataframe column with values:', options)
    isLondonSelector = st.radio("Please select London or the UK", ["London", "UK"], horizontal=True)

    if isLondonSelector == "London":
        filtered_df_gpg_boxplot = df_gpg[(df_gpg['IsLondon'] == 'Yes')]
    else:
        filtered_df_gpg_boxplot = df_gpg[(df_gpg['IsLondon'] == 'No')]

    fig13 = px.box(filtered_df_gpg_boxplot, x='EmployerSize', y=columnSelector, title='Boxplot chart')
    st.plotly_chart(fig13)

    #==================================================================================================================
    st.markdown('<a id="companies-filter"></a>', unsafe_allow_html=True)
    st.subheader('Companies with mean hourly percent GPG size', divider='rainbow')

    st.write('In this dashboard user can select GPG threshold, employment company size and filter the dataset.')
    st.write('For example what companies with 250 to 499 employees in London have GPG more than 30%.')

    # minMeanPercentGpgValue = int(df_gpg['DiffMeanHourlyPercent'].min())
    # maxMeanPercentGpgValue = int(df_gpg['DiffMeanHourlyPercent'].max())
    # meanPecentGpgSelector = st.slider('Select mean hourly percent GPG size', minMeanPercentGpgValue, maxMeanPercentGpgValue, value=0)
    meanPecentGpgSelector = st.slider('Select mean hourly percent GPG size', -100, 100, value=0)
    st.write('You selected:', meanPecentGpgSelector)

    largerOrSmallerSelector = st.radio(
        "Select larger than or smaller than:",
        ["Larger than", "Smaller than"],
        horizontal=True
        )

    employerSize1 = st.radio(
        "Select employer size:",
        ["Less than 250", "250 to 499", "500 to 999", "1000 to 4999", "5000 to 19,999","20,000 or more", "Not Provided"],
        horizontal=True
        )

    # Let's filter our dataframe
    drop_columns = ['IsLondon', 'DiffMedianHourlyPercent',
     'DiffMeanBonusPercent', 'DiffMedianBonusPercent', 'MaleBonusPercent',
     'FemaleBonusPercent', 'MaleLowerQuartile', 'FemaleLowerQuartile',
     'MaleLowerMiddleQuartile', 'FemaleLowerMiddleQuartile',
     'MaleUpperMiddleQuartile', 'FemaleUpperMiddleQuartile',
     'MaleTopQuartile', 'FemaleTopQuartile', 'CompanyLinkToGPGInfo',
      'CurrentName', 'SubmittedAfterTheDeadline', 'DueDate', 'DateSubmitted']

    tab1, tab2 = st.tabs(["London", "UK"])

    with tab1:
        if largerOrSmallerSelector == "Larger than":
            filtered_df_gpg_london = df_gpg[(df_gpg['IsLondon'] == 'Yes') & (df_gpg['DiffMeanHourlyPercent'] > meanPecentGpgSelector) & (df_gpg['EmployerSize'] == employerSize1)]
        else:
            filtered_df_gpg_london = df_gpg[(df_gpg['IsLondon'] == 'Yes') & (df_gpg['DiffMeanHourlyPercent'] < meanPecentGpgSelector) & (df_gpg['EmployerSize'] == employerSize1)]

        # Let's drop columns
        filtered_df_gpg_london = filtered_df_gpg_london.drop(columns=drop_columns)

        st.write('Average GPG for the selection: ', round(filtered_df_gpg_london['DiffMeanHourlyPercent'].mean(), 2))
        st.write('Companies in the selection: ', len(filtered_df_gpg_london['DiffMeanHourlyPercent']))

        # Let's display the resulting filtered dataframe
        st.dataframe(filtered_df_gpg_london)
    with tab2:
        if largerOrSmallerSelector == "Larger than":
            filtered_df_gpg_uk = df_gpg[(df_gpg['IsLondon'] == 'No') & (df_gpg['DiffMeanHourlyPercent'] > meanPecentGpgSelector) & (df_gpg['EmployerSize'] == employerSize1)]
        else:
            filtered_df_gpg_uk = df_gpg[(df_gpg['IsLondon'] == 'No') & (df_gpg['DiffMeanHourlyPercent'] < meanPecentGpgSelector) & (df_gpg['EmployerSize'] == employerSize1)]

        # Let's drop columns
        filtered_df_gpg_uk = filtered_df_gpg_uk.drop(columns=drop_columns)

        st.write('Average GPG for the selection: ', round(filtered_df_gpg_uk['DiffMeanHourlyPercent'].mean(), 2))
        st.write('Companies in the selection: ', len(filtered_df_gpg_uk['DiffMeanHourlyPercent']))

        # Let's display the resulting filtered dataframe
        st.dataframe(filtered_df_gpg_uk)


    #==================================================================================================================
    st.markdown('<a id="gpg-distribution"></a>', unsafe_allow_html=True)
    st.subheader('Distribution of mean hourly percent GPG values depending on company size', divider='rainbow')

    st.write('In this dashboard user can select company size and check how the distribution for the mean hourly percent GPG values')
    st.write('For example select company size 500 to 999 employees and check how the distribution of values looks like.')
    employerSize2 = st.radio(
        "Select employer size:",
        ["Less than 250", "250 to 499", "500 to 999", "1000 to 4999", "5000 to 19,999","20,000 or more"], horizontal=True
        )

    tab3, tab4 = st.tabs(["London", "UK"])
    with tab3:
        filtered_df_gpg_london_2 = df_gpg[(df_gpg['IsLondon'] == 'Yes') & (df_gpg['EmployerSize'] == employerSize2)]

        st.write('Companies in the selection: ', len(filtered_df_gpg_london_2['DiffMeanHourlyPercent']))
        fig1 = px.histogram(filtered_df_gpg_london_2, x='DiffMeanHourlyPercent', nbins=20, marginal='rug', title='Customized Histogram')
        st.plotly_chart(fig1)
    with tab4:
        filtered_df_gpg_uk_2 = df_gpg[(df_gpg['IsLondon'] == 'No') & (df_gpg['EmployerSize'] == employerSize2)]

        st.write('Companies in the selection: ', len(filtered_df_gpg_uk_2['DiffMeanHourlyPercent']))
        fig2 = px.histogram(filtered_df_gpg_uk_2, x='DiffMeanHourlyPercent', nbins=20, marginal='rug', title='Customized Histogram')
        st.plotly_chart(fig2)


    #==================================================================================================================
    st.markdown('<a id="gpg-correlation"></a>', unsafe_allow_html=True)
    st.subheader('Correlation between percentage of men receiving a bonus and women receiving a bonus', divider='rainbow')
    st.write("Let's check if there is a correlation between percentage of men receiving a bonus and women receiving a bonus")
    col1, col2 = st.columns(2)
    with col1:
        st.write('London')
        filtered_df_gpg_london_3 = df_gpg[(df_gpg['IsLondon'] == 'Yes')]
        fig3 = px.scatter(filtered_df_gpg_london_3, x='MaleBonusPercent', y='FemaleBonusPercent')

        correlation_london = round(100 * (filtered_df_gpg_london_3['MaleBonusPercent'].corr(filtered_df_gpg_london_3['FemaleBonusPercent'])), 2)
        st.write(f'Correlation between men receiving a bonus and women is: {correlation_london}%')
        st.plotly_chart(fig3)
    with col2:
        st.write('UK')
        filtered_df_gpg_uk_3 = df_gpg[(df_gpg['IsLondon'] == 'No')]
        fig4 = px.scatter(filtered_df_gpg_uk_3, x='MaleBonusPercent', y='FemaleBonusPercent')

        correlation_uk = round(100 * (filtered_df_gpg_uk_3['MaleBonusPercent'].corr(filtered_df_gpg_uk_3['FemaleBonusPercent'])), 2)
        st.write(f'Correlation between men receiving a bonus and women is: {correlation_uk}%')
        st.plotly_chart(fig4)

    #==================================================================================================================
    st.markdown('<a id="gpg-quartiles"></a>', unsafe_allow_html=True)
    st.subheader('Distribution of men and women across paying quartiles', divider='rainbow')
    st.write("Let's check what is the distribution of men and women across paying quartiles")

    col3, col4 = st.columns(2)

    with col3:
        st.write('London')
        filtered_df_gpg_london_4 = df_gpg[(df_gpg['IsLondon'] == 'Yes')]
        lower_quartile_men_london = filtered_df_gpg_london_4['MaleLowerQuartile'].mean()
        lower_quartile_women_london = filtered_df_gpg_london_4['FemaleLowerQuartile'].mean()

        lower_middle_quartile_men_london = filtered_df_gpg_london_4['MaleLowerMiddleQuartile'].mean()
        lower_middle_quartile_women_london = filtered_df_gpg_london_4['FemaleLowerMiddleQuartile'].mean()

        upper_middle_quartile_men_london = filtered_df_gpg_london_4['MaleUpperMiddleQuartile'].mean()
        upper_middle_quartile_women_london = filtered_df_gpg_london_4['FemaleUpperMiddleQuartile'].mean()

        top_quartile_men_london = filtered_df_gpg_london_4['MaleTopQuartile'].mean()
        top_quartile_women_london = filtered_df_gpg_london_4['FemaleTopQuartile'].astype(float).mean()

        sizes_lower_london = [lower_quartile_men_london, lower_quartile_women_london]
        labels_lower_london = ['MaleLowerQuartile', 'FemaleLowerQuartile']
        fig5 = px.pie(values=sizes_lower_london, names=labels_lower_london, title='Men lower quartile vs women lower quartile')
        st.plotly_chart(fig5)

        sizes_lower_middle_london = [lower_middle_quartile_men_london, lower_middle_quartile_women_london]
        labels_lower_middle_london = ['MaleLowerMiddleQuartile', 'FemaleLowerMiddleQuartile']
        fig6 = px.pie(values=sizes_lower_middle_london, names=labels_lower_middle_london, title='Men lower middle quartile vs women lower middle quartile')
        st.plotly_chart(fig6)

        sizes_upper_middle_london = [upper_middle_quartile_men_london, upper_middle_quartile_women_london]
        labels_upper_middle_london = ['MaleUpperMiddleQuartile', 'FemaleUpperMiddleQuartile']
        fig7 = px.pie(values=sizes_upper_middle_london, names=labels_upper_middle_london, title='Men upper middle quartile vs women upper middle quartile')
        st.plotly_chart(fig7)

        sizes_top_london = [top_quartile_men_london, top_quartile_women_london]
        labels_top_london = ['MaleTopQuartile', 'FemaleTopQuartile']
        fig8 = px.pie(values=sizes_top_london, names=labels_top_london, title='Men top quartile vs women top quartile')
        st.plotly_chart(fig8)

    with col4:
        st.write('UK')
        filtered_df_gpg_uk_4 = df_gpg[(df_gpg['IsLondon'] == 'No')]

        lower_quartile_men_uk = filtered_df_gpg_uk_4['MaleLowerQuartile'].mean()
        lower_quartile_women_uk = filtered_df_gpg_uk_4['FemaleLowerQuartile'].mean()

        lower_middle_quartile_men_uk = filtered_df_gpg_uk_4['MaleLowerMiddleQuartile'].mean()
        lower_middle_quartile_women_uk = filtered_df_gpg_uk_4['FemaleLowerMiddleQuartile'].mean()

        upper_middle_quartile_men_uk = filtered_df_gpg_uk_4['MaleUpperMiddleQuartile'].mean()
        upper_middle_quartile_women_uk = filtered_df_gpg_uk_4['FemaleUpperMiddleQuartile'].mean()

        top_quartile_men_uk = filtered_df_gpg_uk_4['MaleTopQuartile'].mean()
        top_quartile_women_uk = filtered_df_gpg_uk_4['FemaleTopQuartile'].astype(float).mean()

        sizes_lower_uk = [lower_quartile_men_uk, lower_quartile_women_uk]
        labels_lower_uk = ['MaleLowerQuartile', 'FemaleLowerQuartile']
        fig9 = px.pie(values=sizes_lower_uk, names=labels_lower_uk, title='Men lower quartile vs women lower quartile')
        st.plotly_chart(fig9)

        sizes_lower_middle_uk = [lower_middle_quartile_men_uk, lower_middle_quartile_women_uk]
        labels_lower_middle_uk = ['MaleLowerMiddleQuartile', 'FemaleLowerMiddleQuartile']
        fig10 = px.pie(values=sizes_lower_middle_uk, names=labels_lower_middle_uk, title='Men lower middle quartile vs women lower middle quartile')
        st.plotly_chart(fig10)

        sizes_upper_middle_uk = [upper_middle_quartile_men_uk, upper_middle_quartile_women_uk]
        labels_upper_middle_uk = ['MaleUpperMiddleQuartile', 'FemaleUpperMiddleQuartile']
        fig11 = px.pie(values=sizes_upper_middle_uk, names=labels_upper_middle_uk, title='Men upper middle quartile vs women upper middle quartile')
        st.plotly_chart(fig11)

        sizes_top_uk = [top_quartile_men_uk, top_quartile_women_uk]
        labels_top_uk = ['MaleTopQuartile', 'FemaleTopQuartile']
        fig12 = px.pie(values=sizes_top_uk, names=labels_top_uk, title='Men top quartile vs women top quartile')
        st.plotly_chart(fig12)

