import matplotlib.pyplot as plt
import numpy as np
import aviary.api as av
import matplotlib.cm as cm
from tkinter import Tk, Label, Button, StringVar, IntVar
from tkinter.ttk import Combobox
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
import tkinter as tk
from tkinter import ttk

polar_file = "subsystems/aerodynamics/gasp_based/data/GASP_aero_free.txt"
aero_data = av.read_data_file(polar_file, aliases={
    'altitude': 'altitude',
    'mach': 'mach',
    'angle_of_attack': 'angle_of_attack',
    'lift_coefficient': 'cl',
    'drag_coefficient': 'cd'
})


altitude_values = np.unique(aero_data.get_val('altitude', 'ft'))
mach_values = np.unique(aero_data.get_val('mach', 'unitless'))
mach = aero_data.get_val('mach', 'unitless')
CL = aero_data.get_val('lift_coefficient', 'unitless')
CD = aero_data.get_val('drag_coefficient', 'unitless')


# Plotting function
def plot_polar(ax, CD, CL, color, label=None):
    CD.sort()
    CL.sort()
    z = np.polyfit(CD, CL, 4)
    p = np.poly1d(z)
    ax.plot(CD, p(CD), color=color, label=label)

def update_plot():
    fix_variable = fix_variable_var.get()#Chooses which variable to fix(Mach or Altitude)
    fix_value = float(fix_value_var.get())#Chooses value of fixed variable
    
    fig, ax = plt.subplots()
    fig.subplots_adjust(right=0.75)

    if fix_variable == 'Mach':
        indices = mach == fix_value
        fixed_values = altitude_values
        fixed_label = 'Altitude'
    else:
        indices = aero_data.get_val('altitude', 'ft') == fix_value
        fixed_values = mach_values
        fixed_label = 'Mach'

    colors = cm.viridis(np.linspace(0, 1, len(fixed_values)))

    for i, val in enumerate(fixed_values):
        if fix_variable == 'Mach':
            sub_indices = (mach == fix_value) & (aero_data.get_val('altitude', 'ft') == val)
        else:
            sub_indices = (aero_data.get_val('altitude', 'ft') == fix_value) & (mach == val)
        
        plot_polar(ax, CD[sub_indices], CL[sub_indices], color=colors[i], label=f'{fixed_label} {val}')
        print(CL[sub_indices])

    ax.set_xlabel('CD')
    ax.set_ylabel('CL')
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), title=fixed_label)
    plt.title(f'CL vs CD for fixed {fix_variable} = {fix_value}')
    plt.show()
    
    canvas=FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack()
    toolbar=NavigationToolbar2Tk(canvas,window)
    toolbar.update()
    canvas.get_tk_widget().pack()




# Update fix_value_combobox options
def update_fix_value_combobox(*args):
    if fix_variable_var.get() == 'Mach':
        fix_value_combobox['values'] = ( mach_values)
        fix_value_var.set(str(mach_values[0]))
        fix_value_combobox.current(0)
    else:
        fix_value_combobox['values'] = ( altitude_values)
        fix_value_var.set(str(altitude_values[0]))

# Initialize Tkinter root
window=tk.Tk()

# Variables for Combobox
fix_variable_var = StringVar(value='Mach')
fix_value_var = StringVar(value=float(mach_values[0]))


fix_variable_label = Label(master=window, text="Fix Variable:")
fix_variable_label.grid(row=0, column=0, padx=5, pady=5)
fix_variable_combobox = Combobox(master=window, textvariable=fix_variable_var, values=['Mach', 'Altitude'])
fix_variable_combobox.grid(row=0, column=1, padx=5, pady=5)
fix_variable_combobox.bind("<<ComboboxSelected>>", update_fix_value_combobox)
fix_variable_combobox.current(0)





# Combobox for fixing value
fix_value_label = Label(master=window, text="Fix Value:")
fix_value_label.grid(row=1, column=0, padx=5, pady=5)
fix_value_combobox = Combobox(master=window, textvariable=fix_value_var)
fix_value_combobox.grid(row=1, column=1, padx=5, pady=5)
update_fix_value_combobox()  # Initialize fix_value_combobox

# Button to plot
plot_button = Button(master=window, text="Plot", command=update_plot)
plot_button.grid(row=2, columnspan=2, pady=10)

# Start the Tkinter main loop
window.mainloop()
print(str(mach_values))
print(mach_values)
