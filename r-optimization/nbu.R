library(lpSolveAPI)

nbu.solve <- function(redemption, capacity, price, cost, redemption.constraint.type='=') {
	# Create an LP model with 0 constraints and 18 decision variables, where:
	#   Variables 1-4 are x11-x14, 5-8 are x21-x24, etc. 
	#   Variable 17 = total revenue and variable 18 = total cost
	mod <- make.lp(0,18)
	
	# Set to maximize:
	lp.control(mod, sense="max")
	
	# Set objective function:
	set.objfn(mod, c(1, -1), indices=c(17, 18))
	
	# Redemption constraints:
	add.constraint(mod, rep(1, 4), type=redemption.constraint.type, indices=1:4, rhs=redemption[1])
	add.constraint(mod, rep(1, 4), type=redemption.constraint.type, indices=5:8, rhs=redemption[2])
	add.constraint(mod, rep(1, 4), type=redemption.constraint.type, indices=9:12, rhs=redemption[3])
	add.constraint(mod, rep(1, 4), type=redemption.constraint.type, indices=13:16, rhs=redemption[4])
	
	# Capacity constraints:
	add.constraint(mod, rep(1, 4), type='<=', indices=seq(1, 16, by=4), rhs=capacity[1])
	add.constraint(mod, rep(1, 4), type='<=', indices=seq(2, 16, by=4), rhs=capacity[2])
	add.constraint(mod, rep(1, 4), type='<=', indices=seq(3, 16, by=4), rhs=capacity[3])
	add.constraint(mod, rep(1, 4), type='<=', indices=seq(4, 16, by=4), rhs=capacity[4])
	
	# Total revenue constraint:
	rev.coefs <- as.vector(t(as.matrix(price)))
	rev.coefs[17] <- -1
	add.constraint(mod, rev.coefs, type='=', indices=1:17, rhs=0)
	
	# Total cost constraint:
	cost.coefs <- as.vector(t(as.matrix(cost)))
	cost.coefs[17] <- -1
	cost.inds <- 1:16
	cost.inds[17] <- 18
	add.constraint(mod, cost.coefs, type='=', indices=cost.inds, rhs=0)
	
	# Solve the model:
	solve(mod)
	
	# Build the outputs and return them:
	total_margin <- get.objective(mod)
	total_revenue <- get.variables(mod)[17]
	total_cost <- get.variables(mod)[18]
	alloc <- as.data.frame(t(matrix(get.variables(mod)[1:16], nrow=4)))
	list(total_revenue=total_revenue, total_margin=total_margin, total_cost=total_cost, alloc=alloc)
}