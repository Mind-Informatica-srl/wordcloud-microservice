# Word Cloud Microservice

This project is a microservice that generates word cloud images based on provided word frequencies and colors. It exposes an API endpoint that allows users to customize the appearance of the word cloud.

## Project Structure

```
wordcloud-microservice
├── src
│   ├── wordcloud_graph.py  # Contains the function to generate word clouds
│   ├── app.py               # Entry point for the microservice
├── requirements.txt         # Lists project dependencies
└── README.md                # Documentation for the project
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd wordcloud-microservice
   ```

2. **Install dependencies:**
   Make sure you have Python installed, then run:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. **Run the microservice:**
   ```
   python src/app.py
   ```

2. **API Endpoint:**
   The microservice exposes the following endpoint:
   ```
   POST /generate_wordcloud
   ```

   ### Request Parameters:
   - `word_colors`: A JSON object mapping words to their colors (e.g., `{"hello": "rgb(255, 0, 0)", "world": "rgb(0, 255, 0)"}`).
   - `word_frequencies`: A JSON object mapping words to their frequencies (e.g., `{"hello": 10, "world": 5}`).
   - `default_color`: A string representing the default color for words not specified in `word_colors` (e.g., `"rgb(0, 0, 255)"`).

   ### Example Request:
   ```json
   {
       "word_colors": {"hello": "rgb(255, 0, 0)", "world": "rgb(0, 255, 0)"},
       "word_frequencies": {"hello": 10, "world": 5},
       "default_color": "rgb(0, 0, 255)"
   }
   ```

3. **Response:**
   The response will be a PNG image of the generated word cloud.


4. **Docker:**
   `docker build -t wcloud .`
   
   `docker run -p 8080:8080 -d wcloud`

## License

This project is licensed under the MIT License. See the LICENSE file for details.
