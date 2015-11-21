from flask import Flask, render_template, request, redirect
import requests
import pandas as pd
import matplotlib.pylab as plt
import datetime as dt
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components 
import datetime

#Read in available ticker data
#tickers=pd.read_csv('C://Users/Aaron/Documents/Data_Incubator/flask-demo-master/ticker_list.csv', usecols=['Ticker'])

tickers=pd.read_csv('./ticker_list.csv', usecols=['Ticker'])


BASE='https://www.quandl.com/api/v3/datasets/WIKI/'
    
def GetURL(ticker):
    return BASE+str(ticker.upper())+'.json'


def LinePlot(df, p):
    
    colors=['red', 'blue', 'black', 'cyan']
    c=0        
    for pdat in app.vars['close']:
        p.line(df.Date, df[str(pdat)], legend=str(pdat), line_width=2, color=colors[c])
        c+=1
        
    return p
    
    
def CSPlot(df,p):
    
    mids = (df.Open + df.Close)/2
    spans = abs(df.Close-df.Open)

    inc = df.Close > df.Open
    dec = df.Open > df.Close
    w = 12*60*60*1000 # half day in ms
    p.segment(df.Date, df.High, df.Date, df.Low, color="black")
    p.rect(df.Date[inc], mids[inc], w, spans[inc], fill_color="#D5E1DD", line_color="black")
    p.rect(df.Date[dec], mids[dec], w, spans[dec], fill_color="#F2583E", line_color="black")
    p.grid.grid_line_alpha=0.3
    
    
    return p
    

app = Flask(__name__)
app.vars={}

@app.route('/')
def main():
    return redirect('/home')
  
@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html', num=6)  

@app.route('/graph', methods=['GET', 'POST'])
def graph():
        
    if request.method == 'GET':
        return redirect('/home')
    else:
        
        app.vars['name'] = request.form['name_app'].upper()        
        app.vars['close']=request.form.getlist('features')
        app.vars['plottype']=request.form['answer_from_layout_app']
        
        if app.vars['name'] not in tickers.as_matrix():
            return render_template('tickererror.html')
        elif (len(app.vars['close'])==0) and app.vars['plottype']=='line':
            return render_template('selectionerror.html', TICKER=app.vars['name'])
       
        ticker=app.vars['name']       
        r=requests.get(GetURL(ticker)).json()['dataset']        
        df=pd.DataFrame(r['data'], columns=r['column_names'])
        df=df.rename(columns={c: c.replace(" ","") for c in df.columns})
        df['Date'] = pd.to_datetime(df['Date'])
          
        # output to static HTML file
        output_file("lines.html", title=str(ticker).upper()+" Stock Date")
        
        #Prepare axis
        offset=.05*(max(df.High[:21])-min(df.Low[:21]))        
        Y_range=[min(df.Low[:21])-offset, max(df.High[:21])+offset]     
        X_range=[df.Date[20]-datetime.timedelta(hours=12), df.Date[0]+datetime.timedelta(hours=12)]
        p = figure(title="Historical Prices for "+str(ticker).upper(),plot_width=1000, toolbar_location="left",  x_axis_label='Date', y_axis_label='Price (in $)', x_axis_type="datetime", x_range=X_range, y_range=Y_range)
        
        if app.vars['plottype']=="line":
            p=LinePlot(df, p)
        else:
            p=CSPlot(df,p)
        
        
        script, div = components(p)
        return render_template('graph.html', script=script, div=div, TICKER=ticker)      

if __name__ == '__main__':
  app.run(port=33507, debug=True)
