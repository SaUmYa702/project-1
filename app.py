from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from wordcloud import WordCloud
import matplotlib.pyplot as plt


app = Flask(__name__)
app.secret_key = 'supersecretmre'

# Update the encoding to handle potential decoding issues
try:
    df = pd.read_csv('kccdatasets.csv', encoding='latin1')
except UnicodeDecodeError:
    flash("Error reading the CSV file. Please check the file encoding.", "error")
    df = pd.DataFrame()  # Fallback to an empty DataFrame

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')

@app.route("/register",methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # Here you would typically save the user to a database
        flash(f"User {username} registered successfully!", "success")
        return redirect(url_for("index"))
    return render_template("register.html")

@app.route("/about")
def about():
    return render_template("about.html")


#Graphs Functions
def total_queries():
    df['CreatedOn'] = pd.to_datetime(df['CreatedOn'], errors='coerce')
    df['Month_Year'] = df['CreatedOn'].dt.to_period('M').astype(str)
    monthly_queries = df.groupby('Month_Year').size().reset_index(name='Query Count')
    fig1 = px.line(monthly_queries, x='Month_Year', y='Query Count',
               title='Total Queries Over Time', markers=True)
    graph1_html = pio.to_html(fig1, full_html=False)
    return graph1_html

def top_districts():
    top_districts = df['DistrictName'].value_counts().nlargest(10).reset_index()
    top_districts.columns = ['District', 'Query Count']
    fig2 = px.bar(top_districts, x='District', y='Query Count',
                title='Top 10 Districts by Query Volume', text='Query Count')
    graph2_html=pio.to_html(fig2, full_html=False)
    return graph2_html

def Query_distribution():
    sector_counts = df['Sector'].value_counts().reset_index()
    sector_counts.columns = ['Sector', 'Count']
    fig3 = px.pie(sector_counts, names='Sector', values='Count',
                hole=0.4, title='Query Distribution by Sector')
    graph3_html=pio.to_html(fig3, full_html=False )
    return graph3_html

def top_query():
    query_type_counts = df['QueryType'].value_counts().nlargest(15).reset_index()
    query_type_counts.columns = ['QueryType', 'Count']
    fig4 = px.bar(query_type_counts, x='QueryType', y='Count',
                title='Top 15 Query Types', text='Count')
    graph4_html=pio.to_html(fig4, full_html=False)
    return graph4_html

def breakdown_query():
    fig5 = px.sunburst(df, path=['Sector', 'Category'],
                  title='Breakdown of Queries by Sector and Category')
    graph5_html=pio.to_html(fig5, full_html=False)
    return graph5_html

def  sector_distribution():
    fig6=px.pie(df,names="Sector",title="Sector wise distribution")
    graph6_html=pio.to_html(fig6, full_html=False)
    return graph6_html

def districts_distribution():
    fig7 = px.choropleth(df, locations='DistrictName', color='QueryType',
                    featureidkey="properties.ST_NM", scope="asia",
                    title="Query Distribution by District")
    graph7_html=pio.to_html(fig7, full_html=False) 
    return graph7_html

def district_querytype():
    fig8=px.bar(df,x="QueryType",y="DistrictName",title="Distric wise by querytype")
    graph8_html=pio.to_html(fig8, full_html=False )    
    return graph8_html

def Top_crops():
    top_crops = df['Crop'].value_counts().nlargest(10).reset_index()
    top_crops.columns = ['Crop', 'Query Count']
    fig9 = px.bar(top_crops, x='Crop', y='Query Count', 
                title='Top 10 Queried Crops', text='Query Count')
    fig9.update_traces(textposition='outside')
    fig9.update_layout(xaxis_title='Crop', yaxis_title='Query Count')
    graph9_html=pio.to_html(fig9, full_html=False)
    return graph9_html

def Querytype_crop():
    top_crops = df['Crop'].value_counts().nlargest(10).reset_index()
    top_crop_names = top_crops['Crop'].tolist()
    filtered_df = df[df['Crop'].isin(top_crop_names)]
    query_types_per_crop = filtered_df.groupby(['Crop', 'QueryType']).size().reset_index(name='Count')
    fig10 = px.bar(query_types_per_crop, x='Crop', y='Count', color='QueryType',
                title='Query Types per Crop (Stacked Bar)', text='Count')
    fig10.update_layout(barmode='stack', xaxis_title='Crop', yaxis_title='Query Count')
    graph10_html=pio.to_html(fig10, full_html=False)
    return graph10_html

def sectorwise_crop():
    top_crops = df['Crop'].value_counts().nlargest(10).reset_index()
    top_crop_names = top_crops['Crop'].tolist()
    crop_sector = df.groupby(['Crop', 'Sector']).size().reset_index(name='Count')
    top_crop_sector = crop_sector[crop_sector['Crop'].isin(top_crop_names)]
    fig11 = px.bar(top_crop_sector, x='Crop', y='Count', color='Sector',
                title='Sector-wise Crop Grievances (Grouped Bar)',
                text='Count', barmode='group')
    fig11.update_layout(xaxis_title='Crop', yaxis_title='Query Count')
    graph11_html=pio.to_html(fig11, full_html=False)
    return graph11_html

def crop_grievances():
    fig12 = px.treemap(df, path=['Sector', 'Crop'], 
                    values=[1]*len(df),  # har row ko 1 count ki tarah treat karo
                    title='Treemap: Crop Grievances by Sector')
    graph12_html=pio.to_html(fig12, full_html=False)
    return graph12_html

def Mostfriquent_querytype():
    df['CreatedOn'] = pd.to_datetime(df['CreatedOn'], errors='coerce')

    # Extract month and year
    df['Month_Year'] = df['CreatedOn'].dt.to_period('M').astype(str)
    query_type_freq = df['QueryType'].value_counts().reset_index()
    query_type_freq.columns = ['QueryType', 'Count']

    fig13 = px.bar(query_type_freq, x='QueryType', y='Count',
                title='Most Frequent Query Types',
                text='Count', color='QueryType')
    fig13.update_layout(xaxis_title='Query Type', yaxis_title='Query Count', xaxis_tickangle=-45)
    graph13_html=pio.to_html(fig13, full_html=False)
    return graph13_html

def query_distribution():
    top_crops = df['Crop'].value_counts().nlargest(5).index.tolist()
    filtered = df[df['Crop'].isin(top_crops)]

    # Group by crop and query type
    crop_query = filtered.groupby(['Crop', 'QueryType']).size().reset_index(name='Count')

    fig14 = px.bar(crop_query, x='Crop', y='Count', color='QueryType',
                title='Query Type Distribution Across Crops',
                text='Count', barmode='stack')
    fig14.update_layout(xaxis_title='Crop', yaxis_title='Query Count')
    graph14_html=pio.to_html(fig14, full_html=False)
    return graph14_html

def Top20_district():
    df['CreatedOn'] = pd.to_datetime(df['CreatedOn'], errors='coerce')

    # Extract Month-Year
    df['Month_Year'] = df['CreatedOn'].dt.to_period('M').astype(str)
    # Query count per district
    district_query = df.groupby('DistrictName').size().reset_index(name='Query Count')
    district_query = district_query.sort_values(by='Query Count', ascending=False).head(20)

    fig15 = px.bar(district_query, x='DistrictName', y='Query Count',
                title='Top 20 Districts by Number of Queries',
                text='Query Count')
    fig15.update_layout(xaxis_title='District', yaxis_title='Queries', xaxis_tickangle=-45)
    graph15_html=pio.to_html(fig15, full_html=False)
    return graph15_html

def querytype_bydistrict():
    top_districts = df['DistrictName'].value_counts().nlargest(10).index.tolist()
    filtered_df = df[df['DistrictName'].isin(top_districts)]

    # Group by District and QueryType
    dist_querytype = filtered_df.groupby(['DistrictName', 'QueryType']).size().reset_index(name='Count')

    fig16 = px.bar(dist_querytype, x='DistrictName', y='Count', color='QueryType',
                title='Query Types by District (Stacked Bar)', text='Count')
    fig16.update_layout(barmode='stack', xaxis_title='District', yaxis_title='Query Count')
    graph16_html=pio.to_html(fig16, full_html=False)
    return graph16_html

def timetrend_district():
    top_5_districts = df['DistrictName'].value_counts().nlargest(5).index.tolist()
    top_5_df = df[df['DistrictName'].isin(top_5_districts)]

    # Group by Month-Year and District
    district_trend = top_5_df.groupby(['Month_Year', 'DistrictName']).size().reset_index(name='Query Count')

    fig17 = px.line(district_trend, x='Month_Year', y='Query Count', color='DistrictName',
                title='Time Trends for Top 5 Districts', markers=True)
    fig17.update_layout(xaxis_title='Month-Year', yaxis_title='Query Count')
    graph17_html=pio.to_html(fig17, full_html=False)
    return graph17_html

def Querytype_blockname():
    fig18=px.scatter(df,x="QueryType",y="BlockName",title="queries type by blockname")
    graph18_html=pio.to_html(fig18, full_html=False)
    return graph18_html

def querytype_districtname():
    fig19=px.box(df,x="QueryType",y="DistrictName")
    graph19_html=pio.to_html(fig19, full_html=False)
    return graph19_html

def queryby_sector():
    df['CreatedOn'] = pd.to_datetime(df['CreatedOn'], errors='coerce')
    df['Month_Year'] = df['CreatedOn'].dt.to_period('M').astype(str)
    # Count queries grouped by Month and Sector
    sector_time = df.groupby(['Month_Year', 'Sector']).size().reset_index(name='Query Count')

    #  Area Chart
    fig20 = px.area(sector_time, x='Month_Year', y='Query Count', color='Sector',
                title='Queries by Sector Over Time', markers=True)
    fig20.update_layout(xaxis_title='Month-Year', yaxis_title='Number of Queries')
    graph20_html=pio.to_html(fig20, full_html=False)
    return graph20_html

def category_breakdown():
    sector_cat = df.groupby(['Sector', 'Category']).size().reset_index(name='Count')

    # Clustered bar chart (Grouped)
    fig21 = px.bar(sector_cat, x='Sector', y='Count', color='Category',
                title='Category Breakdown per Sector', barmode='group', text='Count')
    fig21.update_layout(xaxis_title='Sector', yaxis_title='Query Count')
    graph21_html=pio.to_html(fig21, full_html=False)
    return graph21_html

def sector_vsquerytype():
    fig22=px.density_heatmap(df,x="Sector",y="QueryType",title="Sector vs querytype")
    graph22_html=pio.to_html(fig22, full_html=False)
    return graph22_html


def monthly_querytrends():
    df['CreatedOn'] = pd.to_datetime(df['CreatedOn'], errors='coerce')

    # Create time-based columns
    df['Month'] = df['CreatedOn'].dt.month
    df['Year'] = df['CreatedOn'].dt.year
    df['Month_Year'] = df['CreatedOn'].dt.to_period('M').astype(str)
    # Top 5 crops for cleaner chart
    top_crops = df['Crop'].value_counts().nlargest(5).index.tolist()
    filtered_df = df[df['Crop'].isin(top_crops)]

    # Group by month-year and crop
    monthly_crop = filtered_df.groupby(['Month_Year', 'Crop']).size().reset_index(name='Query Count')

    # Line chart
    fig23 = px.line(monthly_crop, x='Month_Year', y='Query Count', color='Crop',
                title='Monthly Query Trends by Crop', markers=True)
    fig23.update_layout(xaxis_title='Month-Year', yaxis_title='Query Count')
    graph23_html=pio.to_html(fig23, full_html=False)
    return graph23_html

def yearyquery_count():
    yearly = df.groupby('Year').size().reset_index(name='Query Count')

    # Calculate YOY Growth
    yearly['YOY Growth (%)'] = yearly['Query Count'].pct_change().fillna(0) * 100

    # Bar chart
    fig24 = px.bar(yearly, x='Year', y='Query Count', text='YOY Growth (%)',
                title='Yearly Query Count with YOY Growth')
    fig24.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
    fig24.update_layout(xaxis_title='Year', yaxis_title='Query Count')
    graph24_html=pio.to_html(fig24, full_html=False)
    return graph24_html

def queriesby_day():
    df['DayOfWeek'] = df['CreatedOn'].dt.day_name()

    dow_trend = df['DayOfWeek'].value_counts().reindex(
        ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    ).reset_index()
    dow_trend.columns = ['Day', 'Query Count']

    fig25 = px.line(dow_trend, x='Day', y='Query Count', title='Queries by Day of the Week', markers=True)
    graph25_html=pio.to_html(fig25, full_html=False)
    return graph25_html

def monthlyquery_bysector():
    sector_month = df.groupby(['Month', 'Sector']).size().reset_index(name='Count')

    fig26 = px.bar(sector_month, x='Month', y='Count', color='Sector',
                barmode='group', title='Monthly Query Count by Sector',
                labels={'Month': 'Month Number'})
    fig26.update_layout(xaxis_title='Month', yaxis_title='Query Count')
    graph26_html=pio.to_html(fig26, full_html=False)
    return graph26_html

def word_could():
    text_queries = ' '.join(df['QueryText'].dropna())

    # Create Word Cloud
    wordcloud_queries = WordCloud(width=800, height=400, background_color='white').generate(text_queries)

    # Plot the word cloud using matplotlib
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud_queries, interpolation='bilinear')
    plt.axis("off")
    plt.title("Word Cloud for Farmers' Queries", fontsize=16)
   

    # 2. Word Cloud for Responses (KccAns)
    text_answers = ' '.join(df['KccAns'].dropna())

    # Create Word Cloud for responses
    wordcloud_answers = WordCloud(width=800, height=400, background_color='white').generate(text_answers)

    # Plot the word cloud using matplotlib
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud_answers, interpolation='bilinear')
    plt.axis("off")
    plt.title("Word Cloud for KCC Answers", fontsize=16)
    fig27 = plt.gcf()  # Get the current figure to resolve the undefined fig27 issue
    graph27_html=pio.to_html(fig27, full_html=False)
    return graph27_html

def sentiment_distribution():
        from textblob import TextBlob
        import plotly.express as px

        # Sentiment analysis of KccAns
        df['Sentiment'] = df['KccAns'].apply(lambda x: TextBlob(str(x)).sentiment.polarity)

        # Classify sentiment into categories
        df['Sentiment Category'] = df['Sentiment'].apply(lambda x: 'Positive' if x > 0 else ('Negative' if x < 0 else 'Neutral'))

        # Plot Sentiment Distribution using Plotly
        sentiment_counts = df['Sentiment Category'].value_counts().reset_index()
        sentiment_counts.columns = ['Sentiment', 'Count']

        fig28 = px.bar(sentiment_counts, x='Sentiment', y='Count', title="Sentiment Distribution of Responses")
        graph28_html=pio.to_html(fig28, full_html=False)
        return graph28_html

#Analysis Pages
@app.route('/overview')
def overview():
    graph1 = total_queries()
    graph2 = top_districts()
    graph3 = Query_distribution()
    graph4 =  top_query()
    graph5 = breakdown_query()
    graph6 = sector_distribution()
    graph7 = districts_distribution()
    graph8 = district_querytype()
    return render_template('overview.html',graph1=graph1,graph2=graph2,graph3=graph3,graph4=graph4,graph5=graph5,graph6=graph6,graph7=graph7,graph8=graph8)

@app.route('/crop-specific')
def cropspecific():
    graph9 =  Top_crops()
    graph10 = Querytype_crop()
    graph11 = sectorwise_crop()
    graph12 = crop_grievances()
    return render_template('crop-specific.html',graph9=graph9,graph10=graph10,graph11=graph11,graph12=graph12)

@app.route('/QueryType_deepDrive')
def QueryType_deepDrive():
    graph13 = Mostfriquent_querytype()
    graph14 = query_distribution()
    return render_template('QueryType_deepDrive.html',graph13=graph13,graph14=graph14)

@app.route('/RegionalqueryTrends')
def Regionalquery_Trends():
    graph15 = Top20_district()
    graph16 = querytype_bydistrict()
    graph17 = timetrend_district()
    graph18 = Querytype_blockname()
    graph19 = querytype_districtname()
    return render_template('RegionalqueryTrends.html',graph15=graph15,graph16=graph16,graph17=graph17,graph18=graph18,graph19=graph19)


    graph13 = Mostfriquent_querytype()
    graph14 = query_distribution()
    return render_template('QueryType_deepDrive.html',graph13=graph13,graph14=graph14)

@app.route('/Regional_query_Trends')
def RegionalqueryTrends():
    graph15 = Top20_district()
    graph16 = querytype_bydistrict()
    graph17 = timetrend_district()
    graph18 = Querytype_blockname()
    graph19 = querytype_districtname()
    return render_template('Regional_query_Trends',graph15=graph15,graph16=graph16,graph17=graph17,graph18=graph18,graph19=graph19)

@app.route('/SectorCategoryTrends')
def sectorCategory_trends():
    graph20 = queryby_sector()
    graph21 = category_breakdown()
    graph22 = sector_vsquerytype()
    return render_template('SectorCategorytrends.html' ,graph20=graph20,graph21=graph21,graph22=graph22)


@app.route('/TemporalTrends')
def TemporalTrends():
    graph23 =  monthly_querytrends()
    graph24 =  yearyquery_count()
    graph25 =  queriesby_day()
    graph26 =  monthlyquery_bysector()
    return render_template('TemporalTrends.html' ,graph23=graph23,graph24=graph24,graph25=graph25,graph26=graph26)  

@app.route('/NaturalLanguageInsights')  
def NaturalLanguageInsights():
    graph27 = word_could()
    graph28 =  sentiment_distribution() 
    return render_template('NaturalLanguageInsights.html ',graph27=graph27,graph28=graph28)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)






