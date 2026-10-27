"""Default thresholds from HANDOFF.md §3–§4 (overridable via CLI)."""

DEFAULT_FACE_SIM_THRESHOLD = 0.45
DEFAULT_BLUR_LAPLACIAN_MIN = 60.0
DEFAULT_BLUR_SCORE_MIN = 0.2  # InsightFace quality; conservative when missing
DEFAULT_EAR_MIN = 0.21
DEFAULT_YAW_MAX = 30.0
DEFAULT_PITCH_MAX = 25.0
DEFAULT_EXPOSURE_MEAN_MIN = 50.0
DEFAULT_EXPOSURE_MEAN_MAX = 220.0
DEFAULT_HIGHLIGHT_RATIO_MAX = 0.01
DEFAULT_SHADOW_RATIO_MAX = 0.03

DEFAULT_SESSION_WINDOW_MINUTES = 5
DEFAULT_SESSION_RADIUS_M = 100.0
DEFAULT_PHASH_HAMMING_MAX = 8

DEFAULT_NEAR_TOP_SCORE_DELTA = 0.05

SCORE_WEIGHTS = {
    "blur": 0.40,
    "exposure": 0.25,
    "eye_open": 0.20,
    "face_area": 0.15,
}

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".heic", ".png", ".webp", ".tif", ".tiff"}

EXCLUDE_DIR_NAMES = {".photoslibrary", "photos library.photoslibrary"}
EXCLUDE_FILE_NAMES = {".ds_store"}
EXCLUDE_SUFFIXES = {".aae"}
