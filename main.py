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
    Args: 
        penguin_data (dict): dictionary of penguin data

    Returns:
        flipper_averages (dict): dictionary of averages per island per sex

    """
    
    new_d = {}

    # Unpack dictionary
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

        flipper_averages = {}
        # Unpack the dictionary that we just created
        for island, sex_data in new_d.items():
            flipper_averages[island] = {} 
            for sex, data in sex_data.items():
                avg = data['total'] / data['count']
                flipper_averages[island][sex] = avg

    return flipper_averages


def calculate_chinstrap_percentage(penguin_data):
    """ Calculates the percentage of female Chinstrap penguins with a body mass greater than the average for all female Chinstraps.
    Args:
        penguin_data (dict): dictionary of penguin data
    
    Returns:
        chinstrap_percentage (float): calculation as a float
    """

    female_chinstrap_data = {}
    female_chinstrap_pop = 0
    total_body_mass_g = 0

    for id, penguin_info in penguin_data.items():
        
        # Skip penguins with missing data
        # Use .get to avoid saving variables as strings and re-saving them as ints later.
        if penguin_info.get("sex") == "NA" or penguin_info.get("species") == "NA" or penguin_info.get("body_mass_g") == "NA": 
            continue
        
        species = penguin_info.get("species")
        sex = penguin_info.get("sex")
        body_mass_g = int(penguin_info.get("body_mass_g"))

        body_mass_g = int(body_mass_g)
        # Build a dictionary of only female chinstraps
        if species == "Chinstrap" and sex=="female":
            female_chinstrap_data[id] = {
                "species" : species,
                "sex" : sex,
                "body_mass_g" : body_mass_g
            }

            total_body_mass_g += body_mass_g # Increase total body mass
            female_chinstrap_pop += 1 # Increase the total number of female chinstraps
        
    # Calculate the average body mass of all female chinstraps
    avg_body_mass_g = total_body_mass_g / female_chinstrap_pop

    total_female_chinstraps_above_avg = 0
    for id, chinstrap_data in female_chinstrap_data.items():
        # Check if this chinstrap has an above average body mass
        if chinstrap_data["body_mass_g"] > avg_body_mass_g:
            total_female_chinstraps_above_avg += 1
    
    return (total_female_chinstraps_above_avg / female_chinstrap_pop) * 100
 

def generate_report(flipper_averages, chinstrap_percentage):
    """ Writes the results from each calculation to a .txt file in a readable format
    Args:
        flipper_averages (dict): dictionary of flipper averages
        chinstrap_percentage (float): number of female chinstrips with an above average body mass

    Returns:
        none
    """
    pass

def main():
    penguin_dict = load_penguin('penguins.csv')
    # print(f"PENGUIN DICT: {penguin_dict}") # for debugging
    flipper_averages = calc_average_flipper_length(penguin_dict)
    # print(calc_average_flipper_length(penguin_dict)) # for debugging
    chinstrap_percentage = calculate_chinstrap_percentage(penguin_dict)
    # print(calculate_chinstrap_percentage(penguin_dict)) # for debugging
    generate_report(flipper_averages, chinstrap_percentage)


if __name__ == "__main__":
    main()