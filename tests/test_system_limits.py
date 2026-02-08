    def test_cube_constants(self):
        """The 3×3×3 cube: 27 total, 26 exterior, 1 center."""
        from formulas.constants import CUBE_TOTAL, CUBE_EXTERIOR, CUBE_CENTER
        assert CUBE_TOTAL == 27
        assert CUBE_EXTERIOR == 26
        assert CUBE_CENTER == 1
        assert CUBE_EXTERIOR + CUBE_CENTER == CUBE_TOTAL

    def test_cube_generates_alpha_beta(self):
        """ALPHA and BETA are ratios of the cube, not arbitrary values."""
        from formulas.constants import CUBE_EXTERIOR, CUBE_TOTAL, CUBE_CENTER
        assert abs(ALPHA - CUBE_EXTERIOR / CUBE_TOTAL) < 1e-10
        assert abs(BETA - CUBE_CENTER / CUBE_TOTAL) < 1e-10
