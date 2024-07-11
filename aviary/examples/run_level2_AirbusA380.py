"""
This is a slightly more complex Aviary example of running a coupled aircraft design-mission optimization.
It runs the same mission as the `run_basic_aviary_example.py` script, but it uses the AviaryProblem class to set up the problem.
This exposes more options and flexibility to the user and uses the "Level 2" API within Aviary.

We define a `phase_info` object, which tells Aviary how to model the mission.
Here we have climb, cruise, and descent phases.
We then call the correct methods in order to set up and run an Aviary optimization problem.
This performs a coupled design-mission optimization and outputs the results from Aviary into the `reports` folder.
"""
import aviary.api as av
from outputted_phase_info import phase_info

prob = av.AviaryProblem()

phase_info = {
    "pre_mission": {"include_takeoff":False, "optimize_mass": True},
    "climb": {
        "subsystem_options": {"core_aerodynamics": {"method": "computed"}},
        "user_options": {
            "optimize_mach": False,
            "optimize_altitude": False,#Keep False
            "polynomial_control_order": 1,
            "num_segments": 5,
            "order": 3,
            "solve_for_distance": False,
            "initial_mach": (0.32, "unitless"),
            "final_mach": (0.82, "unitless"),
            "mach_bounds": ((0.3, 0.84), "unitless"),
            "initial_altitude": (0.0, "ft"),
            "final_altitude": (35000.0, "ft"),
            "altitude_bounds": ((0.0, 35500.0), "ft"),
            "throttle_enforcement": "path_constraint",
            "fix_initial": False,
            #"input_initial":True ,#Uncomment for takeoff on
            "constrain_final":False,
            "fix_duration": True,#change to False for takeoff on 
            "initial_bounds": ((0.0, 0.0), "min"),
            "duration_bounds": ((136, 336.0), "min"),
            "add_initial_mass_constraint": False,
        },
        "initial_guesses": {"time": ([0, 200], "min")},
    },
    "cruise": {
        "subsystem_options": {"core_aerodynamics": {"method": "computed"}},
        "user_options": {
            "optimize_mach": False,
            "optimize_altitude": False,
            "polynomial_control_order": 1,
            "num_segments": 5,
            "order": 3,
            "solve_for_distance": False,
            "initial_mach": (0.82, "unitless"),
            "final_mach": (0.82, "unitless"),
            "mach_bounds": ((0.8, 0.84), "unitless"),
            "initial_altitude": (35000.0, "ft"),
            "final_altitude": (35000.0, "ft"),
            "altitude_bounds": ((34500, 36000.0), "ft"),
            "throttle_enforcement": "boundary_constraint",
            "fix_initial": False,
            "constrain_final": False,
            "fix_duration": False,
            "initial_bounds": ((136, 1136), "min"),
            "duration_bounds": ((36.5, 236.5), "min"),
        },
        "initial_guesses": {"time": ([1000, 200], "min")},
    },
    "descent": {
        "subsystem_options": {"core_aerodynamics": {"method": "computed"}},
        "user_options": {
            "optimize_mach": True,
            "optimize_altitude": True,
            "polynomial_control_order": 1,
            "num_segments": 5,
            "order": 3,
            "solve_for_distance": False,
            "initial_mach": (0.82, "unitless"),
            "final_mach": (0.32, "unitless"),
            "mach_bounds": ((0.3, 0.84), "unitless"),
            "initial_altitude": (35500.0, "ft"),
            "final_altitude": (5000.0, "ft"),
            "altitude_bounds": ((4500.0, 36000.0), "ft"),
            "throttle_enforcement": "path_constraint",
            "fix_initial": False,
            "constrain_final": True,
            "fix_duration": False,
            "initial_bounds": ((1136, 3336), "min"),
            "duration_bounds": ((0, 200), "min"),
        },
        "initial_guesses": {"time": ([2000, 200], "min")},
    },
    "post_mission": {
        "include_landing": True,
        "constrain_range": True,
        "target_range": (2251, "nmi"),
    },
}


prob = av.AviaryProblem()

# Load aircraft and options data from user
# Allow for user overrides here
prob.load_inputs('aircraft_AirbusA380.csv', phase_info)

prob.check_and_preprocess_inputs()

prob.add_pre_mission_systems()

prob.add_phases()

prob.add_post_mission_systems()

# Link phases and variables
prob.link_phases()

prob.add_driver("SLSQP", max_iter=1000)

prob.add_design_variables()

prob.add_objective(objective_type="mass", ref=-1e5)

prob.setup()

prob.set_initial_guesses()

prob.run_aviary_problem(record_filename='A380_level2_example.db', suppress_solver_print=True, make_plots=True)