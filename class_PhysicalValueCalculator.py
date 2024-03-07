import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import h, k
import tkinter as tk
from tkinter import filedialog
import Labber  # Import Labber for handling lab data

# Define a class to calculate physical values
class PhysicalValueCalculator:
    def __init__(self):
        pass

    # Method to calculate the input noise temperature (T_in)
    def calculate_T_in(self, freq, T_bath, save_data=False, plot_data=False):
        # Calculate T_in using this formula
        T_in = (h * freq / (2 * k)) * np.cosh(h * freq / (2 * k * T_bath)) / np.sinh(h * freq / (2 * k * T_bath))

        if save_data:  # Check if the user wants to save the data
            root = tk.Tk()
            root.withdraw()  # Hide the main window of Tkinter

            exp_name = filedialog.asksaveasfilename(
                filetypes=[('HDF5 files', '*.hdf5')],
                title='Choose the storage location for the hdf5 file'
            )

            lStep = [dict(name='Bath temperature', unit='K', values=T_bath)]
            lLog = [dict(name='Input noise temperature', unit='K', vector=False)]
            
            f = Labber.createLogFile_ForData(exp_name, lLog, lStep)

            data = {'Input noise temperature': T_in}
            f.addEntry(data)  # Add the entry to the log file

        if plot_data:  # Check if the user wants to plot the data
            plt.figure(figsize=(8, 6))
            plt.plot(T_bath, T_in, label="T_in vs. T_bath")
            plt.xlabel("Bath Temperature [K]")
            plt.ylabel("Input noise temperature [K]")
            plt.title("Input noise temperature vs. Bath temperature")
            plt.grid(True)
            plt.legend()
            plt.show()

        return T_in

# Main execution block
if __name__ == "__main__":
    f = 6e9  # Set the frequency in Hz
    T_bath = np.linspace(0.02, 1, 100)
    calculator = PhysicalValueCalculator()
    result = calculator.calculate_T_in(freq=f, T_bath=T_bath, plot_data=True)
    # print(result)
