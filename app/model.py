import pandas as pd
from sklearn.calibration import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, f1_score

def preprocess_data(df):
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df['Day'] = df['Date'].dt.day
        df['Month'] = df['Date'].dt.month
        df['Year'] = df['Date'].dt.year
        df['Days_Since'] = (df['Date'] - df['Date'].min()).dt.days  
    
    if 'Date' in df.columns:
        df = df.drop(columns=["Date"])
    categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
    for col in categorical_columns:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
    
    return df

def train_model(dataset_path):
    df = pd.read_csv(dataset_path)
    df = preprocess_data(df)
    X = df.drop(columns=["Downtime"])
    y = df["Downtime"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = DecisionTreeClassifier()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average="binary")

    return model, accuracy, f1


def predict_downtime(hydraulic_pressure, coolant_pressure, air_system_pressure, coolant_temperature,
                     hydraulic_oil_temperature, spindle_bearing_temperature, spindle_vibration,
                     tool_vibration, spindle_speed, voltage, torque, cutting):
    model = train_model("uploaded_data/sample_data.csv")[0] 
    input_features = [[
        hydraulic_pressure, coolant_pressure, air_system_pressure, coolant_temperature,
        hydraulic_oil_temperature, spindle_bearing_temperature, spindle_vibration,
        tool_vibration, spindle_speed, voltage, torque, cutting
    ]]
    prediction = model.predict(input_features)[0]
    confidence = model.predict_proba(input_features)[0][prediction]
    
    prediction_str = "Yes" if prediction == 1 else "No"
    
    return prediction_str, confidence

