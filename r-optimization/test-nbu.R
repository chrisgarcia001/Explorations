source('nbu.R')

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

					
print('----- SOLVED RESULTS ------')
#message(build.nbu.data(redemp, cap, price, cost))
res <- nbu.solve(redemp, cap, price, cost)

message(paste('total_revenue =', res$total_revenue))
message(paste('total_cost =', res$total_cost))
message(paste('total_margin =', res$total_margin))
message("alloc:\n")
print(res$alloc)