import matplotlib.pyplot as plt
import numpy as np
import aviary.api as av
import matplotlib.cm as cm
from tkinter import Tk, Label, Button, StringVar, IntVar
from tkinter.ttk import Combobox
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
import tkinter as tk
from tkinter import ttk
import unittest
import tempfile

import numpy as np
from pathlib import Path

from openmdao.utils.assert_utils import assert_near_equal
from openmdao.utils.testing_utils import use_tempdirs

from aviary.utils.functions import get_path
from aviary.utils.aero_table_conversion import _load_flops_aero_table, _load_gasp_aero_table, _exec_ATC


expected_cd0_alt = np.array([0,  5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000, 55000, 60000, 0,  5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000, 55000, 60000, 0,  5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000, 55000, 60000, 0, 5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000, 55000, 60000, 0,  5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000, 55000, 60000, 0,  5000, 10000, 15000, 20000,
                                     25000, 30000, 35000, 40000, 45000, 50000, 55000, 60000, 0,  5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000, 55000, 60000, 0,  5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000, 55000, 60000, 0,  5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000, 55000, 60000, 0,  5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000, 55000, 60000, 0,  5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000, 55000, 60000])
expected_cd0_mach = np.array([0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7,
                            0.7, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.775, 0.775, 0.775, 0.775, 0.775, 0.775, 0.775, 0.775, 0.775, 0.775, 0.775, 0.775, 0.775, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.825, 0.825, 0.825, 0.825, 0.825, 0.825, 0.825, 0.825, 0.825, 0.825, 0.825, 0.825, 0.825, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85])
expected_cd0 = np.array([0.01655, 0.01693, 0.01733, 0.01776, 0.01823, 0.01873, 0.01928, 0.01987, 0.02069, 0.02163, 0.02264, 0.02372, 0.02488, 0.01546, 0.0158, 0.01616, 0.01655, 0.01697, 0.01742, 0.01791, 0.01844, 0.01918, 0.02001, 0.0209, 0.02186, 0.02288, 0.0147, 0.01501, 0.01535, 0.01571, 0.0161, 0.01652, 0.01697, 0.01747, 0.01814, 0.01891, 0.01973, 0.02061, 0.02155, 0.01411, 0.0144, 0.01472, 0.01506, 0.01543, 0.01583, 0.01625, 0.01672, 0.01735, 0.01807, 0.01884, 0.01966, 0.02054, 0.01384, 0.01412, 0.01442, 0.01475, 0.0151, 0.01547, 0.01588, 0.01632, 0.01693, 0.01761, 0.01834, 0.01911, 0.01994, 0.01397, 0.01424, 0.01453, 0.01484, 0.01518,
                        0.01554, 0.01592, 0.01635, 0.01692, 0.01758, 0.01827, 0.01901, 0.0198, 0.01416, 0.01443, 0.01472, 0.01502, 0.01535, 0.0157, 0.01608, 0.0165, 0.01706, 0.0177, 0.01838, 0.0191, 0.01988, 0.01446, 0.01472, 0.015, 0.01531, 0.01563, 0.01598, 0.01636, 0.01677, 0.01733, 0.01796, 0.01863, 0.01935, 0.02011, 0.01504, 0.0153, 0.01558, 0.01588, 0.0162, 0.01655, 0.01692, 0.01732, 0.01788, 0.0185, 0.01917, 0.01988, 0.02064, 0.01648, 0.01674, 0.01702, 0.01731, 0.01763, 0.01797, 0.01834, 0.01874, 0.01929, 0.01991, 0.02057, 0.02127, 0.02202, 0.02945, 0.02971, 0.02998, 0.03027, 0.03059, 0.03093, 0.0313, 0.03169, 0.03224, 0.03285, 0.0335, 0.0342, 0.03494])
expected_cd0_comments = ['# zero-lift drag polar, function of altitude & Mach']

expected_cdi_mach = np.array([0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7,
                                0.7, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.775, 0.775, 0.775, 0.775, 0.775, 0.775, 0.775, 0.775, 0.775, 0.775, 0.775, 0.775, 0.775, 0.775, 0.775, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.825, 0.825, 0.825, 0.825, 0.825, 0.825, 0.825, 0.825, 0.825, 0.825, 0.825, 0.825, 0.825, 0.825, 0.825, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85])
expected_cdi_cl = np.array([0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.2, 0.25, 0.3, 0.35, 0.4,
                            0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9])
expected_cdi = np.array([0.02325, 0.02395, 0.02501, 0.02638, 0.02811, 0.03013, 0.03244, 0.03482, 0.03792, 0.04134, 0.04485, 0.04873, 0.05298, 0.05771, 0.06285, 0.02166, 0.02237, 0.02342, 0.0248, 0.02652, 0.02854, 0.03085, 0.03323, 0.03634, 0.03975, 0.04327, 0.04715, 0.0514, 0.05612, 0.06127, 0.0206, 0.0213, 0.02236, 0.02373, 0.02546, 0.02748, 0.02979, 0.03217, 0.03527, 0.03869, 0.0422, 0.04608, 0.05033, 0.05506, 0.0602, 0.0198, 0.02049, 0.02154, 0.02292, 0.02466, 0.02667, 0.02896, 0.03136, 0.03445, 0.03787, 0.04138, 0.04526, 0.04951, 0.05424, 0.05938, 0.01938, 0.02005, 0.02109, 0.02248, 0.02424, 0.02624, 0.02851, 0.03092, 0.034, 0.03742, 0.04093, 0.04481, 0.04906, 0.05379, 0.05893, 0.01944, 0.02005, 0.02107, 0.02248, 0.02431, 0.02628,
                        0.02848, 0.03093, 0.03398, 0.0374, 0.04091, 0.04479, 0.04904, 0.05377, 0.05891, 0.01965, 0.02021, 0.02122, 0.02265, 0.02451, 0.02647, 0.02862, 0.0311, 0.03411, 0.03749, 0.04103, 0.04504, 0.04954, 0.05461, 0.06022, 0.01997, 0.0205, 0.02149, 0.02293, 0.02484, 0.02678, 0.0289, 0.03138, 0.03439, 0.03774, 0.04173, 0.04658, 0.05226, 0.05893, 0.06653, 0.02069, 0.0211, 0.02206, 0.02355, 0.02556, 0.02756, 0.02973, 0.03226, 0.0356, 0.03965, 0.04498, 0.0511, 0.05799, 0.06558, 0.07388, 0.02252, 0.02265, 0.02352, 0.02511, 0.02742, 0.02979, 0.03244, 0.03596, 0.04021, 0.04641, 0.05251, 0.05976, 0.06817, 0.07769, 0.08832, 0.03669, 0.03593, 0.03651, 0.0384, 0.04164, 0.04582, 0.05105, 0.05619, 0.06639, 0.07341, 0.081, 0.08847, 0.0958, 0.10335, 0.11098])
expected_cdi_comments = ['# lift-dependent drag polar, function of Mach & CL']

input = get_path('utils/test/flops_test_polar.txt')
cdi_data, cdi_comments, cd0_data, cd0_comments = _load_flops_aero_table(input)


# if cdi_comments != expected_cdi_comments:
#     print(cdi_comments)
#     print(expected_cdi_comments)
#     raise ValueError(f'Comments written to csv do not match expected values')

# assert_near_equal(cdi_data.get_val('Mach'), expected_cdi_mach)
# assert_near_equal(cdi_data.get_val('Lift Coefficient'), expected_cdi_cl)
# assert_near_equal(cdi_data.get_val('Lift-Dependent Drag Coefficient'),
#                         expected_cdi)

# #         # test CD0
# # if cd0_comments != expected_cd0_comments:
# #     raise ValueError(f'Comments written to csv do not match expected values')

# assert_near_equal(cd0_data.get_val('Mach'), expected_cd0_mach)
# assert_near_equal(cd0_data.get_val('Altitude', 'ft'), expected_cd0_alt)
# assert_near_equal(cd0_data.get_val('Zero-Lift Drag Coefficient'), expected_cd0)
altitude=cd0_data.get_val('Altitude','ft')

altitude_values =np.unique(cd0_data.get_val('Altitude','ft'))#Change once code is fixed
mach_values = np.unique(cdi_data.get_val('Mach','unitless'))
mach_i = cdi_data.get_val('Mach','unitless')
mach_0= cd0_data.get_val('Mach','unitless')

CL_i = cdi_data.get_val('Lift Coefficient')
CD_d=cdi_data.get_val('Lift-Dependent Drag Coefficient')
# CD_l = CD_d[:len(CD_d)-(len(CD_d)-len(mach))]
# CL_l=CL_i[:len(CL_i)-(len(CL_i)-len(mach))]
# CD_0=np.pad(cd0_data.get_val('Zero-Lift Drag Coefficient'),(0,len(CD_L)-len(mach)),'constant')
CD_o=cd0_data.get_val('Zero-Lift Drag Coefficient')

# CD=np.add(CD_0,CD_L)
# print(len(CD))
# print(len(CL))
# # Plotting function
# print(len(mach))
# print(len(altitude))
def plot_polar(ax, CD, CL, color, label=None):
    # # CD.sort()
    # # CL.sort()
    z = np.polyfit(CD, CL, 2)
    p = np.poly1d(z)
    ax.plot(CD, p(CD), color=color, label=label)

def update_plot():
    fix_variable = fix_variable_var.get()#Chooses which variable to fix(Mach or Altitude)
    fix_value = float(fix_value_var.get())#Chooses value of fixed variable
    
    fig, ax = plt.subplots()
    fig.subplots_adjust(right=0.75)

    if fix_variable == 'Mach':#If user decided to fix mach
        indices = mach_i == fix_value #Use the specific mach value provided by user
        index =mach_0 == fix_value
        fixed_values = altitude_values# Place hold all altitude values
        fixed_label = 'Altitude'
    else:#User fixed altitude
        indices = altitude == fix_value#Use the specific altitude value provided by user
        index = altitude == fix_value
        fixed_values = mach_values#Place hold all Mach values
        fixed_label = 'Mach'
    # print(len(CD_d))
    # print(index)
 
    colors = cm.viridis(np.linspace(0, 1, len(fixed_values)))

    for i, val in enumerate(fixed_values):#for a value in the varying variable
        if fix_variable == 'Mach':# if the fixed variable is mach
            # sub_indices = (mach_i == fix_value) & (altitude == val)#Place hold the specified mach and its corresponding altitude values
            sub_index= (mach_0 == fix_value) & (altitude == val)
            CD_i=np.array(CD_d[indices])
        else:
            # sub_indices = (altitude== fix_value) & (mach_i == val)
            sub_index=(altitude== fix_value) & (mach_0 == val) 
            N=len(mach_i)-len(mach_values)
            mach_n=np.pad(mach_values,(0,N))
            # print(mach_i)
            # print(mach_n)
            sub_sub=(mach_n==mach_i)
            # print(sub_sub)
            CD_i=np.array(CD_d[sub_index])
            # print(CD_i)
        # print((sub_indices))
        # print(len(CD_l))
        
        CD_0=CD_o[sub_index]
        
        CL=CL_i[indices]
        # CD=np.add.outer(CD_i,CD_0)
        a=[x +CD_i for x in CD_0]
        CD=np.array(a[0])
        
        # print((CL))
        # for n in CL:
        #     index=(n==CL)
        #     CD_i=CD_L[index]
       
        #     print(CD_L)
        #     print(CD_0)
        #     print(CD_i)
        #     CD=np.add.outer(CD_i,CD_0)
        #     print((CD))
        #     # print(CD)
        # for g in enumerate(fixed_values)
        #     if CD_0=
            
        # ax.scatter(CD,CL,color=colors[i])
        plot_polar(ax, CD, CL, color=colors[i], label=f'{fixed_label} {val}')


        
        # print(CD[sub_indices])
        # print(CL[sub_indices])
       
        

    ax.set_xlabel('CD')
    ax.set_ylabel('CL')
    ax.set_xlim([0,0.15])
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

