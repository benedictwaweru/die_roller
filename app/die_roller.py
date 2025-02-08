'''
Roll a die 1000 times. Use a generator that generates random numbers between 0 and 1 and give results in a table with the following:

Face			Frequency			Percentage(1dp)
1
2
3
4
5
6 				
					Must add to   Must add to
						1000           100.0

Generate a number. Check if it's between a certain range. If it is, assign it to the numbers 1-6
'''

""" import csv
import random

def roll_die(n=1000):
    face_intervals = [(i / 6, (i + 1) / 6) for i in range(6)]
    face_counts = {i + 1: 0 for i in range(6)}
    
    # Simulate rolling the die n times
    for _ in range(n):
        rand_num = random.random()
        for face, (low, high) in enumerate(face_intervals, start=1):
            if low <= rand_num < high:
                face_counts[face] += 1
                break
    
    return face_counts

def save_to_csv(data, filename="die_rolls.csv"):
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Face", "Frequency"])
        for face, freq in data.items():
            writer.writerow([face, freq])
    print(f"Data saved to {filename}")

def main():
    frequencies = roll_die()
    print("Face Frequencies:")
    for face, count in frequencies.items():
        print(f"Face {face}: {count}")
    
    save_to_csv(frequencies)

if __name__ == "__main__":
    main()

 """

import csv
import pandas as pd
import random

class DieRoller:
	def __init__(self, number_of_rolls = 1000, die_faces = 6):
		self.number_of_rolls = number_of_rolls
		self.die_faces = die_faces

	def roll_die(self):
		face_intervals = [(i / self.die_faces, (i + 1) / self.die_faces) for i in range(self.die_faces)]
		face_counts = {i + 1: 0 for i in range(self.die_faces)}

		for _ in range(self.number_of_rolls):
			random_number = random.random()

			for face, (low, high) in enumerate(face_intervals, start=1):
				if low <= random_number < high:
					face_counts[face] += 1
					break
			
		return face_counts

	def write_to_csv(self, filename = "die_results.csv"):
		face_counts = self.roll_die()

		with open(filename, mode="w", newline="") as file:
			writer = csv.writer(file)
			writer.writerow(["Face", "Frequency", "Percentage"])

			for face, freq in face_counts.items():
				percentage = freq / self.number_of_rolls * 100
				writer.writerow([face, freq, f"{percentage:.1f}%"])

	def create_table(self):
		print(pd.read_csv("die_results.csv").to_string(index=False))


if __name__ == "__main__":
	die_roller = DieRoller()
	die_roller.write_to_csv()
	die_roller.create_table()
