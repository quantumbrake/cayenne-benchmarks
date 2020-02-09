using BioSimulator
using DelimitedFiles

include("models.jl")

function run_model(model, algorithm)
    # simulation parameters
    nrep = 200
    time_final = 51.0
    epochs = 50
    # simulate
    if algorithm == "direct"
        algo_func = Direct()
    elseif algorithm == "tau_leaping"
        algo_func = TauLeaping()
    elseif algorithm == "tau_adaptive"
        algo_func = StepAnticipation()
    else
        error("Unsupported algorithm")
    end
    result = simulate(model, algo_func, Val(:full), time=time_final, epochs=epochs, trials=nrep)
    return result
end

function writemodel(result, dir_name)
    mkpath(dir_name)
    for i = 1:length(result.simulation_data)
        temp_array = []
        for j = 1:length(result.simulation_data[i].tdata)
            row = hcat(result.simulation_data[i].tdata[j], result.simulation_data[i].xdata[j][:])
            push!(temp_array, hcat(row))
        end
        open(string(dir_name, i, ".csv"), "w") do io
            writedlm(io, temp_array, ",")
        end
    end
end

# Actual execution
model_name = ARGS[1]
algorithm = ARGS[2]
model = get_model(model_name)
result = run_model(model, algorithm)
dir_name = string("./results/", model_name, "/BioSim_", algorithm, "/")
writemodel(result, dir_name)
