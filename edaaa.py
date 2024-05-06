from flask import Flask, render_template, request
import pandas as pd
import os
from io import StringIO, BytesIO
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import base64

app = Flask(__name__)

# Specify the template folder explicitly
#app.template_folder = os.path.abspath('templates')

@app.route('/')
def home():
    return render_template('example.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return render_template('example.html', error='No file part')

    file = request.files['file']

    if file.filename == '':
        return render_template('example.html', error='No selected file')

    if file:
        # Check file extension
        file_extension = os.path.splitext(file.filename)[1].lower()

        if file_extension == '.xlsx':
            df = pd.read_excel(file)
        else:
            return render_template('example.html', error='Unsupported file format. Please upload Excel (.xlsx) ')

        # Calculate missing values
        missing_values = df.isnull().sum()

        # Display missing values as a table
        missing_values_table = missing_values[missing_values > 0].to_frame(name='Missing Values').sort_values(by='Missing Values', ascending=False)

        # Convert the table to HTML
        missing_values_html = missing_values_table.to_html(classes='data')

        # Exclude non-numeric columns from the DataFrame
        numeric_columns = df.select_dtypes(include=['number']).columns
        df_numeric = df[numeric_columns]

        # Perform EDA on the numeric DataFrame
        describe_results = df_numeric.describe().to_html(classes='data')

        # Redirect info output to a string
        info_buffer = StringIO()
        df.info(buf=info_buffer, verbose=True)  # Set verbose to True
        info_results = info_buffer.getvalue()

        # Extract unique values from each numeric column
        unique_values = {col: df_numeric[col].unique() for col in df_numeric.columns}

        # Extract column datatypes
        column_datatypes = {col: str(df.dtypes[col]) for col in df.columns}

        # Compute correlation matrix
        correlation_matrix = df_numeric.corr()

        # Generate heatmap
        fig, ax = plt.subplots(figsize=(12, 8))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=.5, ax=ax)
        ax.set_title('Correlation Heatmap')

        # Save the heatmap plot to a BytesIO object
        heatmap_stream = BytesIO()
        FigureCanvasAgg(fig).print_png(heatmap_stream)
        heatmap_image = base64.b64encode(heatmap_stream.getvalue()).decode('utf-8')

        # Generate box plots for each numeric column
        boxplot_images = {}
        for col in df_numeric.columns:
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.boxplot(x=df_numeric[col], ax=ax)
            ax.set_title(f'Box Plot - {col}')
            boxplot_stream = BytesIO()
            FigureCanvasAgg(fig).print_png(boxplot_stream)
            boxplot_images[col] = base64.b64encode(boxplot_stream.getvalue()).decode('utf-8')

        # Generate pair plot
        pairplot_fig = sns.pairplot(df_numeric)
        pairplot_stream = BytesIO()
        pairplot_fig.savefig(pairplot_stream, format='png')
        pairplot_image = base64.b64encode(pairplot_stream.getvalue()).decode('utf-8')

        return render_template('resultexample.html',
                               df=df,
                               describe_results=describe_results,
                               info_results=info_results,
                               unique_values=unique_values,
                               column_datatypes=column_datatypes,
                               heatmap_image=heatmap_image,
                               boxplot_images=boxplot_images,
                               missing_values_table=missing_values_html,
                               pairplot_image=pairplot_image)

if __name__ == '__main__':
    app.run(debug=True)
