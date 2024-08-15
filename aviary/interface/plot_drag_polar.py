import matplotlib.pyplot as plt
import numpy as np
import aviary.api as av
import matplotlib.cm as cm
from tkinter import  Label, Button, StringVar
from tkinter.ttk import Combobox
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
import tkinter as tk
from aviary.utils.functions import get_path

def plot_drag_polar(file_path):
    input =get_path('utils/test/polar_data.csv')
    polar_data=av.read_data_file(input,aliases={'altitude':'altitude','mach_number':'mach_number', 'alpha':'angle_of_attack','CL':'lift_coefficient','CD':'total_drag_coefficient'})
    mach=polar_data.get_val('mach_number')
    mach_values=np.unique(mach)
    altitude=polar_data.get_val('altitude')
    altitude_values=np.unique(altitude)
    alpha_values=polar_data.get_val('alpha')
    CD_values=polar_data.get_val('CD')
    CL_values=polar_data.get_val('CL')

    window=tk.Tk()
    window.title('Drag Polar Plot')
    fig, (ax,ax2) = plt.subplots(nrows=2)
    fig.tight_layout(pad=4)
    canvas=FigureCanvasTkAgg(fig, master=window)
    canvas.get_tk_widget().pack(expand=True,fill='both')
    toolbar=NavigationToolbar2Tk(canvas,window)
        
    def plot_polar(ax, CD, CL, color, label=None,marker='o'):
        ax.plot(CD,CL, color=color, label=label,marker='o')

    def update_plot():
        fix_variable = fix_variable_var.get()
        fix_value = float(fix_value_var.get())
        ax.clear()
        ax2.clear()
        if fix_variable == 'Mach':
            indices = mach == fix_value 
            fixed_values = altitude_values
            fixed_label = 'Altitude'
        else:
            indices=altitude==fix_value
            fixed_values = mach_values
            fixed_label = 'Mach'
        colors = cm.viridis(np.linspace(0, 1, len(fixed_values)))
        for i, val in enumerate(fixed_values):
            if fix_variable == 'Mach':
                indices= (mach == fix_value) & (altitude == val)
                CD=np.array(CD_values[indices])
                CL=CL_values[indices]     
            else:
                index = (altitude== fix_value) & (mach== val)
                CD=np.array(CD_values[indices])
                CL=CL_values[indices]
            plot_polar(ax, CD, CL, color=colors[i], label=f'{fixed_label} {val}')
            plot_polar(ax2, CL, np.array(CL)/np.array(CD), color=colors[i], label=f'{fixed_label} {val}')
            ax.set_xlabel('CL')
            ax.set_ylabel('CD')
            ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), title=fixed_label)
            ax.set_title(f'CL vs CD for fixed {fix_variable} = {fix_value}')
            ax2.set_xlabel('CL')
            ax2.set_ylabel('CL/CD')
            ax2.legend(loc='center left', bbox_to_anchor=(1, 0.5), title=fixed_label)
            ax2.set_title(f'CL/CD vs CL for fixed {fix_variable} = {fix_value}')       
            canvas.draw()
            toolbar.update()

    def update_fix_value_combobox(*args):
        if fix_variable_var.get() == 'Mach':
            fix_value_combobox['values'] = [str(value) for value in mach_values]
            fix_value_var.set(str(mach_values[0]))
            fix_value_combobox.current(0)
        else:
            fix_value_combobox['values'] = [str(value) for value in altitude_values]
            fix_value_var.set(str(altitude_values[0]))

    fix_variable_var = StringVar(value='Mach')
    fix_value_var = StringVar(value=float(mach_values[0]))
    fix_variable_label = Label(master=window, text="Fix Variable:")
    fix_variable_label.pack()
    fix_variable_combobox = Combobox(master=window, textvariable=fix_variable_var, values=['Mach', 'Altitude'])
    fix_variable_combobox.pack()
    fix_variable_combobox.bind("<<ComboboxSelected>>", update_fix_value_combobox)
    fix_variable_combobox.current(0)
    fix_value_label = Label(master=window, text="Fix Value:")
    fix_value_label.pack()
    fix_value_combobox = Combobox(master=window, textvariable=fix_value_var)
    fix_value_combobox.pack()
    update_fix_value_combobox()
    plot_button = Button(master=window, text="Plot", command=update_plot)
    plot_button.pack()
    window.mainloop()


def _setup_plot_drag_polar_parser(parser):
    """
    Set up the command line options for the Model Building tool.
    Parameters
    ----------
    parser : argparse.ArgumentParser
        The parser instance.
    parser : argparse subparser
        The parser we're adding options to.
    """
    parser.add_argument('file_path',type=str, help='csv file path')

def _exec_plot_drag_polar(options, user_args):
    """
    Run the Model Building tool.
    Parameters
    ----------
    options : argparse.Namespace
        Command line options.
    user_args : list of str
        Args to be passed to the user script.
    """
    plot_drag_polar(options.file_path)


if __name__ == "__main__":
    plot_drag_polar()