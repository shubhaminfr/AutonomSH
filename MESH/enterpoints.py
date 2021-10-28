import json

# enter the four parameter values, please stay within the bounds otherwise it will crash
# bounds are 0.25-0.45 for e, 40-50 for i, 0-45 for betafwd, 0-30 for betalat
# if bounds are changed then the hole geometry can become shorter the domain, so domain extension is needed
# this can be done via the geom_script.py script 
# meshparam defines the mesh refinement while making sources, it is actually the first length based on dia (see makesrc.py)
# the output is point.json which is then read by paramcalc for all needed calculations
# it is done this way so that just in case you want to couple it with BATMAN so that like 10 design cases are all done together, it sill be easier
# I would not necessarily recommend it because it would perhaps be longer and it's not that much of a job to press enter 10 times after changin enterpoint.py
# Still can be done if needed

data = {}

data['params'] = []
data['params'].append({
   'd': 0.00035,
   'ep': 0.0008,
   'rf': 0.000175,
   'e': 0.00035,
   'alpha': 50.0,
   'betafwd': 30.0,
   'betalat': 20.0,
   'meshparam': 0.05
})

with open('point.json','w') as outfile:
   json.dump(data,outfile)
   



