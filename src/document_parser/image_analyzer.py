"""
Sources:
- https://konfuzio.com/en/pdf-parsing-python/
- 

Worth mentioning
- https://dev.konfuzio.com/sdk/tutorials.html
    Does AI parsing in one run, however limits the cntrol over the software to its use cases
"""

from openai import OpenAI
from dotenv import load_dotenv
import base64
import mimetypes
import os

load_dotenv()


class IMGAnalyzer:
    def __init__(self, model="llava") -> None:
        if model == "llava":
            self._OPEN_AI_CLIENT = OpenAI(
                base_url="http://localhost:8000/v1", api_key="sk-1234"
            )
        elif model == "openai":
            input(
                "OPENAI SELECTED; THIS MEAN YOU'LL LOOSE MONEY. DO YOU AGREE? Press anything to agree."
            )
            self._OPEN_AI_CLIENT = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def extract_img_information(self, path: str):
        text = self._send_gpt_4_request(path)
        return text

    def _image_to_base64(self, image_path):
        # Guess the MIME type of the image
        mime_type, _ = mimetypes.guess_type(image_path)

        if not mime_type or not mime_type.startswith("image"):
            raise ValueError("The file type is not recognized as an image")

        # Read the image binary data
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")

        # Format the result with the appropriate prefix
        image_base64 = f"data:{mime_type};base64,{encoded_string}"

        return image_base64

    def _send_gpt_4_request(self, img_path: str):
        base64_string = self._image_to_base64(img_path)
        try:
            response = self._OPEN_AI_CLIENT.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Please extract all text from the image. "
                                + "If there are any Pictures with any labels, "
                                + "please write down where they were pointed at and "
                                + "add this to the respective text parts.",
                            },
                            {
                                "type": "image_url",
                                "image_url": {"url": base64_string, "detail": "high"},
                            },
                        ],
                    }
                ],
                max_tokens=300,
            )
        except Exception as e:
            print(e)
            print("Please check if server is up and healthy.")
        return response.choices[0].message.content


if __name__ == "__main__":
    parser = IMGParser()
    print(
        parser._send_gpt_4_request(
            "/Users/tobiasgerlach/Documents/Code/document_parser/src/document_parser/batch_images/batch_5_page_52.png"
        )
    )
