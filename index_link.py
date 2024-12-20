import os
import requests
from flask import Flask, request, jsonify, send_file

app = Flask(__name__)

# Route to handle the Google Drive file download request
@app.route("/", methods=["GET"])
def generate_index_link():
    gdrive_id = request.args.get("id")  # Extract Google Drive file ID from the query parameters

    if not gdrive_id:
        return jsonify({"error": "Missing 'id' parameter"}), 400

    # Construct the Google Drive file URL for direct download
    gdrive_url = f"https://drive.google.com/uc?export=download&id={gdrive_id}"

    try:
        # Fetch the file from Google Drive
        response = requests.get(gdrive_url, stream=True)

        # Check if the file download was successful
        if response.status_code == 200:
            # Set the filename (we can use the Google Drive ID for simplicity)
            filename = f"{gdrive_id}.download"

            # Get the content length from the headers (file size)
            file_size = response.headers.get('Content-Length', None)

            # If file size is available, print it
            if file_size:
                print(f"File size: {int(file_size) / 1024:.2f} KB")

            # Send the file as an attachment with the correct filename
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
