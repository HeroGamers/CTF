from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder="static")

comments = ["Awesome recipy!!1! - Oliver"]

# Serve the static HTML file
@app.route('/')
def serve_html():
    return send_from_directory('static', 'index.html')

# Endpoint to get all comments
@app.route('/comments', methods=['GET'])
def get_comments():
    return jsonify(comments)

# Endpoint to post a new comment
@app.route('/comment', methods=['POST'])
def post_comment():
    data = request.json
    if 'comment' in data:
        comments.append(data['comment'] + " - Guest")
        return jsonify({"status": "success", "message": "Comment added!"}), 201
    return jsonify({"status": "error", "message": "Invalid input"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0')
