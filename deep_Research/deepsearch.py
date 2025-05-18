# deepsearch.py
import importlib
import subprocess
import sys
from typing import List, Dict, Optional, Tuple

def lazy_import(module_name):
    try:
        return importlib.import_module(module_name)
    except ImportError:
        print(f"Installing missing package: {module_name}")
        subprocess.run([sys.executable, "-m", "pip", "install", module_name], check=True)
        return importlib.import_module(module_name)

# Lazy load required packages
asyncio = lazy_import("asyncio")
aiohttp = lazy_import("aiohttp")
BeautifulSoup = lazy_import("bs4").BeautifulSoup
json = lazy_import("json")
os = lazy_import("os")
load_dotenv = lazy_import("dotenv").load_dotenv
Console = lazy_import("rich.console").Console
Progress, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn = lazy_import("rich.progress").Progress, lazy_import("rich.progress").SpinnerColumn, lazy_import("rich.progress").TextColumn, lazy_import("rich.progress").BarColumn, lazy_import("rich.progress").TimeRemainingColumn
Panel = lazy_import("rich.panel").Panel
sync_playwright = lazy_import("playwright.sync_api").sync_playwright
time = lazy_import("time")
retry, stop_after_attempt, wait_exponential = lazy_import("tenacity").retry, lazy_import("tenacity").stop_after_attempt, lazy_import("tenacity").wait_exponential
datetime = lazy_import("datetime").datetime
re = lazy_import("re")
html2text = lazy_import("html2text")
ThreadPoolExecutor, as_completed = lazy_import("concurrent.futures").ThreadPoolExecutor, lazy_import("concurrent.futures").as_completed

console = Console()
load_dotenv()

class DeepResearchAssistant:
    def __init__(self):
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.google_cx = os.getenv("GOOGLE_CX")
        self.outputs_dir = "research_results"
        os.makedirs(self.outputs_dir, exist_ok=True)
        
        self.max_retries = 3
        self.max_threads = 5 # Adjust as needed
        self.timeout = 30
        self.content_elements = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'ul', 'ol', 'table', 'blockquote', 'pre', 'code']
        self.html_converter = html2text.HTML2Text()
        self.html_converter.body_width = 0  # Disable wrapping
        self.html_converter.ignore_links = False
        self.html_converter.ignore_images = False

    async def fetch_search_results(self, query: str) -> List[Dict]:
        """Fetch enhanced search results with site verification"""
        async with aiohttp.ClientSession() as session:
            url = "https://www.googleapis.com/customsearch/v1"
            params = {
                "key": self.google_api_key,
                "cx": self.google_cx,
                "q": query,
                "num": 10,
                "lr": "lang_en"
            }
            
            try:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._filter_results(data.get("items", []))
                    return []
            except Exception as e:
                console.print(f"[red]Search error: {str(e)}[/red]")
                return []

    def _filter_results(self, items: List[Dict]) -> List[Dict]:
        """Filter results with quality checks"""
        filtered = []
        for item in items:
            if any(ext in item.get("link", "").lower() for ext in [".pdf", ".doc", ".docx", ".ppt"]):
                continue
            if "fileFormat" in item:
                continue
            filtered.append({
                "title": item.get("title", "No title"),
                "url": item["link"],
                "snippet": item.get("snippet", ""),
                "source": "Google Search"
            })
        return filtered[:10]

    def _extract_metadata(self, soup: BeautifulSoup) -> Dict:
        """Extract structured metadata from page"""
        metadata = {
            "author": "",
            "date": "",
            "keywords": []
        }
        
        # Author extraction
        author_selectors = [
            {'name': 'meta', 'attrs': {'name': 'author'}},
            {'name': 'meta', 'attrs': {'property': 'article:author'}},
            {'name': 'meta', 'attrs': {'name': 'dc.creator'}}, # Dublin Core
            {'selector': '.author, .byline, [itemprop="author"], [rel="author"]'}
        ]
        for selector in author_selectors:
            if 'name' in selector:
                author_tag = soup.find(selector['name'], attrs=selector.get('attrs'))
                if author_tag:
                    metadata['author'] = author_tag.get('content', '').strip()
                    break
            elif 'selector' in selector:
                author_element = soup.select_one(selector['selector'])
                if author_element:
                    metadata['author'] = author_element.get_text().strip()
                    break

        
        # Date extraction
        date_selectors = [
            {'name': 'meta', 'attrs': {'property': 'article:published_time'}},
            {'name': 'meta', 'attrs': {'name': 'datePublished'}},
            {'name': 'meta', 'attrs': {'name': 'dc.date'}},  # Dublin Core
            {'name': 'time', 'attrs': {'datetime': True}},
             {'selector': '.date, .post-date, .publish-date, [itemprop="datePublished"]'}
        ]

        for selector in date_selectors:
            if 'name' in selector:
                date_tag = soup.find(selector['name'], attrs=selector.get('attrs'))
                if date_tag:
                    date_str = date_tag.get('content', '').strip()
                    # Attempt to parse various date formats
                    for fmt in ("%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%d", "%B %d, %Y"):
                        try:
                            metadata['date'] = datetime.strptime(date_str, fmt).strftime("%Y-%m-%d")
                            break  # Stop if parsing is successful
                        except ValueError:
                            continue
                    break
            elif 'selector' in selector:
                date_element = soup.select_one(selector['selector'])
                if date_element:
                    # First try to get datetime attribute if it exists
                    date_str = date_element.get('datetime', '').strip()
                    if not date_str:
                        date_str = date_element.get_text().strip()
                    for fmt in ("%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%d", "%B %d, %Y"):
                        try:
                            metadata['date'] = datetime.strptime(date_str, fmt).strftime("%Y-%m-%d")
                            break  # Stop if parsing is successful
                        except ValueError:
                            continue
                    break
            
        # Keywords extraction
        keyword_meta = soup.find('meta', attrs={'name': 'keywords'})
        if keyword_meta:
            metadata['keywords'] = [k.strip() for k in keyword_meta.get('content', '').split(',')]
            
        return metadata

    def _convert_to_markdown(self, soup: BeautifulSoup) -> str:
        """Convert content soup to structured Markdown"""
        markdown = []
        for element in soup.find_all(self.content_elements, recursive=True):
            if element.name.startswith('h'):
                level = int(element.name[1])
                markdown.append(f"\n{'#' * level} {element.get_text().strip()}\n")
            elif element.name == 'p':
                text = self.html_converter.handle(str(element)).strip()
                if text:
                    markdown.append(f"{text}\n")
            elif element.name in ['ul', 'ol']:
                list_items = element.find_all('li', recursive=False)
                for idx, li in enumerate(list_items):
                    prefix = "- " if element.name == 'ul' else f"{idx+1}. "
                    markdown.append(f"{prefix}{li.get_text().strip()}\n")
                markdown.append("\n")
            elif element.name == 'table':
                markdown.append(self.html_converter.handle(str(element)))
            elif element.name in ['blockquote', 'pre', 'code']:
                markdown.append(f"```\n{element.get_text().strip()}\n```\n")
        
        return "\n".join(markdown).strip()

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def extract_content(self, url: str) -> Optional[Dict]:
        """Deep extraction with full page interaction"""
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(
                    headless=True,
                    timeout=30000
                )
                context = browser.new_context(
                    viewport={'width': 1920, 'height': 1080},
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    java_script_enabled=True
                )
                
                page = context.new_page()
                page.set_default_timeout(20000)
                
                try:
                    # Deep page interaction
                    page.goto(url, wait_until="networkidle")
                    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                    page.wait_for_timeout(2000)  # Wait for lazy-loaded content

                    # Handle cookie consent banners (example - adjust selectors as needed)
                    try:
                        page.click("button#acceptCookies", timeout=5000)  # Example selector
                    except:
                        pass  # Ignore if not found

                    # Handle pop-ups (example)
                    try:
                        page.click(".close-popup-button", timeout=3000) # Example selector
                    except:
                        pass
                    
                    # Extract rendered content
                    main_content = page.inner_html("body")
                    soup = BeautifulSoup(main_content, 'lxml')
                    
                    # Remove unwanted elements
                    for selector in ['nav', 'footer', 'header', 'aside', 'form', 'iframe', 'script', 'style', 'noscript']:
                        for element in soup.select(selector):
                            element.decompose()
                    
                    # Extract structured content
                    metadata = self._extract_metadata(soup)
                    content_md = self._convert_to_markdown(soup)
                    
                    return {
                        "url": url,
                        "title": soup.title.string.strip() if soup.title else "No title",
                        "content": content_md,
                        "metadata": metadata
                    }
                    
                finally:
                    browser.close()
                    
        except Exception as e:
            console.print(f"[yellow]Deep extraction warning: {url} - {str(e)}[/yellow]")
            return None
    async def process_urls(self, urls: List[str]) -> List[Dict]:
        """Parallel processing with progress tracking"""
        results = []
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TimeRemainingColumn(),
        ) as progress:
            task = progress.add_task("🔍 Deep analyzing pages...", total=len(urls))
            
            with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
                futures = {executor.submit(self.extract_content, url): url for url in urls}
                for future in as_completed(futures):
                    url = futures[future]
                    try:
                        if result := future.result():
                            results.append(result)
                    except Exception as e:
                        console.print(f"[red]Processing error: {url} - {str(e)}[/red]")
                    finally:
                        progress.advance(task)
        
        return results

    def format_results(self, query: str, results: List[Dict]) -> Tuple[str, List[Dict]]:
        """Rich formatting with sources and metadata"""
        formatted = [
            f"# Deep Research Report: {query}",
            f"**Generated at**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**Total Sources Analyzed**: {len(results)}\n"
        ]
        
        sources = []
        for idx, result in enumerate(results, 1):
            formatted.append(f"## Source {idx}: {result['title']}")
            formatted.append(f"**URL**: {result['url']}")
            if result['metadata']['author']:
                formatted.append(f"**Author**: {result['metadata']['author']}")
            if result['metadata']['date']:
                formatted.append(f"**Date**: {result['metadata']['date']}")
            formatted.append("\n### Key Content:\n")
            formatted.append(result['content'][:5000] + ("..." if len(result['content']) > 5000 else ""))
            formatted.append("\n---\n")
            sources.append({"title": result['title'], "url": result['url']})
        
        return "\n".join(formatted), sources

    async def search(self, query: str) -> str:
        """Complete research workflow"""
        start_time = time.time()
        
        # Fetch and filter results
        search_data = await self.fetch_search_results(query)
        if not search_data:
            return "No relevant sources found."
        
        # Deep content extraction
        urls = [result["url"] for result in search_data]
        extracted_data = await self.process_urls(urls)
        
        # Format output
        formatted_report, sources = self.format_results(query, extracted_data)
        sources_section = "## References\n" + "\n".join(
            f"- [{src['title']}]({src['url']})" for src in sources
        )
        
        full_report = f"{formatted_report}\n\n{sources_section}"
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.outputs_dir, f"research_{timestamp}.md")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(full_report)
        
        console.print(Panel(
            f"✅ Deep research completed in {time.time() - start_time:.1f}s\n"
            f"📄 Full report saved to: [underline]{filename}[/underline]",
            title="Research Complete",
            border_style="green"
        ))
        
        return full_report

def web_search(query: str) -> str:
    """Synchronous entry point"""
    researcher = DeepResearchAssistant()
    return asyncio.run(researcher.search(query))

# Example usage:
# results = web_search("Google ")
# console.print(results)