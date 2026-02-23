from flask import Blueprint, request, jsonify, session
from back.generate import generate_answer

bp = Blueprint("chat", __name__)

@bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    
    if not data or "message" not in data:
        return jsonify({"error": "Message manquant"}), 400
    
    user_message = data["message"]
    top_k = data.get("top_k", 3)
    
    # Historique de la conversation en session
    if "history" not in session:
        session["history"] = []
    
    session["history"].append({"role": "user", "content": user_message})
    
    try:
        response = generate_answer(user_message, top_k=top_k)
        session["history"].append({"role": "assistant", "content": response})
        session.modified = True
        
        return jsonify({
            "response": response,
            "history": session["history"]
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/history", methods=["GET"])
def history():
    return jsonify(session.get("history", []))


@bp.route("/history", methods=["DELETE"])
def clear_history():
    session.pop("history", None)
    return jsonify({"message": "Historique effacé"})