from taipy.gui import Gui, notify
import plotly.express as px
import pandas as pd
import numpy as np

# Create sample data
def create_sample_data():
    dates = pd.date_range(start='2024-01-01', periods=100, freq='D')
    values = np.random.randn(100).cumsum()
    df = pd.DataFrame({'Date': dates, 'Value': values})
    return df

# Initialize data
data = create_sample_data()

# Define the page layout
layout = """
<|layout|columns=1 1|
<|
# Taipy + Plotly Demo
This is a simple demonstration of Taipy with Plotly integration.
|>

<|
<|{data}|chart|x=Date|y=Value|mode=lines|title=Sample Time Series|>
|>
|>
"""

# Create and run the GUI
if __name__ == "__main__":
    gui = Gui(page=layout)
    gui.run(title="Taipy Plotly Demo", port=5000)
