# NuKropAI - FastAPI YOLOv8 Server

This is a lightweight FastAPI server designed to run YOLOv8 object detection. It is optimized for free hosting platforms like **Hugging Face Spaces** or **Render**.

## Deployment to Hugging Face Spaces (FREE)

1. Create a new Space on [Hugging Face](https://huggingface.co/new-space).
2. Select **Docker** as the SDK.
3. Choose the **Blank** template or **Dockerfile**.
4. Upload the contents of this `ai_server` folder (main.py, requirements.txt, Dockerfile).
5. Wait for the build to finish.
6. Your API will be available at `https://<your-username>-<space-name>.hf.space`.

## API Endpoints

### 1. Root
- **GET** `/`
- Status check.

### 2. Predict
- **POST** `/predict`
- **Body**: Form-data with key `file` (the image).
- **Returns**: JSON list of detections (boxes, confidence, class names).

## Example Mobile Integration (Dart)

```dart
var request = http.MultipartRequest('POST', Uri.parse('https://your-space.hf.space/predict'));
request.files.add(await http.MultipartFile.fromPath('file', imagePath));
var response = await request.send();
```
