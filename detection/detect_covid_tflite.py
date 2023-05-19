# Libraries
import tensorflow as tf
import numpy as np
from PIL import Image

# Model paths
RESNET_TFLITE_MODEL_PATH = 'detection/saved_models/tflite_models/resnet.tflite'
XCEPTION_TFLITE_MODEL_PATH = 'detection/saved_models/tflite_models/xception.tflite'
INCEPTION_TFLITE_MODEL_PATH = 'detection/saved_models/tflite_models/inception.tflite'


def detect_covid(image_path):
    try:
        # Load the TFLite model and perform COVID-19 detection
        interpreter = tf.lite.Interpreter(model_path=RESNET_TFLITE_MODEL_PATH)
        interpreter.allocate_tensors()

        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()

        print(input_details,output_details)

        # Preprocess the image
        image = Image.open(image_path).resize((224, 224))
        image = image.convert("RGB")  # Ensure image has 3 channels (RGB)
        image = np.array(image) / 255.0
        image = np.expand_dims(image, axis=0).astype(input_details[0]['dtype'])

        # Check if input shape matches expected shape
        expected_shape = input_details[0]['shape']
        if image.shape[1:] != expected_shape[1:]:
            raise RuntimeError("Dimension mismatch error: Expected shape {} but got {}".format(expected_shape[1:], image.shape[1:]))

        interpreter.set_tensor(input_details[0]['index'], image)
        interpreter.invoke()

        # Get the detection results
        output_data = interpreter.get_tensor(output_details[0]['index'])

        return output_data[0]

    except Exception as e:
        # Handle the error
        error_message = str(e)
        raise RuntimeError(f"Error in COVID-19 detection: {error_message}")
