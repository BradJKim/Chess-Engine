from django.test import TestCase
from .views import predict
from chess import Board

# Create your tests here.
class PredictionTestCase(TestCase):
    def setUp(self):
        self.fen = 'rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1'

    """ def test_prediction_route(self):
        result = predict(self.fen)
        self.assertEqual(isinstance(result, str), True) """

    """ def test_fen_to_board(self):
        result = predict(self.fen)
        self.assertEqual(type(result) is Board, True) """
    
    """ def test_return_move(self):
        result = predict(self.fen)
        print(result)
        self.assertEqual(isinstance(result, str), True) """