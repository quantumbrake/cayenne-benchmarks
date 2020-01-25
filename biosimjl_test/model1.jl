using BioSimulator

function runmodel1()
    # initialize
    model = Network("Model 1")

    # species definitions
    model <= Species("S1", 4150)
    model <= Species("S2", 39565)
    model <= Species("S3", 3445)

    # rate definitions
    k1 = 1
    k2 = 0.002
    k3 = 0.5
    k4 = 0.04

    # reaction definitions
    model <= Reaction("death", k1, "S1 --> 0")
    model <= Reaction("fusion", k2, "S1 + S1 --> S2")
    model <= Reaction("fission", k3, "S2 --> S1 + S1")
    model <= Reaction("conv", k4, "S2 --> S3")

    # simulation parameters
    nrep = 200
    time_final = 10.0
    epochs = 1000000

    # simulate
    #= result = simulate(model, Direct(), time = time_final, epochs = epochs, trials = nrep) =#
    result = simulate(model, Direct(), time = time_final, trials = nrep, output_type=Val(:full))
end

@time runmodel1()
