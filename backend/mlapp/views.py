from django.shortcuts import render
from .models import ChessCNN
from .utils import fen_to_binary
from .models import ChessCNN
import torch
import chess
import os
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

model = ChessCNN()
model_path = os.path.join(os.path.dirname(__file__), '../chess_model(1).pth')
model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
model.eval() 

@csrf_exempt 
def predict(request):
    print(request.method)
    if request.method == 'POST':
        try:
            # request is fen board
            """ 
            Get fen from request
            convert fen to python chess board
            Get legal moves from chess board
            """
            data = json.loads(request.body)
            chess_board = chess.Board(fen=data['fen'])
            legal_moves = chess_board.legal_moves

            # Minmax alg: for each possible board, calculate score of all possible opponent move boards and return next
            """ 
            dict- move: highest board eval

            For each possible move
                create new chess board from move
                store max eval

                for each possible opponent move from board  
                    Make board with move
                    Get fen
                    convert binary
                    predict eval
                    store eval if greater
                
                store in dict
            """
            dict = {}

            for move in legal_moves:
                new_board = chess_board.copy()
                new_board.push(move)
                
                max_eval = -100000.0

                for opp_move in new_board.legal_moves:
                    new_opp_board = new_board.copy()
                    new_opp_board.push(opp_move)
                    binary = fen_to_binary(new_opp_board.fen())
                    
                    bin_tensor = torch.Tensor(list(binary))

                    with torch.inference_mode():
                        y_pred = model(bin_tensor)
                        if y_pred > max_eval:
                            max_eval = y_pred

                dict[move] = max_eval

            # return move with min of max eval
            """ 
            return move from dict with highest board eval
            """
            best_move = ''
            min = 100000.0

            for key, value in dict.items():
                print(key, value.item()) 
                if value.item() < min:
                    best_move = key
                    min = value.item()

            return JsonResponse({"move": str(best_move)})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    return JsonResponse({"message": "Only POST requests are accepted"}, status=405)