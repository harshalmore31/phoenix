# bring in our LLAMA_CLOUD_API_KEY
from dotenv import load_dotenv
load_dotenv()

# bring in deps
from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader
import google.generativeai as genai
from rich.console import Console
import os
from datetime import datetime
import asyncio
import json
import re  # Import regex module for email validation

console = Console()

# Set up parser
parser = LlamaParse(
    result_type="markdown"  # "markdown" and "text" are available
)

# Use SimpleDirectoryReader to parse the file
file_extractor = {".csv": parser}
documents = SimpleDirectoryReader(input_files=[r'src\backend\Items.csv'], file_extractor=file_extractor).load_data()

for doc in documents:
    print(doc.text)
    print("-" * 50) 

# Get Google API Key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise EnvironmentError("GOOGLE_API_KEY environment variable not set")

# BEGIN TOOL DEFINITIONS
class TicketManagement:
    def __init__(self):
        self.tickets = {}
        self.next_ticket_id = 1  # Keep track of ticket IDs

    def create_ticket(self, text: str) -> str:
        try:
            data = json.loads(text)
            customer_id = data.get('customer_id')
            issue_type = data.get('issue_type')
            priority = data.get('priority')
            customer_email = data.get('customer_email')  # Get email if provided

            if not customer_id:
              return json.dumps({"error": "Customer ID not provided, please provide customer email"})

            if not customer_email:
              return json.dumps({"error": "Customer Email not provided, please provide customer email"})
            
            if not self._is_valid_email(customer_email):
              return json.dumps({"error": "Invalid customer email. Please provide a valid email."})
            
            ticket = {
                'id': self.next_ticket_id, # Use the incremented id
                'customer_id': customer_id,
                'customer_email' : customer_email,
                'issue_type': issue_type,
                'priority': priority,
                'status': 'open',
                'created_at': datetime.now(),
                'history': []
            }
            self.tickets[ticket['id']] = ticket
            self.next_ticket_id += 1 # Increment ticket ID
            return json.dumps({"ticket_id": ticket['id']}) # Return the new ticket number as json
        except json.JSONDecodeError:
            return json.dumps({"error": "Invalid JSON format. Please provide a valid JSON string."})
        except Exception as e:
            return json.dumps({"error": f"An unexpected error occurred: {str(e)}"})
    
    def update_ticket_status(self, text: str) -> str:
        try:
           data = json.loads(text)
           ticket_id = data.get('ticket_id')
           status = data.get('status')
           ticket_id = int(ticket_id)

           if ticket_id in self.tickets:
               self.tickets[ticket_id]['status'] = status
               self.tickets[ticket_id]['history'].append({
                   'action': f'Status updated to {status}',
                   'timestamp': datetime.now()
               })
               return "true"
           return json.dumps({"error": "Ticket not found."})
        except (json.JSONDecodeError, ValueError):
            return json.dumps({"error":"Invalid JSON format or ticket id."})

    def _is_valid_email(self, email):
        # Very basic email validation
      email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
      return re.match(email_regex, email) is not None



class CommunicationHandler:
    def __init__(self):
        self.channels = {
            'email': EmailService(),
            'chat': ChatService(),
            'sms': SMSService()
        }
    
    async def send_message(self, text: str) -> str:
        try:
            data = json.loads(text)
            channel = data.get('channel')
            customer_id = data.get('customer_id')
            message = data.get('message')
            if channel in self.channels:
              result = await self.channels[channel].send(customer_id, message)
              return str(result)
            raise ValueError(f"Unsupported channel: {channel}")
        except (json.JSONDecodeError, ValueError) as e:
            return json.dumps({"error": f"Error: {str(e)}"})
    
    async def process_response(self, message: str) -> str:
        return json.dumps({
            'intent': self._detect_intent(message),
            'sentiment': self._analyze_sentiment(message),
            'priority': self._determine_priority(message)
        })
    
    def _detect_intent(self, message):
        # Implement intent detection logic
        return "default_intent"
    
    def _analyze_sentiment(self, message):
        # Implement sentiment analysis logic
        return "neutral"
    
    def _determine_priority(self, message):
        # Implement priority determination logic
        return "low"


class KnowledgeBase:
    def __init__(self):
        self.db = {}
        
    def search(self, text: str) -> str:
        query = text
        results = []
        for article_id, content in self.db.items():
            if self._match_query(query, content):
                results.append(content)
        return json.dumps(results[:5])  # Return top 5 matches

    def add_article(self, text: str) -> str:
        try:
           data = json.loads(text)
           title = data.get('title')
           content = data.get('content')
           tags = data.get('tags')
           article_id = len(self.db) + 1
           self.db[article_id] = {
               'id': article_id,
               'title': title,
               'content': content,
               'tags': tags
           }
           return str(article_id)
        except (json.JSONDecodeError, ValueError):
            return json.dumps({"error": "Invalid JSON Format"})
    
    def _match_query(self, query, content):
        # Simple match logic
        return query.lower() in content['title'].lower() or query.lower() in content['content'].lower()


class SecurityManager:
    def __init__(self):
        self.session_store = {}
    
    def authenticate_request(self, text: str) -> str:
       try:
           credentials = json.loads(text)
           return str(self._verify_token(credentials.get('token')))
       except (json.JSONDecodeError, ValueError):
           return json.dumps({"error": "Invalid JSON format"})
    
    def _verify_token(self, token):
        # Simple authentication for now
        return token == "valid_token"


class EmailService:
    async def send(self, customer_id, message):
      await asyncio.sleep(1)
      print(f"Email sent to {customer_id}: {message}")
      return True

class ChatService:
    async def send(self, customer_id, message):
      await asyncio.sleep(1)
      print(f"Chat message sent to {customer_id}: {message}")
      return True

class SMSService:
    async def send(self, customer_id, message):
      await asyncio.sleep(1)
      print(f"SMS sent to {customer_id}: {message}")
      return True
# END TOOL DEFINITIONS

# create instances of the tooling
ticket_manager = TicketManagement()
communication_handler = CommunicationHandler()
knowledge_base = KnowledgeBase()
security_manager = SecurityManager()


def issue(text: str) -> str :
    Issue = text
    print(f"Your Issue \n {issue} \n has been send to the company")

genai.configure(api_key=api_key)

# Model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Join all document text into a single string for context
context = "\n\n".join([doc.text for doc in documents])

# Define system instructions for Gemini with context injection
system_instructions = f"""
You are ThingbitsHelper, an advanced AI-powered support and sales assistant for electronics e-commerce. Your role encompasses comprehensive customer support, sales assistance, and issue resolution.
  
You have access to the following tools:
  
   - **Ticket Management:** Use the TicketManagement tool for creating and updating support tickets.
    - create_ticket(text): Creates a new ticket and returns a JSON object with ticket id. Expects a JSON string with customer_id, issue_type, priority and customer_email. If customer_id or customer_email are not provided ask user to provide a valid email.
    - update_ticket_status(text): Updates an existing ticket with status open, in progress, pending or resolved. Expects a JSON string with ticket_id and status. Returns "true" for success otherwise a JSON error response.
   - **Communication Handler:** Use the CommunicationHandler tool for sending messages through different channels.
     - send_message(text): Sends a message through the specified channel (email, chat, sms). Expects a JSON string with channel, customer_id and message. Returns a JSON object with success or error details.
     - process_response(text) : Processes an incoming message, analyses intent, sentiment and priority and returns it as a json object
   - **Knowledge Base:** Use KnowledgeBase for finding information.
     - search(text): Returns the top 5 most relevant articles as a json array.
     - add_article(text): Adds an article to the Knowledge base and returns article_id. Expects a JSON string with title, content and tags.
   - **Security Manager:** Use SecurityManager for handling secure information.
     - authenticate_request(text): Authenticates the request by checking user credentials and returns true or false. Expects a JSON string with token.
   
  
### Core Capabilities

1. **Customer Support Management**
   - Ticket Creation and Tracking:
   - Priority Levels: Critical, High, Medium, Low
   - Status: Open, In Progress, Pending, Resolved
   - Categories: Technical, Billing, Product, Shipping
   - Issue Recording System:
   - Customer Details
   - Issue Description
   - Resolution Steps
   - Follow-up Actions

2. **Communication Channels**
   - Omnichannel Support Integration:
   - Live Chat
   - Email Support
   - Social Media
   - Voice Support
   - Response Management:
   - Smart Templates
   - Automated Responses
   - Multilingual Support

3. **Product Information System**
   Product details must include:
   - Name
   - Price
   - SKU
   - Stock Status
   - Technical Specifications
   - Warranty Information
   - Related Products

4. **Order Management**
   - Order Tracking
   - Returns Processing
   - Shipping Status Updates
   - Invoice Generation
   - Payment Verification

### Advanced Features

1. **Analytics and Reporting**
   - Performance Metrics:
   - Response Time
   - Resolution Rate
   - Customer Satisfaction
   - Issue Analytics:
   - Common Problems
   - Resolution Patterns
   - Customer Feedback

2. **Customer Experience Tools**
   - Personalization Engine
   - Customer History Tracking
   - Satisfaction Surveys
   - Journey Mapping

3. **Knowledge Management**
   - FAQ Database
   - Technical Documentation
   - Product Manuals
   - Training Materials

4. **Quality Assurance**
   - Conversation Monitoring
   - Quality Scoring
   - Performance Analytics
   - Compliance Checking

### Response Guidelines

1. **Issue Resolution Protocol**
   ```
   [
   "initial_response": [
     "greeting": "personalized",
     "issue_acknowledgment": "clear",
     "next_steps": "outlined"
   ],
   "resolution_process": [
     "identify_issue": "priority",
     "gather_information": "systematic",
     "provide_solution": "step_by_step",
     "verify_resolution": "confirmation"
   ]
   ]
   ```

2. **Product Recommendations**
   ```
   [
   "matching_criteria": [
     "price_range",
     "specifications",
     "availability",
     "customer_preferences"
   ],
   "display_format": [
     "max_products": 3,
     "details": ["name", "price", "specs", "stock"],
     "alternatives": "if_unavailable"
   ]
   ]
   ```

3. **Sales Support Protocol**
   ```
   [
   "upselling": [
     "identify_opportunities": true,
     "suggest_premium": "when_relevant",
     "highlight_benefits": "clear_value"
   ],
   "cross_selling": [
     "complementary_products": true,
     "bundle_offers": "if_available",
     "accessories": "relevant_only"
   ]
   ]
   ```

### Security and Compliance

1. **Data Protection**
   - Encryption Standards
   - Access Controls
   - Privacy Compliance
   - Audit Logging

2. **Transaction Security**
   - Payment Verification
   - Fraud Prevention
   - Secure Communication

You will process queries using the provided context:
{context}

Remember to maintain:
- Professional tone
- Accurate information
- Quick response time
- Solution-oriented approach
- Customer satisfaction focus

"""

# Instantiate the Gemini model
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
    system_instruction=system_instructions,
    tools=[
        ticket_manager.create_ticket, 
        ticket_manager.update_ticket_status,
        communication_handler.send_message,
        communication_handler.process_response,
        knowledge_base.search,
        knowledge_base.add_article,
        security_manager.authenticate_request,
    ]
)

# Start chat session
chat_session = model.start_chat(
    history=[],enable_automatic_function_calling=True
)

# User query
while 1:
    user_query = input("Query : ")
    # Send query and get response from Gemini
    response = chat_session.send_message(user_query)
    console.print(f"[bold red]{response.text}[/bold red]")