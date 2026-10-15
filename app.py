import time
import logging
import numpy as np
from flask import Flask, request, jsonify

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)
logger = logging.getLogger("dl-api")

app = Flask(__name__)

# Class labels for simulated classification model
CLASSES = ["Cat", "Dog", "Bird", "Other"]

def mock_deep_learning_inference(input_vector: list) -> dict:
    """
    Simulates a Deep Learning Neural Network forward pass:
    - Input projection (Dense layer: 5 features -> 4 output classes)
    - Softmax activation function to generate probability distribution
    - Prediction extraction & confidence score
    """
    x = np.array(input_vector, dtype=np.float32)

    # Simulated deterministic weights and bias for reproducibility
    np.random.seed(42)
    weights = np.random.randn(len(x), len(CLASSES)).astype(np.float32)
    biases = np.array([0.1, -0.2, 0.05, 0.0], dtype=np.float32)

    # Linear transformation: logits = xW + b
    logits = np.dot(x, weights) + biases

    # Numerical stability shift for Softmax
    exp_logits = np.exp(logits - np.max(logits))
    probabilities = exp_logits / np.sum(exp_logits)

    predicted_idx = int(np.argmax(probabilities))
    confidence = float(probabilities[predicted_idx])

    return {
        "predicted_class": CLASSES[predicted_idx],
        "class_index": predicted_idx,
        "confidence": round(confidence, 4),
        "probabilities": {
            cls_name: round(float(prob), 4)
            for cls_name, prob in zip(CLASSES, probabilities)
        }
    }

@app.route("/", methods=["GET"])
def index():
    """Root endpoint for basic service check."""
    return jsonify({
        "status": "online",
        "service": "Flask Deep Learning Inference API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "predict": "/predict [POST]"
        }
    }), 200

@app.route("/health", methods=["GET"])
def health():
    """Readiness/Liveness probe for container orchestration."""
    return jsonify({
        "status": "healthy",
        "timestamp": time.time()
    }), 200

@app.route("/predict", methods=["POST"])
def predict():
    """
    Inference endpoint.
    Expects JSON payload:
    {
        "inputs": [0.5, 1.2, -0.4, 0.8, 2.1]
    }
    """
    start_time = time.time()

    if not request.is_json:
        return jsonify({
            "error": "Invalid Content-Type. Expected 'application/json'"
        }), 400

    payload = request.get_json(silent=True)
    if not payload or "inputs" not in payload:
        return jsonify({
            "error": "Missing 'inputs' field in request payload."
        }), 400

    inputs = payload.get("inputs")
    if not isinstance(inputs, list) or len(inputs) == 0:
        return jsonify({
            "error": "'inputs' must be a non-empty list of numerical values."
        }), 400

    try:
        # Validate that all inputs are numeric
        cleaned_inputs = [float(v) for v in inputs]
    except (ValueError, TypeError):
        return jsonify({
            "error": "All items in 'inputs' list must be valid numbers."
        }), 400

    try:
        inference_result = mock_deep_learning_inference(cleaned_inputs)
        latency_ms = round((time.time() - start_time) * 1000, 2)

        response = {
            "status": "success",
            "latency_ms": latency_ms,
            "prediction": inference_result
        }
        logger.info(f"Inference successful: Class={inference_result['predicted_class']} Latency={latency_ms}ms")
        return jsonify(response), 200

    except Exception as e:
        logger.error(f"Inference failed with error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Internal inference error occurred."
        }), 500

if __name__ == "__main__":
    # For local standalone debugging (Docker will use Gunicorn)
    app.run(host="0.0.0.0", port=5000, debug=False)
