from flask import Flask, render_template, request  
import plotly.graph_objs as go  
import plotly.offline as pyo  
#initializing the app
app = Flask(__name__)  

@app.route('/', methods=['GET', 'POST'])  
def index():  
    plot_div = ''  
    if request.method == 'POST':  
        try:  
            # Parse data from the form  
            x_values = request.form.get('x_values').split(',')  
            y_values = request.form.get('y_values').split(',')  
            title = request.form.get('title') or "Sample Plot"  
            x_label = request.form.get('x_label') or "X-Axis"  
            y_label = request.form.get('y_label') or "Y-Axis"  
            graph_type = request.form.get('graph_type')  # Get the selected graph type  
            color = request.form.get('color')  # Get the selected color  
            line_style = request.form.get('line_style')  # Get the selected line style  

            # Clean up x_values and y_values  
            x_values = [x.strip() for x in x_values]  # Keep x values as strings  
            y_values = [float(y.strip()) for y in y_values]  # Convert y values to float  

            # Create the plotly plot based on the selected graph type  
            if graph_type == 'bar':  
                plot_data = go.Bar(x=x_values, y=y_values, marker_color=color)  
            elif graph_type == 'pie':  
                plot_data = go.Pie(labels=x_values, values=y_values, marker=dict(colors=[color]*len(y_values)))  
            elif graph_type == 'scatter':  
                plot_data = go.Scatter(x=x_values, y=y_values, mode='lines+markers', line=dict(color=color, dash=line_style))  

            layout = go.Layout(title=title, xaxis=dict(title=x_label), yaxis=dict(title=y_label))  
            figure = go.Figure(data=[plot_data], layout=layout)  

            # Generate HTML for the plot  
            plot_div = pyo.plot(figure, include_plotlyjs=True, output_type='div')  

        except Exception as e:  
            plot_div = f"<div>Error: {str(e)}</div>"  

    return render_template('index.html', plot_div=plot_div)  

if __name__ == '__main__':  
    app.run(debug=True)