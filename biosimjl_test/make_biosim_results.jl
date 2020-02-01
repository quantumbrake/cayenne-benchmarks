using BioSimulator
using DelimitedFiles

function model_00001()
    # initialize
    model = Network("Model 00001")
    # species definitions
    model <= Species("S1", 100)
    # rate definitions
    k1 = 0.1
    k2 = 0.11
    # reaction definitions
    model <= Reaction("birth", k1, "S1 --> S1 + S1")
    model <= Reaction("death", k2, "S1 --> 0")
    return model
end

function model_00003()
    # initialize
    model = Network("Model 00003")
    # species definitions
    model <= Species("S1", 100)
    # rate definitions
    k1 = 1.0
    k2 = 1.1
    # reaction definitions
    model <= Reaction("birth", k1, "S1 --> S1 + S1")
    model <= Reaction("death", k2, "S1 --> 0")
    return model
end


function get_model(model_name)
    if model_name == "00001"
        model = model_00001()
    elseif model_name == "00003"
        model = model_00003()
    else
        error("Unsupported model_name")
    end
    return model
end

function run_model(model, algorithm)
    # simulation parameters
    nrep = 10000
    time_final = 50.0
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
    result = simulate(model, algo_func, time=time_final, epochs=epochs, trials=nrep, output_type=Val(:fixed))
    return result
end

function writemodel(result, dir_name)
    mkpath(dir_name)
    for i = 1:length(result.simulation_data)
        open(string(dir_name, i, ".csv"), "w") do io
            writedlm(io, hcat(result.simulation_data[i].tdata[:], result.simulation_data[i].xdata[:]), ",")
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
