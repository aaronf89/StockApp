import requests
import pandas as pd
import matplotlib.pylab as plt
import seaborn as sn
import datetime as dt
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components 
import datetime



BASE='https://www.quandl.com/api/v3/datasets/WIKI/'

def GetURL(ticker):
    return BASE+str(ticker.upper())+'.json'

ticker='FB'#raw_input("Enter ticker symbol: ")

r=requests.get(GetURL(ticker)).json()['dataset']
df=pd.DataFrame(r['data'], columns=r['column_names'])
df['Date'] = pd.to_datetime(df['Date'])


# output to static HTML file
output_file("lines.html", title=str(ticker).upper()+" Stock Date")

# create a new plot with a title and axis labels
p = figure(title="Historical Prices for "+str(ticker).upper(), x_axis_label='Date', y_axis_label='Price (in $)', x_axis_type="datetime",  y_range=[min(df.Close[:21]), max(df.Close[:21])], x_range=[df.Date[20], df.Date[0]])

mids = (df.Open + df.Close)/2
spans = abs(df.Close-df.Open)

inc = df.Close > df.Open
dec = df.Open > df.Close
w = 12*60*60*1000 # half day in ms

p = figure(x_axis_type="datetime", plot_width=1000, toolbar_location="left",  y_range=[min(df.Close[:21]), max(df.Close[:21])], x_range=[df.Date[20]-datetime.timedelta(hours=12)
, df.Date[0]+datetime.timedelta(hours=12)])

p.segment(df.Date, df.High, df.Date, df.Low, color="black")
p.rect(df.Date[inc], mids[inc], w, spans[inc], fill_color="#D5E1DD", line_color="black")
p.rect(df.Date[dec], mids[dec], w, spans[dec], fill_color="#F2583E", line_color="black")

#p.xaxis.major_label_orientation = pi/4
p.grid.grid_line_alpha=0.3
show(p)  # open a browser




# add a line renderer with legend and line thickness
'''
p.line(df.Date, df.Close, legend="Closing Price", line_width=2, color='blue')
p.line(df.Date, df.High, legend="High Price", line_width=2, color='red')
# show the results
show(p)

script, div = components(p)
render_template('graph.html', script=script, div=div)

plt.plot(df.Date, df.Close)
plt.xlim([df.Date[20], df.Date[0]])
plt.ylim([min(df.Close[:21]), max(df.Close[:21])])
'''