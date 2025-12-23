import json
import os


def test_models_manifest_structure():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    manifest_path = os.path.join(root, "models_manifest.json")
    assert os.path.exists(manifest_path)

    with open(manifest_path, "r", encoding="utf-8") as handle:
        manifest = json.load(handle)

    assert isinstance(manifest.get("models"), list)
    assert manifest.get("version")
    assert manifest.get("source")

    required_fields = {"id", "tier", "name", "optional"}
    for entry in manifest["models"]:
        assert required_fields.issubset(entry.keys())
        has_repo = bool(entry.get("repo") and entry.get("file"))
        has_url = bool(entry.get("url"))
        assert has_repo or has_url
