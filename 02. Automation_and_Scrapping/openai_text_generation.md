### Install module
```bash
pip install openai
```
### Text Generation
```py
from openai import OpenAI
api_key = ''
model_name = 'gpt-3.5-turbo'   # or any model

def text_generation(previous_prompt, prompt):
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": previous_prompt},
                {"role": "user", "content": prompt}
            ],
            model=model_name,
        )
        return response.choices[0].message.content

```
