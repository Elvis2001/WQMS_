import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from datetime import datetime

data_dir = os.path.join(os.path.dirname(__file__), 'data')

if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# Reads the uploaded dataset
data = pd.read_csv("WQMS/resource/water_consumption_data.csv")

# Defines the features in the dataset
X = data[['Days of the Week', 'Total Water Supply (liters)']]
y_house1 = data['House 1 Consumption (liters)']
y_house2 = data['House 2 Consumption (liters)']
y_house3 = data['House 3 Consumption (liters)']

model_house1 = LinearRegression()
model_house1.fit(X, y_house1)

model_house2 = LinearRegression()
model_house2.fit(X, y_house2)

model_house3 = LinearRegression()
model_house3.fit(X, y_house3)

flow_rate = 100

# Generates predictions for a week based on the given dataset
def weekly_water_prediction(total_water_supply):
    days_of_week = {
        1: 'Monday',
        2: 'Tuesday',
        3: 'Wednesday',
        4: 'Thursday',
        5: 'Friday',
        6: 'Saturday',
        7: 'Sunday'
    }

    predictions_list = []

    for day_encoded in range(1, 8):
        X_new = pd.DataFrame([[day_encoded, total_water_supply]], columns=['Days of the Week', 'Total Water Supply (liters)'])

        prediction_house1 = model_house1.predict(X_new)[0]
        prediction_house2 = model_house2.predict(X_new)[0]
        prediction_house3 = model_house3.predict(X_new)[0]

        total_consumption = prediction_house1 + prediction_house2 + prediction_house3
        convert_2_centiliter_1 = prediction_house1 / 1000
        convert_2_centiliter_2 = prediction_house2 / 1000
        convert_2_centiliter_3 = prediction_house3 / 1000
        time_2_fill_house1 = convert_2_centiliter_1 / flow_rate
        time_2_fill_house2 = convert_2_centiliter_2 / flow_rate
        time_2_fill_house3 = convert_2_centiliter_3 / flow_rate

        predictions_list.append({
            'Day': days_of_week[day_encoded],
            'House 1 (liters)': prediction_house1,
            'Time to Fill House 1': time_2_fill_house1,
            'House 2 (liters)': prediction_house2,
            'Time to Fill House 2': time_2_fill_house2,
            'House 3 (liters)': prediction_house3,
            'Time to Fill House 3': time_2_fill_house3,
            'Total water supplied (liters)': total_consumption
        })

    predictions_df = pd.DataFrame(predictions_list)
    current_date = datetime.now().strftime('%Y-%m-%d')
    current_day = datetime.now().strftime('%A')
    predictions_filename = os.path.join(data_dir, f'water_prediction_data.csv')
    predictions_df.to_csv(predictions_filename, index=False)
    return predictions_df, predictions_filename

# Uses the predicted data to generate thresholds for the system
def control_signals(predictions_df):
    current_day = datetime.now().strftime('%A')
    current_date = datetime.now().strftime('%Y-%m-%d')
    timestamp = datetime.now().strftime('%Y-%m-%d , %H:%M')
    current_day_prediction = predictions_df[predictions_df['Day'] == current_day].iloc[0]

    thresholds = {
        'Day': current_day,
        'Time': timestamp,
        'House 1': current_day_prediction['House 1 (liters)'],
        'House 2': current_day_prediction['House 2 (liters)'],
        'House 3': current_day_prediction['House 3 (liters)'],
        'Time_2_fill_house1': current_day_prediction['Time to Fill House 1'],
        'Time_2_fill_house2': current_day_prediction['Time to Fill House 2'],
        'Time_2_fill_house3': current_day_prediction['Time to Fill House 3']
    }
    thresholds_filename = os.path.join(data_dir, f'water_prediction.json')
    with open(thresholds_filename, 'w') as json_file:
        json.dump(thresholds, json_file, indent=4)

    return thresholds, thresholds_filename

# Plots the linear regression results for each house, save the figures, and display them
def plot_regression(model, X, y, house_name):
    plt.figure(figsize=(10, 6))  # Set figure size

    # Scatter plot of the actual data
    plt.scatter(X['Days of the Week'], y, color='blue', label='Actual Data')

    # Generate predictions using the model
    days_range = np.linspace(X['Days of the Week'].min(), X['Days of the Week'].max(), 100)
    total_water_supply_mean = np.full(days_range.shape, X['Total Water Supply (liters)'].mean())
    X_plot = pd.DataFrame({'Days of the Week': days_range, 'Total Water Supply (liters)': total_water_supply_mean})
    y_pred = model.predict(X_plot)

    # Plot the regression line
    plt.plot(days_range, y_pred, color='green', label='Regression Line')

    # Add labels and title
    plt.xlabel('Days of the Week')
    plt.ylabel(f'{house_name} Consumption (liters)')
    plt.title(f'Linear Regression for {house_name}')
    plt.legend()

    # Save the plot to a file
    plt_filename = os.path.join(data_dir, f'{house_name}_linear_regression.png')
    plt.savefig(plt_filename)
    plt.close()
    print(f"Saved plot: {plt_filename}")

    return plt_filename

water_prediction_data, predictions_filename = weekly_water_prediction(3000)
thresholds, thresholds_filename = control_signals(water_prediction_data)

# Plot the linear regression graphs for each house
house1_plot = plot_regression(model_house1, X, y_house1, 'House 1')
house2_plot = plot_regression(model_house2, X, y_house2, 'House 2')
house3_plot = plot_regression(model_house3, X, y_house3, 'House 3')
