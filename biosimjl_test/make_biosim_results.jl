using BioSimulator
using DelimitedFiles

include("models.jl")

function run_model(model, algorithm, nreps)
    # simulation parameters
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
    result = simulate(model, algo_func, Val(:full), time=time_final, epochs=epochs, trials=nreps)
    return result
end

function writemodel(result, dir_name, nspecies)
    mkpath(dir_name)
    for i = 1:length(result.simulation_data)
        temp_array = []
        for j = 1:length(result.simulation_data[i].tdata)
            t = result.simulation_data[i].tdata[j]
            x = result.simulation_data[i].xdata[j]
            if nspecies == 2
                row = hcat(t, x[1], x[2])
            else
                row = hcat(t, x)
            end
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
nreps = parse(Int64, ARGS[3])
model = get_model(model_name)
if model_name == "00030" || model_name == "00031"
    nspecies = 2
else
    nspecies = 1
end
result = run_model(model, algorithm, nreps)
dir_name = string("./results/", model_name, "/BioSimulator_", algorithm, "/")
writemodel(result, dir_name, nspecies)
