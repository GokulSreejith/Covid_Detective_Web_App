# Libraries
from tensorflow.keras.applications.inception_v3 import preprocess_input as incep_preprocess
from tensorflow.keras.applications.resnet_v2 import preprocess_input as res_preprocess
from tensorflow.keras.applications.xception import preprocess_input as xcep_preprocess
import cv2 as cv 
import numpy as np
from matplotlib import pyplot as plt
from tensorflow.keras.models import load_model

# Model paths
RESNET_H5_MODEL_PATH = 'detection/saved_models/h5_models/resnet_model.h5'
XCEPTION_H5_MODEL_PATH = 'detection/saved_models/h5_models/xception_model.h5'
INCEPTION_H5_MODEL_PATH = 'detection/saved_models/h5_models/inception_model.h5'

def detect_covid(image_path):
    try:
        # Read and preprocess the image
        path = image_path
        image = cv.imread(path)
        img = cv.resize(image, (224, 224))
        img = np.reshape(img, [1, 224, 224, 3])
        res_image = res_preprocess(img)
        xcep_image = xcep_preprocess(img)
        incep_image = incep_preprocess(img)

        # Load the pre-trained models
        resnet = load_model(RESNET_H5_MODEL_PATH, compile=False)
        xception = load_model(XCEPTION_H5_MODEL_PATH, compile=False)
        inception = load_model(INCEPTION_H5_MODEL_PATH, compile=False)

        # Perform predictions using the models
        resnet_pred = resnet.predict(res_image)
        xception_pred = xception.predict(xcep_image)
        inception_pred = inception.predict(incep_image)

        classes = []

        # Get the predicted classes
        classes.append(int(np.argmax(resnet_pred, axis=1)))
        classes.append(int(np.argmax(xception_pred, axis=1)))
        classes.append(int(np.argmax(inception_pred, axis=1)))

        labels = {0: 'negative', 1: 'positive'}

        # Print the predicted classes and the majority label
        print(classes)
        print(labels[max(set(classes), key=classes.count)])

        # Display the image with the predicted label
        plt.title(labels[max(set(classes), key=classes.count)])
        plt.imshow(image)
        plt.show()

    except Exception as e:
        # Handle the error
        error_message = str(e)
        raise RuntimeError(f"Error in COVID-19 detection: {error_message}")
