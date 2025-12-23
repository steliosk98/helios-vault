import os
import subprocess
import sys

import pytest


def _should_run():
    backend = os.getenv("MODEL_BACKEND", "").lower()
    model_path = os.getenv("MODEL_PATH")
    return backend == "llama" and bool(model_path)


pytestmark = pytest.mark.skipif(not _should_run(), reason="Requires MODEL_BACKEND=llama and MODEL_PATH")


def test_streaming_with_real_model():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    script = os.path.join(root, "scripts", "stream_smoke_test.py")
    env = os.environ.copy()
    env.setdefault("MODEL_THREADS", "1")
    env.setdefault("MODEL_N_CTX", "1024")

    result = subprocess.run([sys.executable, script], env=env, capture_output=True, text=True)
    if result.returncode != 0:
        print("stdout:", result.stdout)
        print("stderr:", result.stderr)
    assert result.returncode == 0
