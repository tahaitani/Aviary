import aviary.api as av
from outputted_phase_info import phase_info  
prob = av.run_aviary('aircraft_AirbusA380.csv',phase_info, optimizer="SLSQP", make_plots=True,max_iter=1000)
# prob.model.list_vars()

