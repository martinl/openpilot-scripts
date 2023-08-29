import cantools

dbc_file = 'opendbc/subaru_global_2017_generated.dbc'
dbc_file2 = 'opendbc/subaru_global_2020_hybrid_generated.dbc'
dbc_file3 = 'opendbc/subaru_outback_2015_generated.dbc'

dbc = cantools.database.load_file(dbc_file)
dbc2 = cantools.database.load_file(dbc_file2)
dbc3 = cantools.database.load_file(dbc_file3)
