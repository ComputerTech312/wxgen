# Generates a database of segments from one or more input files
from netCDF4 import Dataset as netcdf
import numpy as np
import sys

if len(sys.argv) < 3:
   print "generate_database.py input [input ...] output"
   sys.exit()

ifilenames = sys.argv[1:-1]
ofilename = sys.argv[-1]
vars = ["air_temperature_2m", "x_wind_10m"]

values = dict()
N = 10
D = len(ifilenames)
O = 10
E = 51

for var in vars:
   values[var] = np.zeros([D, O, E], float)
dates = np.zeros(D, int)

# Loop over files
for d in range(0, D):
   ifile = netcdf(ifilenames[d], 'r')
   dates[d] = ifile.variables["time"][0]
   lats = ifile.variables["latitude"]
   lons = ifile.variables["longitude"]
   xrange = range(100, 130)
   yrange = range(82, 107)
   print lats[yrange]
   print lons[xrange]
   for var in vars:
      data = ifile.variables[var][:, 0, :, xrange, yrange]
      temp = np.mean(np.mean(data, axis=3), axis=2)
      for t in range(0, 10):
         I = range(t*4, (t+1)*4)
         values[var][d, t, :] = np.mean(temp[I, :], axis=0)
   ifile.close()

ofile = netcdf(ofilename, 'w')
ofile.createDimension("date", D)
ofile.createDimension("leadtime", O)
ofile.createDimension("member", E)

vVars = dict()
vDate = ofile.createVariable("date", "i4", ("date"))
vDate[:] = dates
vOffset = ofile.createVariable("leadtime", "i4", ("leadtime"))
vOffset[:] = range(0, O)
for var in vars:
   vVars[var] = ofile.createVariable(var, "f4", ("date", "leadtime", "member"))
   vVars[var][:] = values[var]
ofile.close()
