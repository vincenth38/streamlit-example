import streamlit as st
import json
import os
import functools

# Define table headers and component types
table_headers = ['Component', 'Parameter 1', 'Parameter 2', 'Parameter 3', 'Parameter 4', 'Pressure Drop', 'Outlet Pressure']
components = ['pipe', 'valve']

# Define input fields
gas_type = st.selectbox('Gas Type:', ['hydrogen', 'nitrogen'])
inlet_pressure = st.number_input('Inlet Pressure (bar):', value=100.0)
inlet_temperature = st.number_input('Inlet Temperature (C):', value=25.0)
mass_flow = st.number_input('Mass Flow (kg/s):', value=1.0)

# Load data from file
def load_data_from_file():
    if os.path.exists("table_data.json"):
        with open("table_data.json", "r") as infile:
            return json.load(infile)
    return []

# Save data to file
def save_data_to_file(table_data):
    with open("table_data.json", "w") as outfile:
        json.dump(table_data, outfile)

# Calculate pressure drop for each component
def calculate_pressure_drop(component_type, param1, param2, param3, param4):
    if component_type == 'pipe':
        # Calculate pressure drop for a pipe (using a dummy calculation)
        pressure_drop = param1 * param2 * param3 * param4 * 0.01
    elif component_type == 'valve':
        # Calculate pressure drop for a valve (using a dummy calculation)
        pressure_drop = param1 * param2 * param3 * param4 * 0.005
    else:
        pressure_drop = 0

    return pressure_drop

table_data = load_data_from_file()
data_changed = False

# Display table and handle user interaction
for i, row_data in enumerate(table_data):
    new_row_data = []
    st.write(f"Row {i + 1}")

    component = st.selectbox(f"Component {i + 1}", components, index=components.index(row_data[0]), key=f"component_{i}")
    new_row_data.append(component)

    for j, param_value in enumerate(row_data[1:]):
        param = st.number_input(f"Parameter {j + 1} ({table_headers[j + 1]})", value=param_value, key=f"param_{i}_{j}")
        new_row_data.append(param)

    if component != row_data[0] or any(p1 != p2 for p1, p2 in zip(row_data[1:], new_row_data[1:])):
        data_changed = True
        table_data[i] = new_row_data

if data_changed:
    save_data_to_file(table_data)

# Calculate pressure drops and update table data
if st.button('Calculate All Pressure Drops'):
    for i, row_data in enumerate(table_data):
        pressure_drop = calculate_pressure_drop(row_data[0], row_data[1], row_data[2], row_data[3], row_data[4])
        table_data[i][5] = pressure_drop
        table_data[i][6] = inlet_pressure - pressure_drop

    save_data_to_file(table_data)

    for i, row_data in enumerate(table_data):
        st.write(f"Row {i + 1}: Pressure Drop = {row_data[5]}, Outlet Pressure = {row_data[6]}")
