library(lpSolveAPI)
library(stringr)

# nbu.solve(c(88,42), c(61, 11), data.frame(a=c(1,2),b=c(3,4)), data.frame(a=c(5,6),b=c(7,8))

add.var <- function(var.names, new.vars) {
	for(i in 1:length(new.vars)) {
		if(!is.element(new.vars[i], var.names)) {
			var.names[length(var.names) + i] <- new.vars[i]
		}
	}
	var.names
}

varname <- function(vname, i=NULL, j=NULL) {
	if(!is.null(i)) {
		vname <- paste(vname, i, sep='_')
		if(!is.null(j)) {
			vname <- paste(vname, j, sep='_')
		}
	}
	vname
}

# Reduce using the 2-arity function f (folds from left).
reduce <- function(f, items, identity=0) {
	if(length(items) == 0) {return(identity)}
	total <- items[1]
	for(i in 2:length(items)) {
		total <- f(total, items[i])
	}
	total
}

# Join a vector of items together into a single string. Similar to paste, 
# but takes a vector of items rather than the items.
vec_join <- function(str_vec, sep=' ') {
	reduce(function(x,y){paste(x,y,sep=sep)}, str_vec)
}

nbu.solve <- function(redemptions, capacities, prices, costs) {
	var.names <- c('total_revenue', 'total_revenue')
	grades <- length(redemptions)
	channels <- length(capacities)
	modstr <- 'max: total_revenue - total_revenue;\n'
	for(i in 1:grades) {
		newvars <- sapply(1:channels, function(j) {varname('x',i,j)})
		add.var(var.names, newvars)
		modstr <- paste(modstr, vec_join(newvars, sep=' + '), '=', redemptions[i], ";\n")
	}
	for(i in 1:grades) {
		newvars <- sapply(1:channels, function(j) {varname('x',i,j)})
		add.var(var.names, newvars)
		modstr <- paste(modstr, vec_join(newvars, sep=' + '), '=', redemptions[i], ";\n")
	}
	modstr
	
}