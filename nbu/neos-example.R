library(rneos)

showClass("NeosJob")
## Set up and solve:

## setting path to example model and data file
#modf <- system.file("./", "diet.mod", package = "rneos")
#datf <- system.file("ExAMPL", "diet.dat", package = "rneos")

modf <- 'basic-nbu.mod'
datf <- 'nbu.dat'
cmdf <- 'nbu.run'

## import of file contents
modc <- paste(paste(readLines(modf), collapse = "\n"), "\n")
datc <- paste(paste(readLines(datf), collapse = "\n"), "\n")
cmdc <- paste(paste(readLines(cmdf), collapse = "\n"), "\n")
## create list object

# Use for ASA solver
solver <- 'ASA'
solver.category <- 'go'
argslist <- list(model = modc, data = datc, commands = "", comments = "")

# Use for bpmpd solver
solver <- 'bpmpd'
solver.category <- 'lp'
argslist <- list(mod = modc, dat = datc, com = cmdc, comment = "")

template <-NgetSolverTemplate(category = solver.category, solvername = solver, inputMethod = "AMPL")

# IMPORTANT: Look at XML fields here - arglist keys need to match XML element names
print(template)

## create XML string
xmls <- CreateXmlString(neosxml = template, cdatalist = argslist)
print(xmls)
test <- NsubmitJob(xmlstring = xmls, user = "rneos", interface = "", id = 0)
NgetJobStatus(obj = test, convert = TRUE)
NgetJobInfo(obj = test, convert = TRUE)
result <- NgetFinalResults(obj = test, convert = TRUE)

# Get the result as a string:
print(slot(result, "ans"))
print(result)