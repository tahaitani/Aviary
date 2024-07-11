import aviary.api as av
from outputted_phase_info import phase_info

prob = av.run_aviary('models/test_aircraft/aircraft_for_bench_FwFm.csv',
                     phase_info, optimizer="SLSQP", make_plots=True)