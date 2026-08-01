import unittest
import sys, os

# Adicionar root do projeto no path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.overlay.tyre_predictor import TyrePredictor

class TestTyrePredictor(unittest.TestCase):
    def setUp(self):
        self.predictor = TyrePredictor()
        
    def test_initial_state(self):
        # Nenhuma volta ainda
        p = self.predictor.get_predictions()
        self.assertIsNone(p)
        
    def test_calibrating_state(self):
        # Definir volta atual (ex. primeira volta completa) sem desgaste substancial calculado
        self.predictor.update_wear((5.0, 5.0, 5.0, 5.0))
        self.predictor.update_lap(1, 50)
        
        # Teste deve retornar que esta calibrando (wear rate = 0 ou <= 0.01)
        p = self.predictor.get_predictions()
        self.assertIsNotNone(p)
        self.assertTrue(p.get("is_calibrating"))
        
    def test_valid_prediction_state(self):
        self.predictor.update_wear((5.0, 5.0, 5.0, 5.0))
        self.predictor.update_lap(1, 50)
        
        self.predictor.update_wear((6.5, 6.0, 6.0, 6.0))
        self.predictor.update_lap(2, 50)
        
        p = self.predictor.get_predictions()
        
        self.assertIsNotNone(p)
        self.assertFalse(p.get("is_calibrating"))
        
        # O delta foi de 1.5 no pneu mais gasto (RL), worst_rate = 1.5
        self.assertEqual(p["worst_rate"], 1.5)
        self.assertEqual(p["worst_current"], 6.5)
        
        # next_lap = 6.5 + 1.5 = 8.0
        self.assertEqual(p["next_lap"], 8.0)
        
        # in_5_laps = 6.5 + 1.5 * 5 = 14.0
        self.assertEqual(p["in_5_laps"], 14.0)

if __name__ == '__main__':
    unittest.main()
