# City Population Application

This application maintains a list of cities and their populations. It provides endpoints to insert or update city data and retrieve the population of a city. The data is stored in Elasticsearch and the application is containerized using Docker, packaged for deployment to Kubernetes using a Helm chart.

## Endpoints

- `/health`: GET request to check the health of the application. Returns "OK" if the application is running.
- `/city`: POST request to insert or update a city and its population. Expects a JSON payload with the city name and population.
- `/population/{city_name}`: GET request to retrieve the population of a city. Returns the population as a JSON response.

## Requirements

- Docker
- Kubernetes
- Helm
- Python 3.x

## Installation and Deployment

1. Clone the repository:

```sh
git clone https://github.com/brunomgv/city-population-app.git
```

2. Build the Docker image:

```sh
cd city-population-app
docker build -t city-app:latest .
```

3. Push the Docker image to a container registry:

```sh
docker push your-container-registry/city-app:latest
```

4. Deploy Elasticsearch to Kubernetes using Helm:

```sh
helm repo add elastic https://helm.elastic.co
helm repo update
helm install elasticsearch elastic/elasticsearch
```

5. Deploy the City Population application to Kubernetes using Helm:

```sh
helm install city-app city-app/
```

## Usage

- Check the health of the application:

```sh
curl http://localhost:5000/health
```

- Insert or update city data:

```sh
curl -X POST -H "Content-Type: application/json" -d '{"city":"CityName","population":100000}' http://localhost:5000/city
```

- Retrieve the population of a city:

```sh
curl http://localhost:5000/population/CityName
```

Replace `CityName` with the desired city name and `100000` with the population value.

**_NOTE:_** Make sure Elasticsearch and the City Population application are running and accessible before making requests.

## Configuration

- Elasticsearch Configuration: The application is configured to connect to Elasticsearch using the `elasticsearch` hostname. Update the `app.py` file if your Elasticsearch deployment has a different hostname.

- Docker Image: If you push the Docker image to a container registry other than the default one, update the image name (`city-app:latest`) in the Helm chart's deployment.yaml file.

- Kubernetes Service: By default, the City Population application is exposed as a Kubernetes service on port 80. If you want to change the port or access type, modify the `service` section in the Helm chart's deployment.yaml file.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License.