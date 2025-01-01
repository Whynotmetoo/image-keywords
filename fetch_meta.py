import os
from openai import OpenAI
from PIL import Image
import base64
from dotenv import load_dotenv
from pydantic import BaseModel
import json

class ChatResponse(BaseModel):
    title: str
    keywords: str

load_dotenv()

client = OpenAI()

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')
    
def generate_image_metadata(image_path):
        try:
            base64_image = encode_image(image_path)
            prompt = f"""
            You are an expert in creating SEO-friendly image titles and keywords for stock photography.
            Generate a compelling, searchable title, try to make it longer, but no more then 20 words.
            Generate 50 relevant, high-traffic keywords, two of them are Long Tail Keywords.
            Please give your response in json format.
            """
            response = client.beta.chat.completions.parse(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system", 
                        "content":prompt,
                    },
                    {
                        "role": "user", 
                        "content": [
                             {
                                "type": "image_url",
                                "image_url": {
                                        "url":  f"data:image/jpeg;base64,{base64_image}"
                                    },
                            },
                        ]
                    }
                ],
                response_format=ChatResponse
            )
            
            parsed_content = json.loads(response.choices[0].message.content)

            title = parsed_content['title'].replace(":", " - ")
            keywords = parsed_content["keywords"]
            
            return {
                'title': title,
                'keywords': keywords
            }
        
        except Exception as e:
            print(f"Error processing {image_path}: {e}")
            return None
