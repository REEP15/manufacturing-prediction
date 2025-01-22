
# Manufacturing Prediction API

## Setup and Usage

1. Clone the repository:
    ```bash
    git clone https://github.com/REEP15/manufacturing-prediction.git
    cd manufacturing-prediction
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the API:
    ```bash
    python app/main.py
    ```

4. Test the API using postman:
    - **Upload file**: `POST /upload` (Upload CSV with machine data).
    - **Train model**: `POST /train` (Train the model and get metrics).
    - **Predict downtime**: `POST /predict` (Provide data to predict downtime).

Data used to train (sample_data.csv) taken from Kaggle (https://www.kaggle.com/datasets/srinivasanusuri/optimization-of-machine-downtime?resource=download)
