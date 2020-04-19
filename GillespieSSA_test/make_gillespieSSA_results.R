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
  else if (model_str == "00004"){
    parms <- c(k1=0.1, k2=0.11) # Define parameters
    x0 <- c(S1=10) # Initial state vector
    nu <- matrix(c(+1, -1),
                 nrow=1,byrow=TRUE)
    a <- c("k1*S1", "k2*S1") # Propensity vector
    tf <- 51 # Final time
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
  else if (model_str == "00020"){
    parms <- c(k1=1.0, k2=0.1)  # Define parameters
    x0 <- c(S1=0)                  # Initial state vector
    nu <- matrix(c(+1, -1),
                 nrow=1,byrow=TRUE)
    a  <- c("k1", "k2*S1") # Propensity vector
    tf <- 51                                       # Final time
    simName <- "Model 00020"
  }
  else if (model_str == "00021"){
    parms <- c(k1=10.0, k2=0.1)  # Define parameters
    x0 <- c(S1=0)                  # Initial state vector
    nu <- matrix(c(+1, -1),
                 nrow=1,byrow=TRUE)
    a  <- c("k1", "k2*S1") # Propensity vector
    tf <- 51                                       # Final time
    simName <- "Model 00021"
  }
  else if (model_str == "00022"){
    parms <- c(k1=5.0, k2=0.1)  # Define parameters
    x0 <- c(S1=0)                  # Initial state vector
    nu <- matrix(c(+1, -1),
                 nrow=1,byrow=TRUE)
    a  <- c("k1", "k2*S1") # Propensity vector
    tf <- 51                                       # Final time
    simName <- "Model 00022"
  }
  else if (model_str == "00023"){
    parms <- c(k1=1000.0, k2=0.1)  # Define parameters
    x0 <- c(S1=0)                  # Initial state vector
    nu <- matrix(c(+1, -1),
                 nrow=1,byrow=TRUE)
    a  <- c("k1", "k2*S1") # Propensity vector
    tf <- 51                                       # Final time
    simName <- "Model 00023"
  }
  else if (model_str == "00030"){
    # A + A -> A2
    # A2 -> A + A
    # In the model description, they just say k1 = 0.001 without specifying
    # deterministic or stochastic. They end up using k1_stoc = 0.001. To have
    # k1_stoc = 0.001, we should set k1_det = 0.001/2.
    parms <- c(k1=0.001, k2=0.01)
    x0 <- c(S1=100, S12=0)
    nu <- matrix(c(-2, +2, +1, -1), nrow=2, byrow=TRUE)
    a <- c("k1*S1*(S1-1)/2", "k2*S12")
    tf <- 51
    simName <- "Model 00030, Dimerization"
  }
  else if (model_str == "00031"){
    # A + A -> A2
    # A2 -> A + A
    # In the model description, they just say k1 = 0.001 without specifying
    # deterministic or stochastic. They end up using k1_stoc = 0.001. To have
    # k1_stoc = 0.001, we should set k1_det = 0.001/2.
    parms <- c(k1=0.0002, k2=0.004)
    x0 <- c(S1=1000, S12=0)
    nu <- matrix(c(-2, +2, +1, -1), nrow=2, byrow=TRUE)
    a <- c("k1*S1*(S1-1)/2", "k2*S12")
    tf <- 51
    simName <- "Model 00031, Dimerization"
  }
  else if (model_str == "00037"){
    # 0 -> 5*S1
    # S1 -> 0
    parms <- c(k1=1.0, k2=0.2)
    x0 <- c(S1=0)
    nu <- matrix(c(+5, -1), nrow=1, byrow=TRUE)
    a <- c("k1", "k2*S1")
    tf <- 51
    simName <- "Model 00037"
  }
  else if (model_str == "00038"){
    # 0 -> 10*S1
    # S1 -> 0
    parms <- c(k1=1.0, k2=0.4)
    x0 <- c(S1=0)
    nu <- matrix(c(+10, -1), nrow=1, byrow=TRUE)
    a <- c("k1", "k2*S1")
    tf <- 51
    simName <- "Model 00038"
  }
  else if (model_str == "00039"){
    # 0 -> 100*S1
    # S1 -> 0
    parms <- c(k1=1.0, k2=4.0)
    x0 <- c(S1=0)
    nu <- matrix(c(+100, -1), nrow=1, byrow=TRUE)
    a <- c("k1", "k2*S1")
    tf <- 51
    simName <- "Model 00039"
  }
  else {
    print("Invalid model specified");
    return (0)
  }
  retlist <- list("parms"=parms, "x0"=x0, "nu"=nu, "a"=a, "tf"=tf)
  return (retlist)
}

args = commandArgs(trailingOnly=TRUE)
model_name = args[1]
algo_name = args[2]
nrep = args[3]
write_results_flag = args[4]
res = get_model(model_name)

if (algo_name == "tau_adaptive"){
  algo = ssa.otl()
} else if (algo_name == "direct"){
  algo = ssa.d()
} else if (algo_name == "tau_leaping"){
  algo = ssa.etl(tau=0.1)
} else {
  print("Bad algorithm");
  return (0)
}

dir_name = paste("./results/",model_name, "/GillespieSSA_",algo_name,"/", sep="")
dir.create(dir_name, recursive=TRUE)
if (write_results_flag == "True"){
  for (i in 1:nrep) {
  fname = paste(dir_name, i, ".csv", sep="")
  # fname = paste("..\\results\\",model_name, "\\GillespieSSA_otl\\", i, ".csv", sep="")
  out <- ssa(res$x0,res$a,res$nu,res$parms,res$tf,method=algo,res$simName,verbose=FALSE,consoleInterval=1)
  write.table(out$data, quote=FALSE, row.names=FALSE, col.names=FALSE, sep=",", file=fname)
  }
} else {
  for (i in 1:nrep) {
  out <- ssa(res$x0,res$a,res$nu,res$parms,res$tf,method=algo,res$simName,verbose=FALSE,consoleInterval=1)
  }
  print("Not saving results");
}

