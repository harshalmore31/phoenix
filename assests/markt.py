from markitdown import MarkItDown

md = MarkItDown()
result = md.convert(r"Cpath")
with open("output.md",'a') as f:
    f.write(result.text_content)
# print(result.text_content)

## Adv. RAG implementation