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

@app.route("/health", methods=["GET"])
def health_check():
    """
    Endpoint to check the health of the application.
    """
    return "OK"

@app.route("/city", methods=["POST"])
def insert_or_update_city():
    """
    Endpoint to insert or update city data
    """
    city = request.json.get("city")
    population = request.json.get("population")

    if not city or not population:
        return jsonify({"error": "Invalid data. 'city' and 'population' are required."}), 400

    try:
        # Check if the city already exists in the index
        result = es.get(index=index_name, id=city)
        operation = "update"

        # Retrieve the existing population
        existing_population = result["_source"]["population"]
        if existing_population != population:
            # Update the population if it has changed
            doc = {"city": city, "population": population}
            es.index(index=index_name, id=city, body=doc)
            message = "Population updated successfully"
        else:
            message = "Population unchanged"
    except exceptions.NotFoundError:
        operation = "insert"

        # Insert the new city document
        doc = {"city": city, "population": population}
        es.index(index=index_name, id=city, body=doc)
        message = "City inserted successfully"
    except exceptions.RequestError:
        return jsonify({"error": "Elasticsearch request error"}), 500
    except Exception:
        return jsonify({"error": "An error occurred"}), 500

    return jsonify({"message": message, "operation": operation})

@app.route("/population/<city>", methods=["GET"])
def get_population(city):
    """
    Endpoint to retrieve the population of a specific city
    """
    if not city:
        return jsonify({"error": "Invalid request. 'city' parameter is missing."}), 400

    try:
        # Retrieve the city document from the index
        result = es.get(index=index_name, id=city)
        population = result["_source"]["population"]
        return jsonify({"city": city, "population": population})
    except exceptions.NotFoundError:
        return jsonify({"error": "City not found"}), 404
    except exceptions.RequestError:
        return jsonify({"error": "Elasticsearch request error"}), 500
    except Exception:
        return jsonify({"error": "An error occurred"}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)