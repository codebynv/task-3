"""
Face Detection & Encoding Module
=================================
Detects faces in an input image, encodes them, and saves the cropped face.
Uses DeepFace (RetinaFace backend) -- no C++ compiler required on Windows.

Usage:
    python face_module.py <image_path>
"""

import sys
import os
import json
import hashlib

# Fix Windows terminal encoding (cp1252 cannot handle emoji from DeepFace internals)
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# Suppress TensorFlow logging before any TF imports happen inside DeepFace
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import numpy as np
import cv2
from PIL import Image, ImageDraw


def process_face(image_path: str, output_dir: str = "output") -> dict:
    """
    Detect and encode a face from an input image.

    This is the primary interface for Phase 1. It:
      1. Loads the image
      2. Detects faces using DeepFace (RetinaFace backend)
      3. Generates a 128-dimensional FaceNet embedding
      4. Saves cropped face and annotated image
      5. Computes a SHA-256 hash of the embedding

    Args:
        image_path: Path to the input image file.
        output_dir: Directory to save output files.

    Returns:
        dict with keys:
            face_found (bool), face_location (dict), face_encoding (list),
            encoding_dimensions (int), model_used (str), detector_backend (str),
            cropped_face_path (str), annotated_image_path (str),
            face_hash (str), original_image_path (str), error (str or None)
    """
    print("=" * 60)
    print("  Phase 1: Face Detection & Encoding")
    print("=" * 60)

    # --- Validate input ---
    if not os.path.exists(image_path):
        print(f"[ERROR] Image not found: {image_path}")
        return {"face_found": False, "error": "Image file not found"}

    # --- Load image ---
    print(f"\n[1/5] Loading image: {image_path}")
    image_bgr = cv2.imread(image_path)
    if image_bgr is None:
        print(f"[ERROR] Could not read image (corrupt or unsupported format): {image_path}")
        return {"face_found": False, "error": "Could not read image"}

    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    h, w = image_bgr.shape[:2]
    print(f"  OK - Image loaded ({w} x {h} px)")

    # --- Detect + Encode using DeepFace ---
    print(f"\n[2/5] Detecting and encoding face (DeepFace + RetinaFace)...")

    model_name = "Facenet"
    detector_backend = "retinaface"

    try:
        from deepface import DeepFace

        embedding_results = DeepFace.represent(
            img_path=image_path,
            model_name=model_name,
            detector_backend=detector_backend,
            enforce_detection=True,
        )

        if not embedding_results:
            print("[ERROR] No faces detected in the image.")
            return {"face_found": False, "error": "No faces detected"}

        # Use the first (largest/most confident) face
        result_data = embedding_results[0]
        encoding = result_data["embedding"]
        facial_area = result_data["facial_area"]
        x = facial_area["x"]
        y = facial_area["y"]
        fw = facial_area["w"]
        fh = facial_area["h"]

        print(f"  OK - Face detected")
        print(f"       Bounding box: x={x}, y={y}, w={fw}, h={fh}")
        print(f"  OK - Face encoded ({len(encoding)}-dimensional {model_name} embedding)")

    except Exception as e:
        error_msg = str(e).encode('ascii', 'replace').decode('ascii')
        print(f"[ERROR] Face detection/encoding failed: {error_msg}")
        return {"face_found": False, "error": error_msg}

    # --- Crop and save the face ---
    print(f"\n[3/5] Saving cropped face...")
    os.makedirs(output_dir, exist_ok=True)
    pil_image = Image.fromarray(image_rgb)
    padding = int(max(fw, fh) * 0.3)
    crop_left = max(0, x - padding)
    crop_top = max(0, y - padding)
    crop_right = min(w, x + fw + padding)
    crop_bottom = min(h, y + fh + padding)

    face_crop = pil_image.crop((crop_left, crop_top, crop_right, crop_bottom))
    cropped_path = os.path.join(output_dir, "face_crop.jpg")
    face_crop.save(cropped_path, "JPEG", quality=95)
    print(f"  OK - Cropped face saved: {cropped_path}")

    # --- Save annotated image ---
    print(f"\n[4/5] Saving annotated image...")
    annotated = pil_image.copy()
    draw = ImageDraw.Draw(annotated)
    draw.rectangle([x, y, x + fw, y + fh], outline="lime", width=3)
    annotated_path = os.path.join(output_dir, "annotated_image.jpg")
    annotated.save(annotated_path, "JPEG", quality=95)
    print(f"  OK - Annotated image saved: {annotated_path}")

    # --- Generate hash of the embedding ---
    print(f"\n[5/5] Computing face hash...")
    encoding_str = json.dumps(encoding[:128], sort_keys=True)
    face_hash = hashlib.sha256(encoding_str.encode()).hexdigest()
    print(f"  OK - SHA-256: {face_hash[:32]}...")

    # --- Summary ---
    print("\n" + "-" * 60)
    print("  SUMMARY")
    print("-" * 60)
    print(f"  Face Found       : Yes")
    print(f"  Bounding Box     : x={x}, y={y}, w={fw}, h={fh}")
    print(f"  Model            : {model_name}")
    print(f"  Detector         : {detector_backend}")
    print(f"  Embedding Dims   : {len(encoding)}")
    preview = ", ".join([f"{v:.4f}" for v in encoding[:5]])
    print(f"  Embedding Preview: [{preview}, ...]")
    print(f"  Cropped Face     : {os.path.abspath(cropped_path)}")
    print(f"  Annotated Image  : {os.path.abspath(annotated_path)}")
    print(f"  Face Hash        : {face_hash[:32]}...")
    print("-" * 60)

    return {
        "face_found": True,
        "face_location": {"x": int(x), "y": int(y), "w": int(fw), "h": int(fh)},
        "face_encoding": encoding,
        "encoding_dimensions": len(encoding),
        "model_used": model_name,
        "detector_backend": detector_backend,
        "cropped_face_path": os.path.abspath(cropped_path),
        "annotated_image_path": os.path.abspath(annotated_path),
        "face_hash": face_hash,
        "original_image_path": os.path.abspath(image_path),
        "error": None,
    }


# Keep backward-compatible alias
detect_and_encode = process_face


def main():
    """CLI entry point for standalone testing."""
    if len(sys.argv) < 2:
        print("Usage: python face_module.py <image_path>")
        print("Example: python face_module.py test_images/einstein.jpg")
        sys.exit(1)

    image_path = sys.argv[1]
    result = process_face(image_path)

    if result["face_found"]:
        print("\n[SUCCESS] Phase 1 Complete - Face detected and encoded successfully!")
    else:
        print(f"\n[FAILED] Phase 1 Failed - {result.get('error', 'Unknown error')}")
        sys.exit(1)

    return result


if __name__ == "__main__":
    main()
