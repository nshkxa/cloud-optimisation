import pandas as pd
import time
from sklearn.ensemble import RandomForestRegressor

def update_replicas(new_value):
    with open("replica_state.txt", "w") as f:
        f.write(str(new_value))

def log_scaling(predicted_cpu, decision, replicas):
    with open("scaling_log.txt", "a") as f:
        f.write(f"Predicted CPU: {predicted_cpu:.2f} → {decision} → Replicas: {replicas}\n")

def run_prediction():
    try:
        data = pd.read_csv("metrics_log.csv")

        if len(data) < 20:
            return

        X = data[["request_count", "memory", "response_time"]]
        y = data["cpu"]

        model = RandomForestRegressor(n_estimators=50)
        model.fit(X, y)

        latest = X.iloc[-1:].values
        predicted_cpu = model.predict(latest)[0]

        with open("replica_state.txt", "r") as f:
            replicas = int(f.read())

        decision = "Maintain"

        if predicted_cpu > 75:
            replicas += 1
            decision = "Scale Up"
        elif predicted_cpu < 40 and replicas > 1:
            replicas -= 1
            decision = "Scale Down"

        update_replicas(replicas)
        log_scaling(predicted_cpu, decision, replicas)

        print(f"Predicted CPU: {predicted_cpu:.2f} → {decision} → Replicas: {replicas}")

    except:
        pass

while True:
    run_prediction()
    time.sleep(5)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
