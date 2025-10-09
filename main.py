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
    """Calculates the average flipper length for each sex on each island.
    

    """

    # Unpack dictionary
    new_d = {}
    for id, penguin_info in penguin_data.items():

        # Keep as string to check if NA
        flipper_length_str = penguin_info.get("flipper_length_mm")
        sex = penguin_info.get("sex")
        island = penguin_info.get("island")

        # Skip penguins with missing data
        if sex == "NA" or flipper_length_str == "NA" or island == "NA": 
            continue
        
        # If island not already in dictionary, add it
        if island not in new_d:
            new_d[island] = {}

        # If no data for the sex on this island exists, initalize it
        if sex not in new_d[island]:
            new_d[island][sex] = {'total' : 0, 'count' : 0}
        
        
        new_d[island][sex]['total'] += float(flipper_length_str)
        new_d[island][sex]['count'] += 1

        averages = {}
        # Unpack the dictionary that we just created
        for island, sex_data in new_d.items():
            averages[island] = {} 
            for sex, data in sex_data.items():
                avg = data['total'] / data['count']
                averages[island][sex] = avg

    return averages
        
def calculate_chinstrap_percentage(penguin_data):
    pass

def generate_report(flipper_averages, chinstrap_percentage):
    pass

def main():
    penguin_dict = load_penguin('penguins.csv')
    # print(f"PENGUIN DICT: {penguin_dict}") # for debugging
    calc_average_flipper_length(penguin_dict)
    print(calc_average_flipper_length(penguin_dict)) # for debugging

    pass

if __name__ == "__main__":
    main()