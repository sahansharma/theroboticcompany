@ai_bp.route('/ask', methods=['POST'])
def ask_ai():
    # Receives prompt and streams AI response using OpenAI
