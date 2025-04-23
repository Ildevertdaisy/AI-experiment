
import ollama


prompt = """
- Instrution: Extract the text from the image attached in markdown format. Make sure to only extract only the text and don't forget to consider and detect checkboxex in images."
- Constrain:"
   - Don't forget any text inside the image
   - You only respond with the text extract in markdown.
   - You also respect the table(s) structure(s) mentionned and reflect it in markdown
   - Don't include the ```mardown <text extracted>``` delimiter in your response
   - You also respect the checkmark in checkboxes presented.
   - If there's a checked checbox, represents if with this character: ☑️
   - If there's an unchecked checbox, represents if with this character: ☐
""" 

response = ollama.chat(
    model='llama3.2-vision',
    messages=[
        {
            'role': 'user',
            'content': prompt,
            'images': ['ball.jpg']
        }
    ]
)


print(response)