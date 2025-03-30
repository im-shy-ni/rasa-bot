from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import AllSlotsReset, Restarted
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import time


# ✅ Base URL of your university website
BASE_URL = "https://b-u.ac.in/"

class ActionScrapeEntireWebsite(Action):
    """Scrapes the entire university website and searches for the user query."""

    def name(self) -> Text:
        return "action_scrape_entire_website"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_query = tracker.latest_message.get("text")

        # Dictionary to store all scraped content
        scraped_data = {}

        # Use a session with headers to prevent bot detection
        session = requests.Session()
        session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        })

        try:
            visited = set()
            to_visit = [BASE_URL]
            
            while to_visit:
                url = to_visit.pop(0)

                if url in visited:
                    continue

                visited.add(url)

                try:
                    response = session.get(url, timeout=10)  
                    response.raise_for_status()
                except (requests.ConnectionError, requests.Timeout) as e:
                    print(f"⚠️ Failed to fetch {url}: {str(e)}")
                    continue

                soup = BeautifulSoup(response.content, "html.parser")

                # Store page content
                page_content = []

                # Extract headings, paragraphs, and links
                for section in soup.find_all(["h1", "h2", "h3", "p"]):
                    text = section.get_text().strip()
                    if text:
                        page_content.append(text)

                # Store content in dictionary
                scraped_data[url] = page_content

                # Extract and append new links
                for link in soup.find_all("a", href=True):
                    full_link = urljoin(BASE_URL, link["href"])
                    if full_link not in visited and full_link.startswith(BASE_URL):
                        to_visit.append(full_link)

                time.sleep(1)  # Prevent overloading the server

            # Save scraped data to JSON
            with open("university_data.json", "w", encoding="utf-8") as file:
                json.dump(scraped_data, file, ensure_ascii=False, indent=4)

            # Search for the user query in the scraped data
            found = False
            results = []

            for page, content in scraped_data.items():
                for item in content:
                    if user_query.lower() in item.lower():
                        results.append(f"✅ Found on {page}: {item}")
                        found = True

            if found:
                dispatcher.utter_message("\n".join(results))
            else:
                dispatcher.utter_message("❌ Sorry, I couldn't find the information you requested on the website.")

        except Exception as e:
            dispatcher.utter_message(f"❌ Error: {str(e)}")

        return []


# -----------------------------------------------------
# ✅ Clear and Continue Chat Actions
# -----------------------------------------------------

class ActionClearChat(Action):
    """Clears the chat and resets all slots."""

    def name(self) -> str:
        return "action_clear_chat"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: dict) -> list:
        try:
            dispatcher.utter_message(text="🧹 Chat has been cleared!")
            return [AllSlotsReset(), Restarted()]
        except Exception as e:
            dispatcher.utter_message(f"❌ Error clearing chat: {str(e)}")
            return []


class ActionContinueChat(Action):
    """Continues the chat session."""

    def name(self) -> str:
        return "action_continue_chat"

    async def run(self, dispatcher, tracker, domain):
        try:
            dispatcher.utter_message(text="👍 Okay! Let's continue.")
            return []
        except Exception as e:
            dispatcher.utter_message(f"❌ Error continuing chat: {str(e)}")
            return []


class ActionClear(Action):
    """Clears the conversation and restarts the session."""

    def name(self) -> str:
        return "action_clear"

    def run(self, dispatcher, tracker, domain):
        try:
            dispatcher.utter_message(text="🧹 Chat has been cleared!")
            return [Restarted()]
        except Exception as e:
            dispatcher.utter_message(f"❌ Error restarting chat: {str(e)}")
            return []
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
from bs4 import BeautifulSoup

class ActionGetAdmissionDates(Action):
    def name(self) -> str:
        return "action_get_admission_dates"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:

        url = "https://www.b-u.ac.in/Home/Admissions"  # Replace with the correct URL
        response = requests.get(url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Example: Extracting admission date details
            dates_section = soup.find("div", class_="admission-dates")
            if dates_section:
                dates = dates_section.text.strip()
                message = f"📅 The current admission dates are: \n{dates}"
            else:
                message = "⚠️ Unable to fetch the latest admission dates. Please check the website."
        else:
            message = "❌ Failed to connect to the university website. Please try again later."
        
        dispatcher.utter_message(text=message)
        return []
class ActionGetPublishedPapers(Action):
    def name(self) -> str:
        return "action_get_published_papers"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:

        url = "https://www.b-u.ac.in/Home/ResearchPublications"  # Replace with the correct URL
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            papers = []
            for item in soup.find_all("li", class_="paper-item", limit=5):
                title = item.text.strip()
                link = item.a["href"]
                papers.append(f"- [{title}]({link})")

            if papers:
                message = "📰 Here are some recently published papers:\n" + "\n".join(papers)
            else:
                message = "⚠️ No recent papers found."
        else:
            message = "❌ Failed to connect to the university website. Please try again later."

        dispatcher.utter_message(text=message)
        return []

