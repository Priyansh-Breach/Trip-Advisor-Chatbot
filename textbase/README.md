# Trip Advisor AI Chatbot

![Trip Advisor AI Chatbot](https://example.com/chatbot_image.png)

Trip Advisor AI is a chatbot designed to help users plan their perfect trip. The chatbot uses GPT-3.5 Turbo from OpenAI to provide natural, conversational responses to user queries about travel destinations, budgets, durations, weather forecasts, and more.

## Requirements

- Python 3.6+
- OpenAI API key
- WeatherAPI key

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/trip-advisor-ai.git
```

2. Create a virtual environment (optional but recommended):

```bash
cd trip-advisor-ai
python -m venv venv
```

3. Activate the virtual environment:

On Windows:

```bash
venv\Scripts\activate
```

On macOS and Linux:

```bash
source venv/bin/activate
```

4. Install the required dependencies:

```bash
pip install -r requirements.txt
```

5. Set up the environment variables:

Create a `.env` file in the root directory of the project and add your API keys:

```plaintext
OPENAI_API_KEY=your_openai_api_key
WEATHER_API_KEY=your_weatherapi_key
```

## Usage

Run the chatbot script:

```bash
python main.py
```

The chatbot will start, and you can interact with it by typing your messages. To exit the chatbot, type "exit" or "quit."

## Features

- Plan a trip: Start planning your trip by telling the chatbot that you want to start a new trip.
- Destination, Budget, and Duration: The chatbot can understand your preferences for the trip.
- Weather Forecast: Ask for weather forecasts for specific cities.
- Natural Conversation: The chatbot responds in a natural, conversational manner.

## Implementation with Textbase

The Trip Advisor AI chatbot is built using the Textbase framework. Textbase is a framework for building chatbots using NLP and ML. To implement the `on_message` function in `main.py`, Textbase takes care of the rest of the chatbot logic.

### Installation of Textbase

Clone the Textbase repository and install the dependencies using Poetry (you might have to [install Poetry](https://python-poetry.org/docs/#installation) first).

```bash
git clone https://github.com/cofactoryai/textbase
cd textbase
poetry install
```

### Start the Development Server

> If you're using the default template, **remember to set the OpenAI API key** in `main.py`.

Run the following command:

```bash
poetry run python textbase/textbase_cli.py test main.py
```

Now go to [http://localhost:4000](http://localhost:4000) and start chatting with your bot! The bot will automatically reload when you change the code.

_Simpler version using PyPI package and CLI coming soon!_

## Contributing

Contributions are welcome! If you have any improvements or new features to suggest, please create a pull request. For major changes, please open an issue first to discuss the changes.

## License

[MIT License](LICENSE)

## Coming Soon

- PyPI package for easier installation
- SMS integration for more accessibility
- Easy web deployment via `textbase deploy`
- Native integration of other models (Claude, Llama, ...)
