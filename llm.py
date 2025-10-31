from openai import OpenAI
import os
from dotenv import load_dotenv
class LLMAPI:
    def __init__(self, model_LLM = "gpt-5-ca", api_endpoint="https://api.chatanywhere.tech/v1" ):
        self.api_endpoint = api_endpoint
        


        load_dotenv()
        self.api_key = os.environ.get("OPENAI_API_KEY")
        self.model_LLM = model_LLM
        

        self.client = OpenAI(
            # defaults to os.environ.get("OPENAI_API_KEY")
            api_key= self.api_key,
            base_url= api_endpoint
            # base_url="https://api.chatanywhere.org/v1"
        )
        print("Test LLM API:",self.get_reponse("1+1=?"))
    def get_reponse(self,prompt_text):
        response = self.client.chat.completions.create(
        model="gpt-5-mini-ca",
        messages=[
                
                {"role": "user", "content": prompt_text}
            ]
        )
        return response.choices[0].message.content