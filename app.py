import dash
import dash_html_components as html
import dash_core_components as dcc

#For reading the csv files
import pandas as pd

#For plotting - Plotly Libraries
import plotly.express as px
import plotly.graph_objects as go

#For current date and time
from datetime import datetime

#For scrapping the data
import bs4
import requests

#Load the data from CSV into the respective dataframes
#Statewise  CSV
statewise_df = pd.read_csv('data/COVIDstatewise.csv',sep=',')

#Raw data CSV
raw_data_df = pd.read_csv('data/COVIDraw_data_df.csv',sep=',')

#Cases CSV
cases_df = pd.read_csv('data/COVIDcases.csv',sep=',')

#Current updates
# get url (published from google sheets, cannot download, only html)
url = r'https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_India'

# read the url and put as text
rtext = requests.get(url).text

soup = bs4.BeautifulSoup(rtext, "lxml")
cases_table = soup.find('table', class_='wikitable mw-collapsible')

newcases=0
totalcases=0
diff= 0
newdeaths=0
totaldeaths=0
date = 0
for row in cases_table.findAll('tr'):
    cells=row.findAll('td')
    #print(len(cells))
    if len(cells)==40:
      #print(cells[38].find(text=True))
        date = cells[0].find(text=True).split('\n')[0]
        newcases = cells[34].find(text=True).split('\n')[0]
        totalcases = cells[35].find(text=True).split('\n')[0]
        diff = cells[36].find(text=True).split('\n')[0]
        newdeaths=cells[37].find(text=True).split('\n')[0]
        totaldeaths=cells[38].find(text=True).split('\n')[0]
#todf = {'Date':date,'New Cases':newcases,'Total Cases':totalcases,'Difference in %':diff,'New Deaths':newdeaths,'Total Deaths':totaldeaths}

fig = go.Figure(layout=go.Layout(height=100,autosize=True,margin={'t': 0,'b':0}),data=[go.Table(
  header=dict(
    values=['Date', 'New Cases', 'Total Cases', 'Difference in %', 'New Deaths', 'Total Deaths'],
    line_color='white', fill_color='white',
    align='center',font=dict(color='black', size=14)
  ),
  cells=dict(
    values=[date, newcases, totalcases,diff,newdeaths,totaldeaths],
    align='center', font=dict(color='black', size=12)
    ))
])
#Statewise Bar Chart
toplot = statewise_df[statewise_df['Confirmed']>5]

CovidCasebyStatefig = go.Figure(go.Bar(x=toplot['State'], y=toplot['Active'], name='Active'))
CovidCasebyStatefig.add_trace(go.Bar(x=toplot['State'], y=toplot['Deaths'], name='Deaths'))
CovidCasebyStatefig.add_trace(go.Bar(x=toplot['State'], y=toplot['Recovered'], name='Recovered'))

CovidCasebyStatefig.update_layout(title='Covid-19 Case Statuses by State',barmode='stack', xaxis={'categoryorder':'array', 'categoryarray':toplot.loc[1:,'State']}, xaxis_title="States",
    yaxis_title="Case Count")

#Statewise Pie Chart
labels = statewise_df['State']
values =  statewise_df['Recovered']
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
DailyNumberofcasesfig.update_layout(xaxis_range=['2020-01-25','2020-04-22'],
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
TotalNumberofcasesfig.update_layout(xaxis_range=['2020-01-25','2020-04-22'],
                  title_text="Total number of cases- Confirmed, Recovered,Deceased",
                  xaxis_title="Date",
                  yaxis_title="Case Count")

#Raw Data 

#Gender Bar Chart
new_df = raw_data_df.groupby(['Nationality'])['Patient Number'].count()
new_df = new_df.to_frame()
new_df.reset_index(inplace=True)

CovidpercentbyNationfig = go.Figure(data=[go.Pie(labels=new_df['Nationality'], values=new_df['Patient Number'],hole=.5)])
CovidpercentbyNationfig.update_traces(textposition='inside')
CovidpercentbyNationfig.update_layout(title='Covid-19 Confirmed Cases percent by Nationalities',uniformtext_minsize=12, uniformtext_mode='hide')
#CovidPatientPercentfig.show()

#Age Group Bar Chart
age_df = raw_data_df.groupby(['Age Groups','Gender'])['Patient Number'].count()
age_df = age_df.to_frame()
age_df.reset_index(inplace=True)

AgeDataNA = age_df.loc[age_df['Age Groups']=='Data not available','Patient Number'][23]+age_df.loc[age_df['Age Groups']=='Data not available','Patient Number'][24]+age_df.loc[age_df['Age Groups']=='Data not available','Patient Number'][25]
#print("There are {} patients whose Age data is not Available.\n {} Female {} Male and {} whose age and gender data is not available.\nThe Graph has been prepared for the patients whose Age data is available.".format(AgeDataNA,FemaleNA,MaleNA,overallNA))
CovidPatientAgefig = px.bar(age_df[age_df['Age Groups'] !='Data not available'], x="Age Groups", y="Patient Number", color='Gender', barmode='group',
             height=400)
CovidPatientAgefig.update_layout(title='COVID-19 affected Age Groups by Gender',yaxis_title="Case Count")

#DASH APP

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = 'Covid and India'
app.layout = html.Div([

    html.H3(children='COVID - 19 in India',style={'font-family': 'Helvetica', 'font-weight': 'bold', 'textAlign': 'center'}),
    html.H4(children='At a glance',style={'font-family': 'Helvetica', 'font-weight': 'bold', 'textAlign': 'center'}),
    html.P('Built using Python, Dash and Plotly.',style={'font-family': 'Helvetica', 'textAlign': 'center'}),
    html.Hr(),
    html.Div([
            html.H5(children='Current Updates',style={'font-family': 'Helvetica', 'font-weight': 'bold', 'textAlign': 'center'}),
            dcc.Graph(figure=fig)
        ]),
    html.Div([
            #html.H3('Column 1'),
            #dcc.Graph(id='g1', figure={'data': [{'y': [1, 2, 3]}]})
        html.Div([
            html.P(children='Choose from the drop-down',style={'font-family': 'Helvetica', 'font-weight': 'bold', 'textAlign': 'right','padding': 10},className="six columns"),
            dcc.Dropdown(
                id='demo-dropdown1',
                options=[
                    {'label': 'Daily number of cases', 'value': 'Daily'},
                    {'label': 'Total number of cases', 'value': 'Total'}
                ],
                value='Daily',
                className="six columns",
                placeholder="Select from Daily and Total"
            )
        ], className="row"),
        html.Div(id='dd-output-container1')
    ]),
    html.Hr(),
    html.Div([
        html.Div([
            #dcc.Graph(figure=CovidCasebyStatefig)
            #html.H3('Column 2'),
            #dcc.Graph(id='g2', figure={'data': [{'y': [1, 2, 3]}]})
            dcc.Dropdown(
                id='demo-dropdown',
                options=[
                    {'label': 'Case Status Count by State', 'value': 'bar'},
                    {'label': 'Recovery percent by State', 'value': 'pie'},
                ],
                value='pie',
                style={'text-align': 'center'}
            ),
            html.Div(id='dd-output-container'),
        ], className="six columns"),
        
        html.Div([
            #dcc.Graph(figure=CovidpercentbyStatefig)
            dcc.Dropdown(
                id='demo-dropdown3',
                options=[
                    {'label': 'Number of cases by Age', 'value': 'Age'},
                    {'label': 'Number of cases by Nationalities', 'value': 'nation'}
                ],
                value='Age',
                style={'text-align': 'center'}
            ),
            html.P(
            'There are {} number of patients whose Age data is unavailable.'.format(AgeDataNA)
        ),
            html.Div(id='dd-output-container3')
        ], className="six columns"),
    ]),
    #html.Hr(),
    html.Div([
            #html.H3('Column 1'),
            #dcc.Graph(id='g1', figure={'data': [{'y': [1, 2, 3]}]})
        html.Div([
            #html.P(children='Choose from the drop-down',style={'font-family': 'Helvetica', 'font-weight': 'bold'}),
            dcc.Dropdown(
                id='demo-dropdown2',
                options=[
                    {'label': 'Covid Cases by State', 'value': 'Choropeth'},
                    {'label': 'Covid Cases by Cities', 'value': 'Bubble'},
                ],
                value='Choropeth',
                className="six columns",
                placeholder='Choose from Map Type'
            )
        ], className="row"),
        html.Div(id='dd-output-container2',style={'padding': 20}),
    ]),
     html.Hr(),
     html.P('Last updated on 2020-04-20 12:39:50 IST',style={'font-family': 'Helvetica', 'textAlign': 'center'})

])

@app.callback(
    dash.dependencies.Output('dd-output-container1', 'children'),
    [dash.dependencies.Input('demo-dropdown1', 'value')])
def update_output1(value):
    #Statewise Bar Chart
    figurestring = DailyNumberofcasesfig
    if value == "Total":
        figurestring = TotalNumberofcasesfig
        
    return dcc.Graph(figure=figurestring)

@app.callback(
    dash.dependencies.Output('dd-output-container2', 'children'),
    [dash.dependencies.Input('demo-dropdown2', 'value')])
def update_output2(value):
    #Statewise Bar Chart
    figurestring = 'data/COVIDIndiamap_ch.html'
    if value == "Bubble":
        figurestring = 'data/COVIDIndiamap_bubble.html'
        
    return html.Iframe(id = 'map',srcDoc = open(figurestring,'r').read(),width = '100%', height = '600')

@app.callback(
    dash.dependencies.Output('dd-output-container3', 'children'),
    [dash.dependencies.Input('demo-dropdown3', 'value')])
def update_output3(value):
    figurestring = CovidpercentbyNationfig
    if value == "Age":
        figurestring = CovidPatientAgefig
    return dcc.Graph(figure=figurestring)

@app.callback(
    dash.dependencies.Output('dd-output-container', 'children'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_output(value):
    #Statewise Bar Chart
    figurestring = CovidCasebyStatefig
    if value == "pie":
        figurestring = CovidpercentbyStatefig
    return dcc.Graph(figure=figurestring)

if __name__ == '__main__':
    app.run_server(debug=True)