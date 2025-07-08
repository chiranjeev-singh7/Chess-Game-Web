from flask import Flask, request, jsonify, session
from flask_cors import CORS
import chess

app = Flask(__name__)
CORS(app)
app.secret_key = "supersecret"

AI_COLOR = chess.BLACK

piece_values = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0
}

board = chess.Board()
move_history = []

def evaluate_board(board):
    if board.is_checkmate():
        return -9999 if board.turn else 9999
    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    eval = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            value = piece_values[piece.piece_type]
            eval += value if piece.color == chess.BLACK else -value
    return eval

def minimax(board, depth, alpha, beta, maximizing):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board), None

    best_move = None

    if maximizing:
        max_eval = -float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval, _ = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval, _ = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move

@app.route("/new_game", methods=["POST"])
def new_game():
    global board, move_history
    board = chess.Board()
    move_history = []
    session["mode"] = request.json.get("mode", "human")
    return jsonify({
        "fen": board.fen(),
        "message": "New game started!"
    })

@app.route("/move", methods=["POST"])
def make_move():
    global board, move_history
    data = request.get_json()
    move_str = data["move"]
    mode = data.get("mode", "human")
    session["mode"] = mode

    move = chess.Move.from_uci(move_str)
    if move not in board.legal_moves:
        return jsonify({
            "fen": board.fen(),
            "message": "Illegal move.",
            "success": False
        })

    board.push(move)
    move_history.append(move.uci())
    player = "w" if board.turn == chess.BLACK else "b"

    response = {
        "fen": board.fen(),
        "message": "Move made.",
        "move_text": move.uci(),
        "success": True,
        "player": player
    }

    if mode == "ai" and not board.is_game_over():
        _, ai_move = minimax(board, 2, -float('inf'), float('inf'), True)
        if ai_move:
            board.push(ai_move)
            move_history.append(ai_move.uci())
            response["fen"] = board.fen()
            response["ai_move"] = ai_move.uci()
            response["message"] = f"AI played {ai_move.uci()}"
            response["player"] = "b"

    if board.is_checkmate():
        response["message"] += " Checkmate!"
    elif board.is_stalemate():
        response["message"] += " Stalemate."

    return jsonify(response)

@app.route("/undo", methods=["POST"])
def undo():
    global board, move_history
    mode = request.json.get("mode", "human")
    if board.move_stack:
        board.pop()
        if mode == "ai" and board.move_stack:
            board.pop()
        move_history = move_history[:-2] if mode == "ai" else move_history[:-1]
    return jsonify({
        "fen": board.fen(),
        "message": "Move undone!"
    })

if __name__ == "__main__":
    app.run(debug=True)
