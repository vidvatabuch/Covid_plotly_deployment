#For reading the csv files
import pandas as pd

#For plotting - Plotly Libraries
import plotly.express as px
import plotly.graph_objects as go

#Dash libraries
import dash
import dash_core_components as dcc
import dash_html_components as html

#from flask import Flask
import os


#Load the data from CSV into the respective dataframes
#Statewise  CSV
statewise_df = pd.read_csv('data/COVIDstatewise_08042020.csv',sep='\t')

#Raw data CSV
raw_data_df = pd.read_csv('data/COVIDraw_data_df_08042020.csv',sep='\t')

#Cases CSV
cases_df = pd.read_csv('data/COVIDcases_08042020.csv',sep='\t')


#Prepare the Plotly Charts to publish them on web page later

#Statewise Bar Chart
toplot = statewise_df[statewise_df['Confirmed']>5]

CovidCasebyStatefig = go.Figure(go.Bar(x=toplot.loc[1:,'State'], y=toplot.loc[1:,'Active'], name='Active'))
CovidCasebyStatefig.add_trace(go.Bar(x=toplot.loc[1:,'State'], y=toplot.loc[1:,'Deaths'], name='Deaths'))
CovidCasebyStatefig.add_trace(go.Bar(x=toplot.loc[1:,'State'], y=toplot.loc[1:,'Recovered'], name='Recovered'))

CovidCasebyStatefig.update_layout(title='Covid-19 Case Statuses by State',barmode='stack', xaxis={'categoryorder':'array', 'categoryarray':toplot.loc[1:,'State']}, xaxis_title="States",
    yaxis_title="Case Count")

#Statewise Pie Chart
labels = statewise_df.loc[1:,'State']
values =  statewise_df.loc[1:,'Recovered']
CovidpercentbyStatefig = go.Figure(data=[go.Pie(labels=labels, values=values,hole=.3)])
CovidpercentbyStatefig.update_traces(textposition='inside')
CovidpercentbyStatefig.update_layout(title='Covid-19 Recovered Cases percent by State',uniformtext_minsize=12, uniformtext_mode='hide')

#Cases 

# Daily  Confirmed, Recovered and Deaths
DailyNumberofcasesfig = go.Figure()
DailyNumberofcasesfig.add_trace(go.Scatter(
                x=cases_df['Date'],
                y=cases_df['Daily Confirmed'],
                name="Daily Confirmed",
                line_color='deepskyblue',
                opacity=0.8))

DailyNumberofcasesfig.add_trace(go.Scatter(
                x=cases_df['Date'],
                y=cases_df['Daily Recovered'],
                name="Daily Recovered",
                line_color='green',
                opacity=0.8))

DailyNumberofcasesfig.add_trace(go.Scatter(
                x=cases_df['Date'],
                y=cases_df['Daily Deceased'],
                name="Daily Deceased",
                line_color='red',
                opacity=0.8))

# Use date string to set xaxis range
DailyNumberofcasesfig.update_layout(xaxis_range=['2020-01-25','2020-04-08'],
                  title_text="Daily number of cases- Confirmed, Recovered,Deceased",
                  xaxis_title="Date",
                  yaxis_title="Case Count")
#DailyNumberofcasesfig.show()

#Total Confirmed, Recovered and Deaths
TotalNumberofcasesfig = go.Figure()
TotalNumberofcasesfig.add_trace(go.Scatter(
                x=cases_df['Date'],
                y=cases_df['Total Confirmed'],
                name="Total Confirmed",
                line_color='deepskyblue',
                opacity=0.8))

TotalNumberofcasesfig.add_trace(go.Scatter(
                x=cases_df['Date'],
                y=cases_df['Total Recovered'],
                name="Total Recovered",
                line_color='green',
                opacity=0.8))

TotalNumberofcasesfig.add_trace(go.Scatter(
                x=cases_df['Date'],
                y=cases_df['Total Deceased'],
                name="Total Deceased",
                line_color='red',
                opacity=0.8))

# Use date string to set xaxis range
TotalNumberofcasesfig.update_layout(xaxis_range=['2020-01-25','2020-04-08'],
                  title_text="Total number of cases- Confirmed, Recovered,Deceased",
                  xaxis_title="Date",
                  yaxis_title="Case Count")

#Raw Data 

#Gender Bar Chart
new_df = raw_data_df.groupby(['Current Status','Gender'])['Patient Number'].count()
new_df = new_df.to_frame()
new_df.reset_index(inplace=True)

CovidPatientPercentfig = px.bar(new_df, x="Current Status", y="Patient Number", color='Gender', barmode='group',height=400)
CovidPatientPercentfig.update_layout(title='Patient Status by Gender',yaxis_title="Case Count")
#CovidPatientPercentfig.show()

#Age Group Bar Chart
age_df = raw_data_df.groupby(['Age Groups','Gender'])['Patient Number'].count()
age_df = age_df.to_frame()
age_df.reset_index(inplace=True)

AgeDataNA = age_df.loc[age_df['Age Groups']=='Data not available','Patient Number'][24]+age_df.loc[age_df['Age Groups']=='Data not available','Patient Number'][25]+age_df.loc[age_df['Age Groups']=='Data not available','Patient Number'][26]
MaleNA = age_df.loc[age_df['Age Groups']=='Data not available','Patient Number'][26]
FemaleNA = age_df.loc[age_df['Age Groups']=='Data not available','Patient Number'][25]
overallNA = age_df.loc[age_df['Age Groups']=='Data not available','Patient Number'][24]
#print("There are {} patients whose Age data is not Available.\n {} Female {} Male and {} whose age and gender data is not available.\nThe Graph has been prepared for the patients whose Age data is available.".format(AgeDataNA,FemaleNA,MaleNA,overallNA))
CovidPatientAgefig = px.bar(age_df[age_df['Age Groups'] !='Data not available'], x="Age Groups", y="Patient Number", color='Gender', barmode='group',
             height=400)
CovidPatientAgefig.update_layout(title='COVID-19 affected Age Groups by Gender',yaxis_title="Case Count")

# DASH APP

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#server = Flask(__name__)
#server.secret_key = os.environ.get('secret_key', 'secret')
#app = dash.Dash(name = __name__, server = server)
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app = dash.Dash(__name__)
server = app.server

app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})
app.title = 'Covid and India'
app.layout = html.Div(children=[
    html.H3(children='COVID - 19 in India',style={'font-family': 'Helvetica', 'font-weight': 'bold', 'textAlign': 'center'}),
    html.H4(children='At a glance',style={'font-family': 'Helvetica', 'font-weight': 'bold', 'textAlign': 'center'}),
    html.P('Built using Python, Dash and Plotly.',style={'font-family': 'Helvetica', 'textAlign': 'center'}),
     
    dcc.Graph(figure=DailyNumberofcasesfig),
    
    dcc.Graph(figure=TotalNumberofcasesfig),
    #dcc.Graph(figure=Numberofcasesfig)
    html.Div([
        html.Div([
            dcc.Graph(figure=CovidCasebyStatefig)
        ], className="six columns"),

        html.Div([
            dcc.Graph(figure=CovidpercentbyStatefig)
        ], className="six columns"),
    ], className="row"),
    
    html.Div([
        html.Div([
            dcc.Graph(figure=CovidPatientPercentfig)
        ], className="six columns"),

        html.Div([
            dcc.Graph(figure=CovidPatientAgefig),
            html.P(
            'There {} no of patients whose Age data is unavailable.{} Male, {} Female, {} Gender NA'.format(AgeDataNA,MaleNA,FemaleNA,overallNA)
        ),
        ], className="six columns"),
    ], className="row"),

    html.Div([
        html.H4(children='COVID in Major Indian Cities.',style={'textAlign': 'center'}),
        html.Iframe(id = 'map',srcDoc = open('data/COVIDIndiamap_08042020.html','r').read(),width = '100%', height = '600')
    ])


])
if __name__ == '__main__':
    app.run_server(debug=True, port=3000)
#app.run_server(debug=True, use_reloader=True)  # Turn off reloader if inside Jupyter