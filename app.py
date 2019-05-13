import dash
import dash_core_components as dcc
import dash_html_components as html
import metapy
import pytoml
import extract  as ext
import plotly.graph_objs as go
import pandas as pd
import subprocess
import sys
from sys import platform


from dash.dependencies import Input, Output, State

cycleFlag = False

# concatenate lemur stopwords w/ user stopwords
# if no user inputted stopword file, use antibiotic stopwords + lemur stopwords
if len(sys.argv) == 1:
    if platform == "win32":
        subprocess.call("type lemur_stopwords.txt antibiotic_resistance_stopwords.txt > user_combined_stopwords.txt",shell=True)
    else:
        subprocess.call("cat lemur_stopwords.txt antibiotic_resistance_stopwords.txt > user_combined_stopwords.txt",shell=True)
else:
    user_file = str(sys.argv[1])
    if platform == "win32":
        subprocess.call("type lemur_stopwords.txt " + user_file + " > user_combined_stopwords.txt",shell=True)
    else:
        subprocess.call("cat lemur_stopwords.txt " + user_file + " > user_combined_stopwords.txt",shell=True)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)



colors = {
    'background': '#C2DFFF',
    'text': '#2F4F4F'
}

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(children='PubText: A PubMed Text Search Tool Documentation',
    style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.P([
        'NCBI Query: ',
        dcc.Input(value='Antibiotics Resistance', type='text',id='query-text-id',

            style={
                'textAlign': 'center',
                'width': '80%',
                'margin': 20
            }
        )], id = 'query-text-p', style={

            'color': colors['text']

        } ),
    html.P([
        'Keyword Frequency Search: ',
        dcc.Input(value='Genes', type='text',id='tf-text-id',

            style={
                'textAlign': 'center',
                'width': '80%',
                'margin': 20
            }
        )], id = 'tf-text-p', style={

            'color': colors['text']

        } ),

    html.P([
        'Number of Docs:  ',
        dcc.Input(
            id='no-docs-id',
            type='number',
            value='20',
        style={
            'textAlign': 'left',
            'width': '5%',
            'margin': 20

        }

    )], id='no-docs-p', style={

            'color': colors['text']

        } ),
    html.Button(
            'Search',
            id='search-button',
            n_clicks=0,
            style={'width': '12%', 'margin': 10}
    ),
    dcc.Graph(id='search-output-histogram'),
    dcc.Graph(id='search-output-scatter'),
    html.Div(id='abstract-div', style={'background': '#FFFFFF'}, children= [
        html.H2(children='Abstract',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
       ),
       html.H4(id='abstract-html')
         ]

	),
     # Hidden div inside the app that stores the intermediate value
    html.Div(id='intermediate-value', style={'display': 'none'})

] )


# This is the call back  that gets called when the search button is submitted.
# The results are cached in the hidden div
@app.callback(Output('intermediate-value', 'children'),
              [Input('search-button', 'n_clicks')],
              [State('query-text-id', 'value'),
               State('tf-text-id', 'value'),
               State('no-docs-id', 'value')])
def update_cache(n_clicks, search_text, tf_text, no_docs):

        with open('config.toml', 'r') as fin:
            cfg_d = pytoml.load(fin)
        global cycleFlag
        extract = ext.Extract(cfg_d,cycleFlag)

        dff = extract.extract_abstracts (search_text, tf_text, int(no_docs))
        cycleFlag = True
        return dff.to_json(date_format='iso', orient='split')


# This is the call back  that gets called after the search histogram is populated
# The scatter plot is the output
@app.callback(Output('search-output-scatter', 'figure'),
              [Input('search-output-histogram', 'figure')],
              [State('intermediate-value', 'children')])
def update_scatter(val,json_data):

        ddff = pd.read_json(json_data, orient='split')
        dff = ddff['scatter']
        return {
            'data': [go.Scatter(
                x= dff['terms'],
                y= dff['frequency'],
                text=dff['links'],
                mode='markers',
                marker={
                    'size': 15,
                    'opacity': 0.5,
                    'line': {'width': 0.5, 'color': 'white'}
                }
            )],
            'layout': go.Layout(
                xaxis={
                    'title': 'terms',
                    'type': 'linear'
                },
                yaxis={
                    'title': 'frequency',
                    'type': 'linear'
                },
                margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
                hovermode='closest'
            )
    }


def readDict(filename):
    d = {}
    with open(filename) as f:
        for line in f:
           (key, val) = line.split()
           d[key] = val
    return d

# This is the call back  that gets called after the cache is populated.
# The histogram gets populated from cached data

@app.callback(Output('search-output-histogram', 'figure'),
              [Input('intermediate-value', 'children')])
def update_histogram(json_data):

        ddff = pd.read_json(json_data, orient='split')
        dff = ddff['top_words']
        stemmedDict=readDict("stem_dict.txt")
        newText=[]
        for i in dff['words']:
            if i in stemmedDict:
                newText.append(stemmedDict[i])
            else:
                newText.append(i)
        return {
            'data': [go.Bar(
                x= dff['index'],
                y= dff['freq'],
                text=newText
            )],
            'layout': go.Layout(
                xaxis={
                    'title': 'words',
                    'type': 'linear'
                },
                yaxis={
                    'title': 'frequency',
                    'type': 'linear'
                },
                margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
                hovermode='closest'
            )
    }

@app.callback(
    Output(component_id='abstract-html', component_property='children'),
    [Input('search-output-scatter', 'clickData')],
    [State('intermediate-value', 'children')])
def update_output_div(clickData, json_data):


    try:
        link = clickData['points'][0]['text']
        ddff = pd.read_json(json_data, orient='split')
        dff = ddff['link_abstract_map']
        print (link)
        print (dff)
        abstract = dff[link]

        #abstract=dff.loc[dff['links'] == link, 'abstracts'].iloc[0]
    except BaseException as e:
        abstract = str(e)

    return '"{}"'.format(abstract)






def empty_df():
    data_df = pd.DataFrame({'links' : [], 'abstracts': [], 'terms': [], 'frequency': []})
    return data_df





if __name__ == '__main__':
    app.run_server(debug=True)
