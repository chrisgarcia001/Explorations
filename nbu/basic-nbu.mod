#-----------------------------------------------------------------------------------------
# Author: Chris Garcia (chris.garcia@amrutainc.com)
# Date: 8.22.2016
#-----------------------------------------------------------------------------------------

#Declaration of parameters

# Sets:
set GRADES;
set CHANNELS;

# Key params:
param Cost {GRADES, CHANNELS};
param Price {GRADES, CHANNELS};
param Capacity {CHANNELS};
param Redemption {GRADES};

#Decision variables:
var alloc {GRADES, CHANNELS} >= 0;
var total_cost;
var total_revenue;

#Objective Function
maximize total_margin: total_revenue - total_cost;

#Constraints
subject to constr1 {i in GRADES}: sum {j in CHANNELS} alloc[i,j] = Redemption[i];
subject to constr2 {j in CHANNELS}: sum {i in GRADES} alloc[i,j] <= Capacity[j];
subject to constr3: total_revenue = sum {i in GRADES, j in CHANNELS} Price[i,j] * alloc[i,j];
subject to constr4: total_cost = sum {i in GRADES, j in CHANNELS} Cost[i,j] * alloc[i,j];
