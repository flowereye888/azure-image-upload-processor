import io
import logging

import azure.functions as func
from PIL import Image, ImageOps


app = func.FunctionApp()


@app.function_name(name="ProcessUploadedImage")
@app.blob_trigger(
    arg_name="input_blob",
    path="original-images/{name}",
    connection="AzureWebJobsStorage",
    source="EventGrid",
)
@app.blob_output(
    arg_name="output_blob",
    path="processed-images/{name}",
    connection="AzureWebJobsStorage",
)
def process_uploaded_image(
    input_blob: func.InputStream,
    output_blob: func.Out[bytes],
) -> None:
    logging.info(
        "Processing image %s (%s bytes)",
        input_blob.name,
        input_blob.length,
    )

    with Image.open(io.BytesIO(input_blob.read())) as image:
        original_format = (image.format or "JPEG").upper()
        image = ImageOps.exif_transpose(image)
        image.thumbnail((800, 800))

        if original_format in {"JPG", "JPEG"}:
            original_format = "JPEG"
            if image.mode not in {"RGB", "L"}:
                image = image.convert("RGB")
        elif original_format != "PNG":
            original_format = "PNG"

        processed = io.BytesIO()
        image.save(processed, format=original_format, optimize=True)
        output_blob.set(processed.getvalue())

    logging.info("Processed image saved to processed-images")
