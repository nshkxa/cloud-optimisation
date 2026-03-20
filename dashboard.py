import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="AI Cloud Auto-Scaling Dashboard", layout="wide")

st.title("🚀 Intelligent Cloud Resource Management Dashboard")

st.markdown("""
### 📘 Metric Descriptions
- **CPU Usage (%)** → Current processor utilization of the server.
- **Memory Usage (%)** → Current RAM usage.
- **Response Time (ms)** → Time taken to respond to user request.
- **Replicas** → Number of active service instances (simulated Kubernetes scaling).
""")

placeholder = st.empty()

while True:
    try:
        data = pd.read_csv("metrics_log.csv")

        latest = data.iloc[-1]

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("CPU Usage (%)", f"{latest['cpu']:.2f}")
        col2.metric("Memory Usage (%)", f"{latest['memory']:.2f}")
        col3.metric("Response Time (ms)", f"{latest['response_time']:.2f}")
        col4.metric("Active Replicas", int(latest["replicas"]))

        st.markdown("---")

        st.subheader("📊 Live Performance Trends")

        st.line_chart(data["cpu"], use_container_width=True)
        st.line_chart(data["memory"], use_container_width=True)
        st.line_chart(data["response_time"], use_container_width=True)
        st.line_chart(data["replicas"], use_container_width=True)

        st.markdown("---")

        # Scaling Log Display
        try:
            with open("scaling_log.txt", "r") as f:
                logs = f.readlines()[-5:]
                st.subheader("⚙️ Recent Scaling Decisions")
                for log in logs:
                    st.text(log.strip())
        except:
            pass

        time.sleep(3)

    except:
        st.warning("Waiting for metrics data...")
        time.sleep(3)
