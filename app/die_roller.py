import csv
import pandas as pd
import random

class DieRoller:
	def __init__(self, number_of_rolls = 1000, die_faces = 6, filename = "die_results.csv"):
		self.number_of_rolls = number_of_rolls
		self.die_faces = die_faces
		self.filename = filename

	def roll_die(self):
		face_intervals = [(i / self.die_faces, (i + 1) / self.die_faces) for i in range(self.die_faces)] # Output: [(0.0, 0.16666667), ..., (0.83333333, 1.0)]
		face_counts = {i + 1: 0 for i in range(self.die_faces)} # Output: {1:0, 2:0, 3:0, 4:0, 5:0, 6:0}

		for _ in range(self.number_of_rolls):
			random_number = random.random()

			for face, (low, high) in enumerate(face_intervals, start=1):
				if low <= random_number < high:
					face_counts[face] += 1
					break
			
		return face_counts

	def write_to_csv(self):
		face_counts = self.roll_die()

		with open(self.filename, mode="w", newline="") as file:
			writer = csv.writer(file)
			writer.writerow(["Face", "Frequency", "Percentage (%)"])

			for face, freq in face_counts.items():
				percentage = freq / self.number_of_rolls * 100
				writer.writerow([face, freq, f"{percentage:.1f}"])

	def create_table(self):
		df = pd.read_csv(self.filename)

		df["Percentage (%)"] = df["Percentage (%)"].astype(float)

		total_frequency = df["Frequency"].sum()
		total_percentage = df["Percentage (%)"].sum()

		df.loc[len(df.index)] = ["Total", total_frequency, total_percentage]
		
		print(df.to_string(index=False))


if __name__ == "__main__":
	die_roller = DieRoller()
	die_roller.write_to_csv()
	die_roller.create_table()
