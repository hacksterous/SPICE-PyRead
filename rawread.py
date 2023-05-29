# MIT license: https://opensource.org/licenses/MIT
# See https://github.com/Isotel/mixedsim/blob/master/python/ngspice_read.py
# for a more complete library. Isotel's version is GPL licensed
###from __future__ import division
import numpy as np

BSIZE_SP = 512 # Max size of a line of data; we don't want to read the
			   # whole file to find a line, in case file does not have
			   # expected structure.
MDATA_LIST = [b'title', b'date', b'plotname', b'flags', b'no. variables',
			  b'no. points', b'dimensions', b'command', b'option']

def rawread(fname: str):
	"""Read ngspice binary raw files. Return tuple of the data, and the
	info metadata. The dtype of the data contains field names. This is
	not very robust yet, and only supports ngspice.
	>>> darr, data = rawread('test.py')
	>>> darr.dtype.names
	>>> plot(np.real(darr[0]['frequency']), np.abs(darr[0]['v(out)']))
	"""
	# Example header of raw file
	# Title: rc band pass example circuit
	# Date: Sun Feb 21 11:29:14  2016
	# Plotname: AC Analysis
	# Flags: complex
	# No. Variables: 3
	# No. Points: 41
	# Variables:
	#		 0	   frequency	   frequency	   grid=3
	#		 1	   v(out)  voltage
	#		 2	   v(in)   voltage
	# Binary:
	fp = open(fname, 'rb')
	info = {}
	count = 0
	arrs = []
	meta = []
	dims = (0, 0)
	while (True):
		try:
			data = fp.readline(BSIZE_SP).split(b':', maxsplit=1)
		except:
			print ("Error reading file: ", fname)
			exit(1)
		if len(data) == 2:
			if data[0].lower() in MDATA_LIST:
				info[data[0].lower()] = data[1].strip()
			if data[0].lower() == b'variables':
				nvars = int(info[b'no. variables'])
				npoints = int(info[b'no. points'])
				#print ("Dimensions: dims = ", info[b'dimensions'].decode('utf-8'))
				x = 0
				if b'dimensions' in info.keys():
					dims = info[b'dimensions'].decode('utf-8').split(',')
					x = int(dims[0])
					y = int(dims[1])
					dims = (x, y)
					#print ("Dimensions: x = ", x, " y = ", y)
				info['varnames'] = []
				info['varunits'] = []
				for varn in range(nvars):
					varspec = (fp.readline(BSIZE_SP).strip()
							   .decode('ascii').split())
					if varn != int(varspec[0]):
						print ("Error: incorrect variable specs in raw file.")
						exit(1)
					#assert(varn == int(varspec[0]))
					info['varnames'].append(varspec[1])
					info['varunits'].append(varspec[2])
			if data[0].lower() == b'binary':
				rowdtype = np.dtype({'names': info['varnames'],
									 'formats': [np.complex_ if b'complex'
												 in info[b'flags']
												 else np.float_]*nvars})
				# We should have all the metadata by now
				arr = np.fromfile(fp, dtype=rowdtype, count=npoints)
				#print ("arr = ", arr)
				if x != 0:
					arr = arr.reshape(x, y)
				arrs.append(arr)
				meta.append(info)
				fp.readline() # Read to the end of line
		else:
			break
	return (arrs, meta, dims)


