aotd-graph-d3
=============

a d3.js based interactive visualization for "album of the day" selections

basically an improved version of [aotd-graph](https://github.com/thomasgilgenast/aotd-graph)

Quick start
-----------

1. Clone this repository

        $ git clone https://github.com/thomasgilgenast/aotd-graph-d3
        $ cd aotd-graph-v3
        
2. Prepare a Python 3.5 virtualenv

        $ virtualenv venv
        $ source venv/bin/activate

3. Install Python dependencies

        $ pip install -r requirements.txt
        
4. Scrape AOTD data from Google Docs and graph data from YouTube

        $ python scrape.py

5. Load `index.html` in a development webserver (must serve `graph.json`)
