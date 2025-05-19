import math
import random
import sys

QUEUE_LIMIT = 1000
BUSY = 1
IDLE = 0

class QueueSimulation:
	def __init__(self):
		""" State variables """
		self.next_event_type = 0
		self.num_custs_delayed = 0
		self.num_delays_required = 0
		self.num_events = 2
		self.num_in_queue = 0
		self.server_status = IDLE

		""" Statistical Counters """
		self.area_num_in_queue = 0.0
		self.area_server_status = 0.0
		self.mean_interarrival = 0.0
		self.mean_service = 0.0
		self.simulation_time = 0.0
		self.time_arrival = [0.0] * (QUEUE_LIMIT + 1)
		self.time_last_event = 0.0
		self.time_next_event = [0.0, 0.0, 0.0]
		self.total_of_delays = 0.0

		""" File handlers """
		self.input_file = None
		self.output_file = None

	def initialize(self):
		self.simulation_time = 0.0

		self.server_status = IDLE
		self.num_in_queue = 0
		self.time_last_event = 0.0

		self.num_custs_delayed = 0
		self.total_of_delays = 0.0
		self.area_num_in_queue = 0.0
		self.area_server_status = 0.0

		self.time_next_event[1] = self.simulation_time + self.expon(self.mean_interarrival)
		self.time_next_event[2] = 1.0e+30

	def timing(self):
		min_time_next_event = 1.0e+29
		self.next_event_type = 0

		for i in range(1, self.num_events + 1):
			if self.time_next_event[i] < min_time_next_event:
				min_time_next_event = self.time_next_event[i]
				self.next_event_type = i

		if self.next_event_type == 0:
			self.output_file.write(f"\nEvent list empty at time {self.simulation_time}")
			sys.exit(1)

		self.simulation_time = min_time_next_event

	def arrive(self):
		self.time_next_event[1] = self.simulation_time + self.expon(self.mean_interarrival)

		if self.server_status == BUSY:
			self.num_in_queue += 1

			if self.num_in_queue > QUEUE_LIMIT:
				self.output_file.write(f"\nOverflow of the array time arrival at")
				self.output_file.write(f" time {self.simulation_time}")
				sys.exit(2)
			
			self.time_arrival[self.num_in_queue] = self.simulation_time
		
		else:
			delay = 0.0
			self.total_of_delays += delay

			self.num_custs_delayed += 1
			self.server_status = BUSY

			self.time_next_event[2] = self.simulation_time + self.expon(self.mean_service)

	def depart(self):
		if self.num_in_queue == 0:
			self.server_status = IDLE
			self.time_next_event[2] = 1.0e+30
		
		else:
			self.num_in_queue -= 1

			delay = self.simulation_time - self.time_arrival[1]
			self.total_of_delays += delay

			self.num_custs_delayed += 1
			self.time_next_event[2] = self.simulation_time + self.expon(self.mean_service)

			for i in range(1, self.num_in_queue + 1):
				self.time_arrival[i] = self.time_arrival[i + 1]

	def report(self):
		self.output_file.write("\n\nAverage delay in queue{:11.3f} minutes\n\n".format(self.total_of_delays / self.num_custs_delayed))
		self.output_file.write("Average number in queue{:10.3f}\n\n".format(self.area_num_in_queue / self.simulation_time))
		self.output_file.write("Server utilization{:15.3f}\n\n".format(self.area_server_status / self.simulation_time))
		self.output_file.write("Time simulation ended{:12.3f} minutes".format(self.simulation_time))

	def update_time_avg_stats(self):
		time_since_last_event = self.simulation_time - self.time_last_event
		self.time_last_event = self.simulation_time

		self.area_num_in_queue += self.num_in_queue * time_since_last_event
		self.area_server_status += self.server_status * time_since_last_event

	def expon(self, mean):
		return -mean * math.log(random.random())
	
	def main(self):
		self.input_file = open("mm1_queue.in", "r")
		self.output_file = open("mm1_queue.out", "w")

		params = self.input_file.readline().strip().split()
		self.mean_interarrival = float(params[0])
		self.mean_service = float(params[1])
		self.num_delays_required = int(params[2])

		self.output_file.write("Single-server queuing system\n\n")
		self.output_file.write(f"Mean interarrival time{self.mean_interarrival:11.3f} minutes\n\n")
		self.output_file.write(f"Mean service time{self.mean_service:16.3f} minutes\n\n")
		self.output_file.write(f"Number of customers{self.num_delays_required:14d}\n\n")

		self.initialize()

		while self.num_custs_delayed < self.num_delays_required:
			self.timing()

			self.update_time_avg_stats()

			if self.next_event_type == 1:
				self.arrive()
			elif self.next_event_type == 2:
				self.depart()
		
		self.report()
		self.input_file.close()
		self.output_file.close()

if __name__ == "__main__":
	simulation = QueueSimulation()
	simulation.main()
