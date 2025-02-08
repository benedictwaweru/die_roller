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
