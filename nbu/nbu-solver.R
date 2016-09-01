library(rneos)
library(stringr)

interleave <- function(v1, v2) {
	v3 <- c()
	len <- 0
	i <- 1
	while(i <= max(length(v1), length(v2))) {
		if(i <= length(v1)) {len <- len + 1; v3[len] <- v1[i]}
		if(i <= length(v2)) {len <- len + 1; v3[len] <- v2[i]}
		i <- i + 1
	}
	v3
}

ffilter <- function(f, lst) {
	v <- c()
	for(i in lst) { if(f(i)) {v[length(v) + 1] <- i} }
	v
}

add.var <- function(var.names, new.vars) {
	for(i in 1:length(new.vars)) {
		if(!is.element(new.vars[i], var.names)) {
			var.names[length(var.names) + i] <- new.vars[i]
		}
	}
	var.names
}

build.matrix.data <- function(param, dataf) {
	dstr <- paste('param', param, ":=")
	for(i in rownames(dataf)) {
		for(j in colnames(dataf)) {
			dstr <- paste(dstr, paste('[', i, ',', j, ']',sep = ''), dataf[i,j])
		}
	}
	paste(dstr, ';')
}

build.nbu.data <- function(redemption, capacity, price, cost) {
	grades <- rownames(price)
	channels <- colnames(price)
	grds <- paste(grades, collapse=' ')
	chnls <- paste(channels, collapse=' ')
	red <- paste(interleave(grades, redemption), collapse=' ')
	cap <- paste(interleave(channels, capacity), collapse=' ')
	dstr <- ''
	dstr <- paste('set GRADES := ', paste(grds, ';'))
	dstr <- paste(dstr, paste('set CHANNELS := ', chnls, ';'), sep="\n")
	dstr <- paste(dstr, paste('param Redemption := ', red, ';'), sep="\n") 
	dstr <- paste(dstr, paste('param Capacity := ', cap, ';'), sep="\n") 
	dstr <- paste(dstr, build.matrix.data('Price', price), sep="\n")
	dstr <- paste(dstr, build.matrix.data('Cost', cost), sep="\n")
	dstr
} 

find.single.var <- function(lines, varname) {
	rxp <- paste('^', varname, sep='')
	for(a in lines) {
		if(str_detect(a, rxp)) {
			return(as.numeric(str_split(str_replace_all(a, ' ', ''), '=')[[1]][2]))
		}
	}
	return(0)
}

find.2d.var <- function(lines, varname) {
	rxp <- paste('^', varname, sep='')
	rownames <- c()
	colnames <- c()
	vals <- c()
	i <- 1
	while(i <= length(lines)) {
		if(str_detect(lines[i], rxp)) {
			i <- i + 1
			while((i <= length(lines)) && (!str_detect(lines[i], ';'))) {
				curr <- ffilter(function(x){x != ''}, str_split(lines[i], ' ')[[1]])
				rownames <- add.var(rownames, curr[1])
				colnames <- add.var(colnames, curr[2])
				vals[length(vals) + 1] <- as.numeric(curr[3])
				i <- i + 1
			}
			i <- length(lines)
		}
		i <- i + 1
	}
	print(rownames)
	print(colnames)
	mat <- matrix(vals, nrow=length(rownames), ncol=length(colnames))
	dataf <- as.data.frame(mat)
	rownames(dataf) <- rownames
	colnames(dataf) <- colnames
	dataf
}

nbu.solve <- function(redemption, capacity, price, cost) {
	modf <- 'basic-nbu.mod'
	cmdf <- 'nbu.run'

	## import of file contents
	modc <- paste(paste(readLines(modf), collapse = "\n"), "\n")
	datc <- build.nbu.data(redemption, capacity, price, cost)
	cmdc <- paste(paste(readLines(cmdf), collapse = "\n"), "\n")
	message(datc)
	## create list object

	# Use for bpmpd solver
	solver <- 'bpmpd'
	solver.category <- 'lp'
	argslist <- list(mod = modc, dat = datc, com = cmdc, comment = "")

	template <-NgetSolverTemplate(category = solver.category, solvername = solver, inputMethod = "AMPL")
	
	## create XML string
	xmls <- CreateXmlString(neosxml = template, cdatalist = argslist)
	#print(xmls)
	test <- NsubmitJob(xmlstring = xmls, user = "rneos", interface = "", id = 0)
	NgetJobStatus(obj = test, convert = TRUE)
	NgetJobInfo(obj = test, convert = TRUE)
	result <- NgetFinalResults(obj = test, convert = TRUE)

	# Get the results and parse out variables:
	#message(slot(result, "ans"))
	result.lines <- str_split(slot(result, "ans"), "\n")[[1]]
	total_revenue <- find.single.var(result.lines, "total_revenue")
	total_margin <- find.single.var(result.lines, "total_margin")
	total_cost <- total_revenue - total_margin
	alloc <- find.2d.var(result.lines, "alloc")
	list(total_revenue=total_revenue, total_margin=total_margin, total_cost=total_cost, alloc=alloc)
}
