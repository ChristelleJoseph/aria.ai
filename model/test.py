import os

predict_dir = os.path.dirname(os.path.abspath(__file__))
notes_path = os.path.join(predict_dir, 'data', 'notes')
weights_path = os.path.join(predict_dir, 'weights', 'weights-improvement-01-4.0499.keras')


# Check if the weights file exists
if os.path.exists(weights_path):
    print("Weights file exists:", weights_path)
    # If the file exists, proceed to load your model weights
else:
    print("Weights file does not exist:", weights_path)
