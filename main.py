import os
import unittest
import csv


def load_penguin(file_name):
    """ Takes data from a csv file and return it as a nested dictionary where the outermost keys are ids, and the inner keys are each column.
    Args:
        file_name (str): name of csv as a string

    Returns:
        dictionary (dict): csv file's data formatted into a python dict. 
    
    """

    d = {}
    
    # Tries to open file in current directory
    try:
        with open(file_name, mode='r', newline='') as file:

            # Create reader object
            csv_reader = csv.reader(file)

            # Skip the header
            headers = next(csv_reader)

            for row in csv_reader:
                id = row[0]
                species = row[1]
                island = row[2]
                bill_length_mm = row[3]
                bill_depth_mm = row[4]
                flipper_length_mm = row[5]
                body_mass_g = row[6]
                sex = row[7]
                year = row[8]

                d[id] = {
                    headers[1] : species,
                    headers[2] : island,
                    headers[3] : bill_length_mm,
                    headers[4] : bill_depth_mm,
                    headers[5] : flipper_length_mm,
                    headers[6] : body_mass_g,
                    headers[7] : sex,
                    headers[8] : year,
                }

    except FileNotFoundError:
        return f"The file {file_name} was not found"

    return d
            
def calc_average_flipper_length(penguin_data):
    pass

def calculate_chinstrap_percentage(penguin_data):
    pass

def generate_report(flipper_averages, chinstrap_percentage):
    pass

def main():
    penguin_dict = load_penguin('penguins.csv')
    # print(penguin_dict) # for debugging
    calc_average_flipper_length(penguin_dict)

    pass

if __name__ == "__main__":
    main()