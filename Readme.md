# Weather Forecast API

This API provides endpoints to retrieve weather forecasts in JSON format based on a provided dataset.

## Getting Started

To get started with using the Weather Forecast API, follow the instructions below.

### Prerequisites

- Python 3.x
- Flask (install via `pip install Flask`)

### Installation

1. Clone the repository:

    ```bash
    git clone <repository-url>
    ```

2. Navigate to the project directory:

    ```bash
    cd weather_forecasting
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

### Usage

1. Start the Flask server:

    ```bash
    flask run
    ```

2. Once the server is running, you can access the following endpoints:

    - `/forecasts`: Retrieve the most recent weather forecasts for a given time.
        - Parameters:
            - `now`: Current datetime (ISO format)
            - `then`: Target datetime (ISO format)
        - Example usage:
            ```bash
            GET http://localhost:5000/forecasts?now=2024-02-14T12:00:00&then=2024-02-15T12:00:00
            ```

    - `/tomorrow`: Determine if the next day is expected to be warm, sunny, and windy.
        - Parameters:
            - `now`: Current datetime (ISO format)
        - Example usage:
            ```bash
            GET http://localhost:5000/tomorrow?now=2024-02-14T12:00:00
            ```

3. Replace `http://localhost:5000` with the appropriate host and port if the server is running on a different address.
