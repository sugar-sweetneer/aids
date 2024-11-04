import pandas as pd
from IPython.core.display import display, HTML

url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df = pd.read_csv(url)

chart_data = df.groupby('Sex')['Survived'].sum().reset_index()

html_code = f'''
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">
      google.charts.load('current', {{'packages':['corechart']}});
      google.charts.setOnLoadCallback(drawChart);
      
      function drawChart() {{
        var data = google.visualization.arrayToDataTable([
          ['Gender', 'Survived'],
          ['Male', {chart_data.loc[chart_data['Sex'] == 'male', 'Survived'].values[0]}],
          ['Female', {chart_data.loc[chart_data['Sex'] == 'female', 'Survived'].values[0]}]
        ]);

        var options = {{
          title: 'Survival Count by Gender',
          chartArea: {{width: '50%'}},
          hAxis: {{
            title: 'Survived',
            minValue: 0
          }},
          vAxis: {{
            title: 'Gender'
          }}
        }};

        var chart = new google.visualization.BarChart(document.getElementById('bar_chart'));
        chart.draw(data, options);
      }}
    </script>
    <div id="bar_chart" style="width: 900px; height: 500px;"></div>
'''
display(HTML(html_code))


survived_count = df['Survived'].value_counts()

html_code = f'''
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">
      google.charts.load('current', {{'packages':['corechart']}});
      google.charts.setOnLoadCallback(drawChart);
      
      function drawChart() {{
        var data = google.visualization.arrayToDataTable([
          ['Survived', 'Count'],
          ['Survived', {survived_count[1]}],
          ['Did Not Survive', {survived_count[0]}]
        ]);

        var options = {{
          title: 'Survival Rate',
          pieHole: 0.4,
        }};

        var chart = new google.visualization.PieChart(document.getElementById('pie_chart'));
        chart.draw(data, options);
      }}
    </script>
    <div id="pie_chart" style="width: 900px; height: 500px;"></div>
'''

display(HTML(html_code))



survival_by_class = df.groupby('Pclass')['Survived'].sum().reset_index()

html_code = f'''
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">
      google.charts.load('current', {{'packages':['corechart']}});
      google.charts.setOnLoadCallback(drawChart);
      
      function drawChart() {{
        var data = google.visualization.arrayToDataTable([
          ['Pclass', 'Survived'],
          ['1st Class', {survival_by_class.loc[survival_by_class['Pclass'] == 1, 'Survived'].values[0]}],
          ['2nd Class', {survival_by_class.loc[survival_by_class['Pclass'] == 2, 'Survived'].values[0]}],
          ['3rd Class', {survival_by_class.loc[survival_by_class['Pclass'] == 3, 'Survived'].values[0]}]
        ]);

        var options = {{
          title: 'Survival by Passenger Class',
          hAxis: {{title: 'Class'}},
          vAxis: {{title: 'Survived'}},
          legend: 'none'
        }};

        var chart = new google.visualization.ColumnChart(document.getElementById('column_chart'));
        chart.draw(data, options);
      }}
    </script>
    <div id="column_chart" style="width: 900px; height: 500px;"></div>
'''

display(HTML(html_code))


html_code = '''
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">
      google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(drawChart);
      
      function drawChart() {
        var data = google.visualization.arrayToDataTable([
          ['Age'],
          %s
        ]);

        var options = {
          title: 'Age Distribution of Passengers',
          legend: { position: 'none' },
          histogram: { bucketSize: 5 }
        };

        var chart = new google.visualization.Histogram(document.getElementById('histogram_chart'));
        chart.draw(data, options);
      }
    </script>
    <div id="histogram_chart" style="width: 900px; height: 500px;"></div>
''' % ','.join([f"[{row['Age']}]" for idx, row in df.dropna(subset=['Age']).iterrows()])

display(HTML(html_code))


df['AgeBucket'] = pd.cut(df['Age'], bins=[0, 18, 35, 50, 80], labels=["0-18", "19-35", "36-50", "51+"])
survival_by_age = df.groupby('AgeBucket')['Survived'].sum().reset_index()

html_code = f'''
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">
      google.charts.load('current', {{'packages':['corechart']}});
      google.charts.setOnLoadCallback(drawChart);
      
      function drawChart() {{
        var data = google.visualization.arrayToDataTable([
          ['Age Range', 'Survived'],
          ['0-18', {survival_by_age.loc[survival_by_age['AgeBucket'] == '0-18', 'Survived'].values[0]}],
          ['19-35', {survival_by_age.loc[survival_by_age['AgeBucket'] == '19-35', 'Survived'].values[0]}],
          ['36-50', {survival_by_age.loc[survival_by_age['AgeBucket'] == '36-50', 'Survived'].values[0]}],
          ['51+', {survival_by_age.loc[survival_by_age['AgeBucket'] == '51+', 'Survived'].values[0]}]
        ]);

        var options = {{
          title: 'Survival by Age Range',
          hAxis: {{title: 'Age Range'}},
          vAxis: {{title: 'Survived'}},
          isStacked: true
        }};

        var chart = new google.visualization.AreaChart(document.getElementById('area_chart'));
        chart.draw(data, options);
      }}
    </script>
    <div id="area_chart" style="width: 900px; height: 500px;"></div>
'''

display(HTML(html_code))