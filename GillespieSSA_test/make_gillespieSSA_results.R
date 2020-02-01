#!/usr/bin/env Rscript

library(GillespieSSA)

get_model <- function(model_str="00001"){
  if (model_str == "00001"){
    parms <- c(k1=0.1, k2=0.11)  # Define parameters
    x0 <- c(S1=100)                  # Initial state vector
    nu <- matrix(c(+1, -1),
                 nrow=1,byrow=TRUE)
    a  <- c("k1*S1", "k2*S1") # Propensity vector
    tf <- 51                                       # Final time
    simName <- "Birth-Death Reaction Set"
  }
  else if (model_str == "00003"){
    parms <- c(k1=1.0, k2=1.1)  # Define parameters
    x0 <- c(S1=100)                  # Initial state vector
    nu <- matrix(c(+1, -1),
                 nrow=1,byrow=TRUE)
    a  <- c("k1*S1", "k2*S1") # Propensity vector
    tf <- 51                                       # Final time
    simName <- "Birth-Death Reaction Set"
  }
  else if (model_str == "00005"){
    parms <- c(k1=0.1, k2=0.11)  # Define parameters
    x0 <- c(S1=10000)                  # Initial state vector
    nu <- matrix(c(+1, -1),
                 nrow=1,byrow=TRUE)
    a  <- c("k1*S1", "k2*S1") # Propensity vector
    tf <- 51                                       # Final time
    simName <- "Birth-Death Reaction Set"
  }
  else if (model_str == "00011"){
    parms <- c(k1=0.1/2, k2=0.11/2)  # Define parameters
    x0 <- c(S1=100)                  # Initial state vector
    nu <- matrix(c(+1, -1),
                 nrow=1,byrow=TRUE)
    a  <- c("k1*S1", "k2*S1") # Propensity vector
    tf <- 51                                       # Final time
    simName <- "Birth-Death Reaction Set"
  }
  retlist <- list("parms"=parms, "x0"=x0, "nu"=nu, "a"=a, "tf"=tf)
  return (retlist)
}


# Optimized tau-leap method

# OTL
model_name="00001"
nrep = 10
res = get_model(model_name)
dir_name = paste("./results/",model_name, "/GillespieSSA_otl/", sep="")
dir.create(dir_name, recursive=TRUE)
for (i in 1:nrep) {
  fname = paste(dir_name, i, ".csv", sep="")
  # fname = paste("..\\results\\",model_name, "\\GillespieSSA_otl\\", i, ".csv", sep="")
  out <- ssa(res$x0,res$a,res$nu,res$parms,res$tf,method=ssa.otl(),res$simName,verbose=FALSE,consoleInterval=1) 
  write.table(out$data, quote=FALSE, row.names=FALSE, col.names=FALSE, sep=",", file=fname)
}

