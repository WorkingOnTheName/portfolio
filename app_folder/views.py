from app_folder import app, db
from flask import render_template, redirect, url_for
import pandas as pd; import plotly.express as px; import plotly.io as pio; import plotly.subplots as sp; import plotly.graph_objects as go

db.init_app(app)

@app.route("/")
def index():
    return redirect(url_for('portfolio'))

@app.route("/portfolio", methods=["GET"])
def portfolio():
        engine = db.engine
        high_customer = db.engine.execute("SELECT * FROM high_risk_customers;")

        #getting the engine that connect to the Postgre database and passing it to pandas to connect it, and making a dataframe out of the portfolio_data table
        daily_tx_df = pd.read_sql('SELECT "Date"::DATE, "ATM", SUM("Cash") FROM portfolio_data GROUP BY "Date"::DATE, "ATM" ORDER BY "ATM"', con=engine)
        daily_tx_df["Date"] = pd.to_datetime(daily_tx_df["Date"])
        daily_tx_fig = px.scatter(daily_tx_df, x="Date", y="sum", color="ATM", labels={'x':'Date', 'y':'Daily Sum'},title='Daily Sum Per Location')
        daily_tx_fig.update_layout(title_x=0.5, title_font_size=30, height=600)
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
        daily_tx_plot = pio.to_html(daily_tx_fig)

        #making the chart for low performing locations
        monthly_low_df = pd.read_sql("SELECT * FROM low_performer;", con=engine)
        monthly_low_fig = px.bar(monthly_low_df, x="Month", y="Monthly Total", color="ATM", barmode="overlay", labels={'x':'Date', 'y':'Monthly Sum'},title='Low Performer Monthly Sum')
        monthly_low_fig.update_layout(title_x=0.5, title_font_size=30, height=600)#, margin=dict(t=20, l=20, r=20, b=20))
        monthly_low_fig.update_traces(width=2103840000)
        monthly_low_plot = pio.to_html(monthly_low_fig)

        #creating the pie chart for trade volume
        pie_tx_df = pd.read_sql('SELECT * FROM tx_pie', con=engine)
                
        #creating the pie chart for sum cash volumes
        pie_sum_df = pd.read_sql('SELECT * FROM tx_sum_pie', con=engine)
        
        pie_figs = sp.make_subplots(rows=1, cols=2, subplot_titles=("Transaction Volume", "Cash Sum"), specs=[[{'type': 'domain'},{'type': 'domain'}]])

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

        pie_figs.update_layout(title_xanchor='center', margin=dict(l=20, r=20, t=20, b=20), height=600)
        pie_sub_plots = pio.to_html(pie_figs)
        
        return render_template("public/portfolio.html", monthly_low_plot=monthly_low_plot, pie_sub_plots=pie_sub_plots, daily_tx_plot=daily_tx_plot, high_customer=high_customer)