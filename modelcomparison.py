# -*- coding: utf-8 -*-
"""ModelComparison

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1liys-I9i8g2RRcVFKXzomAouB_UNEjW7
"""

# Import necessary libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import beta, binom
from scipy.special import factorial

# Part 1: Posterior Analysis

# Define data points and prior parameters
data = np.array([10, 15, 15, 14, 14, 14, 13, 11, 12, 16])
n = 20  # Number of trials
alpha1_prior, beta1_prior = 6, 6  # Prior parameters for Model 1
alpha2_prior, beta2_prior = 20, 60  # Prior parameters for Model 2

# Calculate total successes and trials
total_successes = np.sum(data)
total_trials = n * len(data)

# Calculate posterior parameters for both models
alpha1_post = alpha1_prior + total_successes
beta1_post = beta1_prior + total_trials - total_successes
alpha2_post = alpha2_prior + total_successes
beta2_post = beta2_prior + total_trials - total_successes

# Generate theta values for plotting
theta = np.linspace(0, 1, 1000)

# Compute posterior densities for both models
posterior1 = beta.pdf(theta, alpha1_post, beta1_post)
posterior2 = beta.pdf(theta, alpha2_post, beta2_post)

# Create DataFrame for plotting
df = pd.DataFrame({
    'theta': np.concatenate((theta, theta)),
    'density': np.concatenate((posterior1, posterior2)),
    'model': ['Model 1: Beta({}, {})'.format(alpha1_post, beta1_post)] * len(theta) +
             ['Model 2: Beta({}, {})'.format(alpha2_post, beta2_post)] * len(theta)
})

# Plot posterior distributions
plt.figure(figsize=(10, 6))
sns.lineplot(data=df, x='theta', y='density', hue='model')
plt.title('Posterior Distributions of θ for Model 1 and Model 2')
plt.xlabel('θ')
plt.ylabel('Density')
plt.legend(title='Model')
plt.grid(True)
plt.show()

# Exercise 1.2: Compute log pointwise predictive density (lppd) for each model

# Function to compute log pointwise predictive density (lppd) for a given model
def compute_lppd(alpha_prior, beta_prior):
    alpha_posterior = alpha_prior + np.sum(data)
    beta_posterior = beta_prior + len(data) * n - np.sum(data)
    theta_samples = beta.rvs(alpha_posterior, beta_posterior, size=1000)
    log_pd = np.array([np.log(np.mean(binom.pmf(y_i, n, theta_samples))) for y_i in data])
    return np.sum(log_pd)

# Compute lppd for Model 1
lppd_model1 = compute_lppd(alpha1_prior, beta1_prior)
print(f'Log pointwise predictive density for Model 1: {lppd_model1}')

# Compute lppd for Model 2
lppd_model2 = compute_lppd(alpha2_prior, beta2_prior)
print(f'Log pointwise predictive density for Model 2: {lppd_model2}')

# Exercise 1.3: Calculate in-sample deviance for each model from the log pointwise predictive density (lppd)

# Function to compute in-sample deviance for a given model
def compute_deviance(alpha_prior, beta_prior):
    alpha_posterior = alpha_prior + np.sum(data)
    beta_posterior = beta_prior + len(data) * n - np.sum(data)
    theta_samples = beta.rvs(alpha_posterior, beta_posterior, size=1000)
    predictive_densities = [np.mean(binom.pmf(y_i, n, theta_samples)) for y_i in data]
    return -2 * np.sum(np.log(predictive_densities))

# Compute deviance for Model 1
deviance_model1 = compute_deviance(alpha1_prior, beta1_prior)
print(f'In-sample deviance for Model 1: {deviance_model1}')

# Compute deviance for Model 2
deviance_model2 = compute_deviance(alpha2_prior, beta2_prior)
print(f'In-sample deviance for Model 2: {deviance_model2}')

# Exercise 1.4: Based on in-sample deviance, which model is a better fit to the data?
better_model = "Model 1" if deviance_model1 < deviance_model2 else "Model 2"
print(f"{better_model} is a better fit to the data based on in-sample deviance.")

# Exercise 1.5: Predicting new data points and calculating out-of-sample deviance

# Define new data points
new_data_points = np.array([5, 6, 10, 8, 9])

# Function to compute log predictive densities for new data points
def log_predictive_density(y, theta_samples, n):
    return np.log(np.mean(binom.pmf(y, n, theta_samples)))

# Function to compute out-of-sample deviance
def compute_out_of_sample_deviance(alpha_prior, beta_prior):
    alpha_post = alpha_prior + np.sum(data)
    beta_post = beta_prior + len(data) * n - np.sum(data)
    theta_samples = beta.rvs(alpha_post, beta_post, size=1000)
    log_pd_new = np.array([log_predictive_density(y, theta_samples, n) for y in new_data_points])
    return -2 * np.sum(log_pd_new)

# Compute out-of-sample deviance for Model 1
out_sample_deviance_model1 = compute_out_of_sample_deviance(alpha1_prior, beta1_prior)
print(f"Out-of-sample deviance for Model 1: {out_sample_deviance_model1}")

# Compute out-of-sample deviance for Model 2
out_sample_deviance_model2 = compute_out_of_sample_deviance(alpha2_prior, beta2_prior)
print(f"Out-of-sample deviance for Model 2: {out_sample_deviance_model2}")

# Determine which model is better based on out-of-sample deviance
better_model = "Model 1" if out_sample_deviance_model1 < out_sample_deviance_model2 else "Model 2"
print(f"{better_model} is better at predicting new data based on out-of-sample deviance.")

# Exercise 1.6: Perform leave-one-out cross-validation (LOO-CV) to compare models

# Function to compute LOO-CV lppd for a given model
def compute_loo_lppd(alpha_prior, beta_prior):
    loo_lppd = 0
    for i in range(len(data)):
        y_train = np.delete(data, i)
        alpha_post = alpha_prior + np.sum(y_train)
        beta_post = beta_prior + len(y_train) * n - np.sum(y_train)
        theta_samples = beta.rvs(alpha_post, beta_post, size=1000)
        loo_lppd += np.log(np.mean(binom.pmf(data[i], n, theta_samples)))
    return loo_lppd

# Compute LOO-CV lppd and deviance for Model 1
loo_lppd_model1 = compute_loo_lppd(alpha1_prior, beta1_prior)
loo_deviance_model1 = -2 * loo_lppd_model1
print(f'LOO-CV in-sample deviance for Model 1: {loo_deviance_model1}')

# Compute LOO-CV lppd and deviance for Model 2
loo_lppd_model2 = compute_loo_lppd(alpha2_prior, beta2_prior)
loo_deviance_model2 = -2 * loo_lppd_model2
print(f'LOO-CV in-sample deviance for Model 2: {loo_deviance_model2}')

# Determine which model is better based on LOO-CV in-sample deviance
better_model = "Model 1" if loo_deviance_model1 < loo_deviance_model2 else "Model 2"
print(f"{better_model} is better based on LOO-CV in-sample deviance.")

# Part 2: Marginal Likelihood and Prior Sensitivity

# Function to calculate marginal likelihood for binomial data
def ML_binomial(k, n, a, b):
    ML = (factorial(n) / (factorial(k) * factorial(n - k))) * \
         (factorial(k + a - 1) * factorial(n - k + b - 1) / factorial(n + a + b - 1))
    return ML

# Number of successes (k) and trials (n)
k = 2
n = 10

# List of priors to evaluate
priors = [(0.1, 0.4), (1, 1), (2, 6), (6, 2), (20, 60), (60, 20)]

# Calculate marginal likelihoods for each prior
ml_values = [ML_binomial(k, n, p[0], p[1]) for p in priors]

# Print results
for i, prior in enumerate(priors):
    print(f"Marginal likelihood for Beta({prior[0]}, {prior[1]}): {ml_values[i]}")

# Exercise 2.2: Estimate the marginal likelihood using Monte Carlo Integration

# Function to compute marginal likelihood using Monte Carlo integration
def mc_integration(k, n, a, b, N=10000):
    theta_samples = beta.rvs(a, b, size=N)  # Draw samples from Beta distribution
    likelihoods = binom.pmf(k, n, theta_samples)  # Compute likelihoods for each sample
    marginal_likelihood = np.mean(likelihoods)  # Average the likelihoods
    return marginal_likelihood

# Calculate Monte Carlo estimated marginal likelihood for each prior
mc_ml_values = [mc_integration(k, n, p[0], p[1]) for p in priors]

# Print results
for i, prior in enumerate(priors):
    print(f"Monte Carlo estimated marginal likelihood for Beta({prior[0]}, {prior[1]}): {mc_ml_values[i]}")