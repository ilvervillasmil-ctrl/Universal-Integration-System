tests/
============================= test session starts ==============================
platform linux -- Python 3.10.19, pytest-9.0.2, pluggy-1.6.0
rootdir: /home/runner/work/Universal-Integration-System/Universal-Integration-System
configfile: pyproject.toml
collected 237 items

tests/test_coherence_engine.py ............                              [  5%]
tests/test_constants.py ..                                               [  5%]
tests/test_energy.py .........                                           [  9%]
tests/test_entropy.py ...........                                        [ 14%]
tests/test_entropy_fractality.py ......F..                               [ 18%]
tests/test_greetings.py ...........                                      [ 22%]
tests/test_integration_cross_module.py .........                         [ 26%]
tests/test_interaction.py ........                                       [ 29%]
tests/test_metaconsciousness.py .......                                  [ 32%]
tests/test_negentropy.py ......                                          [ 35%]
tests/test_neuroscience_logic.py ............                            [ 40%]
tests/test_phi_dynamics.py ............                                  [ 45%]
tests/test_presence.py .                                                 [ 45%]
tests/test_resonance.py ..                                               [ 46%]
tests/test_resonance_extended.py ..                                      [ 47%]
tests/test_resonance_processor.py .....................                  [ 56%]
tests/test_security_edge_cases.py ...................................... [ 72%]
....                                                                     [ 74%]
tests/test_self_prediction.py .........                                  [ 78%]
tests/test_stability.py .................                                [ 85%]
tests/test_universal.py .................................                [ 99%]
tests/test_vision_manifestation.py .                                     [ 99%]
tests/test_wonder.py .                                                   [100%]

=================================== FAILURES ===================================
_ TestEntropyFractalityIntegration.test_fractal_first_level_dominates_entropy __

self = <test_entropy_fractality.TestEntropyFractalityIntegration object at 0x7fe3d30f9ed0>

    def test_fractal_first_level_dominates_entropy(self):
        """
        In a PHI-based fractal distribution, the first level
        gets the most energy (total/PHI). Removing it should
        significantly change the entropy.
        """
        energies = Fractality.fractal_energy_distribution(1.0, 7)
        entropy_full = EntropyTool.adjusted_entropy(energies)
        entropy_without_first = EntropyTool.adjusted_entropy(energies[1:])
>       assert entropy_without_first > entropy_full
E       assert 1.5219314575407645 > 1.5391164804423627

tests/test_entropy_fractality.py:101: AssertionError
=========================== short test summary info ============================
FAILED tests/test_entropy_fractality.py::TestEntropyFractalityIntegration::test_fractal_first_level_dominates_entropy - assert 1.5219314575407645 > 1.5391164804423627
======================== 1 failed, 236 passed in 0.46s =========================
Error: Process completed with exit code 1.
