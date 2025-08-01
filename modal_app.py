from modal import App, Image, asgi_app, gpu

app = App(name="chatterbox-server")

# 🔧 Build image with dependencies and mount the local folder
chatterbox_image = (
    Image.debian_slim()
    .apt_install("ffmpeg", "libsndfile1")
    .pip_install(
        "fastapi", "uvicorn", "torch", "chatterbox-tts", "transformers",
        "diffusers", "safetensors", "librosa", "soundfile", "pydub",
        "praat-parselmouth", "s3tokenizer", "python-multipart"
    )
    .add_local_dir(".", remote_path="/root")
)

# 🚀 Declare function using app.function()
@app.function(image=chatterbox_image, timeout=3600, gpu="A10G")
@asgi_app()
def fastapi_app():
    from server import app as chatterbox_fastapi
    return chatterbox_fastapi
