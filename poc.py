#This is a simple example of the humidity level sensor using particle filtering
#Simple data of probabilities of level humid (low, medium ,high)

# Low Medium High
# 0.7, 0.2, 0.1
# 0.3, 0.5, 0.2
# 0.1, 0.3, 0.6

# #The emission ~ normal distribution
# low ~ N(20,3)
# medium ~ N(50,5)
# high ~ N(80,4)


######## Attempt draft #######

import numpy as np
from numpy.random import normal
#Define  HMM
prob_matrix = np.array([[0.7, 0.2, 0.1],
                              [0.3, 0.5, 0.2],
                              [0.1, 0.3, 0.6]])

emission_params = np.array([[20, 3],   # Low humidity: mean=20, std=3
                            [50, 5],   # Medium humidity: mean=50, std=5
                            [80, 4]])  # High humidity: mean=80, std=4

#Function to generate noisy sensor readings
def generate_sensor_reading(true_state):
    mean, std = emission_params[true_state]
    return np.random.normal(mean, std)

#Particle filtering algorithm
def particle_filter(num_particles, observations):
    num_states = prob_matrix.shape[0]
    particles = np.random.choice(num_states, size=num_particles)
    weights = np.ones(num_particles) / num_particles

    for obs in observations:
        #Predict:move particles according to probabilities
        particles = np.random.choice(num_states, size=num_particles, p=prob_matrix[particles[-1]])

        #Update: calculate weights based on observation likelihood
        observation_likelihoods = np.exp(-0.5 * ((obs - emission_params[:, 0])**2) / (emission_params[:, 1]**2))
        weights *= observation_likelihoods[particles]
        weights /= np.sum(weights)

        #Resampling:based on weights
        indices = np.random.choice(num_particles, size=num_particles, p=weights)
        particles = particles[indices]
        weights.fill(1.0 / num_particles)

    #Estimate the humidity level using weighted average of particles
    estimated_humidity = np.sum(particles * weights)
    return estimated_humidity

#Simulated sensor 
sensor_readings = [generate_sensor_reading(state) for state in [0, 1, 2, 1, 0]]

#Number of particles
num_particles = 1000

# Estimate humidity using particle filtering
estimated_humidity = particle_filter(num_particles, sensor_readings)
print("Estimated Humidity Level:", estimated_humidity)

