import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import h, k
import tkinter as tk
from tkinter import filedialog
import Labber  # Import Labber for handling lab data

# Define a class to convert physical values
class PhysicalValueConverter:
    def __init__(self):
        pass

    def dBm_to_W(self, dBm, save_data = False, plot_data = False):
        power = (1/1000) * (10**(dBm/10))
        if plot_data:
            plot_attributes = {
                "title": "dBm to Watt Conversion",
                "x_label": "Power [dBm]",
                "y_label": "Power [W]",
            }
            self._plotter(dBm, power, plot_attributes)

        if save_data:
            data_attributes = {
                "x_label": "Power in dBm",
                "y_label": "Power in W",
                "x_unit": "dBm",
                "y_unit": "W"
            }
            self._HDF5_saver(dBm, power, data_attributes)

        return power

    def dBm_to_Vrms(self, dBm, impedance = 50, save_data = False, plot_data = False):
        Vrms = np.sqrt((impedance/1000) * (10**(dBm/10)))

        if plot_data:
            plot_attributes = {
                "title": "dBm to Root Mean Square Voltage Conversion",
                "x_label": "Power [dBm]",
                "y_label": "Vrms [V]",
            }
            self._plotter(dBm, Vrms, plot_attributes)

        if save_data:
            data_attributes = {
                "x_label": "Power",
                "y_label": "Vrms",
                "x_unit": "dBm",
                "y_unit": "V"
            }
            self._HDF5_saver(dBm, Vrms, data_attributes)

        return Vrms
    
    def _plotter(self, x, y, plot_attributes):
        plt.figure(figsize=(8, 6))
        plt.plot(x, y)
        plt.xlabel(plot_attributes["x_label"])
        plt.ylabel(plot_attributes["y_label"])
        plt.title(plot_attributes["title"])
        plt.grid(True)
        plt.show()

    def _HDF5_saver(self, x, y, data_attributes):
        root = tk.Tk()
        root.withdraw()  # Hide the main window of Tkinter

        exp_name = filedialog.asksaveasfilename(
            filetypes=[('HDF5 files', '*.hdf5')],
            title='Choose the storage location for the hdf5 file'
        )

        lStep = [dict(name=data_attributes["x_label"], unit=data_attributes["x_unit"], values=x)]
        lLog = [dict(name=data_attributes["y_label"], unit=data_attributes["y_unit"], vector=False)]
        
        f = Labber.createLogFile_ForData(exp_name, lLog, lStep)

        data = {data_attributes["y_label"]: y}
        f.addEntry(data)  # Add the entry to the log file

# Main execution block
if __name__ == "__main__":
    converter = PhysicalValueConverter()
    dBm_array = np.linspace(-128, -125, 100)
    # dBm_array = -128
    result = converter.dBm_to_W(dBm_array, plot_data = True, save_data= True)
    print(result)
