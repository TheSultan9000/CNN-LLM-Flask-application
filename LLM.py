# Import packages
import tensorflow as tf
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
import torch

def image_to_text_class(input):
    """Generates a textual caption for an input image using a pre-trained image captioning model
    Expects: input (str or bytes): The input image in string or bytes format
    Returns: str: The generated textual caption for the input image
    """
    # Load the pre-trained image captioning model and its components
    model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
    feature_extractor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
    tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

    # Check if a CUDA-enabled GPU is available, otherwise use CPU
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)  # Move the model to the selected device (GPU or CPU)

    # Set max length and beams
    max_length = 16
    num_beams = 4
    gen_kwargs = {"max_length": max_length, "num_beams": num_beams}

    img_tensor = tf.image.decode_image(input)
    images = [img_tensor]

    # Extract the pixel values of the selected image
    pixel_values = feature_extractor(images=images, return_tensors="pt").pixel_values
    pixel_values = pixel_values.to(device)

    # Generate captions for the image using the model
    output_ids = model.generate(pixel_values, **gen_kwargs)

    # Decode the output IDs using the tokenizer
    preds = tokenizer.batch_decode(output_ids, skip_special_tokens=True)
    preds = [pred.strip() for pred in preds]

    outputs = "".join(preds).capitalize()
    
    return outputs
