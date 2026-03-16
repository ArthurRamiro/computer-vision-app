import os
import joblib
import mediapipe as mp

from pathlib import Path

# Caminho base do projeto (um nível acima da pasta core)
BASE_DIR = Path(__file__).resolve().parent.parent

# Caminhos padrão
MP_MODEL_PATH = (BASE_DIR / "models" / "gesture_recognizer.task").as_posix()
CUSTOM_MODEL_PATH = (BASE_DIR / "models" / "gesture_model.joblib").as_posix()
ENCODER_PATH = (BASE_DIR / "models" / "label_encoder.joblib").as_posix()

def load_custom_models():
    """Carrega o classificador customizado e o encoder de labels."""
    print(f"Debug: Carregando modelos de {CUSTOM_MODEL_PATH}")
    if not all(os.path.exists(p) for p in [CUSTOM_MODEL_PATH, ENCODER_PATH]):
        raise FileNotFoundError(f"Modelos customizados não encontrados em: {CUSTOM_MODEL_PATH} ou {ENCODER_PATH}")
    
    clf = joblib.load(CUSTOM_MODEL_PATH)
    label_encoder = joblib.load(ENCODER_PATH)
    return clf, label_encoder

def get_mediapipe_options():
    """Retorna as configurações do MediaPipe Gesture Recognizer."""
    if not os.path.exists(MP_MODEL_PATH):
        raise FileNotFoundError(f"Modelo MediaPipe não encontrado em: {MP_MODEL_PATH}")
    
    # Lendo o modelo como buffer para evitar problemas com caracteres especiais no caminho (Windows)
    with open(MP_MODEL_PATH, "rb") as f:
        model_buffer = f.read()

    BaseOptions = mp.tasks.BaseOptions
    GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
    VisionRunningMode = mp.tasks.vision.RunningMode

    options = GestureRecognizerOptions(
        base_options=BaseOptions(model_asset_buffer=model_buffer),
        running_mode=VisionRunningMode.VIDEO,
        num_hands=2,
        min_hand_detection_confidence=0.5,
        min_hand_presence_confidence=0.5,
        min_tracking_confidence=0.5,
    )
    return options
