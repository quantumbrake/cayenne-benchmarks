#!/usr/bin/env Rscript

library(GillespieSSA)

parms <- c(k1=1.0, k2=1.1)  # Define parameters
x0 <- c(S1=100)                  # Initial state vector
nu <- matrix(c(1, -1), nrow=1,byrow=TRUE)
a  <- c("k1*S1", "k2*S1") # Propensity vector
tf <- 50                                       # Final time
simName <- "Decaying-Dimerizing Reaction Set"

# Run simulations 

"
# Direct method
set.seed(1)
out <- ssa(x0,a,nu,parms,tf,method='D',simName,verbose=TRUE,consoleInterval=1) 
ssa.plot(out,show.title=TRUE,show.legend=FALSE)

# Explict tau-leap method
set.seed(1)
out <- ssa(x0,a,nu,parms,tf,method='ETL',simName,tau=0.003,verbose=TRUE,consoleInterval=1) 
ssa.plot(out,show.title=FALSE,show.legend=FALSE) 

# Binomial tau-leap method
set.seed(1)
out <- ssa(x0,a,nu,parms,tf,method='BTL',simName,verbose=TRUE,consoleInterval=1) 
ssa.plot(out,show.title=FALSE,show.legend=FALSE) 
"

# Optimized tau-leap method
# set.seed(1)
start_time = Sys.time()
# OTL
for (i in 1:10) {
    out <- ssa(x0,a,nu,parms,tf,method='D',simName,verbose=FALSE,consoleInterval=1) 
    write.table(out$data, file=paste(i, ".csv", sep=""), sep=",", row.names=FALSE)
}
end_time = Sys.time()
print(paste("Time elapsed in seconds:", end_time - start_time))
ssa.plot(out,show.title=FALSE,show.legend=FALSE) 
