import os
import json
from tavily import TavilyClient
from dotenv import load_dotenv
from rich.console import Console
import google.generativeai as genai

console = Console()


load_dotenv

def format_query_results(json_data):
    """
    Formats JSON data into a structured text format.
    :param json_data: Dictionary containing query results.
    :return: Formatted string.
    """
    formatted_text = []

    # Add the main query
    query = json_data.get("query", "No query provided.")
    formatted_text.append(f"### Query\n{query}\n\n---\n")

    # Add the results
    results = json_data.get("results", [])
    formatted_text.append("### Results\n")

    if not results:
        formatted_text.append("No results found.\n")
    else:
        for i, result in enumerate(results, 1):
            title = result.get("title", "No title")
            url = result.get("url", "No URL")
            content = result.get("content", "No content available.")
            score = result.get("score", "Not available")

            formatted_text.append(f"{i}. **Title**: {title}\n")
            formatted_text.append(f"   **URL**: {url}\n")
            formatted_text.append(f"   **Content**: {content}\n")
            formatted_text.append(f"   **Score**: {score}\n\n")

    return "".join(formatted_text)

def search(query: str) -> str:
    # Step 1. Instantiating your TavilyClient
    tavily_client = TavilyClient(api_key=os.getenv("tvly_API_KEY"))

    # Step 2. Executing a simple search query
    response = tavily_client.search(query)

    # Step 3. That's it! You've done a Tavily Search!
    print(response)
    formatted_text = format_query_results(response)


    api_key = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=api_key)

    # Create the model
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    # Enhanced System Instructions for Gemini
    system_instructions = f"""
You are an expert summarization assistant. Your task is to analyze and synthesize information from multiple sources provided as search results to generate a concise, comprehensive summary of the topic in question. 

**Your Objectives:**
1. **Understand the Query:**  
   - Focus on addressing the user's {query} by summarizing key facts and insights from the provided search results.  
   - Identify relevant information while excluding unrelated or repetitive content.

2. **Analysis and Summarization:**  
   - **Identify Main Points:** Extract the central facts, arguments, and unique insights from each source.  
   - **Synthesize Information:** Combine insights from all sources into a unified summary that avoids redundancies. Highlight notable achievements, context, and distinguishing details.  
   - **Contrast Perspectives:** If different viewpoints or interpretations exist, mention and summarize them.

3. **Output Format:**  
   - **Summary Section:**  
     - Write a clear, structured summary in markdown format.  
     - Use paragraphs, bullet points, or numbered lists for readability.  
     - Reference sources explicitly within the text using a numbered format (e.g., "[1]").  
   - **Citations Section:**  
     - List all sources at the end under the "Sources" heading.  
     - Include the source title, URL, and a brief note on its contribution to the summary.

4. **Citation Standards:**  
   - Attribute each key fact or statement to its respective source using inline citations.  
   - Maintain transparency in referencing and avoid ambiguity in source attribution.

5. **Guidelines:**  
   - Avoid conversational filler and keep the tone professional and factual.  
   - Ensure the output is coherent, concise, and tailored to answer the user's query effectively.  
   - Prioritize the highest-scoring and most reliable sources but incorporate diverse perspectives if available.  

---

### Example Input:

**Query:**  
query

**Results:**  
- **Title:** title  
  **URL:** url  
  **Content:** content  
  **Score:** core  

---

### Example Output:

#### Summary:
Lionel Messi, an Argentine footballer born in 1987, is widely regarded as one of the greatest players of all time. Known for his exceptional dribbling, vision, and goal-scoring abilities, Messi spent most of his career at FC Barcelona, where he won numerous league and UEFA Champions League titles [1][2].  

In 2008, Messi won an Olympic gold medal, which he described as one of his most cherished victories [2]. By 2009, he helped Barcelona secure their first "treble," and he was already recognized as one of the world's dominant players [3]. His rivalry with Cristiano Ronaldo is considered one of the greatest in sports history [4].  

Messi has also achieved international success, leading Argentina to the 2014 World Cup final and securing multiple Ballon d'Or awards, including a record eight [4].

---

#### Sources:
1. **Lionel Messi Facts | Britannica**  
   [https://www.britannica.com/facts/Lionel-Messi](https://www.britannica.com/facts/Lionel-Messi)  

2. **Lionel Messi | Biography, Competitions, Wins and Medals**  
   [https://olympics.com/en/athletes/lionel-messi](https://olympics.com/en/athletes/lionel-messi)  

3. **Lionel Messi | Records, Height, Ballon d'Or, Inter Miami, & Facts**  
   [https://www.britannica.com/biography/Lionel-Messi](https://www.britannica.com/biography/Lionel-Messi)  

4. **Lionel Messi - Wikipedia**  
   [https://en.wikipedia.org/wiki/Lionel_Messi](https://en.wikipedia.org/wiki/Lionel_Messi)  

    """
    # Send prompt to Gemini with the extracted content
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        generation_config=generation_config,
        system_instruction=system_instructions
    )

    chat_session = model.start_chat(
        history=[
        ]
    )

    responsex = chat_session.send_message(formatted_text)
    console.print(f"[bold red]{responsex.text}[/bold red]")
    return responsex.text

# search("who won elections 2024")