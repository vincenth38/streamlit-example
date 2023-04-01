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

table_data = []


def save_data_to_file(table_data):
    with open("table_data.json", "w") as outfile:
        json.dump(table_data, outfile)


def load_data_from_file():
    if os.path.exists("table_data.json"):
        with open("table_data.json", "r") as infile:
            return json.load(infile)
    return []


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


def add_row():
    row = [components[0]] + [0.0] * 6
    table_data.append(row)
    update_table()


def update_table():
    table = st.empty()

    # Render table
    table.write(table_data, header=table_headers)

    # Render button to add a row
    if st.button("Add Row"):
        add_row()

    # Render action buttons
    for i, row_data in enumerate(table_data):
        with st.container():
            # Component type dropdown
            component_type = st.selectbox('Component Type', components, index=components.index(row_data[0]), key=f"component_type_{i}")

            # Update the component type in the table data
            table_data[i][0] = component_type

            # Parameter inputs
            for j in range(1, 5):
                table_data[i][j] = st.number_input(f"Parameter {j}", value=row_data[j], key=f"parameter_{i}_{j}")

            # Calculate pressure drop and outlet pressure
            pressure_drop = calculate_pressure_drop(*row_data[:5])
            outlet_pressure = inlet_pressure - pressure_drop

            # Update the pressure drop and outlet pressure in the table data
            table_data[i][5] = pressure_drop
            table_data[i][6] = outlet_pressure

            # Display the pressure drop and outlet pressure
            st.write(f"Pressure Drop: {pressure_drop:.2f}")
            st.write(f"Outlet Pressure: {outlet_pressure:.2f}")

    save_data_to_file(table_data)


table_data = load_data_from_file()
update_table()
