####################
# System 1
####################

MODEL_00001 = """
    r1: S1 => S1 + S1; k1*S1;
    r2: S1 => ; k2*S1;

    k1 = 0.1;
    k2 = 0.11;

    S1 = 100;
"""

MODEL_00003 = """
    r1: S1 => S1 + S1; k1*S1;
    r2: S1 => ; k2*S1;

    k1 = 1.0;
    k2 = 1.1;

    S1 = 100;
"""

MODEL_00004 = """
    r1: S1 => S1 + S1; k1*S1;
    r2: S1 => ; k2*S1;

    k1 = 0.1;
    k2 = 0.11;

    S1 = 10;
"""

MODEL_00005 = """
    r1: S1 => S1 + S1; k1*S1;
    r2: S1 => ; k2*S1;

    k1 = 0.1;
    k2 = 0.11;

    S1 = 10000;
"""

MODEL_00011 = """
    r1: S1 => S1 + S1; k1*S1;
    r2: S1 => ; k2*S1;

    k1 = 0.05;
    k2 = 0.055;

    S1 = 100;
"""
####################
# System 2
####################

MODEL_00020 = """
    r1: => S1; k1;
    r2: S1 => ; k2*S1;

    k1 = 1.0;
    k2 = 0.1;

    S1 = 0;
"""

MODEL_00021 = """
    r1: => S1; k1;
    r2: S1 => ; k2*S1;

    k1 = 10..0;
    k2 = 0.1;

    S1 = 0;
"""

MODEL_00022 = """
    r1: => S1; k1;
    r2: S1 => ; k2*S1;

    k1 = 5.0;
    k2 = 0.1;

    S1 = 0;
"""

MODEL_00023 = """
    r1: => S1; k1;
    r2: S1 => ; k2*S1;

    k1 = 1000.0;
    k2 = 0.1;

    S1 = 0;
"""

####################
# System 3
####################

MODEL_00030 = """
    r1: S1 + S1 => S2; k1*S1*S1;
    r2: S2 => S1 + S1; k2*S2;

    k1 = 0.0005;
    k2 = 0.01;

    S1 = 100;
    S2 = 0;
"""

MODEL_00031 = """
    r1: S1 + S1 => S2; k1*S1*S1;
    r2: S2 => S1 + S1; k2*S2;

    k1 = 0.0001;
    k2 = 0.004;

    S1 = 1000;
    S2 = 0;
"""

####################
# System 3
####################

MODEL_00037 = """
    r1: => 5 S1; k1;
    r2: S1 => ; k2*S1;

    k1 = 1.0;
    k2 = 0.2;

    S1 = 0;
"""

MODEL_00038 = """
    r1: => 10 S1; k1;
    r2: S1 => ; k2*S1;

    k1 = 1.0;
    k2 = 0.4;

    S1 = 0;
"""

MODEL_00039 = """
    r1: => 100 S1; k1;
    r2: S1 => ; k2*S1;

    k1 = 1.0;
    k2 = 4;

    S1 = 0;
"""


def get_model(model_id):
    """ Returns model given model_id """
    model_name = "MODEL_" + model_id
    return globals()[model_name]
