using BioSimulator
using CSV
using DataFrames
using BioSimulator: tablefy

include("models.jl")

function run_model(model, algorithm, nreps, interpolation)
    # simulation parameters
    time_final = 51.0
    # simulate
    if algorithm == "direct"
        algo_func = Direct()
    elseif algorithm == "tau_leaping"
        # NOTE: This is an adaptive tau-leaping algorithm
        algo_func = TauLeapingDGLP2003()
    elseif algorithm == "tau_adaptive"
        algo_func = HybridSAL()
    else
        error("Unsupported algorithm")
    end
    if interpolation == "True"
        results = [simulate(model, algo_func, tfinal=time_final, save_points=0:1:time_final) for _ in 1:nreps]
    else
        results = [simulate(model, algo_func, tfinal=time_final, save_points=nothing) for _ in 1:nreps]
    end
    return results
end

function write_results(results, dir_name, nspecies)
    print(results)
    mkpath(dir_name)
    for i = 1:length(results)
        file_name = string(dir_name, i, ".csv")
        CSV.write(file_name, DataFrame(tablefy(results[i])), delim=',', writeheader=false)
    end
end

# Actual execution
model_name = ARGS[1]
algorithm = ARGS[2]
nreps = parse(Int64, ARGS[3])
interpolation = ARGS[4]
model = get_model(model_name)
if model_name == "00030" || model_name == "00031"
    nspecies = 2
else
    nspecies = 1
end
results = run_model(model, algorithm, nreps, interpolation)
folder_name = interpolation == "True" ? "/BioSimulatorIntp_" : "/BioSimulator_"
dir_name = string("./results/", model_name, folder_name, algorithm, "/")
write_results(results, dir_name, nspecies)
