import math


class ExternalInteraction:
    """
    I_ext = sqrt(C1^2 + C2^2 + 2*C1*C2*cos(theta))

    theta = 0:   Love (coherence adds)
    theta = pi/2: Independence
    theta = pi:  Conflict (destructive)
    """

    @staticmethod
    def compute_pair(c1, c2, theta=0.0):
        """Interaction between two systems."""
        inner = c1**2 + c2**2 + 2 * c1 * c2 * math.cos(theta)
        return math.sqrt(max(0.0, inner))

    @staticmethod
    def compute_multi(coherences, angles=None):
        """Interaction between n systems."""
        n = len(coherences)
        if n == 0:
            return 0.0
        if n == 1:
            return coherences[0]
        total = sum(c**2 for c in coherences)
        for i in range(n):
            for j in range(i + 1, n):
                theta = 0.0
                if angles is not None:
                    theta = angles[i][j]
                total += 2 * coherences[i] * coherences[j] * math.cos(theta)
        return math.sqrt(max(0.0, total))

    @staticmethod
    def love(c1, c2):
        """theta=0: C1 + C2"""
        return c1 + c2

    @staticmethod
    def independence(c1, c2):
        """theta=pi/2: sqrt(C1^2 + C2^2)"""
        return math.sqrt(c1**2 + c2**2)

    @staticmethod
    def conflict(c1, c2):
        """theta=pi: |C1 - C2|"""
        return abs(c1 - c2)
