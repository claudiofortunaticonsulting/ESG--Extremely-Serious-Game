import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="ESG Market Game", layout="wide")

st.title("🌱 ESG Market Simulator")
st.markdown("Gioca con il mercato: scopri quando ESG vince davvero.")

# SIDEBAR
st.sidebar.header("Parametri")

MARKET_CONTROL = st.sidebar.slider("Controllo mercato", 0.1, 1.0, 0.6)
PENALTY = st.sidebar.slider("Penalità greenwashing", 0.2, 1.0, 0.7)
ESG_COST = st.sidebar.slider("Costo ESG", 5, 40, 15)
ESG_REWARD = st.sidebar.slider("Reward ESG", 0.05, 1.0, 0.3)
GW_BONUS = st.sidebar.slider("Bonus Greenwashing", 0.1, 0.5, 0.25)
THRESHOLD = st.sidebar.slider("Soglia conversione", 0.1, 0.8, 0.4)

class Azienda:
    def __init__(self):
        self.strategy = np.random.choice(['ESG','Greenwash','Waiter'], p=[0.1,0.2,0.7])
        self.reputation = 0.9

    def step(self, esg_pct):
        profit = 20

        if self.strategy == 'ESG':
            profit -= ESG_COST
            profit += esg_pct * ESG_REWARD
            self.reputation = min(1.2, self.reputation + 0.02)

        elif self.strategy == 'Greenwash':
            prob = MARKET_CONTROL * (1.2 - self.reputation)
            if np.random.rand() < prob:
                profit *= (1 - PENALTY)
                self.reputation *= 0.6
            else:
                profit += ESG_COST * GW_BONUS

        elif self.strategy == 'Waiter':
            if esg_pct > THRESHOLD:
                self.strategy = 'ESG'

        profit *= (0.6 + 0.4 * self.reputation)

        return max(0, profit)

def run_sim():
    pop = [Azienda() for _ in range(100)]
    history = {'ESG':[], 'Greenwash':[], 'Waiter':[]}

    for _ in range(50):
        strategies = [a.strategy for a in pop]
        esg_pct = strategies.count('ESG') / 100

        profits = {'ESG':[], 'Greenwash':[], 'Waiter':[]}

        for a in pop:
            p = a.step(esg_pct)
            profits[a.strategy].append(p)

        avg = {k: np.mean(v) if v else 0 for k,v in profits.items()}

        for a in pop:
            if np.random.rand() < 0.15:
                best = max(avg, key=avg.get)
                if best != a.strategy and np.random.rand() < 0.5:
                    a.strategy = best

        for k in history:
            history[k].append(strategies.count(k))

    return history

if st.button("🚀 Run Simulation"):
    history = run_sim()

    fig, ax = plt.subplots()
    ax.plot(history['ESG'], label='ESG')
    ax.plot(history['Greenwash'], label='Greenwash')
    ax.plot(history['Waiter'], label='Waiter')
    ax.legend()

    st.pyplot(fig)
    st.success("Simulazione completata!")
