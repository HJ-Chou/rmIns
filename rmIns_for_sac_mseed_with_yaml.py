# ----------------------------------------------------------------------------------------------------
# HJC
# IESDMC
# 2024-12-11
# ver1.0
# ----------------------------------------------------------------------------------------------------
import os
import sys
import yaml
import numpy as np
from obspy import read, read_inventory


def yaml_read(yaml_path):
    """
    Reads yaml config file and extracts required param.

    Parameters:
    yaml_path (str): The file path of the yaml config file.

    Returns:
    required param in str
        - input_data_path: Path to the input data file.
        - xml_path: Path to the XML configuration file.
        - output_units: Desired output units (e.g., displacement, velocity, or acceleration).
        - output_file: Path for the output file to be saved.
    """
    # Read YAML file containing building information
    with open(yaml_path, 'r') as tmp:
        yaml_config = yaml.safe_load(tmp)

    # Extract config info
    RmIns_config = 'RmIns_config'
    input_data_path = yaml_config[RmIns_config]['input_data']
    xml_path = yaml_config[RmIns_config]['xml']
    output_units = yaml_config[RmIns_config]['output_units'].upper()
    output_format = yaml_config[RmIns_config]['output_format'].upper()
    output_folder = yaml_config[RmIns_config]['output_folder']

    return input_data_path, xml_path, output_units, output_format, output_folder


def write_output_file(tr, station, network, location, channel, input_format, output_format, output_folder):
    if output_format == 'SAC':
        tr.write(os.path.join(output_folder, f"{station}.{network}.{location}.{channel}_rmIns_{output_units}.sac"), format='SAC')
    else:
        if input_format=='SAC' and output_format=='DEFAULT':
            tr.write(os.path.join(output_folder, f"{station}.{network}.{location}.{channel}_rmIns_{output_units}.sac"), format='SAC')
        else:
            # Determine appropriate encoding based on dtype
            if tr.data.dtype == np.int16:
                output_encoding = "INT16"
            elif tr.data.dtype == np.int32:
            # Use STEIM2 for integer data (compressed format)
                output_encoding = "STEIM2"
            elif tr.data.dtype == np.float32:
                output_encoding = "FLOAT32"
            elif tr.data.dtype == np.float64:
            # FLOAT64 is not supported in MiniSEED; must downcast
                #print(f"Warning: Converting FLOAT64 to FLOAT32 for trace {tr.id}")
                tr.data = tr.data.astype(np.float32)
                output_encoding = "FLOAT32"
            else:
                raise ValueError(f"Unsupported data type {tr.data.dtype} for MiniSEED")

            # Set the encoding for writing
            try:
                tr.write(os.path.join(output_folder, f"{station}.{network}.{location}.{channel}_rmIns_{output_units}.mseed"), format='MSEED', encoding=output_encoding)
            except Exception as e:
                print(f"Error: {e}")
                sys.exit(1)


def remove_instrument_response(input_data_path, xml_path, output_units, output_format, output_folder):
    """
    Remove the instrument response.
    Processed files will be saved in the same format as the input.

    :param data_path: Path to the input data file (SAC or MiniSEED).
    :param response_path: Path to the instrument response StationXML file.
    """

    # Load seismic data
    print(f"Loading seismic data: {input_data_path}")
    st = read(input_data_path)

    # Load the full inventory (StationXML)
    print(f"Loading full inventory: {xml_path}")
    input_inventory = read_inventory(xml_path)

    # Process each trace in the stream
    for tr in st:
        station = tr.stats.station
        network = tr.stats.network
        location = tr.stats.location
        channel = tr.stats.channel
        
        input_format = tr.stats._format
        print(network, station, location, channel)
        # Select the relevant part of the inventory
        print(f"Selecting inventory for station: {station}, channel: {channel}")
        try:
            selected_inventory = input_inventory.select(station=station, network=network, location=location, channel=channel)
        except Exception as e:
            print(f"Error selecting inventory for trace {tr.id}: {e}. Skipping.")
            continue

        # Remove the instrument response
        try:
            print(f"Removing instrument response for trace {tr.id}")
            tr.remove_response(inventory=input_inventory, output=output_units, pre_filt=None)
            write_output_file(tr, station, network, location, channel, input_format, output_format, output_folder)
        except Exception as e:
            print(f"Error removing instrument response for trace {tr.id}: {e}. Skipping.")
            continue


if __name__ == "__main__":
    # input param check
    try:
        pwd = os.getcwd()
        yaml_path = os.path.join(pwd, 'rmIns_config.yaml')
        if not os.path.exists(yaml_path):
            raise FileNotFoundError(f"Error: can't found yaml file: '{yaml_path}', please check the path to yaml.")

        # yaml param
        input_data_path, xml_path, output_units, output_format, output_folder = yaml_read(yaml_path)

        # check yaml param
        if output_units.upper() not in ['ACC', 'VEL', 'DISP']:
            raise FileNotFoundError(f"Error: parameter  output unit is wrong, please check the yaml content.")

        if output_format.upper() not in ['MSEED', 'SAC', 'DEFAULT']:
            raise FileNotFoundError(f"Error: parameter output file format is wrong, please check the yaml content.")

        if not os.path.isfile(input_data_path):
            raise FileNotFoundError(f"Error: can't found the input data file: '{input_data_path}', please check the yaml content.")

        if not os.path.isfile(xml_path):
            raise FileNotFoundError(f"Error: can't found the xml file:'{xml_path}', please check the yaml content.")

        if not os.path.isdir(output_folder):
            raise FileNotFoundError(f"Error: can't found the output file folder:'{output_folder}', please check the yaml content.")

    except FileNotFoundError as e:
        print(e)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)
    
    print("st rmIns")    
    try:
        remove_instrument_response(input_data_path, xml_path, output_units, output_format, output_folder)

    except ValueError as e:
        print(f"Error: {e}")
