import shutil
import docker, json, io, tarfile, uuid, tempfile
from pathlib import Path
import boto3
import redis
from backend.database.redis import r
import os
from dotenv import load_dotenv
load_dotenv()

BUCKET_NAME = os.getenv("BUCKET_NAME", "text-2-manim")

def sandbox_render(code: str, file_name: str, class_name: str, job_id: str) -> str:
    """
    Render `class_name` from `code` inside an isolated Manim container,
    upload the resulting .mp4 to S3, and return the public URL.
    """
    tmp_dir = Path(tempfile.mkdtemp(prefix="manim_"))
    out_dir = tmp_dir / "out"
    out_dir.mkdir()

    tar_stream = io.BytesIO()
    with tarfile.open(fileobj=tar_stream, mode="w") as t:
        data = code.encode()
        ti = tarfile.TarInfo(name=file_name)
        ti.size = len(data)
        t.addfile(ti, io.BytesIO(data))
    tar_stream.seek(0)

    client = docker.from_env()

    container = client.containers.create(
        image="manim-renderer:latest",
        command=[
            "--disable_caching",
            "-ql",
            "--media_dir=/sandbox/out",
            file_name,
            class_name,
        ],
        user="1000:1000",
        network_mode="none",
        cpuset_cpus="0",
        mem_limit="1g",
        pids_limit=256,
        security_opt=["no-new-privileges"],
        cap_drop=["ALL"],
        volumes={str(out_dir): {"bind": "/sandbox/out", "mode": "rw"}},
        detach=True,
    )

    container.put_archive("/sandbox", tar_stream)
    container.start()

    try:
        exit_status = container.wait(timeout=500)
    except docker.errors.APIError:
        container.kill()
        raise RuntimeError("Render timed out")

    logs = container.logs().decode()
    container.remove(force=True)

    if exit_status["StatusCode"] != 0:
        raise RuntimeError(f"Render failed:\n{logs}")

    mp4_files = list(out_dir.rglob("*.mp4"))
    if not mp4_files:
        r.set(job_id, "FAILED")
        r.set(f"{job_id}:logs", logs)
        raise RuntimeError("Render succeeded but no .mp4 found.\n" + logs)

    mp4 = mp4_files[0]

    s3 = boto3.client("s3")
    bucket = BUCKET_NAME
    key = f"{uuid.uuid4()}.mp4"
    s3.upload_file(str(mp4), bucket, key, ExtraArgs={"ACL": "public-read"})
    url = f"https://{bucket}.s3.amazonaws.com/{key}"
    r.set(job_id, "COMPLETED")
    r.set(f"{job_id}:url", url)
    shutil.rmtree(tmp_dir, ignore_errors=True)
    return url
