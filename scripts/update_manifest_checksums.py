#!/usr/bin/env python3
import argparse
import hashlib
import json
import os
import sys


DEFAULT_MANIFEST = os.path.join(os.path.dirname(__file__), "..", "models_manifest.json")


def load_manifest(path):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def save_manifest(path, data):
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)
        handle.write("\n")


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        while True:
            chunk = handle.read(1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def main():
    parser = argparse.ArgumentParser(description="Update SHA256 checksums in models manifest")
    parser.add_argument("--manifest", default=DEFAULT_MANIFEST, help="Path to models manifest JSON")
    parser.add_argument("--models-dir", default="models", help="Directory containing GGUF files")
    parser.add_argument("--model", action="append", help="Model id to update (repeatable)")
    parser.add_argument("--all", action="store_true", help="Update all models found locally")
    args = parser.parse_args()

    manifest = load_manifest(args.manifest)
    models = manifest.get("models", [])
    if not models:
        print("No models found in manifest.")
        return 1

    target_ids = set(args.model or [])
    updated = 0
    for entry in models:
        if not args.all and target_ids and entry.get("id") not in target_ids:
            continue
        filename = entry.get("file")
        if not filename:
            continue
        path = os.path.join(args.models_dir, filename)
        if not os.path.exists(path):
            continue
        entry["sha256"] = sha256_file(path)
        updated += 1
        print(f"Updated {entry.get('id')} -> {entry['sha256']}")

    if updated == 0:
        print("No checksums updated. Ensure models are downloaded and IDs match.")
        return 1

    save_manifest(args.manifest, manifest)
    return 0


if __name__ == "__main__":
    sys.exit(main())
