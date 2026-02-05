def final_decision(risk_score, fidelity_score):
    """
    Central safety decision fusion logic
    """

    if risk_score > 70:
        return "UNSAFE", "Risk score exceeds allowed threshold"

    if fidelity_score < 75:
        return "UNSAFE", "Simulation fidelity too low for hardware trust"

    return "SAFE", "All safety conditions satisfied"
