import matplotlib.pyplot as plt
import tellurium as te

model = """
r1: S1 => ; k1*S1;
r2: S1 + S1 => S2; k2*S1*(S1-1);
r3: S2 => S1 + S1; k3*S2;
r4: S2 => S3; k4*S2;

k1 = 1;
k2 = 0.002;
k3 = 0.5;
k4 = 0.04;

S1 = 4150;
S2 = 39565;
S3 = 3445;
"""


te_model = te.loada(model)
te_model.integrator = "gillespie"
# te_model.integrator.seed = 1234
te_model.integrator.variable_step_size = True

nrep = 10
points = 1_000_000

sim_list = []
for i in range(nrep):
    te_model.reset()
    sim = te_model.simulate(0, 10, steps=points)
    sim_list.append(sim)
    fig = te_model.plot(sim, alpha=0.7, show=False)
te.show()
plt.savefig("simulation.pdf")
