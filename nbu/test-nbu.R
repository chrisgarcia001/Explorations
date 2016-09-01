source("nbu-solver.R")

# nbu.solve(c(88,42), c(61, 11), data.frame(a=c(1,2),b=c(3,4)), data.frame(a=c(5,6),b=c(7,8))
redemp <- c(88,42)
cap <- c(61, 11)
price <- data.frame(a=c(1,2),b=c(3,4))
cost <- data.frame(a=c(5,6),b=c(7,8))

print(interleave(c(1,2,3), c("a","b","c")))
#message(build.nbu.data(redemp, cap, price, cost))

lns <- readLines('sample-solver-output.txt')
#print(find.single.var(lns, 'total_margin'))
#print(find.2d.var(lns, 'alloc'))


grades <- c('A', 'B', 'C', 'D')
channels <- c('sc_internal_use', 'negotiated_selloff', 'auction_selloff', 'cpo_dtc')
redemp <- c(24, 666 ,64, 48)
cap <- c(600, 50, 1000, 150)
price <- data.frame(a=c(395.00, 385.00, 390.00, 415.00 ),
					b=c(395.00, 385.00, 387.50, 415.00 ),
					c=c(395.00, 285.00, 300.00, 415.00 ),
					d=c(395.00, 270.00, 280.00, 415.00))
cost <- data.frame(a=c(285.00, 315.00, 315.00, 335.00),
					b=c(310.00, 315.00, 315.00, 360.00 ),
					c=c(320.00, 315.00, 315.00, 370.00 ),
					d=c(390.00, 375.00, 375.00, 410.00))
rownames(price) <- grades
colnames(price) <- channels
rownames(cost) <- grades
colnames(cost) <- channels
				

#total_revenue <- find.single.var(result.lines, "total_revenue")
#	total_margin <- find.single.var(result.lines, "total_margin")
#	total_cost <- total_revenue - total_margin
#	alloc <- find.2d.var(result.lines, "alloc")

print('----- SOLVED RESULTS ------')
#message(build.nbu.data(redemp, cap, price, cost))
res <- nbu.solve(redemp, cap, price, cost)

message(paste('total_revenue =', res$total_revenue))
message(paste('total_cost =', res$total_cost))
message(paste('total_margin =', res$total_margin))
message("alloc:\n")
print(res$alloc)
