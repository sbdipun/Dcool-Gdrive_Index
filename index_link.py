import os
import requests
from flask import Flask, request, jsonify, send_file

app = Flask(__name__)

@app.route("/", methods=["GET"])
def generate_index_link():
    gdrive_id = request.args.get("id")  # This gets the 'id' parameter from the query string

    if not gdrive_id:
        return jsonify({"error": "Missing 'id' parameter"}), 400

    # Construct the Google Drive file URL
    gdrive_url = f"https://drive.google.com/uc?export=download&id={gdrive_id}"

    try:
        # Fetch the file from Google Drive
        response = requests.get(gdrive_url, stream=True)

        if response.status_code == 200:
            # Get the file name from the Google Drive ID (or provide a custom name)
            filename = gdrive_id + ".download"

            # Send the file as an attachment
            return send_file(
                response.raw,
                as_attachment=True,
                download_name=filename,
                mimetype="application/octet-stream"
            )
        else:
            return jsonify({"error": "Failed to download the file from Google Drive."}), 500

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error fetching the file: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
