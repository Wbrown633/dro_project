import pandas as pd
import matplotlib.pyplot as plt
import math
import re
from scipy import stats
from dataclasses import dataclass


@dataclass
class log_csv_grouping:
    log_location: str
    csv_location: str
    pump_duration: list[int]
    target_vols: list[float]
    data: pd.DataFrame = None

    def __init__(self, device, log_location, csv_location, pump_duration, target_vols, target_rates) -> None:
        self.device = device
        self.log_location = log_location
        self.csv_location = csv_location
        self.pump_duration = pump_duration
        self.target_vols = target_vols
        self.target_rates = target_rates
        self.data = pd.read_csv(csv_location, header=None)
        self.pump_starts = self.get_start_time()
        self.pump_ends = self.get_end_time()
        self.steps = self.make_steps()
        self.list_of_durations = self.get_step_durations()
        self.list_of_rates = self.get_list_of_rates()
        self.list_of_volumes = self.get_list_of_volumes()

    def get_start_time(self):
        with open(self.log_location, "r") as file:
            log_data = file.read().replace("\n", "")
            list_of_matches = re.findall(
                "Pump step \S+ started at: \d+.\d+", log_data)

        return [float(step.split(": ")[1]) for step in list_of_matches]

    def get_end_time(self):
        return [sum(tup) for tup in zip(self.pump_starts, self.pump_duration)]

    def make_steps(self):
        list_of_steps = []
        for pump_step_start, pump_step_end in zip(self.pump_starts, self.pump_ends):
            step = self.data[(self.data[2] > pump_step_start)
                             & (self.data[2] < pump_step_end)
                             & (self.data[0] > -800)]
            list_of_steps.append(step)

        return list_of_steps

    def plot_self(self):
        # Example in the docs
        # https://matplotlib.org/stable/gallery/lines_bars_and_markers/markevery_demo.html#sphx-glr-gallery-lines-bars-and-markers-markevery-demo-py
        self.slope = []
        fig, axs = plt.subplots(3, 2, figsize=(10, 6), layout="constrained")
        for step_number, (ax, step) in enumerate(zip(axs.flat, self.steps)):
            ax.set_title(f"{self.device} step: {step_number + 1}")
            ax.plot(step[1], step[0])
            slope, intercept, r_value, p_value, std_err = stats.linregress(step[1], step[0])
            # slope is in mm/sec 
            slope = 0.9 * 12.45 * 12.45 * math.pi * slope
            self.slope.append(slope)
        plt.show()

    def get_step_durations(self):
        return [step.iloc[-1, [0, 1]] - step.iloc[0, [0, 1]] for step in self.steps]

    def get_list_of_rates(self):
        '''Return list of rates for given steps in mm/hr'''
        return [abs(dur[0]/dur[1]) * 3600 for dur in self.list_of_durations]

    def get_list_of_volumes(self):
        return [math.pi*pow((12.45/2), 2) * dur[0]/1000 for dur in self.list_of_durations]

    def get_diffs_from_target(self):
        return [abs(actual) - ideal for actual, ideal in zip(self.list_of_volumes, self.target_vols)]

    def calc_slope_error(self):
        return [abs((actual - ideal)/ideal * 100) for actual, ideal in zip(self.slope, self.target_rates)]
        
    def save_data(self):
        self.data.to_csv(f"{self.device}_save_data.csv")

    def summary_stats(self):
        print(f"Slopes: {self.slope}")
        print(f"slope percent error: {self.calc_slope_error()}")
        print(f"diffs: {self.get_diffs_from_target()}")


if __name__ == "__main__":
    pump_duration = [240, 720, 72, 240, 720, 72]
    target_vols = [1.0, 0.2, 1.0, 1.0, 0.2, 1.0]
    target_rates = [-15.0, -1.0, -50, -15.0, -1.0, -50.0]
    cd_04 = log_csv_grouping("CD_04", "cd_04_2023-03-06_14-06-55.log",
                             "dro-2023;03;06;02;45;51cd_04_water_1.csv",
                             pump_duration, target_vols, target_rates)
    cd_06 = log_csv_grouping("CD_06",
                             "cda_2023-03-06_17-59-12_cd_06_water_1.log",
                             "dro-2023;03;06;12;37;22cd_06_water_1.csv",
                             pump_duration,
                             target_vols, target_rates)
    cd_14 = log_csv_grouping("CD_14", "cda_2023-03-06_15-02-53.log",
                             "dro-2023;03;06;03;41;05cd_14_water.csv",
                             pump_duration, target_vols, target_rates)

    data = [cd_04, cd_06, cd_14]

    for d in data:
        d.plot_self()
        d.summary_stats()
        d.save_data()
