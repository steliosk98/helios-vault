#!/usr/bin/env python3
import argparse
import hashlib
import json
import os
import sys
import urllib.request


DEFAULT_MANIFEST = os.path.join(os.path.dirname(__file__), "..", "models_manifest.json")


def load_manifest(path):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def get_urls(entry):
    urls = []
    if entry.get("urls"):
        urls.extend(entry["urls"])
    if entry.get("url"):
        urls.append(entry["url"])
    repo = entry.get("repo")
    filename = entry.get("file")
    if not repo or not filename:
        return urls
    revision = entry.get("revision", "main")
    urls.append(f"https://huggingface.co/{repo}/resolve/{revision}/{filename}")
    return urls


def list_models(models):
    for model in models:
        optional = "optional" if model.get("optional") else "required"
        print(f"{model['id']} | tier {model['tier']} | {optional} | {model['name']}")


def select_models(models, tiers=None, model_ids=None, include_optional=False):
    selected = []
    for model in models:
        if tiers is not None and model["tier"] not in tiers:
            continue
        if model_ids and model["id"] not in model_ids:
            continue
        if model.get("optional") and not include_optional:
            continue
        selected.append(model)
    return selected


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        while True:
            chunk = handle.read(1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def download(url, dest_path):
    tmp_path = dest_path + ".part"
    with urllib.request.urlopen(url) as response, open(tmp_path, "wb") as handle:
        total = response.headers.get("Content-Length")
        total_bytes = int(total) if total else None
        downloaded = 0
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            handle.write(chunk)
            downloaded += len(chunk)
            if total_bytes:
                percent = (downloaded / total_bytes) * 100
                print(f"\r  {downloaded // (1024 * 1024)}MB / {total_bytes // (1024 * 1024)}MB ({percent:.1f}%)", end="")
        print("")
    os.replace(tmp_path, dest_path)


def main():
    parser = argparse.ArgumentParser(description="Download GGUF models for Helios Vault")
    parser.add_argument("--manifest", default=DEFAULT_MANIFEST, help="Path to models manifest JSON")
    parser.add_argument("--dest", default="models", help="Destination directory for model files")
    parser.add_argument("--list", action="store_true", help="List available models")
    parser.add_argument("--tier", action="append", type=int, help="Tier to download (repeatable)")
    parser.add_argument("--model", action="append", help="Model id to download (repeatable)")
    parser.add_argument("--include-optional", action="store_true", help="Include optional models")
    parser.add_argument("--force", action="store_true", help="Re-download even if file exists")

    args = parser.parse_args()

    manifest = load_manifest(args.manifest)
    models = manifest.get("models", [])

    if args.list:
        list_models(models)
        return 0

    tiers = set(args.tier or [])
    model_ids = set(args.model or [])
    selected = select_models(models, tiers if tiers else None, model_ids if model_ids else None, args.include_optional)

    if not selected:
        print("No models selected. Use --list to see options.")
        return 1

    os.makedirs(args.dest, exist_ok=True)

    for entry in selected:
        urls = get_urls(entry)
        if not urls:
            print(f"Skipping {entry['id']}: missing url/repo/file")
            continue
        filename = entry.get("file") or os.path.basename(urls[0])
        dest_path = os.path.join(args.dest, filename)
        if os.path.exists(dest_path) and not args.force:
            print(f"Skipping {entry['id']} (exists): {dest_path}")
            continue
        print(f"Downloading {entry['id']} -> {dest_path}")
        downloaded = False
        last_error = None
        for url in urls:
            try:
                download(url, dest_path)
                downloaded = True
                break
            except Exception as exc:
                last_error = exc
                print(f"  Failed: {url} ({exc})")

        if not downloaded:
            print(f"Download failed for {entry['id']}")
            if last_error:
                print(f"Last error: {last_error}")
            continue

        expected = entry.get("sha256")
        if expected:
            actual = sha256_file(dest_path)
            if actual.lower() != expected.lower():
                print(f"Checksum mismatch for {entry['id']}")
                print(f"Expected: {expected}")
                print(f"Actual:   {actual}")
                return 2
            print(f"Checksum OK for {entry['id']}")
        else:
            print(f"No checksum for {entry['id']} (add sha256 to manifest for verification).")

    return 0


if __name__ == "__main__":
    sys.exit(main())
