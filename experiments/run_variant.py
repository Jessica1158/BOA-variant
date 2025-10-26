import math, random, os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Crear carpetas para guardar resultados y figuras
os.makedirs("results", exist_ok=True)
os.makedirs("figures", exist_ok=True)

# ===============================
# 1. Definición del problema CHLP
# ===============================
class Problem:
    def __init__(self):
        self.n_clients = 24
        self.n_hubs = 8

        # Matriz de distancias cliente-hub (24 x 8)
        self.distancias = [
            [6, 8, 12, 7, 9, 6, 10, 11],
            [5, 9, 6, 10, 8, 7, 9, 12],
            [8, 7, 10, 6, 11, 9, 8, 10],
            [7, 6, 8, 9, 10, 6, 7, 9],
            [9, 6, 9, 12, 7, 10, 11, 8],
            [6, 5, 10, 11, 9, 8, 6, 7],
            [8, 7, 6, 6, 10, 8, 9, 9],
            [7, 6, 10, 8, 6, 9, 11, 10],
            [5, 9, 11, 7, 11, 8, 10, 12],
            [9, 6, 7, 8, 9, 6, 10, 8],
            [6, 10, 8, 7, 5, 9, 6, 8],
            [8, 6, 9, 10, 6, 8, 10, 7],
            [7, 9, 10, 8, 11, 9, 7, 8],
            [6, 7, 8, 9, 10, 8, 9, 11],
            [9, 8, 6, 10, 7, 6, 9, 10],
            [7, 6, 9, 8, 10, 7, 6, 9],
            [8, 9, 10, 6, 11, 10, 8, 7],
            [9, 7, 6, 9, 10, 8, 7, 6],
            [6, 8, 7, 10, 9, 7, 8, 6],
            [8, 9, 10, 8, 9, 10, 9, 7],
            [7, 6, 8, 9, 7, 9, 10, 8],
            [5, 9, 11, 10, 9, 7, 8, 6],
            [6, 8, 7, 9, 6, 10, 11, 9],
            [8, 7, 9, 8, 10, 8, 7, 6],
        ]
        self.costs = [22, 25, 18, 20, 19, 24, 21, 23]
        self.capacidad = [4, 4, 4, 4, 4, 3, 4, 3]
        self.D_max = 9

    def check(self, x):
        conteo = [0] * self.n_hubs
        for c in range(self.n_clients):
            h = x[c]
            if self.distancias[c][h] > self.D_max:
                return False
            conteo[h] += 1
            if conteo[h] > self.capacidad[h]:
                return False
        return True

    def fit(self, x):
        hubs = [0] * self.n_hubs
        total = sum(self.distancias[c][x[c]] for c in range(self.n_clients))
        for h in x:
            hubs[h] = 1
        total += sum(self.costs[j] for j in range(self.n_hubs) if hubs[j] == 1)
        return total


# ====================================
# 2. Definición de la partícula (bobcat)
# ====================================
class Particle:
    def __init__(self, problem):
        self.p = problem
        self.dimension = self.p.n_clients
        self.position = [random.randint(0, self.p.n_hubs - 1) for _ in range(self.dimension)]
        self.p_best = self.position.copy()
        self.best_fit = self.p.fit(self.position)
        self.stagnation = 0

    def fitness(self):
        return self.p.fit(self.position)

    def update_p_best(self):
        f = self.fitness()
        if f < self.best_fit:
            self.best_fit = f
            self.p_best = self.position.copy()
            self.stagnation = 0
        else:
            self.stagnation += 1

    # --- Fase de rastreo (exploración) ---
    def tracking_and_move(self, swarm, alpha):
        CP = [p for p in swarm if p.fitness() < self.fitness()]
        if not CP:
            return
        SP = random.choice(CP).position
        new_position = []
        for k in range(self.dimension):
            I = random.choice([1, 2])
            r = random.random()
            val = self.position[k] + alpha * ((1 - 2*r) * (SP[k] - I * self.position[k]))
            val = max(0, min(self.p.n_hubs - 1, round(val)))
            new_position.append(val)
        if self.p.check(new_position):
            self.position = new_position

    # --- Fase de persecución (explotación) ---
    def chasing_to_catch(self, t, alpha):
        new_position = []
        for k in range(self.dimension):
            r = random.random()
            val = self.position[k] + alpha * (((1 - 2*r)/(1+t)) * self.position[k])
            val = max(0, min(self.p.n_hubs - 1, round(val)))
            new_position.append(val)
        if self.p.check(new_position):
            self.position = new_position

    # --- Mutación adaptativa si se estanca ---
    def mutate(self, mutation_rate):
        for i in range(self.dimension):
            if random.random() < mutation_rate:
                self.position[i] = random.randint(0, self.p.n_hubs - 1)
        if not self.p.check(self.position):
            # Reajuste si mutación genera solución inválida
            self.position = [random.randint(0, self.p.n_hubs - 1) for _ in range(self.dimension)]


# ==================================
# 3. Algoritmo principal AE-BOA
# ==================================
class AEBOA:
    def __init__(self, n_particles, max_iter, p_elite=0.2, stagnation_limit=10, mutation_rate=0.05):
        self.N = n_particles
        self.T = max_iter
        self.p = Problem()
        self.swarm = []
        self.global_best = None
        self.convergence = []
        self.p_elite = p_elite
        self.stagnation_limit = stagnation_limit
        self.mutation_rate = mutation_rate

    def initialize(self):
        while len(self.swarm) < self.N:
            p = Particle(self.p)
            if self.p.check(p.position):
                self.swarm.append(p)
        self.global_best = min(self.swarm, key=lambda s: s.fitness())
        self.convergence.append(self.global_best.fitness())

    def evolve(self):
        for t in range(1, self.T + 1):
            alpha = 1 - (t / self.T)  # factor adaptativo
            elite_size = max(1, int(self.p_elite * self.N))
            elites = sorted(self.swarm, key=lambda s: s.fitness())[:elite_size]

            for p in self.swarm:
                # Probabilidad de guiarse por la élite
                if random.random() < self.p_elite:
                    elite = random.choice(elites)
                    for i in range(p.dimension):
                        if random.random() < 0.3:
                            p.position[i] = elite.position[i]

                # Fases BOA clásicas
                p.tracking_and_move(self.swarm, alpha)
                p.chasing_to_catch(t, alpha)
                p.update_p_best()

                # Mutación si no mejora por mucho tiempo
                if p.stagnation >= self.stagnation_limit:
                    p.mutate(self.mutation_rate)

            # Actualizar global best
            candidate = min(self.swarm, key=lambda s: s.fitness())
            if candidate.fitness() < self.global_best.fitness():
                self.global_best = candidate

            self.convergence.append(self.global_best.fitness())
            print(f"Iter {t}: Mejor global = {self.global_best.fitness():.3f}")

    def solve(self):
        self.initialize()
        self.evolve()
        return self.global_best


# ==================================
# 4. Ejecución experimental
# ==================================
part = 20
iter = 1000
n_runs = 20

resultados = []
convergencia = None
mayor_mejora = -float('inf')

for i in range(n_runs):
    print(f"\n--- Ejecución {i+1} ---")
    boa = AEBOA(part, iter)
    best = boa.solve()
    resultados.append(best.fitness())
    mejora = boa.convergence[0] - boa.convergence[-1]
    if mejora > mayor_mejora:
        mayor_mejora = mejora
        convergencia = boa.convergence

# Guardar resumen estadístico
serie = pd.Series(resultados, name='fitness')
summary = serie.describe(percentiles=[0.25, 0.5, 0.75]).rename({
    '25%': 'Q1',
    '50%': 'Mediana',
    '75%': 'Q3'
})
summary_df = summary.to_frame().T
summary_df.to_csv("results/resultados_variant.txt", index=False)

print("\nResultados de cada corrida:", resultados)
print("\nTabla de resumen:\n", summary_df)

# ============================
# 5. Gráficos de resultados
# ============================
plt.figure(figsize=(10, 5))
plt.plot(convergencia, marker='o')
plt.title('Convergencia AE-BOA (instancia dura)')
plt.xlabel('Iteración')
plt.ylabel('Mejor Fitness')
plt.grid(True)
plt.tight_layout()
plt.savefig("figures/Convergencia_variant.png")

f_optimo = 271
f_max = max(convergencia)
qmetric_iter = [(f_max - f_ach) / (f_max - f_optimo) if f_max != f_optimo else 0 for f_ach in convergencia]
qmetric_iter = [max(0, min(1, q)) for q in qmetric_iter]

plt.figure(figsize=(10, 5))
plt.plot(qmetric_iter, color='green')
plt.title('QMetric por iteración (AE-BOA)')
plt.xlabel('Iteración')
plt.ylabel('QMetric')
plt.grid(True)
plt.tight_layout()
plt.savefig("figures/QMetric_variant.png")

plt.figure(figsize=(6, 5))
sns.boxplot(data=resultados, orient='v', color='skyblue')
plt.title('Boxplot del fitness (AE-BOA)')
plt.ylabel('Fitness')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig("figures/Boxplot_variant.png")
