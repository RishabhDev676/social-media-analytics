import os
import joblib
from src.core.train import train_model

class ModelManager:
    """
    Manages the lifecycle of the machine learning model and vectorizer.
    Responsible for checking their existence, triggering training if missing,
    and loading them into memory.
    """
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.models_dir = os.path.join(self.base_dir, "..", "..", "models")
        self.model_path = os.path.join(self.models_dir, "sentiment_model.pkl")
        self.vectorizer_path = os.path.join(self.models_dir, "vectorizer.pkl")
        
        # Cache variables
        self._model = None
        self._vectorizer = None

    def check_models_exist(self):
        """Returns True if both the model and vectorizer files exist."""
        return os.path.exists(self.model_path) and os.path.exists(self.vectorizer_path)

    def train_if_missing(self):
        """Checks if models exist, and automatically triggers training if they do not."""
        if not self.check_models_exist():
            print("Model Manager: Model or vectorizer missing. Initiating automatic training...")
            # We assume train_model defaults to the correct data and model directories
            train_model()
            
            # Double check if training successfully created the files
            if not self.check_models_exist():
                raise FileNotFoundError("Model Manager: Training failed to produce model files.")
        else:
            print("Model Manager: Pre-trained model and vectorizer found.")

    def get_models(self):
        """
        Ensures models are available, loads them into memory (caches them), and returns them.
        
        Returns:
            tuple: (model, vectorizer)
        """
        if self._model is not None and self._vectorizer is not None:
            return self._model, self._vectorizer

        # Ensure models exist (trains if missing)
        self.train_if_missing()

        print(f"Model Manager: Loading model from {self.model_path}...")
        self._model = joblib.load(self.model_path)
        
        print(f"Model Manager: Loading vectorizer from {self.vectorizer_path}...")
        self._vectorizer = joblib.load(self.vectorizer_path)

        return self._model, self._vectorizer


if __name__ == "__main__":
    # Quick Test Block
    print("Testing Model Manager...")
    manager = ModelManager()
    
    # We will just call get_models to see if it finds them and loads them
    model, vectorizer = manager.get_models()
    if model is not None and vectorizer is not None:
        print("Test Passed: Model and vectorizer successfully loaded via ModelManager.")
