import pandas as pd
import time
import numpy as np
from sklearn.ensemble import RandomForestRegressor, IsolationForest

# ----------------------------
# Reinforcement Learning Setup
# ----------------------------
Q = np.zeros((3, 3))  # 3 states, 3 actions
alpha = 0.1
gamma = 0.9

def get_state(cpu):
    if cpu < 40:
        return 0
    elif cpu < 75:
        return 1
    else:
        return 2

def update_replicas(new_value):
    with open("replica_state.txt", "w") as f:
        f.write(str(new_value))

def get_current_replicas():
    with open("replica_state.txt", "r") as f:
        return int(f.read())

def log_scaling(predicted_cpu, decision, replicas):
    with open("scaling_log.txt", "a") as f:
        f.write(f"Predicted CPU: {predicted_cpu:.2f} → {decision} → Replicas: {replicas}\n")

def run_prediction():
    try:
        data = pd.read_csv("metrics_log.csv")

        if len(data) < 30:
            print("Waiting for enough data...")
            return

        # ----------------------------
        # Train Random Forest Model
        # ----------------------------
        X = data[["request_count", "memory", "response_time"]]
        y = data["cpu"]

        model = RandomForestRegressor(n_estimators=50)
        model.fit(X, y)

        latest = X.iloc[-1:].values
        predicted_cpu = model.predict(latest)[0]

        # ----------------------------
        # Anomaly Detection
        # ----------------------------
        iso = IsolationForest(contamination=0.02)
        anomaly_labels = iso.fit_predict(data[["cpu", "memory", "response_time"]])

        if anomaly_labels[-1] == -1:
            print("⚠ Anomaly Detected!")

        # ----------------------------
        # Reinforcement Learning Policy
        # ----------------------------
        state = get_state(predicted_cpu)
        action = np.argmax(Q[state])

        replicas = get_current_replicas()
        decision = "Maintain"

        # Scaling logic
        if predicted_cpu > 75:
            replicas += 1
            decision = "Scale Up"
        elif predicted_cpu < 40 and replicas > 1:
            replicas -= 1
            decision = "Scale Down"

        # RL reward update
        reward = 5 if action == state else -2
        Q[state, action] += alpha * (
            reward + gamma * np.max(Q[state]) - Q[state, action]
        )

        update_replicas(replicas)
        log_scaling(predicted_cpu, decision, replicas)

        print(f"Predicted CPU: {predicted_cpu:.2f} → {decision} → Replicas: {replicas}")

    except Exception as e:
        print("Error:", e)

# ----------------------------
# Continuous Monitoring Loop
# ----------------------------
while True:
    run_prediction()
    time.sleep(5)
