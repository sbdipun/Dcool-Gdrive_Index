from flask import Flask, request, jsonify

app = Flask(__name__)

# Replace with your custom domain or base URL
BASE_INDEX_URL = ""

@app.route("/direct", methods=["GET"])
def generate_index_link():
    # Extract the Google Drive ID from the query parameters
    gdrive_id = request.args.get("id")

    if not gdrive_id:
        return jsonify({"error": "Missing 'id' parameter"}), 400

    # Construct the index link
    index_link = f"{BASE_INDEX_URL}?id={gdrive_id}"
    return jsonify({"status": "success", "index_link": index_link})

if __name__ == "__main__":
    app.run(debug=True)
