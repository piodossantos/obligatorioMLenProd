from fastapi import FastAPI, HTTPException
from fastapi import File, UploadFile
from keras.preprocessing import image
from keras.models import load_model
import numpy as np
from PIL import Image
import uvicorn
from keras import backend as K
from typing import List


def recall_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())
    return recall

def precision_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    return precision

def f1_m(y_true, y_pred):
    precision = precision_m(y_true, y_pred)
    recall = recall_m(y_true, y_pred)
    return 2*((precision*recall)/(precision+recall+K.epsilon()))

def load_image(image_file):
  try:
      image = Image.open(image_file.file)
      image = np.expand_dims(image, axis=0)
      return image
  except Exception as e:
      raise HTTPException(status_code=400, detail=f"Error processing image: {e}")

print('STARTING APP')

app = FastAPI()

try:
    model = load_model('models/model1.h5', custom_objects={
      'recall_m': recall_m,
      'precision_m': precision_m,
      'f1_m': f1_m
    })
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

@app.get("/health")
async def health_check():
    return {"status": "OK"}


@app.post('/predict')
async def predict(image_file: UploadFile = File(...)):
    if not model:
        raise HTTPException(status_code=500, detail="Model could not be loaded")
    try:
        image = Image.open(image_file.file)
        image = np.expand_dims(image, axis=0)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing image: {e}")

    try:
        predictions = model.predict(image)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error making prediction: {e}")

    try:
        # Obten la clase con mayor score
        predicted_class = np.argmax(predictions[0])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interpreting prediction: {e}")

    return {"predicted_class": int(predicted_class)}

@app.post('/predict_batch')
async def predict_batch(images: List[UploadFile]):
    if not model:
        raise HTTPException(status_code=500, detail="Model could not be loaded")
    try:
        image_list = map(load_image, images)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing image: {e}")

    try:
        predictions = model.predict(image_list)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error making prediction: {e}")

    try:
        classes = []
        for prediction in predictions:
          classes.append(int(np.argmax(prediction)))
        return {"predicted_classes": classes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interpreting prediction: {e}")


if __name__ == "__main__":
    import uvicorn 
    uvicorn.run(app, host="0.0.0.0", port=80)