"""
Basic Open AI Implementation for character based conversation replies
by hannahbanana
"""

import openai
import pandas as pd
from seinfeld_api.settings import OPEN_AI_API_KEY
from django.db import connection

API_KEY = OPEN_AI_API_KEY

# TODO: fine tune the llm with each character's personality
class AIConversation:

    def __init__(self, speaker, season=7, episode=None):
        self.speaker = speaker
        self.season = season
        self.episode = episode
        self.get_character_lines()
        self.generate_system_prompt()
        self.client = openai.OpenAI(api_key=API_KEY)
        self.num_hist = 0
        self.messages = [
            {
                "role": "system",
                "content": [{"type": "text", "text": self.system_prompt}],
            }
        ]

    def get_character_lines(self):
        if self.episode is None:
            query = f"""
                    select episode.id
                    ,episode.season_number
                    ,sentence.text
                    ,utterance.speaker

                from episode
                inner join utterance on episode.id = utterance.episode_id
                inner join sentence on utterance.id = sentence.utterance_id

                where episode.season_number = {self.season}
                and utterance.speaker = '{self.speaker}'
                """
        else:
            query = f"""
                    select episode.id
                    ,episode.season_number
                    ,sentence.text
                    ,utterance.speaker

                from episode
                inner join utterance on episode.id = utterance.episode_id
                inner join sentence on utterance.id = sentence.utterance_id

                where episode.season_number = {self.season}
                and utterance.speaker = '{self.speaker}'
                and episode.episode_number = {self.episode}
                """

        lines = pd.read_sql_query(query, connection)
        text = []
        for line in lines["text"]:
            if len(line.split(" ")) >= 10:
                text.append(line)
        self.text = "\n".join(text)
        return

    def generate_system_prompt(self):
        self.system_prompt = f"""
        Given the lines of a character, understand the way they talk, and then answer the question with 1 liner response using the way this character talks, and make it funny.\n
        Character Name: {self.speaker}\n
        Character lines: {self.text}
        """
        return

    # TODO: re-write chat history part with LangChain https://stackoverflow.com/questions/74711107/openai-api-continuing-conversation-in-a-dialogue#:~:text=The%20best%20solution%20I%20found%20is%20to%20use%20langchain
    def chat(self, usr_message):
        if self.num_hist < 10:
            self.num_hist += 1
        else:
            system = self.messages[0]
            self.messages = system + self.messages[2:]
        self.messages.append({"role": "user", "content": usr_message})
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=self.messages,
            temperature=0.7,
            max_tokens=50,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            response_format={"type": "text"},
            stop=["\n"],
        )
        self.messages.append(
            {
                "role": "assistant",
                "content": response.choices[0].message.content.strip(),
            }
        )
        return response.choices[0].message.content.strip()

    def clear_history(self):
        self.messages = self.messages[0]
        self.num_hist = 0
