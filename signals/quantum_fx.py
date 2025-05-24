import dimod
from dimod import SimulatedAnnealingSampler

def quantum_portfolio(returns, cov, risk):
    n = len(returns.columns)
    Q = {}
    mu, Sigma = returns.mean(), returns.cov()
    for i in range(n):
        Q[(i,i)] = (1-risk)*Sigma.iloc[i,i] - risk*mu[i]
        for j in range(i+1, n):
            Q[(i,j)] = (1-risk)*Sigma.iloc[i,j]
    sampler = SimulatedAnnealingSampler()
    sol = next(sampler.sample_qubo(Q, num_reads=20).samples())
    picks = [returns.columns[i] for i,bit in sol.items() if bit]
    if not picks:
        return {}
    w = 1.0 / len(picks)
    return {p: w for p in picks}
