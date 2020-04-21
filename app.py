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


#Cases CSV
cases_df = pd.read_csv('data/COVIDcases.csv',sep=',')

#Treemap Counties
treemapdf = pd.read_csv('data/treemapcountries.csv',sep=',')

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
    if len(cells)==41:
      #print(cells[38].find(text=True))
        date = cells[0].find(text=True).split('\n')[0]
        newcases = cells[35].find(text=True).split('\n')[0]
        totalcases = cells[36].find(text=True).split('\n')[0]
        diff = cells[37].find(text=True).split('\n')[0]
        newdeaths=cells[38].find(text=True).split('\n')[0]
        totaldeaths=cells[39].find(text=True).split('\n')[0]
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


# Treemap
treemapfig = go.Figure(go.Treemap(
    labels = treemapdf['Countries'],
    parents = treemapdf['Top10'],
    values = treemapdf['Confirmed_Covid_cases']
))

treemapfig.update_layout(title={
        'text': 'India in comaparison with Top 10 countries with highest Covid Cases',
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})

#Statewise Bar Chart
toplot = statewise_df[statewise_df['Confirmed']>5]

CovidCasebyStatefig = go.Figure(go.Bar(x=toplot['State'], y=toplot['Active'], name='Active'))
CovidCasebyStatefig.add_trace(go.Bar(x=toplot['State'], y=toplot['Deaths'], name='Deaths'))
CovidCasebyStatefig.add_trace(go.Bar(x=toplot['State'], y=toplot['Recovered'], name='Recovered'))

CovidCasebyStatefig.update_layout(title='Covid-19 Case Statuses by State',barmode='stack', xaxis={'categoryorder':'array', 'categoryarray':toplot['State']}, xaxis_title="States",
    yaxis_title="Case Count")

#Statewise Pie Chart
#labels = statewise_df['State']
#values =  statewise_df['Recovered']
CovidpercentbyStatefig =px.pie(statewise_df, values='Recovered', names='State')
CovidpercentbyStatefig.update_traces(textposition='inside')
CovidpercentbyStatefig.update_layout(title='Covid-19 Recovered Cases percent by State',uniformtext_minsize=12, uniformtext_mode='hide')


#Cases 
if cases_df['Date'].dtypes == object:
    cases_df['Date'] = pd.to_datetime(cases_df['Date'], format='%d-%m-%Y') 

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
DailyNumberofcasesfig.update_layout(xaxis_range=['2020-02-03','2020-05-15'],
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
TotalNumberofcasesfig.update_layout(xaxis_range=['2020-02-03','2020-05-15'],
                  title_text="Total number of cases- Confirmed, Recovered,Deceased",
                  xaxis_title="Date",
                  yaxis_title="Case Count")


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
            dcc.Graph(figure=fig),
            dcc.Graph(figure=treemapfig,style={
            'height': 500,
            'width': 900,
            "display": "block",
            "margin-left": "auto",
            "margin-right": "auto",
            })
        ]),
    html.Div([
            #html.H3('Column 1'),
            #dcc.Graph(id='g1', figure={'data': [{'y': [1, 2, 3]}]})
            #html.P('{}'.format(cases_df.dtypes),style={'font-family': 'Helvetica', 'textAlign': 'center'}),
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
            dcc.Graph(figure=CovidCasebyStatefig)
            #html.H3('Column 2'),
            #dcc.Graph(id='g2', figure={'data': [{'y': [1, 2, 3]}]})
        ], className="six columns"),
        
        html.Div([
            dcc.Graph(figure=CovidpercentbyStatefig)
        ], className="six columns"),
    ]),
    #html.Hr(),
    html.Div([
            #html.H3('Column 1'),
            #dcc.Graph(id='g1', figure={'data': [{'y': [1, 2, 3]}]})
        html.Iframe(id = 'map',srcDoc = open('data/COVIDIndiamap_ch.html','r').read(),width = '100%', height = '600')
    ]),
     html.Hr()

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

if __name__ == '__main__':
    app.run_server(debug=True)