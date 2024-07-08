from IPython.display import display
import pathlib
import textwrap
import google.generativeai as genai
from IPython.display import clear_output
from data import *


class Stack:
    def __init__(self, max_size):
        self.items = []
        self.max_size = max_size

    def push(self, item):
        if len(self.items) == self.max_size:
            self.items.pop(0)  # Remove the first (oldest) element
        self.items.append(item)  # Add the new item to the end

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        else:
            return None

    def is_empty(self):
        return len(self.items) == 0

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        else:
            return None

    def size(self):
        return len(self.items)
		
		
GOOGLE_API_KEY = 'YOUR_API_KEY'
genai.configure(api_key=GOOGLE_API_KEY)
		
for m in genai.list_models():
  if 'generateContent' in m.supported_generation_methods:
    print(m.name)
	
gemini = genai.GenerativeModel('gemini-1.5-flash-latest')

def remove_after_newline(text):
  """Removes everything after a newline character in a string if it exists."""
  if '\n' in text:
    return text.split('\n')[0]
  else:
    return text
	
stack = Stack(4)

while(1):
  prompt = "Below will be given to you a current query and a history stack consisting of past few queries. You are to return only a context aware query. if history stack is empty, return the current query as it is, if history stack is irrelevant, return current query as it is. latest in the stack should have more weight than older entries. The resultant query should be constructed in such a way that history is no longer needed to understand the query.  Return format should be: \"Updated Query: xyz\" :"
  query = input("Enter your query: ")
  clear_output()

  prompt += "\nCurrent Query: "
  prompt += query
  prompt += "\nHistory_stack: "
  prompt += str(stack.items)

  stack.push(query)

  response = gemini.generate_content(prompt)


  print("\n Query: ", query)
  query = response.text

  query = remove_after_newline(query)
  print("\n\n\n",query,"\n\n\n")

  query = query.replace("Updated Query: ", "")


  inputs2 = processor(text = [query], return_tensors="pt")
  text_features = model.get_text_features(**inputs2)
  query = text_features[0].detach().numpy()

  D, I = index.search(query.reshape(1, -1), k=3)
  image = Image.open('data/'+filenames[I[0][0]])
  print("Top match: ")
  display(image)