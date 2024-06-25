import random
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from joblib import Parallel, delayed

# Données historiques de température (date, latitude, longitude, température en °F)
historical_data = [
    # Données de Lyon
    (datetime(2010, 1, 1), 45.7640, 4.8357, 32),
    (datetime(2010, 7, 1), 45.7640, 4.8357, 77),
    (datetime(2015, 1, 1), 45.7640, 4.8357, 34),
    (datetime(2015, 7, 1), 45.7640, 4.8357, 79),
    (datetime(2020, 1, 1), 45.7640, 4.8357, 36),
    (datetime(2020, 7, 1), 45.7640, 4.8357, 78),
    (datetime(2022, 1, 1), 45.7640, 4.8357, 35),
    (datetime(2022, 7, 1), 45.7640, 4.8357, 80),
    (datetime(2023, 1, 1), 45.7640, 4.8357, 33),
    (datetime(2023, 7, 1), 45.7640, 4.8357, 81),
    (datetime(2024, 6, 24), 45.7640, 4.8357, 69),  # Ajouté

    # Données d'Istanbul
    (datetime(2010, 1, 1), 41.0082, 28.9784, 41),
    (datetime(2010, 7, 1), 41.0082, 28.9784, 82),
    (datetime(2015, 1, 1), 41.0082, 28.9784, 43),
    (datetime(2015, 7, 1), 41.0082, 28.9784, 84),
    (datetime(2020, 1, 1), 41.0082, 28.9784, 45),
    (datetime(2020, 7, 1), 41.0082, 28.9784, 83),
    (datetime(2022, 1, 1), 41.0082, 28.9784, 44),
    (datetime(2022, 7, 1), 41.0082, 28.9784, 85),
    (datetime(2023, 1, 1), 41.0082, 28.9784, 42),
    (datetime(2023, 7, 1), 41.0082, 28.9784, 86),
    (datetime(2024, 6, 24), 41.0082, 28.9784, 76),  # Ajouté

    # Données de Tokyo
    (datetime(2010, 1, 1), 35.6895, 139.6917, 41),
    (datetime(2010, 7, 1), 35.6895, 139.6917, 86),
    (datetime(2015, 1, 1), 35.6895, 139.6917, 43),
    (datetime(2015, 7, 1), 35.6895, 139.6917, 88),
    (datetime(2020, 1, 1), 35.6895, 139.6917, 45),
    (datetime(2020, 7, 1), 35.6895, 139.6917, 87),
    (datetime(2022, 1, 1), 35.6895, 139.6917, 44),
    (datetime(2022, 7, 1), 35.6895, 139.6917, 89),
    (datetime(2023, 1, 1), 35.6895, 139.6917, 42),
    (datetime(2023, 7, 1), 35.6895, 139.6917, 90),
    (datetime(2024, 6, 24), 35.6895, 139.6917, 80),  # Ajouté

    # Données de New York
    (datetime(2010, 1, 1), 40.7128, -74.0060, 35),
    (datetime(2010, 7, 1), 40.7128, -74.0060, 80),
    (datetime(2015, 1, 1), 40.7128, -74.0060, 37),
    (datetime(2015, 7, 1), 40.7128, -74.0060, 82),
    (datetime(2020, 1, 1), 40.7128, -74.0060, 39),
    (datetime(2020, 7, 1), 40.7128, -74.0060, 81),
    (datetime(2022, 1, 1), 40.7128, -74.0060, 38),
    (datetime(2022, 7, 1), 40.7128, -74.0060, 83),
    (datetime(2023, 1, 1), 40.7128, -74.0060, 36),
    (datetime(2023, 7, 1), 40.7128, -74.0060, 84),
    (datetime(2024, 6, 24), 40.7128, -74.0060, 83),  # Ajouté

    # Données de Sydney
    (datetime(2010, 1, 1), 33.8688, 151.2093, 72),
    (datetime(2010, 7, 1), 33.8688, 151.2093, 60),
    (datetime(2015, 1, 1), 33.8688, 151.2093, 74),
    (datetime(2015, 7, 1), 33.8688, 151.2093, 62),
    (datetime(2020, 1, 1), 33.8688, 151.2093, 76),
    (datetime(2020, 7, 1), 33.8688, 151.2093, 61),
    (datetime(2022, 1, 1), 33.8688, 151.2093, 75),
    (datetime(2022, 7, 1), 33.8688, 151.2093, 63),
    (datetime(2023, 1, 1), 33.8688, 151.2093, 73),
    (datetime(2023, 7, 1), 33.8688, 151.2093, 64),
    (datetime(2024, 6, 24), 33.8688, 151.2093, 53)  # Ajouté
]

# Modifiez la fonction d'initialisation pour créer des individus plus grands
def initialize_population(size, seed_size=37):  # Augmenté de 23 à 37
    return np.random.uniform(-1, 1, (size, seed_size))

def mutate(population, mutation_rate):
    population = np.array(population)  # Convertir en tableau NumPy si ce n'est pas déjà le cas
    mutation = np.random.normal(0, mutation_rate, population.shape)
    return population + mutation

def fitness(population, historical_data):
    total_error = Parallel(n_jobs=-1)(delayed(single_fitness)(individual, historical_data) for individual in population)
    total_error = np.array(total_error)
    return (1 - total_error / max_possible_error) * 100

def single_fitness(individual, historical_data):
    error = 0
    for date, lat, lon, actual_temp in historical_data:
        generated_temp = temperature_generator(date, lat, lon, individual)
        error += np.abs(generated_temp - actual_temp)
    return error

def universalist_universe_equation(Ev, Ed, Em, C_values, Pz, Re, Ec, Is, Ws, H, T):
    # Composantes de l'Énergie totale
    E = Ev + Ed + Em

    # Conscience collective
    C = sum(C_values)
    
    # Spiritualité et valeurs universelles
    S = Pz + Re + Ec

    # Lumière de l’illumination spirituelle
    L = Is + Ws

    # Potentialités et possibilités futures
    P = f(T)
    
    # Équation de l'Univers Universaliste
    U = (E + (C * S * L) / H) * P
    return U

def f(T):
    # Fonction des potentialités et possibilités futures dépendant du temps
    # Vous pouvez ajuster cette fonction selon vos besoins
    return T

def temperature_generator(date, lat, lon, individual):
    day_of_year = date.timetuple().tm_yday
    seasonal_factor = np.sin(2 * np.pi * day_of_year / 365)
    
    base_temp = 15 + 10 * seasonal_factor
    lat_effect = (lat - 45) * individual[0]
    lon_effect = (lon - 4) * individual[1]
    time_effect = (date.year - 2010) * individual[2]
    
    altitude_effect = individual[3]
    humidity_effect = individual[4] * seasonal_factor
    urban_heat_effect = individual[5] * (1 + 0.1 * (date.year - 2010))
    ocean_current_effect = individual[6] * np.sin(2 * np.pi * (day_of_year + 60) / 365)
    solar_activity_effect = individual[7] * np.random.normal(0, 1)
    climate_change_effect = individual[8] * (date.year - 2010) ** 2 / 100
    
    # Nouveaux effets ajoutés
    el_nino_effect = individual[9] * np.sin(2 * np.pi * (date.year - 2010) / 5)  # Cycle El Niño approximatif
    volcanic_activity = individual[10] * np.random.poisson(0.1)  # Activité volcanique rare mais impactante
    jet_stream_effect = individual[11] * np.sin(4 * np.pi * day_of_year / 365)  # Effet du courant-jet
    land_use_change = individual[12] * (date.year - 2010) / 10  # Changement progressif d'utilisation des terres
    air_pollution_effect = individual[13] * (1 + np.sin(2 * np.pi * day_of_year / 365))  # Effet cyclique de la pollution
    ocean_oscillation = individual[14] * np.sin(2 * np.pi * (date.year - 2010) / 60)  # Oscillation océanique à long terme
    
    # Effets d'interaction
    latitude_season_interaction = individual[15] * lat * seasonal_factor
    urban_heat_pollution_interaction = individual[16] * urban_heat_effect * air_pollution_effect
    climate_change_ocean_interaction = individual[17] * climate_change_effect * ocean_oscillation
    
    # Nouveaux effets spéciaux
    gravity_effect = individual[18] * 9.8  # Effet fictif de la gravité
    human_appearance_effect = individual[19] * (date.year - 2000000)  # Apparition des humains il y a 2 millions d'années
    stock_market_effect = individual[20] * np.sin(2 * np.pi * (date.year - 2020) / 5)  # Effet basé sur un cycle boursier fictif
    
    random_effect = np.random.normal(0, 1) * individual[21]
    long_term_trend = individual[22] * (date.year - 2010) ** 3 / 1000  # Tendance à très long terme
    
    # Universalist Universe Equation components
    Ev = individual[23]
    Ed = individual[24]
    Em = individual[25]
    C_values = individual[26:26+5]  # Assume we have 5 components for C_values
    Pz = individual[31]
    Re = individual[32]
    Ec = individual[33]
    Is = individual[34]
    Ws = individual[35]
    H = individual[36]
    T = (date - datetime(2010, 1, 1)).days / 365  # Convert date to years since 2010
    
    U = universalist_universe_equation(Ev, Ed, Em, C_values, Pz, Re, Ec, Is, Ws, H, T)

    return (base_temp + lat_effect + lon_effect + time_effect + altitude_effect + 
            humidity_effect + urban_heat_effect + ocean_current_effect + 
            solar_activity_effect + climate_change_effect + el_nino_effect +
            volcanic_activity + jet_stream_effect + land_use_change +
            air_pollution_effect + ocean_oscillation + latitude_season_interaction +
            urban_heat_pollution_interaction + climate_change_ocean_interaction +
            gravity_effect + human_appearance_effect + stock_market_effect +
            random_effect + long_term_trend + U)

def selection(population, scores, elite_size):
    elite_indices = np.argsort(scores)[-elite_size:]
    elite = population[elite_indices]
    
    selection_probs = scores / np.sum(scores)
    selected_indices = np.random.choice(len(population), len(population) - elite_size, p=selection_probs)
    selected = population[selected_indices]
    
    return np.vstack((elite, selected))

def crossover(elite, offspring_size):
    offspring = []
    num_elite = elite.shape[0]
    for _ in range(offspring_size):
        parent1_idx, parent2_idx = np.random.choice(num_elite, 2, replace=False)
        parent1, parent2 = elite[parent1_idx], elite[parent2_idx]
        child = np.where(np.random.rand(*parent1.shape) < 0.5, parent1, parent2)
        offspring.append(child)
    return np.array(offspring)

def select_elite(population, scores, elite_size):
    elite_indices = np.argsort(scores)[-elite_size:]
    return np.array(population[elite_indices])

# Augmentons la taille de la population et ajustons d'autres paramètres
population_size = 300  # Diminuez de 10000 à 5000 pour tester
mutation_rate = 0.1  # Légèrement réduit
elite_size = 12  # Augmenté de 50 à 100
generations_per_iteration = 50  # Diminuez de 1000 à 500 pour tester

# Le reste des fonctions (crossover, mutate, select_elite) reste inchangé
# Définition de max_possible_error
max_possible_error = sum([abs(200 - actual_temp) for _, _, _, actual_temp in historical_data])

# Dans la boucle principale
population = initialize_population(population_size, seed_size=37)
best_fitness = float('-inf')
best_individual = None
iteration = 0

average_fitness_per_generation = []
best_fitness_history = []

try:
    while True:
        for generation in range(generations_per_iteration):
            scores = fitness(population, historical_data)
            average_fitness = np.mean(scores)
            average_fitness_per_generation.append(average_fitness)
            
            best_index = np.argmax(scores)
            if scores[best_index] > best_fitness:
                best_fitness = scores[best_index]
                best_individual = population[best_index]
            
            best_fitness_history.append(best_fitness)
            
            elite = select_elite(population, scores, elite_size)
            offspring = crossover(elite, population_size - elite_size)
            offspring = mutate(offspring, mutation_rate)
            
            population = np.vstack((elite, offspring))
        
        iteration += 1
        print(f"Iteration {iteration} completed. Best fitness: {best_fitness}")
        print(f"Best seed: {best_individual}")
        
        # Affichage du graphique toutes les 10 itérations
        # if iteration % 10 == 0:
        #     plt.figure(figsize=(12, 6))
        #     plt.plot(average_fitness_per_generation, label='Average Fitness')
        #     plt.plot(best_fitness_history, label='Best Fitness')
        #     plt.title('Fitness per Generation')
        #     plt.xlabel('Generation')
        #     plt.ylabel('Fitness')
        #     plt.legend()
        #     plt.show()
        
        # Affichage des meilleurs seeds en temps réel
        print(f"Best fitness after iteration {iteration}: {best_fitness}")
        print(f"Best seed after iteration {iteration}: {best_individual}")
        
except KeyboardInterrupt:
    print("Training interrupted by user.")
    print(f"Best fitness achieved: {best_fitness}")
    print(f"Best seed: {best_individual}")
