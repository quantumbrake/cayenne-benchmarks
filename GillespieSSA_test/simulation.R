#!/usr/bin/env Rscript

library(GillespieSSA)

parms <- c(k1=1.0, k2=0.002, k3=0.5, k4=0.04)  # Define parameters
x0 <- c(S1=4150, S2=39565, S3=3445)                  # Initial state vector
nu <- matrix(c(-1, -2, +2,  0,                 # State-change matrix
                0, +1, -1, -1,
                0,  0,  0, +1),
                nrow=3,byrow=TRUE)
a  <- c("k1*S1", "k2*S1*(S1-1)", "k3*S2", "k4*S2") # Propensity vector
tf <- 10                                       # Final time
simName <- "Decaying-Dimerizing Reaction Set"

# Run simulations 

# Direct method
set.seed(1)
out <- ssa(x0,a,nu,parms,tf,method="D",simName,verbose=TRUE,consoleInterval=1) 
ssa.plot(out,show.title=TRUE,show.legend=FALSE)

# Explict tau-leap method
set.seed(1)
out <- ssa(x0,a,nu,parms,tf,method="ETL",simName,tau=0.003,verbose=TRUE,consoleInterval=1) 
ssa.plot(out,show.title=FALSE,show.legend=FALSE) 

# Binomial tau-leap method
set.seed(1)
out <- ssa(x0,a,nu,parms,tf,method="BTL",simName,verbose=TRUE,consoleInterval=1) 
ssa.plot(out,show.title=FALSE,show.legend=FALSE) 

# Optimized tau-leap method
set.seed(1)
out <- ssa(x0,a,nu,parms,tf,method="OTL",simName,verbose=TRUE,consoleInterval=1) 
ssa.plot(out,show.title=FALSE,show.legend=FALSE) 
