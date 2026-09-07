"""
Phase 2: Genuine Reverse Image / Web Search Module
===================================================
Uses SerpApi (Google Lens engine) to perform a genuine runtime reverse-image search.
Supports both local image files (uploaded via SerpApi Image API) and image URLs.
No hardcoded URLs, mock data, or fake results.

Setup:
  1. Sign up at https://serpapi.com (free: 250 searches/month)
  2. Create a .env file with: SERPAPI_KEY=your_key_here
  3. pip install google-search-results python-dotenv

Exposes: search_reverse_image(image_path_or_url)
"""

import os
import sys
import json
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv

# Reconfigure stdout/stderr for UTF-8 on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

SOCIAL_MEDIA_DOMAINS = [
    "twitter.com", "x.com",
    "instagram.com",
    "facebook.com", "fb.com",
    "reddit.com",
    "linkedin.com",
    "pinterest.com",
    "tiktok.com",
    "tumblr.com",
    "flickr.com",
    "youtube.com",
]


def _upload_image_to_serpapi(image_path: str, api_key: str) -> str:
    """
    Upload a local image to SerpApi's Image API and return a temporary image_id.
    The image_id expires after ~10 minutes.
    Max file size: 500 KB.
    """
    file_size = os.path.getsize(image_path)
    if file_size > 500 * 1024:
        # Resize the image to fit under 500KB
        print(f"  [WARN] Image is {file_size // 1024} KB (max 500 KB). Attempting to compress...")
        from PIL import Image
        import io
        img = Image.open(image_path)
        # Reduce quality progressively
        for quality in [80, 60, 40, 20]:
            buf = io.BytesIO()
            img.save(buf, format="JPEG", quality=quality)
            if buf.tell() <= 500 * 1024:
                print(f"  [OK] Compressed to {buf.tell() // 1024} KB (quality={quality})")
                buf.seek(0)
                resp = requests.post(
                    "https://serpapi.com/image",
                    params={"api_key": api_key},
                    files={"image": ("image.jpg", buf, "image/jpeg")},
                    timeout=30,
                )
                resp.raise_for_status()
                data = resp.json()
                if "image_id" not in data:
                    raise ValueError(f"SerpApi upload failed: {data}")
                return data["image_id"]
        raise ValueError("Could not compress image below 500 KB")
    else:
        with open(image_path, "rb") as f:
            resp = requests.post(
                "https://serpapi.com/image",
                params={"api_key": api_key},
                files={"image": (os.path.basename(image_path), f, "image/jpeg")},
                timeout=30,
            )
        resp.raise_for_status()
        data = resp.json()
        if "image_id" not in data:
            raise ValueError(f"SerpApi upload failed: {data}")
        return data["image_id"]


def _classify_result(url: str) -> dict:
    """Classify a URL as social media or generic web."""
    is_social = any(domain in url.lower() for domain in SOCIAL_MEDIA_DOMAINS)
    parsed = urlparse(url)
    return {
        "is_social_media": is_social,
        "domain": parsed.netloc,
    }


def search_reverse_image(image_input: str) -> dict:
    """
    Perform a genuine reverse-image search using SerpApi Google Lens.

    Args:
        image_input: Path to a local image file, or a publicly accessible image URL.

    Returns:
        dict with keys: success, query_image, search_method, best_match, results,
        social_media_found, error (if failed).
    """
    load_dotenv()
    api_key = os.getenv("SERPAPI_API_KEY") or os.getenv("SERPAPI_KEY")

    print("=" * 60)
    print("  Phase 2: Genuine Reverse Image Search")
    print("=" * 60)

    # ── Validate API key ──────────────────────────────────────
    if not api_key:
        msg = (
            "SERPAPI_API_KEY not found in .env file.\n"
            "  Setup: sign up at https://serpapi.com (free: 250 searches/month)\n"
            "  Then create a .env file with: SERPAPI_API_KEY=your_key_here"
        )
        print(f"\n[ERROR] {msg}")
        return {"success": False, "error": msg, "search_method": "SerpApi Google Lens"}

    print(f"\n[1/4] Initializing search provider: SerpApi (Google Lens)...")

    try:
        from serpapi import GoogleSearch
    except ImportError:
        return {
            "success": False,
            "error": "google-search-results package not installed. Run: pip install google-search-results",
            "search_method": "SerpApi Google Lens",
        }

    # ── Determine input type (local file vs URL) ──────────────
    is_url = image_input.startswith("http://") or image_input.startswith("https://")
    is_local = not is_url and os.path.exists(image_input)

    if not is_url and not is_local:
        return {
            "success": False,
            "error": f"Image not found: {image_input}",
            "search_method": "SerpApi Google Lens",
        }

    params = {
        "engine": "google_lens",
        "api_key": api_key,
        "hl": "en",
    }

    # ── Handle local file: upload to SerpApi first ────────────
    if is_local:
        print(f"\n[2/4] Uploading local image to SerpApi: {image_input}")
        try:
            image_id = _upload_image_to_serpapi(image_input, api_key)
            params["image_id"] = image_id
            print(f"  OK - Received temporary image_id: {image_id[:40]}...")
        except Exception as e:
            error_msg = f"Failed to upload image to SerpApi: {e}"
            print(f"[ERROR] {error_msg}")
            return {"success": False, "error": error_msg, "search_method": "SerpApi Google Lens"}
    else:
        print(f"\n[2/4] Using image URL: {image_input[:80]}...")
        params["url"] = image_input

    # ── Perform the search ────────────────────────────────────
    print(f"\n[3/4] Performing runtime Google Lens search... (This may take a moment)")

    try:
        search = GoogleSearch(params)
        result = search.get_dict()

        if "error" in result:
            print(f"[ERROR] SerpApi returned error: {result['error']}")
            return {"success": False, "error": result["error"], "search_method": "SerpApi Google Lens"}

        visual_matches = result.get("visual_matches", [])

        if not visual_matches:
            print("[WARN] Search completed but no visual matches found.")
            return {
                "success": False,
                "error": "No visual matches returned from search.",
                "search_method": "SerpApi Google Lens",
            }

        print(f"  OK - Discovered {len(visual_matches)} candidate matches")

    except Exception as e:
        error_msg = f"Search failed during execution: {e}"
        print(f"[ERROR] {error_msg}")
        return {"success": False, "error": error_msg, "search_method": "SerpApi Google Lens"}

    # ── Evaluate & classify results ───────────────────────────
    print(f"\n[4/4] Evaluating candidates and classifying results...")

    formatted_results = []
    social_media_matches = []
    generic_matches = []

    for match in visual_matches:
        url = match.get("link", "")
        title = match.get("title", "")
        source = match.get("source", "")
        thumbnail = match.get("thumbnail", "")
        position = match.get("position", None)

        if not url:
            continue

        classification = _classify_result(url)

        match_info = {
            "title": title,
            "url": url,
            "source": source,
            "domain": classification["domain"],
            "thumbnail": thumbnail,
            "is_social_media": classification["is_social_media"],
            "position": position,
        }

        if classification["is_social_media"]:
            social_media_matches.append(match_info)
        else:
            generic_matches.append(match_info)

        formatted_results.append(match_info)

    if not formatted_results:
        return {
            "success": False,
            "error": "Could not extract valid URLs from search results.",
            "search_method": "SerpApi Google Lens",
        }

    # Best match logic: Prioritize social media matches
    best_match = None
    if social_media_matches:
        best_match = social_media_matches[0]
        print(f"  OK - Identified matching SOCIAL MEDIA post!")
    else:
        best_match = generic_matches[0] if generic_matches else formatted_results[0]
        print(f"  OK - Identified generic matching web result (No social media post found).")

    # ── Print summary ─────────────────────────────────────────
    print("\n" + "-" * 60)
    print("  SEARCH SUMMARY")
    print("-" * 60)
    print(f"  Method           : SerpApi Google Lens (runtime)")
    print(f"  Total Candidates : {len(formatted_results)}")
    print(f"  Social Matches   : {len(social_media_matches)}")
    print(f"  Generic Matches  : {len(generic_matches)}")
    print(f"  Best Match Title : {best_match['title']}")
    print(f"  Best Match Source: {best_match['source']}")
    print(f"  Best Match URL   : {best_match['url']}")
    print(f"  Social Media?    : {'YES' if best_match['is_social_media'] else 'NO'}")
    print("-" * 60)

    # Print all results briefly
    if len(formatted_results) > 1:
        print("\n  ALL RESULTS:")
        for i, r in enumerate(formatted_results[:10]):
            tag = " [SOCIAL]" if r["is_social_media"] else ""
            print(f"    [{i+1}] {r['title'][:60]}")
            print(f"        {r['url'][:80]}{tag}")

    return {
        "success": True,
        "query_image": os.path.abspath(image_input) if is_local else image_input,
        "search_method": "SerpApi Google Lens",
        "best_match": best_match,
        "results": formatted_results[:10],
        "social_media_found": len(social_media_matches) > 0,
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python reverse_search.py <image_path_or_url>")
        print("\nExamples:")
        print("  python reverse_search.py test_images/einstein.jpg")
        print("  python reverse_search.py https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Einstein_1921_by_F_Schmutzer_-_restoration.jpg/800px-Einstein_1921_by_F_Schmutzer_-_restoration.jpg")
        sys.exit(1)

    result = search_reverse_image(sys.argv[1])

    print("\n" + "=" * 60)
    if result["success"]:
        print("  PHASE 2 RESULT: SUCCESS")
    else:
        print("  PHASE 2 RESULT: FAILED")
        print(f"  Error: {result['error']}")
    print("=" * 60)

    if not result["success"]:
        sys.exit(1)
