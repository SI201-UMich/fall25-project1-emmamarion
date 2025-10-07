import os
import unittest
import csv


def load_penguin(file_name):
    d = {}

    with open(file_name, mode='r', newline='') as file:
        csv_reader = csv.reader(file)
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
                "species" : species,
                "island" : island,
                "bill_length_mm" : bill_length_mm,
                "bill_depth_mm" : bill_depth_mm,
                "flipper_length_mm" : flipper_length_mm,
                "body_mass_g" : body_mass_g,
                "sex" : sex,
                "year" : year,
            }

    print(d)
            




def calc_average_flipper_length(penguin_data):
    pass

def calculate_chinstrap_percentage(penguin_data):
    pass

def generate_report(flipper_averages, chinstrap_percentage):
    pass

def main():
    load_penguin('penguins.csv')

    pass

if __name__ == "__main__":
    main()