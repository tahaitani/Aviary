import matplotlib.pyplot as plt
import numpy as np
import aviary.api as av
from tkinter import * 
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk) 
import tkinter as tk
from tkinter import ttk

# Load data
polar_file = "subsystems/aerodynamics/gasp_based/data/large_single_aisle_1_aero_free_reduced_alpha.txt"
aero_data = av.read_data_file(polar_file, aliases={
    'altitude': 'altitude',
    'mach': 'mach',
    'angle_of_attack': 'angle_of_attack',
    'lift_coefficient': 'cl',
    'drag_coefficient': 'cd'
})

# Extract unique values
altitude_values = np.unique(aero_data.get_val('altitude', 'ft'))
mach_values = np.unique(aero_data.get_val('mach', 'unitless'))
angle_of_attack = np.unique(aero_data.get_val('angle_of_attack', 'deg'))
mach = aero_data.get_val('mach', 'unitless')
CL = aero_data.get_val('lift_coefficient', 'unitless')
CD = aero_data.get_val('drag_coefficient', 'unitless')

print(CD)
def plot_polar(ax, CD, CL, color, label=None):
    CD.sort()
    CL.sort()
    z = np.polyfit(CD, CL, 4)
    p = np.poly1d(z)
    ax.plot(CD, p(CD), color=color, label=label)
fig, ax = plt.subplots()
fig.subplots_adjust(right=0.75)

#fix_variable, fix_value):
def update_plot(_):

    if combobox.current() == 0:
        indices = mach ==combobox_2.get()
        fixed_values = altitude_values
        fixed_label = 'Altitude'
        variable_name = 'altitude'
    else:
        indices = aero_data.get_val('altitude', 'ft') == combobox_2.get()
        fixed_values = mach_values
        fixed_label = 'Mach'
        variable_name = 'mach'
    colors = cm.viridis(np.linspace(0, 1, len(fixed_values)))

    for i, val in enumerate(fixed_values):
        if combobox.current() == 0:
            sub_indices = (mach == combobox_2.get()) & (aero_data.get_val('altitude', 'ft') == val)
        else:
            sub_indices = (aero_data.get_val('altitude', 'ft') == combobox_2.get()) & (mach == val)
        

    
    ax.set_xlabel('CD')
    ax.set_ylabel('CL')
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), title=fixed_label)
    plt.title(f'CL vs CD for fixed {combobox.get()} = {combobox_2.get()}')
    ax.scatter(CD[sub_indices],CL[sub_indices],color=colors[i])
    plot_polar(ax, CD[sub_indices], CL[sub_indices], color=colors[i], label=f'{fixed_label} {val}')  
    
    anvas=FigureCanvasTkAgg(fig,master= window)
    canvas.draw()
    canvas.get_tk_widget().pack()
    toolbar=NavigationToolbar2Tk(canvas, window)
    toolbar.update()
    canvas.get_tk_widget().pack()
        
    # ax.set_xlabel('CD')
    # ax.set_ylabel('CL')
    # ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), title=fixed_label)
    # plt.title(f'CL vs CD for fixed {fix_variable} = {fix_value}')

    # for i, val in enumerate(fixed_values):
    #     if combobox.current == 'Mach':
    #         sub_indices = (mach == fix_value) & (aero_data.get_val('altitude', 'ft') == val)
    #     else:
    #         sub_indices = (aero_data.get_val('altitude', 'ft') == fix_value) & (mach == val)
        
    #     ax.scatter(CD[sub_indices],CL[sub_indices],color=colors[i])
    #     plot_polar(ax, CD[sub_indices], CL[sub_indices], color=colors[i], label=f'{fixed_label} {val}')
    #     canvas=FigureCanvasTkAgg(fig,master= window)
    #     canvas.draw()
    #     canvas.get_tk_widget().pack()
    #     toolbar=NavigationToolbar2Tk(canvas, window)
    #     toolbar.update()
    #     canvas.get_tk_widget().pack()
        
    # ax.set_xlabel('CD')
    # ax.set_ylabel('CL')
    # ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), title=fixed_label)
    # plt.title(f'CL vs CD for fixed {fix_variable} = {fix_value}')


# Create dropdowns and button
window=tk.Tk()
window.title('plot')
window.geometry("500x500")
combobox = ttk.Combobox(master=window, values=('Mach','Altitude'), height=2, width=10, text="Plot")
combobox_2=ttk.Combobox(master=window,values=(mach_values,altitude_values), height=2, width=10)
combobox.bind("<<ComboboxSelected>>",update_plot)
combobox_2.bind("<<ComboboxSelected>>",update_plot)
combobox.pack(side='top')
combobox_2.pack(side='top')
window.mainloop()




