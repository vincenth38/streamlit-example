import streamlit as st
import pandas as pd
import json
import os

# Define table headers and component types
components = ['pipe', 'valve']

# Define input fields
gas_type = st.selectbox('Gas Type:', ['hydrogen', 'nitrogen'])
inlet_pressure = st.number_input('Inlet Pressure (bar):', value=100.0)
inlet_temperature = st.number_input('Inlet Temperature (C):', value=25.0)
mass_flow = st.number_input('Mass Flow (kg/s):', value=1.0)

def load_data():
    if os.path.exists("table_data.json"):
        with open("table_data.json", "r") as infile:
            data = json.load(infile)
            return pd.DataFrame(data)
    else:
        data = {
            "Component": [],
            "Parameter 1": [],
            "Parameter 2": [],
            "Parameter 3": [],
            "Parameter 4": [],
            "Pressure Drop": [],
            "Outlet Pressure": [],
        }
        return pd.DataFrame(data)

def save_data(df):
    with open("table_data.json", "w") as outfile:
        json.dump(df.to_dict(orient='records'), outfile)

def calculate_pressure_drop(row):
    component_type, param1, param2, param3, param4 = row["Component"], row["Parameter 1"], row["Parameter 2"], row["Parameter 3"], row["Parameter 4"]
    
    if component_type == 'pipe':
        pressure_drop = param1 * param2 * param3 * param4 * 0.01
    elif component_type == 'valve':
        pressure_drop = param1 * param2 * param3 * param4 * 0.005
    else:
        pressure_drop = 0
        
    return pressure_drop

def calculate_outlet_pressure(row):
    return inlet_pressure - row["Pressure Drop"]

def update_table(df):
    df["Pressure Drop"] = df.apply(calculate_pressure_drop, axis=1)
    df["Outlet Pressure"] = df.apply(calculate_outlet_pressure, axis=1)

    return df

# Load the data
df = load_data()

# Display the data
st.write(df)

# Add row
if st.button("Add Row"):
    new_row = {
        "Component": "pipe",
        "Parameter 1": 0.0,
        "Parameter 2": 0.0,
        "Parameter 3": 0.0,
        "Parameter 4": 0.0,
        "Pressure Drop": 0.0,
        "Outlet Pressure": inlet_pressure,
    }
    df = df.append(new_row, ignore_index=True)

# Update table with user input
for index, row in df.iterrows():
    with st.container():
        component = st.selectbox("Component", components, index=components.index(row["Component"]), key=f"component_{index}")
        df.at[index, "Component"] = component

        for i in range(1, 5):
            value = st.number_input(f"Parameter {i}", value=row[f"Parameter {i}"], key=f"param_{index}_{i}")
            df.at[index, f"Parameter {i}"] = value

# Recalculate and display updated data
df = update_table(df)

# Save the data
save_data(df)
