# Chess-Game-Web

# Python Chess Web

A web-based chess game built with:

✅ **Frontend:** HTML, CSS, JavaScript, jQuery, Chessboard.js, Chess.js  
✅ **Backend:** Python Flask (with a simple Minimax AI)  
✅ **Deployment:** Frontend on Netlify, Backend on Render

---

## 🎮 Features

- Play **Human vs Human** or **Human vs AI**
- Pawn promotion (choose the piece!)
- Undo moves
- Highlights king in check
- Displays checkmate and stalemate
- Move list showing played moves
- Responsive design for desktop and mobile

---

## 🌐 Live Demo

- Frontend (Netlify): https://chess-webapp-chiranjeev.netlify.app/

---

## 🚀 How it Works

- The frontend sends move requests via AJAX to the Flask backend.
- The backend validates moves using python-chess.
- In **Human vs AI** mode, the AI responds using a Minimax algorithm.
- Board updates dynamically and shows check/checkmate highlights.
