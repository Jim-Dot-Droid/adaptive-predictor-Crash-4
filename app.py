import streamlit as st
import numpy as np

st.title("Crash Game Predictor (Adaptive + Accuracy)")

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []
if "correct_predictions" not in st.session_state:
    st.session_state.correct_predictions = 0
if "total_predictions" not in st.session_state:
    st.session_state.total_predictions = 0
if "last_prediction" not in st.session_state:
    st.session_state.last_prediction = None

# Sidebar: manual input and controls
st.sidebar.header("Manual Input")
new_val = st.sidebar.text_input("Enter multiplier (e.g., 1.87)")
if st.sidebar.button("Add to history"):
    try:
        f = float(new_val)
        # Check previous prediction accuracy
        if st.session_state.last_prediction is not None:
            actual = "Above" if f > 2 else "Under"
            if actual == st.session_state.last_prediction:
                st.session_state.correct_predictions += 1
            st.session_state.total_predictions += 1
        st.session_state.history.append(f)
        st.sidebar.success(f"Added {f} to history")
    except:
        st.sidebar.error("Invalid number format.")

if st.sidebar.button("Reset history"):
    st.session_state.history = []
    st.session_state.correct_predictions = 0
    st.session_state.total_predictions = 0
    st.session_state.last_prediction = None
    st.sidebar.warning("History and stats reset.")

# Model selection
st.sidebar.header("Prediction Model")
model = st.sidebar.radio("Choose model:", ["Frequency", "Moving Average", "Markov Chain"])

# Display recent history
st.subheader("Recent History (last 10)")
if st.session_state.history:
    recent = st.session_state.history[-10:]
    st.write(recent)
else:
    st.write("No data available.")

# Prediction Models
def frequency_model(data, threshold=2.0):
    if not data:
        return 0.5, 0.5
    data = np.array(data)
    above = np.sum(data > threshold)
    under = np.sum(data <= threshold)
    total = above + under
    return above / total, under / total

def moving_average_model(data, window=5, threshold=2.0):
    if len(data) < window:
        return 0.5, 0.5
    recent = data[-window:]
    avg = np.mean(recent)
    if avg > threshold:
        return 0.7, 0.3
    elif avg < threshold:
        return 0.3, 0.7
    else:
        return 0.5, 0.5

def markov_chain_model(data, threshold=2.0):
    if len(data) < 2:
        return 0.5, 0.5
    states = ["U" if x <= threshold else "A" for x in data]
    transitions = {"U": {"U": 0, "A": 0}, "A": {"U": 0, "A": 0}}
    for i in range(len(states)-1):
        transitions[states[i]][states[i+1]] += 1
    for s in transitions:
        total = transitions[s]["U"] + transitions[s]["A"]
        if total > 0:
            transitions[s]["U"] /= total
            transitions[s]["A"] /= total
    last_state = states[-1]
    return transitions[last_state]["A"], transitions[last_state]["U"]

# Compute confidence based on selected model
history = st.session_state.history
if model == "Frequency":
    above_conf, under_conf = frequency_model(history)
elif model == "Moving Average":
    window = st.sidebar.slider("Moving Average Window", 3, 15, 5)
    above_conf, under_conf = moving_average_model(history, window)
elif model == "Markov Chain":
    above_conf, under_conf = markov_chain_model(history)

# Determine next prediction
if above_conf > under_conf:
    next_prediction = "Above"
else:
    next_prediction = "Under"
st.session_state.last_prediction = next_prediction

# Show confidence and prediction
st.subheader("Next Round Prediction")
st.write(f"Prediction: **{next_prediction} 2**")
st.write(f"Above 200%: {above_conf:.1%} | Under 200%: {under_conf:.1%}")

# Accuracy stats
st.subheader("Prediction Accuracy")
if st.session_state.total_predictions > 0:
    accuracy = (st.session_state.correct_predictions / st.session_state.total_predictions) * 100
else:
    accuracy = 0.0
st.write(f"Correct Predictions: {st.session_state.correct_predictions}/{st.session_state.total_predictions}")
st.write(f"Accuracy: {accuracy:.1f}%")

# Footer
st.markdown("---")
st.write("*Prediction is auto-generated after each input. Accuracy updates after each actual outcome is added.*")
