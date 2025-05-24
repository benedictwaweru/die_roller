import tkinter as tk
import random
import math

import vehicles

def get_random_color():
	return f"#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}"

class CarSimulationApp:
	CAR_MAKES = [
    "Acura", "Alfa Romeo", "Aston Martin", "Audi", "Bentley", "BMW", "Bugatti", "Buick",
    "Cadillac", "Chevrolet", "Chrysler", "Citroën", "Dacia", "Daewoo", "Daihatsu", "Dodge",
    "Donkervoort", "DS Automobiles", "Eagle", "Ferrari", "Fiat", "Fisker", "Ford", "Genesis",
    "GMC", "Great Wall", "Haval", "Holden", "Honda", "Hummer", "Hyundai", "Infiniti", "Isuzu",
    "Jaguar", "Jeep", "Kia", "Koenigsegg", "Lada", "Lamborghini", "Lancia", "Land Rover", "Lexus",
    "Lincoln", "Lotus", "Lucid", "Mahindra", "Maserati", "Maybach", "Mazda", "McLaren", "Mercedes-Benz",
    "Mercury", "Mini", "Mitsubishi", "Morgan", "Nio", "Nissan", "Noble", "Opel", "Pagani", "Peugeot",
    "Polestar", "Pontiac", "Porsche", "Proton", "RAM", "Renault", "Rivian", "Rolls-Royce", "Saab",
    "Saturn", "Scion", "SEAT", "Škoda", "Smart", "SsangYong", "Subaru", "Suzuki", "Tata", "Tesla",
    "Toyota", "TVR", "Vauxhall", "Volkswagen", "Volvo", "Wiesmann", "Zotye"
	]

	NUMBER_OF_PETALS = 5
	PETAL_COLOR = "orange"
	CENTER_DISK_COLOR = "red"
	STEM_COLOR = "darkgreen"
	CENTER_DISK_RADIUS_RATIO = 0.22
	PETAL_RADIUS_RATIO = 0.40
	PETAL_OFFSET_RATIO = 0.28
	STEM_LENGTH_RATIO = 1.0
	STEM_WIDTH_RATIO = 0.15

	HEADLIGHT_COLOR = "white"

	FLOWER_AVOID_BUFFER = 40
	MIN_FLOWER_X_BOUNDARY = 30

	def __init__(self, root):
		self.root = root
		self.root.title("Assignment 3")

		self.canvas_width = 750
		self.canvas_height = 500

		self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height, bg="lightyellow")
		self.canvas.pack(pady=20)

		control_frame = tk.Frame(root)
		control_frame.pack(pady=10)

		self.car_button = tk.Button(control_frame, text="Car", command=self.draw_car_action)
		self.car_button.grid(row=0, column=0, padx=5, pady=5)

		self.suv_button = tk.Button(control_frame, text="SUV", command=self.draw_suv_action)
		self.suv_button.grid(row=0, column=1, padx=5, pady=5)

		self.truck_button = tk.Button(control_frame, text="Truck", command=self.draw_truck_action)
		self.truck_button.grid(row=0, column=2, padx=5, pady=5)

		self.current_vehicle_object = None
		self.summary_text_id = None

		self.vehicle_footprint_x1 = None
		self.vehicle_footprint_x2 = None

		self.draw_initial_scene()

		self._draw_new_batch_of_flowers()

	def draw_initial_scene(self):
		ground_top_y = self.canvas_height * 0.8

		self.canvas.create_rectangle(0, ground_top_y, self.canvas_width, self.canvas_height, fill="green", outline="darkgreen", tags="ground")

	def clear_dynamic_elements(self):
		self.canvas.delete("vehicle_part")
		self.canvas.delete("flower_part")

	def update_vehicle_summary(self, vehicle_type_on_canvas):
		if self.summary_text_id:
			self.canvas.delete(self.summary_text_id)

		summary_lines = []
		if self.current_vehicle_object:
			make = self.current_vehicle_object.get_make()
			year = self.current_vehicle_object.get_model()
			mileage = self.current_vehicle_object.get_mileage()
			price = self.current_vehicle_object.get_price()

			summary_lines.append(f"Type: {vehicle_type_on_canvas}")
			summary_lines.append(f"Make: {make}")
			summary_lines.append(f"Year: {year}")
			summary_lines.append(f"Mileage: {mileage:,}")
			summary_lines.append(f"Price: ${price:,.2f}")

			if isinstance(self.current_vehicle_object, vehicles.Car):
				summary_lines.append(f"Doors: {self.current_vehicle_object.get_doors()}")
			elif isinstance(self.current_vehicle_object, vehicles.SUV):
				summary_lines.append(f"Capacity: {self.current_vehicle_object.get_pass_cap()} passengers")
			elif isinstance(self.current_vehicle_object, vehicles.Truck):
				summary_lines.append(f"Drive: {self.current_vehicle_object.get_drive_type()}")

			summary_text = "\n".join(summary_lines)

			self.summary_text_id = self.canvas.create_text(15, 15, anchor=tk.NW, text=summary_text, font=("Arial", 11, "bold"), fill="black", tags="summary_info")

		else:
			self.summary_text_id = None
			self.vehicle_footprint_x1 = None
			self.vehicle_footprint_x2 = None

	def draw_vehicle_on_canvas(self, vehicle_type_name):
		self.clear_dynamic_elements()

		body_length = random.randint(120, 220)
		size_factor = random.uniform(0.7, 1.1)
		vehicle_color = get_random_color()
		wheel_color = "darkgray"
		window_color = "lightblue"

		ground_level = self.canvas_height * 0.8
		x_center = self.canvas_width / 2

		self.vehicle_footprint_x1 = x_center - body_length / 2
		self.vehicle_footprint_x2 = x_center + body_length / 2

		random_make = random.choice(self.CAR_MAKES)
		random_year = random.randint(1995, 2024)
		random_mileage = random.randint(5000, 2000000)
		random_price = random.uniform(8000.0, 10000000.0)

		body_height = 50 * size_factor
		wheel_radius = 20 * size_factor
		y_base_for_body_bottom = ground_level - wheel_radius

		vehicle_type_for_summary = vehicle_type_name

		if vehicle_type_name == "Car":
			vehicle_type_for_summary = "Salon"
			random_doors = random.choice([2, 4])

			self.current_vehicle_object = vehicles.Car(make=random_make, model=random_year, mileage=random_mileage, price=random_price, doors=random_doors)
			body_height = 50 * size_factor; wheel_radius = 20 * size_factor

			y_base_for_body_bottom = ground_level - wheel_radius

			body_x1 = self.vehicle_footprint_x1
			body_y1_top = y_base_for_body_bottom - body_height

			body_x2 = self.vehicle_footprint_x2
			body_y2_bottom = y_base_for_body_bottom

			self.canvas.create_rectangle(body_x1, body_y1_top, body_x2, body_y2_bottom, fill=vehicle_color, outline="black", tags="vehicle_part")
			roof_height = 30 * size_factor; roof_inset_factor = 0.15

			self.canvas.create_polygon(body_x1 + body_length * roof_inset_factor, body_y1_top, body_x2 - body_length * roof_inset_factor, body_y1_top, body_x2 - body_length * (roof_inset_factor + 0.1), body_y1_top - roof_height, body_x1 + body_length * (roof_inset_factor + 0.1), body_y1_top - roof_height, fill=vehicle_color, outline="black", tags="vehicle_part")

			win_x1 = body_x1 + body_length * (roof_inset_factor + 0.1) + 5; win_y1_top_edge = body_y1_top - roof_height + 5
			win_y2_bottom_edge = body_y1_top - 5; mid_pillar = body_x1 + body_length / 2 - 2

			self.canvas.create_rectangle(win_x1, win_y1_top_edge, mid_pillar, win_y2_bottom_edge, fill=window_color, outline="black", tags="vehicle_part")
			self.canvas.create_rectangle(mid_pillar + 4, win_y1_top_edge, body_x2 - body_length * (roof_inset_factor + 0.1) - 5, win_y2_bottom_edge, fill=window_color, outline="black", tags="vehicle_part")

			headlight_width = body_length * 0.10 * size_factor; headlight_height = body_height * 0.25
			headlight_y_offset = body_height * 0.20
			hl_x1 = body_x1 + 5; hl_y1 = body_y1_top + headlight_y_offset
			hl_x2 = hl_x1 + headlight_width; hl_y2 = hl_y1 + headlight_height
			self.canvas.create_rectangle(hl_x1, hl_y1, hl_x2, hl_y2, fill=self.HEADLIGHT_COLOR, outline="gray", tags="vehicle_part")

		elif vehicle_type_name == "SUV":
			random_pass_cap = random.randint(5, 8)
			self.current_vehicle_object = vehicles.SUV(make=random_make, model=random_year, mileage=random_mileage, price=random_price, pass_cap=random_pass_cap)

			body_height = 70 * size_factor
			wheel_radius = 25 * size_factor
			y_base_for_body_bottom = ground_level - wheel_radius

			body_x1 = self.vehicle_footprint_x1
			body_y1_top = y_base_for_body_bottom - body_height

			body_x2 = self.vehicle_footprint_x2
			body_y2_bottom = y_base_for_body_bottom

			self.canvas.create_rectangle(body_x1, body_y1_top, body_x2, body_y2_bottom, fill=vehicle_color, outline="black", tags="vehicle_part")

			roof_height = 45 * size_factor
			roof_inset_factor = 0.05

			self.canvas.create_rectangle(body_x1 + body_length * roof_inset_factor, body_y1_top - roof_height, body_x2 - body_length * roof_inset_factor, body_y1_top, fill=vehicle_color, outline="black", tags="vehicle_part")

			win_x_start = body_x1 + body_length * roof_inset_factor + 5
			win_y_start_edge = body_y1_top - roof_height + 5
			win_y_end_edge = body_y1_top - 5
			win_x_end = body_x2 - body_length * roof_inset_factor - 5
			num_windows = 2
			win_width = (win_x_end - win_x_start - (num_windows - 1) * 5) / num_windows

			for i in range(num_windows):
				wx1 = win_x_start + i * (win_width + 5)
				wx2 = wx1 + win_width

				self.canvas.create_rectangle(wx1, win_y_start_edge, wx2, win_y_end_edge, fill=window_color, outline="black", tags="vehicle_part")

			headlight_width = body_length * 0.12 * size_factor
			headlight_height = body_height * 0.20
			headlight_y_offset = body_height * 0.25
			hl_x1 = body_x1 + 7
			hl_y1 = body_y1_top + headlight_y_offset
			hl_x2 = hl_x1 + headlight_width
			hl_y2 = hl_y1 + headlight_height
			self.canvas.create_rectangle(hl_x1, hl_y1, hl_x2, hl_y2, fill=self.HEADLIGHT_COLOR, outline="gray", tags="vehicle_part")

		elif vehicle_type_name == "Truck":
			random_drive_type = random.choice(["2WD", "4WD"])
			self.current_vehicle_object = vehicles.Truck(make=random_make, model=random_year, mileage=random_mileage, price=random_price, drive_type=random_drive_type)

			cab_height= 60 * size_factor
			wheel_radius = 28 * size_factor

			y_base_for_body_bottom = ground_level - wheel_radius
			cab_length_ratio = 0.4; cab_length = body_length * cab_length_ratio

			cab_x1 = self.vehicle_footprint_x1; cab_y1_top = y_base_for_body_bottom - cab_height
			cab_x2 = cab_x1 + cab_length; cab_y2_bottom = y_base_for_body_bottom

			self.canvas.create_rectangle(cab_x1, cab_y1_top, cab_x2, cab_y2_bottom, fill=vehicle_color, outline="black", tags="vehicle_part")
			self.canvas.create_rectangle(cab_x1 + 10, cab_y1_top + 10, cab_x2 - 10, cab_y2_bottom - 10 - cab_height * 0.3, fill=window_color, outline="black", tags="vehicle_part")

			bed_height_ratio = 0.6
			bed_height = cab_height * bed_height_ratio

			bed_x1 = cab_x2
			bed_y1_top = y_base_for_body_bottom - bed_height
			bed_x2 = self.vehicle_footprint_x2
			bed_y2_bottom = y_base_for_body_bottom

			self.canvas.create_rectangle(bed_x1, bed_y1_top, bed_x2, bed_y2_bottom, fill=vehicle_color, outline="black", tags="vehicle_part")

		current_wheel_radius = wheel_radius
		front_wheel_center_x = self.vehicle_footprint_x1 + current_wheel_radius + (body_length * 0.05)
		rear_wheel_center_x = self.vehicle_footprint_x2 - current_wheel_radius - (body_length * 0.05)

		if rear_wheel_center_x <= front_wheel_center_x + 2 * current_wheel_radius:
			front_wheel_center_x = self.vehicle_footprint_x1 + current_wheel_radius + 10
			rear_wheel_center_x = self.vehicle_footprint_x2 - current_wheel_radius - 10

		wheel_y_center = ground_level - current_wheel_radius
		self.canvas.create_oval(front_wheel_center_x - current_wheel_radius, wheel_y_center - current_wheel_radius, front_wheel_center_x + current_wheel_radius, wheel_y_center + current_wheel_radius, fill=vehicle_color, outline="black", tags="vehicle_part")
		self.canvas.create_oval(rear_wheel_center_x - current_wheel_radius, wheel_y_center - current_wheel_radius, rear_wheel_center_x + current_wheel_radius, wheel_y_center + current_wheel_radius, fill=vehicle_color, outline="black", tags="vehicle_part")

		self.update_vehicle_summary(vehicle_type_for_summary)

		if self.current_vehicle_object:
			print(f"\n--- Drawn {vehicle_type_name} ({vehicle_type_for_summary}) ---")

		self._draw_new_batch_of_flowers()

	def _draw_single_flower(self, x_center, y_flower_center, flower_overall_size):
		center_disk_rad = flower_overall_size * self.CENTER_DISK_RADIUS_RATIO
		petal_rad = flower_overall_size * self.PETAL_RADIUS_RATIO
		petal_offset = flower_overall_size * self.PETAL_OFFSET_RATIO

		stem_len = flower_overall_size * self.STEM_LENGTH_RATIO
		stem_wid = max(1, flower_overall_size * self.STEM_WIDTH_RATIO)
		stem_y1 = y_flower_center
		stem_y2 = y_flower_center + stem_len

		self.canvas.create_line(x_center, stem_y1, x_center, stem_y2, fill=self.STEM_COLOR, width=stem_wid, capstyle=tk.ROUND, tags="flower_part")

		for i in range(self.NUMBER_OF_PETALS):
			angle_deg = (360 / self.NUMBER_OF_PETALS) * i - 90
			angle_rad = math.radians(angle_deg)
			petal_center_x = x_center + petal_offset * math.cos(angle_rad)
			petal_center_y = y_flower_center + petal_offset * math.sin(angle_rad)

			self.canvas.create_oval(petal_center_x - petal_rad, petal_center_y - petal_rad, petal_center_x + petal_rad, petal_center_y + petal_rad, fill=self.PETAL_COLOR, outline="", tags="flower_part")
			self.canvas.create_oval(x_center - center_disk_rad, y_flower_center - center_disk_rad, x_center + center_disk_rad, y_flower_center + center_disk_rad, fill=self.CENTER_DISK_COLOR, outline="", tags="flower_part")

	def _draw_new_batch_of_flowers(self):
		num_flowers_to_draw = random.randint(6, 10)
		print(f"\n--- Drawing a new batch of {num_flowers_to_draw} flowers ---")
		ground_line_y = self.canvas_height * 0.8

		max_flower_x_boundary = self.canvas_width - self.MIN_FLOWER_X_BOUNDARY

		for _ in range(num_flowers_to_draw):
			flower_size_param = random.randint(20, 35)
			flower_x = 0

			possible_x_ranges = []

			if self.vehicle_footprint_x1 is not None and self.vehicle_footprint_x2 is not None:
				left_range_end = self.vehicle_footprint_x1 - self.FLOWER_AVOID_BUFFER
				right_range_start = self.vehicle_footprint_x2 + self.FLOWER_AVOID_BUFFER

				if left_range_end > self.MIN_FLOWER_X_BOUNDARY:
					possible_x_ranges.append((self.MIN_FLOWER_X_BOUNDARY, int(left_range_end)))
				
				if right_range_start < max_flower_x_boundary:
					possible_x_ranges.append((int(right_range_start), max_flower_x_boundary))

				if not possible_x_ranges:
					flower_x = random.randint(self.MIN_FLOWER_X_BOUNDARY, max_flower_x_boundary)

				else:
					chosen_range = random.choice(possible_x_ranges)
					if chosen_range[0] >= chosen_range[1]:
						flower_x = chosen_range[0]
					else:
						flower_x = random.randint(chosen_range[0], chosen_range[1])

			else:
				flower_x = random.randint(self.MIN_FLOWER_X_BOUNDARY, max_flower_x_boundary)

			head_radius_above_center = self.PETAL_OFFSET_RATIO * flower_size_param + self.PETAL_RADIUS_RATIO * flower_size_param
			stem_base_target_y = ground_line_y - 5

			y_flower_center = stem_base_target_y - (self.STEM_LENGTH_RATIO * flower_size_param)
			min_y_allowable = head_radius_above_center + 5
			max_y_allowable = self.canvas_height - 5

			if y_flower_center + (self.STEM_LENGTH_RATIO * flower_size_param) > max_y_allowable:
				y_flower_center = max_y_allowable - (self.STEM_LENGTH_RATIO * flower_size_param)

			if y_flower_center - head_radius_above_center < min_y_allowable:
				y_flower_center = min_y_allowable + head_radius_above_center


			self._draw_single_flower(flower_x, int(y_flower_center), flower_size_param)

	def draw_car_action(self):
		self.draw_vehicle_on_canvas("Car")
	
	def draw_suv_action(self):
		self.draw_vehicle_on_canvas("SUV")

	def draw_truck_action(self):
		self.draw_vehicle_on_canvas("Truck")

if __name__ == "__main__":
	main_window = tk.Tk()
	app = CarSimulationApp(main_window)
	main_window.mainloop()
