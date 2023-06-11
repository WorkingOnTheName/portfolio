# importing all of the dependencies we need
from app_folder import app, db
from flask import render_template, redirect, url_for
import pandas as pd
import plotly.express as px
import plotly.io as pio
import plotly.subplots as sp
import plotly.graph_objects as go

# initializing the FlaskSqlAlchemy Object known as db
db.init_app(app)

# just rerouting people who visit the website to /portfolio
@app.route("/")
def index():
    return redirect(url_for('portfolio'))

@app.route("/portfolio", methods=["GET"])
def portfolio():
    # getting the engine that connect to the Postgre database and passing it
    # to pandas to connect it, and making a dataframe out of the
    # portfolio_data table
    engine = db.engine

    #Getting a list of high risk customers from the database which will later
    #be used in generating an html table when we pass this to the html template
    high_customer = engine.execute("SELECT * FROM high_risk_customers;")

    # Using pandas read_sql method and passing engine to it as connection.
    # Currently we are making a dataframe for the chart that will show
    # Daily Sum per day for each location or daily_tx_df
    daily_tx_df = pd.read_sql(""" SELECT "Date"::DATE, "Location", SUM("Cash") 
        FROM portfolio_data 
        GROUP BY "Date"::DATE, "Location" ORDER BY "Location" """, con=engine)

    # Convert the Date collumn to a format acceptable for pandas
    # Then we use plotly express to make a scatter plot with the data frame
    daily_tx_df["Date"] = pd.to_datetime(daily_tx_df["Date"])
    daily_tx_fig = px.scatter(daily_tx_df, x="Date", y="sum", color="Location",
    labels={'x': 'Date', 'y': 'Daily Sum'}, title='Double-Click Legend Items to Isolate Series')
    # Make the figure object taller than defualt 450px and center title
    daily_tx_fig.update_layout(title_x=0.5, title_font_size=30, height=600)
    # Add a range slider + buttons for different views of the data
    daily_tx_fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )
    # Take the figure and convert it to an html object
    daily_tx_plot = pio.to_html(daily_tx_fig)

    # The Dataframe for the low performing locations using pandas to query a
    # postgres database.
    monthly_low_df = pd.read_sql("SELECT * FROM low_performer;",
                                 con=engine)
    # Creating a figure with plotly express and passing in above dataframe
    monthly_low_fig = px.bar(monthly_low_df, x="Month", y="Monthly Total",
    color="Location", barmode="overlay", labels={'x': 'Date', 'y': 'Monthly Sum'},
    title='Interactive Bar Chart')
    #making the bar chart tallerand centering the title
    monthly_low_fig.update_layout(title_x=0.5, title_font_size=30, height=600)
    # telling the figure to make the bar width 2103840000 miliseconds wide
    # because the xaxis measures width in miliseconds when it comes to time
    monthly_low_fig.update_traces(width=2103840000)
    # convert the figure to html
    monthly_low_plot = pio.to_html(monthly_low_fig)

    # creating the dataframe for trade volume (number of transactions)
    pie_tx_df = pd.read_sql('SELECT * FROM tx_pie', con=engine)

    # creating the dataframe for sum cash (cash total of transactions)
    pie_sum_df = pd.read_sql('SELECT * FROM tx_sum_pie', con=engine)

    # Putting both pie charts side by side using a subplot
    pie_figs = sp.make_subplots(rows=1, cols=2, 
    subplot_titles=("Volume", "Price"),
    specs=[[{'type': 'domain'}, {'type': 'domain'}]])

    pie_figs.add_trace(go.Pie(labels=pie_tx_df.columns,
                              values=pie_tx_df.iloc[0],
                              legendgroup='1',
                              ),
                       row=1, col=1)
    pie_figs.add_trace(go.Pie(labels=pie_sum_df.columns,
                              values=pie_sum_df.iloc[0],
                              legendgroup='1',
                              ),
                       row=1, col=2)

    #maxing the subplot taller and centering the title
    pie_figs.update_layout(title_xanchor='center',
    margin=dict(l=20, r=20, t=20, b=20), height=600)
    #converting the subplot figure into an html object
    pie_sub_plots = pio.to_html(pie_figs)

    #rendering the html templace for /portfolio and passing the html charts
    return render_template("public/portfolio.html", 
    monthly_low_plot=monthly_low_plot, pie_sub_plots=pie_sub_plots,
    daily_tx_plot=daily_tx_plot, high_customer=high_customer)