from flask import Flask, jsonify, request, redirect
from flask_cors import CORS

app = Flask(__name__)
CORS(
    app,
    origins=["*"],
    methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "ngrok-skip-browser-warning"],
)


@app.route("/")
def index():
    return redirect("https://github.com/ghrlt/statiflix-backend")


DATABASE = {}


@app.route("/temporary/accounts/add", methods=["POST"])
def add_account():
    """
    POST /temporary/accounts/add

    Adds a new account to the temporary accounts database.

    Body should contain a JSON object with the following keys:

    - unique-identifier (required)
    - content (required)

    Returns a JSON object with a success message upon successful addition.
    Returns a 400 error if the unique-identifier key is not present in the body.
    Returns a 409 error if the unique-identifier already exists in the database.
    """

    data = request.get_json()
    if not data.get("unique-identifier"):
        return jsonify({"message": "unique-identifier is required"}), 400

    if data.get("unique-identifier") in DATABASE:
        return jsonify({"message": "unique-identifier already exists"}), 409

    DATABASE[data.get("unique-identifier")] = data.get("content")

    return jsonify({"message": "success"}), 201


@app.route("/temporary/accounts/get", methods=["GET"])
def get_account():
    """
    GET /temporary/accounts/get

    Retrieves a new account from the temporary accounts database.

    Body should contain a JSON object with the following keys:

    - unique-identifier (required)

    Returns a JSON object with the stored data if the unique-identifier exists.

    Returns a 400 error if the unique-identifier key is not present in the body.
    Returns a 404 error if the unique-identifier does not exist in the database.
    """

    data = request.args.to_dict()
    if not data.get("unique-identifier"):
        return jsonify({"message": "unique-identifier is required"}), 400

    if data.get("unique-identifier") not in DATABASE:
        return (
            jsonify(
                {
                    "message": f"unique-identifier `{data.get('unique-identifier')}` does not exist"
                }
            ),
            404,
        )

    return jsonify({"data": DATABASE[data.get("unique-identifier")]})


@app.route("/temporary/accounts/delete", methods=["DELETE"])
def delete_account():
    """
    DELETE /temporary/accounts/delete

    Deletes a new account from the temporary accounts database.

    Body should contain a JSON object with the following key:

    - unique-identifier (required)

    Returns a JSON object with a success message upon successful deletion.
    Returns a 400 error if the unique-identifier key is not present in the body.
    Returns a 204 error if the unique-identifier was not found in the database.
    """

    data = request.args.to_dict()
    if not data.get("unique-identifier"):
        return jsonify({"message": "unique-identifier is required"}), 400

    if data.get("unique-identifier") not in DATABASE:
        return (
            jsonify(
                {
                    "message": f"unique-identifier `{data.get('unique-identifier')}` does not exist"
                }
            ),
            204,
        )

    del DATABASE[data.get("unique-identifier")]

    return jsonify({"message": "success"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8082, debug=False)
