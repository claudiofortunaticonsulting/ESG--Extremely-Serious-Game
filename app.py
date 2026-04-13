import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Improved simulation parameters
st.sidebar.title('Simulation Parameters')
num_simulations = st.sidebar.number_input('Number of Simulations', min_value=1, max_value=1000, value=100)
duration = st.sidebar.slider('Duration (Years)', min_value=1, max_value=10, value=5)
initial_investment = st.sidebar.number_input('Initial Investment', min_value=0, value=10000)

class Azienda:
    def __init__(self, initial_investment):
        self.initial_investment = initial_investment
        self.profit_history = []
        self.current_value = initial_investment

    def simulate_year(self):
        # Example profit generation logic
        profit = np.random.normal(loc=0.1, scale=0.02) * self.current_value
        self.current_value += profit
        self.profit_history.append(profit)

def run_sim(num_simulations, duration, initial_investment):
    azienda = Azienda(initial_investment)
    metrics = {'Year': [], 'Profit': [], 'Total Value': []}

    for year in range(duration):
        azienda.simulate_year()
        metrics['Year'].append(year + 1)
        metrics['Profit'].append(azienda.profit_history[-1])
        metrics['Total Value'].append(azienda.current_value)

    return metrics

if __name__ == '__main__':
    st.title('Azienda Simulation')
    metrics = run_sim(num_simulations, duration, initial_investment)
    df = pd.DataFrame(metrics)

    # Visualization
    st.subheader('Profit Over Time')
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=df, x='Year', y='Profit', marker='o')
    st.pyplot()

    st.subheader('Total Value Over Time')
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=df, x='Year', y='Total Value', marker='o', color='g')
    st.pyplot()