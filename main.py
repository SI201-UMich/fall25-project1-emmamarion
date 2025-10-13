# Name: Emma Marion
# Student ID: 63863051
# Email: emarion@umich.edu
# Who or what you worked with on this homework (including generative AI like ChatGPT):
# I worked by myself, and used Gemini to help me debug issues after making a strong attempt myself.
# I also used it to help me brainstorm test case ideas.

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

                # Save everything as a string so we can filter out "NA" values later.
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
    flipper_averages = {}

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

        # Build a dictionary of only female chinstraps
        if species == "Chinstrap" and sex=="female":
            female_chinstrap_data[id] = {
                "species" : species,
                "sex" : sex,
                "body_mass_g" : body_mass_g
            }

            total_body_mass_g += body_mass_g # Add total body mass
            female_chinstrap_pop += 1 # Increase the total number of female chinstraps
    # If no female chinstraps were found, return 0.0
    if female_chinstrap_pop == 0:
        return 0.0

    # Calculate the average body mass of all female chinstraps
    avg_body_mass_g = total_body_mass_g / female_chinstrap_pop

    total_female_chinstraps_above_avg = 0

    # Iterate through each female chinstrap
    for id, chinstrap_data in female_chinstrap_data.items():
        # Check if this chinstrap has an above average body mass
        if chinstrap_data["body_mass_g"] > avg_body_mass_g:
            total_female_chinstraps_above_avg += 1  # Add to count
    
    return (total_female_chinstraps_above_avg / female_chinstrap_pop) * 100
 

def generate_report(flipper_averages, chinstrap_percentage):
    """ Writes the results from each calculation to a .txt file in a readable format
    Args:
        flipper_averages (dict): dictionary of flipper averages
        chinstrap_percentage (float): number of female chinstrips with an above average body mass

    Returns:
        none
    """
    filename = "penguin_calculations.txt"

    # open .txt file in write mode
    with open(filename, "w") as f:
        f.write("Penguin Data Analysis Report\n")
        f.write("===========================\n\n")

        f.write("Average Flipper Length (mm) by Island and Sex:\n")
        for island, sex_data in flipper_averages.items():
            f.write(f"- {island}\n")
            for sex, avg in sex_data.items():
                f.write(f"  - {sex.capitalize()}: {avg:.2f} mm\n")
        
        f.write("\n")
        f.write("Chinstrap Penguin Analysis:\n")
        f.write(f"Percentage of female Chinstraps with above-average body mass: {chinstrap_percentage:.2f}%\n")


def main():
    penguin_dict = load_penguin('penguins.csv')
    # print(f"PENGUIN DICT: {penguin_dict}") # for debugging
    flipper_averages = calc_average_flipper_length(penguin_dict)
    # print(calc_average_flipper_length(penguin_dict)) # for debugging
    chinstrap_percentage = calculate_chinstrap_percentage(penguin_dict)
    # print(calculate_chinstrap_percentage(penguin_dict)) # for debugging
    generate_report(flipper_averages, chinstrap_percentage)


class TestPenguinCalculations(unittest.TestCase):
    def test_calc_average_flipper_length_general_1(self):
        """ General test with simple, clean data. """
        data = {
            '1': {'species': 'Adelie', 'island': 'Torgersen', 'bill_length_mm': '39.1', 'bill_depth_mm': '18.7', 'flipper_length_mm': '181', 'body_mass_g': '3750', 'sex': 'male', 'year': '2007'},
            '2': {'species': 'Adelie', 'island': 'Torgersen', 'bill_length_mm': '39.5', 'bill_depth_mm': '17.4', 'flipper_length_mm': '186', 'body_mass_g': '3800', 'sex': 'female', 'year': '2007'},
            '3': {'species': 'Gentoo', 'island': 'Biscoe', 'bill_length_mm': '46.1', 'bill_depth_mm': '13.2', 'flipper_length_mm': '211', 'body_mass_g': '4500', 'sex': 'female', 'year': '2007'}
        }
        result = calc_average_flipper_length(data)
        self.assertAlmostEqual(result['Torgersen']['male'], 181.0)
        self.assertAlmostEqual(result['Torgersen']['female'], 186.0)
        self.assertAlmostEqual(result['Biscoe']['female'], 211.0)

    def test_calc_average_flipper_length_general_2(self):
        """ General test with multiple penguins per category to test averaging. """
        data = {
            '1': {'flipper_length_mm': '180', 'sex': 'male', 'island': 'Torgersen'},
            '2': {'flipper_length_mm': '190', 'sex': 'male', 'island': 'Torgersen'}, # Avg for Torgersen male = 185
            '3': {'flipper_length_mm': '210', 'sex': 'female', 'island': 'Biscoe'},
            '4': {'flipper_length_mm': '220', 'sex': 'female', 'island': 'Biscoe'}  # Avg for Biscoe female = 215
        }
        result = calc_average_flipper_length(data)
        self.assertAlmostEqual(result['Torgersen']['male'], 185.0)
        self.assertAlmostEqual(result['Biscoe']['female'], 215.0)

    def test_calc_average_flipper_length_edge_empty(self):
        """ Edge case test with an empty input dictionary. """
        data = {}
        result = calc_average_flipper_length(data)
        self.assertEqual(result, {})

    def test_calc_average_flipper_length_edge_na_values(self):
        """ Edge case test to ensure 'NA' values are skipped correctly. """
        data = {
            '1': {'flipper_length_mm': '180', 'sex': 'male', 'island': 'Torgersen'},
            '2': {'flipper_length_mm': 'NA', 'sex': 'male', 'island': 'Torgersen'},
            '3': {'flipper_length_mm': '210', 'sex': 'NA', 'island': 'Biscoe'},
            '4': {'flipper_length_mm': '220', 'sex': 'female', 'island': 'NA'}
        }
        result = calc_average_flipper_length(data)
        self.assertEqual(result, {'Torgersen': {'male': 180.0}}) # Only the first penguin is valid

    def test_calculate_chinstrap_percentage_general_1(self):
        """ General test with a simple 50% split. """
        data = {
            '1': {'species': 'Chinstrap', 'sex': 'female', 'body_mass_g': '3000'},
            '2': {'species': 'Chinstrap', 'sex': 'female', 'body_mass_g': '4000'}, # Avg = 3500, this one is above
            '3': {'species': 'Adelie', 'sex': 'female', 'body_mass_g': '5000'} # Should be ignored
        }
        result = calculate_chinstrap_percentage(data)
        self.assertAlmostEqual(result, 50.0)

    def test_calculate_chinstrap_percentage_general_2(self):
        """ General test with more varied data. """
        data = {
            '1': {'species': 'Chinstrap', 'sex': 'female', 'body_mass_g': '3200'},
            '2': {'species': 'Chinstrap', 'sex': 'female', 'body_mass_g': '3400'},
            '3': {'species': 'Chinstrap', 'sex': 'female', 'body_mass_g': '3600'}, # Above avg
            '4': {'species': 'Chinstrap', 'sex': 'female', 'body_mass_g': '3800'}, # Above avg
            '5': {'species': 'Chinstrap', 'sex': 'male', 'body_mass_g': '6000'},   # Ignored (male)
        }
        # Total mass = 3200+3400+3600+3800 = 14000. Count = 4. Avg = 3500.
        # Two are above average (3600, 3800).
        result = calculate_chinstrap_percentage(data)
        self.assertAlmostEqual(result, 50.0) # (2/4) * 100

    def test_calculate_chinstrap_percentage_edge_no_chinstraps(self):
        """ Edge case test where no female Chinstraps exist, which could cause a ZeroDivisionError. """
        data = {
            '1': {'species': 'Adelie', 'sex': 'female', 'body_mass_g': '3000'},
            '2': {'species': 'Gentoo', 'sex': 'female', 'body_mass_g': '4000'}
        }
        result = calculate_chinstrap_percentage(data)
        self.assertEqual(result, 0.0)

    def test_calculate_chinstrap_percentage_edge_all_same_mass(self):
        """ Edge case test where all body masses are identical. """
        data = {
            '1': {'species': 'Chinstrap', 'sex': 'female', 'body_mass_g': '3500'},
            '2': {'species': 'Chinstrap', 'sex': 'female', 'body_mass_g': '3500'}
        }
        # The average is 3500. No penguin has a mass > 3500.
        result = calculate_chinstrap_percentage(data)
        self.assertAlmostEqual(result, 0.0)

    

if __name__ == "__main__":
    main() # Run calculations and create 
    unittest.main() # Unittests