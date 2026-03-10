'''
Using Playwright to capture network requests and then format them for 
Postman is a very effective way to create automated API testing collections based on real user interactions.
python code using Playwright to capture the request details (URL, Headers, and Payload/Body) and structure them into a JSON file 
compatible for easy import into Postman.

script captures requests and outputs a list of JSON objects, which you can easily transform into a Postman Collection later.

output captured_requests.json file contains a list of objects, where each object represents one API request.

Run the Python Script: Execute the code above.

Inspect the JSON: Open captured_requests.json. You'll see the structured data for each captured request.

Create Requests in Postman:

Open Postman.

Create a new collection.

For each object in the JSON file:

Create a new request in your Postman collection.

Set the Method (GET, POST, etc.) using the method value.

Set the URL using the url value.

Go to the Headers tab and manually add the key-value pairs from the headers field (e.g., Content-Type: application/json).

If payload_body is present, go to the Body tab, select raw, choose JSON, and paste the content of the payload_body.

This process allows you to quickly and accurately replicate complex client-side API calls into a reusable Postman testing collection.
'''
import asyncio
import json
from playwright.async_api import async_playwright

# --- Configuration ---
# The URL to navigate to and trigger the network requests
TARGET_URL = 'https://jsonplaceholder.typicode.com/'
# The file where the captured requests will be saved
OUTPUT_FILE = 'captured_requests.json'
# A filter to only capture requests containing this substring (e.g., API calls)
URL_FILTER = 'posts'

# List to store the structured data for each captured request
captured_data = []

def format_request_for_postman(request):
    """
    Formats the Playwright request object into a standard structure.
    """
    
    # Capture Request Payload/Body
    try:
        # Playwright provides post_data which is the body content
        payload = request.post_data
        
        # If payload exists, try to format it as JSON for Postman's raw body.
        if payload:
            try:
                # Attempt to parse as JSON if Content-Type is application/json
                if 'application/json' in request.headers.get('content-type', '').lower():
                    # If it's JSON, we typically want the structured object
                    # We can use json.loads() here if we want to ensure it's valid, 
                    # but for storage, the raw string is often best.
                    pass 
                
            except json.JSONDecodeError:
                # If it fails to decode, just keep the raw string payload
                pass
    except Exception:
        payload = None

    # --- Construct the dictionary for output ---
    request_data = {
        "url": request.url,
        "method": request.method,
        "headers": dict(request.headers), # Convert ReadOnlyDict to standard dict
        "payload_body": payload,
        "request_details": {
            "description": f"Captured {request.method} request to {request.url}",
            # Postman specific fields could be added here later (e.g., body mode, etc.)
        }
    }
    return request_data

async def capture_network_data():
    """Main function to run Playwright and capture requests."""
    async with async_playwright() as p:
        # Launch browser in headless mode (no visible window)
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        print(f"Navigating to {TARGET_URL}...")
        
        def handle_request(request):
            """Event handler that processes every request made by the page."""
            
            # Filter the requests: Only capture requests matching the URL filter
            # and exclude simple resource loads like images, CSS, etc.
            if URL_FILTER in request.url and request.resource_type in ('xhr', 'fetch', 'document'):
                
                # Check if it has an associated response (i.e., not blocked/aborted)
                if request.response: 
                    # Format and store the captured request data
                    data = format_request_for_postman(request)
                    captured_data.append(data)
                    print(f"Captured: {data['method']} {data['url']}")

        # Register the listener before navigating or performing actions
        page.on("request", handle_request)
        
        # Navigate to the target URL
        await page.goto(TARGET_URL, wait_until='networkidle')

        # --- Perform actions to trigger the requests ---
        # If the API calls require user interaction (e.g., a button click), 
        # add the Playwright action here:
        
        # Example: Triggering a request by clicking a link (optional, for demonstration)
        try:
            # Find and click an element that triggers the desired XHR/Fetch request
            await page.click('text="sunt aut facere"')
        except Exception:
            print("Could not find element to click or action failed. Relying on navigation requests.")

        # Wait a moment for any pending network requests to complete
        await asyncio.sleep(3) 

        await browser.close()
        print("Browser closed.")

# Run the asynchronous main function
if __name__ == "__main__":
    asyncio.run(capture_network_data())

    # --- Final Output to JSON File ---
    if captured_data:
        with open(OUTPUT_FILE, 'w') as f:
            json.dump(captured_data, f, indent=4)
        print(f"\n✅ Successfully captured {len(captured_data)} requests.")
        print(f"Data saved to {OUTPUT_FILE} for Postman import.")
    else:
        print("\n❌ No requests matching the filter were captured.")