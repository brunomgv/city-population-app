from flask import Flask, jsonify, request
from elasticsearch import Elasticsearch, exceptions

app = Flask(__name__)
es = Elasticsearch("http://elasticsearch:9200")

index_name = "cities"  # Name of the Elasticsearch index

def create_index():
    # Check if the index exists
    if not es.indices.exists(index=index_name):
        # Create the index if it doesn't exist
        es.indices.create(index=index_name)

create_index()  # Create the index when the application starts

def validate_insert_or_update_payload(data):
    # Validate the input data for the insert or update endpoint
    if not data or "city" not in data or "population" not in data:
        return False, "Invalid data. 'city' and 'population' are required."

    city = data["city"]
    population = data["population"]

    if not isinstance(city, str):
        return False, "Invalid data type. 'city' must be a string."

    if not isinstance(population, int):
        return False, "Invalid data type. 'population' must be an integer."

    if population < 0:
        return False, "Invalid population value. 'population' must be a non-negative integer."

    return True, ""

@app.route("/city", methods=["POST"])
def insert_or_update_city():
    # Retrieve the request payload as JSON
    data = request.get_json()

    # Validate the input data
    valid, error_message = validate_insert_or_update_payload(data)
    if not valid:
        return jsonify({"error": error_message}), 400

    city = data["city"]
    population = data["population"]

    try:
        # Check if the city already exists in the index
        result = es.get(index=index_name, id=city)
        existing_population = result["_source"]["population"]

        # Update the population if it's different from the existing value
        if existing_population != population:
            doc = {"city": city, "population": population}
            es.index(index=index_name, id=city, body=doc)
            message = "Population updated successfully"
        else:
            message = "Population unchanged"

        operation = "update"

    except exceptions.NotFoundError:
        # City doesn't exist, insert a new document
        doc = {"city": city, "population": population}
        es.index(index=index_name, id=city, body=doc)
        message = "City inserted successfully"
        operation = "insert"

    except exceptions.RequestError:
        # Elasticsearch request error
        return jsonify({"error": "Elasticsearch request error"}), 500

    except Exception:
        # Generic error
        return jsonify({"error": "An error occurred"}), 500

    # Return the response
    return jsonify({"message": message, "operation": operation})


def validate_get_population_parameter(city):
    # Validate the city parameter for the get_population endpoint
    if not isinstance(city, str):
        return False, "Invalid request. 'city' parameter must be a string."
    return True, ""


@app.route("/population/<city>", methods=["GET"])
def get_population(city):
    # Validate the city parameter
    valid, error_message = validate_get_population_parameter(city)
    if not valid:
        return jsonify({"error": error_message}), 400

    try:
        # Retrieve the document from Elasticsearch
        result = es.get(index=index_name, id=city)
        population = result["_source"]["population"]
        return jsonify({"city": city, "population": population})

    except exceptions.NotFoundError:
        # City not found
        return jsonify({"error": "City not found"}), 404

    except exceptions.RequestError:
        # Elasticsearch request error
        return jsonify({"error": "Elasticsearch request error"}), 500

    except Exception:
        # Generic error
        return jsonify({"error": "An error occurred"}), 500
    
@app.route("/health", methods=["GET"])
def health_check():
    """
    Endpoint to check the health of the application.
    """
    return "OK"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)