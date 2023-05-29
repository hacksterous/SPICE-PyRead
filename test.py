from rawread import rawread
import matplotlib.pyplot as plot

if __name__ == '__main__':
	data, plots, dims = rawread('jfet.bin.raw')
	dimx, dimy = dims
	#print(data)
	varslist = plots[0]['varnames']
	#print(varslist)

	#time = data[0]['time']
	#xname = 'v(gate)'
	xname = 'v(v-sweep)'
	yname = 'i(vdrain)'
	a = data[0][xname]
		
	b = data[0][yname]
	#print (a, b)
	if len(a) != dimx or len(b) != dimx:
		print ("Error: dimension is wrong: ", len(a))
		exit(1)
	#print ("len a ", len(a))
	#print ("len b ", len(b))
	#print (a[1], b[1])
	plot.xlabel(xname)
	plot.ylabel(yname)
	plot.title(yname.upper() + " vs " + xname)
	for i in range(dimx):
		plot.plot(a[i], -b[i])
	plot.show()


