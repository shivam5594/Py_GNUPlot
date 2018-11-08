import sys, getopt, os, string

#print "This is the name of the script: ", sys.argv[0]
#print "Number of arguments: ", len(sys.argv)
#print "The arguments are: " , str(sys.argv)

pwd = os.getcwd()

def use():
	print("""Usage: \n	pyPlot.py -s / --script <Path to GNU script to write>
		  -d / --data   <Path to data file>
				 { USE / IN PATH. EX: C:/Users/Profile/name.csv }
		  -x / --xAxis  <Column no. to be on X axis>
				 { KEEP IT 1 FOR SIMPLICITY. EX: -x 1 }
		  -y / --yAxis  <Column nos. to be on Y axis>
				 { EX: -y 3 -y 4 -y 2 -y 5 }
		  -w / --style  <Data marking style DEFAULT: dots>
				 { lines, dots, steps, errorbars, xerrorbar, xyerrorlines, vectors, parallelaxes,
		      		points, impulses, fsteps, errorlines, xerrorlines, yerrorbars, surface,
				linespoints, labels, histeps, financebars, xyerrorbars, yerrorlines }
		  -t / --term   <Choose terminal DEFAULT: wxt>
				 { windows, canvas, cgm, dumb, caca, dxf, emf, fig, hpgl, png, jpeg, gif,
				 epslatex, pslatex and pstex, postscript, qms, svg, domterm, tgif, tkcanvas, latex,
				 eepic, tpic, pstricks, texdraw, mf, mp, context, wxt, epscairo, cairolatex, 
				 pdfcairo, pngcairo, lua, tikz, qt }
		  -S / --sensor <Sensor id to plot selective rows>
				 { This will a condition to while plotting the value. If sensor value is same as
				 first colomn value, then will be plotted. It has to be the first colomn value. 
				 EX: --sensor 34 }""")

def isValidStyle(styl):
	flag = 0
	for temp in dpStyle:
		if temp == styl:
			flag = 1
			break
	return flag
	

def isValidTerm(term):
	flag = 0
	for temp in terminals:
		if temp == term:
			flag = 1
			break
	return flag


if len(sys.argv) <= 2:
	print("--------------------------------------------------------------------------------------------------------")
	#print("Insufficient arguments\n")
	use()
	print("--------------------------------------------------------------------------------------------------------")
	sys.exit()

opts, args = getopt.getopt(sys.argv[1:], "hs:d:x:y:w:t:S:",["help","script=","data=","xAxis=","yAxis=","style=","term=","sensor="])

dpStyle = ["lines", "dots", "steps", "errorbars", "xerrorbar", "xyerrorlines", "vectors", "parallelaxes", \
		"points", "impulses", "fsteps", "errorlines", "xerrorlines", "yerrorbars", "surface", \
		"linespoints", "labels", "histeps", "financebars", "xyerrorbars", "yerrorlines"]
terminals = ["windows", "canvas", "cgm", "dumb", "caca", "dxf", "emf", "fig", "hpgl", "png", "jpeg", "gif", \
		"epslatex", "pslatex and pstex", "postscript", "qms", "svg", "domterm", "tgif", "tkcanvas", "latex", \
		"eepic", "tpic", "pstricks", "texdraw", "mf", "mp", "context", "wxt", "epscairo", "cairolatex", \
		"pdfcairo", "pngcairo", "lua", "tikz", "qt"]

plots = []
style = "dots"
term = "wxt"
sensor = 0

for opt, arg in opts:
	print(opt, arg)

	if opt in ("-h", "--help"):
		use()
	elif opt in ("-s", "--script"):
		GNUscript = arg		
	elif opt in ("-d", "--data"):
		data = arg
	elif opt in ("-x", "--xAxis"):
		ref = arg
	elif opt in ("-y", "--yAxis"):
		plots.append(arg)
	elif opt in ("-w", "--style"):
		if isValidStyle(arg) == 1:
			style = arg
		else:
			print(arg+" is not a valid option. Set back to default DOTS.\n")
			style = "dots"
	elif opt in ("-h", "--help"):
		use()
	elif opt in ("-t", "--term"):
		if isValidTerm(arg) == 1:
			term = arg
		else:
			print(arg+" is not a valid option. Set back to default wxt.\n")
			term = "wxt"
	elif opt in ("-S", "--sensor"):
		sensor = arg
	else:
		use()

#print "--"+GNUscript

if GNUscript.endswith('.gnu') and (data.endswith('.csv') or data.endswith('.CSV')):

    #scptBuf = "set term "+term+" size 1920,1080\n"
    #scptBuf += "set size 1, 1\n"
    scptBuf = "set grid\n"

    if term == "png":
        scptBuf += "set output \""+string.replace(pwd,'\\','/')+"/graph.png\"\n"
    elif term == "jpeg":
        scptBuf += "set output \""+"C:/Users/schauhan/GNUPlot/graph.jpg\"\n"

    scptBuf += "set datafile separator \",\"\n"
    if sensor != 0:
	scptBuf += "sensor = "+ sensor+"\n"
    scptBuf += "plot "

    for y in plots:
	if sensor != 0:
		scptBuf += "\""+data +"\" using "+ "($1 == sensor ? $2 : 1/0)"+":"+y+" with " + style
	else:
	        scptBuf += "\""+data +"\" using "+ ref+":"+y+" with " + style
	
	if y != plots[len(plots)-1]:
		scptBuf += ","
   
    scptBuf +="\n"
    scptBuf += "set xlabel \"Time\"\n"
    scptBuf += "set ylabel \"Values\"\n" 
    scptBuf += "pause -1"

    print(scptBuf)

    scptHndl = open(GNUscript, "w")
    scptHndl.write(scptBuf)
    scptHndl.close()
else:
    print("Check paths to script and data files. This accepts only .gnu and .csv for GNUPlot and data respectively.\n")
