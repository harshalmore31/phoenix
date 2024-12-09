import requests

def cal(eventname: str, date: str, start_time: str = None, end_time: str = None, description: str = None, location: str = None) -> str:
    """
    Sends an event creation request to a Zapier webhook to add an event to Google Calendar.
    
    Args:
        eventname (str): Name of the event (Required).
        date (str): Event date in YYYY-MM-DD format (Required).
        start_time (str): Event start time in HH:MM 24-hour format (Optional).
        end_time (str): Event end time in HH:MM 24-hour format (Optional).
        description (str): Description of the event (Required).
        location (str): Event location (Optional).
    
    Returns:
        str: A message indicating success or failure of the request.
    """

    # Check for mandatory fields
    if not eventname or not date or not description:
        return "Error: 'eventname', 'date', and 'description' are required fields."

    print("Adding the event to Google Calendar:")
    choice = input("Confirm? Enter Y/N: ").strip().lower()
    
    if choice == "y":
        # Webhook URL from Zapier
        webhook_url = "https://hooks.zapier.com/hooks/catch/10321312/2rx22ly/"  # Replace with your actual Zapier webhook URL
        
        # Build the event data payload
        event_data = {
            "summary": eventname,
            "start": {
                "dateTime": f"{date}T{start_time}:00" if start_time else None,  # Include only if start_time is provided
                "timeZone": "UTC"
            },
            "end": {
                "dateTime": f"{date}T{end_time}:00" if end_time else None,  # Include only if end_time is provided
                "timeZone": "UTC"
            },
            "description": description,
            "location": location or "Not specified"
        }
        
        # Remove keys with None values to ensure a clean payload
        event_data = {k: v for k, v in event_data.items() if v is not None}
        if "start" in event_data:
            event_data["start"] = {k: v for k, v in event_data["start"].items() if v is not None}
        if "end" in event_data:
            event_data["end"] = {k: v for k, v in event_data["end"].items() if v is not None}

        try:
            # Send POST request to the webhook URL
            response = requests.post(webhook_url, json=event_data)

            if response.status_code == 200:
                return f"Event '{eventname}' added successfully to Google Calendar!"
            else:
                return f"Failed to add event. Status code: {response.status_code}, Response: {response.text}"
        except Exception as e:
            return f"An error occurred: {e}"
    else:
        return "Event creation canceled by user."