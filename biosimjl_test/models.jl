using BioSimulator

####################
# System 1
####################

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
    model = Network("Model 00003")
    model <= Species("S1", 100)
    k1 = 1.0
    k2 = 1.1
    model <= Reaction("birth", k1, "S1 --> S1 + S1")
    model <= Reaction("death", k2, "S1 --> 0")
    return model
end

function model_00004()
    model = Network("Model 00004")
    model <= Species("S1", 10)
    k1 = 0.1
    k2 = 0.11
    model <= Reaction("birth", k1, "S1 --> S1 + S1")
    model <= Reaction("death", k2, "S1 --> 0")
    return model
end

function model_00005()
    model = Network("Model 00005")
    model <= Species("S1", 10000)
    k1 = 0.1
    k2 = 0.11
    model <= Reaction("birth", k1, "S1 --> S1 + S1")
    model <= Reaction("death", k2, "S1 --> 0")
    return model
end

function model_00011()
    model = Network("Model 00011")
    model <= Species("S1", 100)
    k1 = 0.1 / 2
    k2 = 0.11 / 2
    model <= Reaction("birth", k1, "S1 --> S1 + S1")
    model <= Reaction("death", k2, "S1 --> 0")
    return model
end

####################
# System 2
####################

function model_00020()
    model = Network("Model 00020")
    model <= Species("S1", 0)
    k1 = 1.0
    k2 = 0.1
    model <= Reaction("immigration", k1, "0 --> S1")
    model <= Reaction("death", k2, "S1 --> 0")
    return model
end

function model_00021()
    model = Network("Model 00021")
    model <= Species("S1", 0)
    k1 = 10.0
    k2 = 0.1
    model <= Reaction("immigration", k1, "0 --> S1")
    model <= Reaction("death", k2, "S1 --> 0")
    return model
end

function model_00022()
    model = Network("Model 00022")
    model <= Species("S1", 0)
    k1 = 5.0
    k2 = 0.1
    model <= Reaction("immigration", k1, "0 --> S1")
    model <= Reaction("death", k2, "S1 --> 0")
    return model
end

function model_00023()
    model = Network("Model 00023")
    model <= Species("S1", 0)
    k1 = 1000
    k2 = 0.1
    model <= Reaction("immigration", k1, "0 --> S1")
    model <= Reaction("death", k2, "S1 --> 0")
    return model
end

####################
# System 3
####################

function model_00030()
    model = Network("Model 00030")
    model <= Species("S1", 100)
    model <= Species("S2", 0)
    k1 = 0.001 / 2
    k2 = 0.01
    model <= Reaction("dimerization", k1, "S1 + S1 --> S2")
    model <= Reaction("monomerization", k2, "S2 --> S1 + S1")
    return model
end

function model_00031()
    model = Network("Model 00031")
    model <= Species("S1", 1000)
    model <= Species("S2", 0)
    k1 = 0.0002 / 2
    k2 = 0.004
    model <= Reaction("dimerization", k1, "S1 + S1 --> S2")
    model <= Reaction("monomerization", k2, "S2 --> S1 + S1")
    return model
end

####################
# System 4
####################

function model_00037()
    model = Network("Model 00037")
    model <= Species("S1", 0)
    k1 = 1.0
    k2 = 0.2
    model <= Reaction("immigration", k1, "0 --> 5 * S1")
    model <= Reaction("death", k2, "S1 --> 0")
    return model
end

function model_00038()
    model = Network("Model 00038")
    model <= Species("S1", 0)
    k1 = 1.0
    k2 = 0.4
    model <= Reaction("immigration", k1, "0 --> 10 * S1")
    model <= Reaction("death", k2, "S1 --> 0")
    return model
end

function model_00039()
    model = Network("Model 00039")
    model <= Species("S1", 0)
    k1 = 1.0
    k2 = 4.0
    model <= Reaction("immigration", k1, "0 --> 100 * S1")
    model <= Reaction("death", k2, "S1 --> 0")
    return model
end



function get_model(model_name)
    fn_name = string("model_", model_name)
    try
        fn = getfield(Main, Symbol(fn_name))
        model = fn()
        return model
    catch UndefVarError
        error("Unsupported model name")
    end
end
