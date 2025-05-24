def aggregate(signals, weights=None):
    """
    signals: dict of {name: {pair: signal_value}}
    weights: optional blend weights per signal name
    """
    if weights is None:
        weights = {k: 1/len(signals) for k in signals}
    scores = {}
    for name, sig in signals.items():
        w = weights.get(name, 1/len(signals))
        for pair, val in sig.items():
            scores[pair] = scores.get(pair, 0) + w * val
    # keep positive only
    alloc = {p: max(0, s) for p, s in scores.items()}
    total = sum(alloc.values()) or 1
    return {p: s/total for p, s in alloc.items()}
