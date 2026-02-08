import math


class PresenceLogic:
    """
    Temporal Presence: P_t = e^(-|delta_t|/tau)

    delta_t = mental displacement from now
    tau = attention window width (meditation expands this)

    P = 1: total presence (here and now)
    P < 1: mind scattered in past/future
    """

    @staticmethod
    def compute(delta_t, tau=1.0):
        """P_t = e^(-|delta_t|/tau)"""
        return math.exp(-abs(delta_t) / max(tau, 0.001))

    @staticmethod
    def compute_pt(delta_t, tau=1.0):
        """Alias: P_t = e^(-|delta_t|/tau)"""
        return PresenceLogic.compute(delta_t, tau)

    @staticmethod
    def from_state(anxiety=0, depression=0, mindfulness=1.0):
        """
        Compute from human-readable values (0-10 scales).

        anxiety: how much the mind is in the future
        depression: how much the mind is in the past
        mindfulness: width of attention (meditation expands)
        """
        delta_t = max(anxiety, depression)
        tau = max(0.1, mindfulness)
        return PresenceLogic.compute(delta_t, tau)


TemporalPresence = PresenceLogic
