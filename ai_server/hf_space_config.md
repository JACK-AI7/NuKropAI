# 🚀 Hugging Face Space Configuration

To ensure a successful deployment of the NuKropAI Enterprise AI Server, please configure the following settings in your Hugging Face Space.

## 1. Secrets (Variables)
Go to **Settings > Variables and Secrets** and add:

| Name | Value | Description |
| :--- | :--- | :--- |
| `HF_TOKEN` | `your_token` | Required for downloading gated or large models. |
| `AI_API_KEY` | `your_secret` | Required for mobile app authentication. |
| `REDIS_URL` | `redis_url` | (Optional) URL for Redis caching layer. |
| `CELERY_BROKER_URL` | `redis_url` | (Optional) URL for background task queue. |

## 2. Space Runtime
- **Hardware**: For production, use **T4 Small** or **A10G Small** GPU for optimal inference.
- **Docker**: The Space must be set to **Docker** SDK.
- **Port**: The internal port is **7860** (exposed by default).

## 3. Persistent Storage
If you need to persist datasets or logs, enable **Persistent Storage** in settings and mount it to `/app/dataset`.

## 4. Building
The build process automatically runs `download_weights.py`. Ensure your `HF_TOKEN` has read access to the required repositories.
