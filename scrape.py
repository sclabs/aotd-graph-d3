import json

from bs4 import BeautifulSoup
import pandas as pd
import requests


DATA_URL = 'https://docs.google.com/spreadsheets/d/1vA8z1uV6LLDmcSYty8toxYGF1ZcYGdnbQoBzuAqb92U/pub?gid=0&single=true&output=csv'
MAX_DEPTH = 2


def explore(vertices, edges, queue, visited):
    # return if the queue is empty
    if not queue:
        return

    # pick a vertex to explore
    v = queue.pop()

    # short circuit if this vertex is already at MAX_DEPTH
    if v['depth'] == MAX_DEPTH:
        return

    # scrape the web
    base_url = 'https://www.youtube.com'
    soup = BeautifulSoup(requests.get(base_url + v['url']).text, 'lxml')

    # iterate over related videos
    for el in soup.findAll('a', {'class': 'content-link'}):
        # if we've been here before, add a new edge
        if el['href'] in visited:
            print('adding edge')
            edges.append({'source': v['url'], 'target': el['href']})
        elif 'album' in el['title'].lower():
            print('adding node to %s' % el['title'].encode('utf-8'))
            child = {
                'url': el['href'],
                'title': el['title'],
                'depth': v['depth'] + 1,
            }
            vertices.append(child)
            edges.append({'source': v['url'], 'target': child['url']})
            queue.append(child)
            visited[child['url']] = child


def main():
    # parse data
    df = pd.read_csv(DATA_URL, parse_dates=[0])

    # set up lists for vertices and edges
    vertices = []
    edges = []

    # set up queue and visited set
    queue = []
    visited = {}

    # populate queue with initial vertices
    for index, row in df.iterrows():
        if row['Link'].startswith('https://www.youtube.com/watch?v='):
            v = {
                'url': row['Link'].split('https://www.youtube.com')[1],
                'title': '%s - %s' % (row['Artist'], row['Album']),
                'submitter': row['Selected by'],
                'date': row['Date'].isoformat(),
                'depth': 0
            }
            vertices.append(v)
            queue.append(v)
            visited[v['url']] = v

    # explore the graph
    while queue:
        explore(vertices, edges, queue, visited)

    # save to disk
    with open('graph.json', 'w', encoding='utf-8') as handle:
        json.dump({'vertices': vertices, 'edges': edges}, handle,
                  ensure_ascii=False)

if __name__ == '__main__':
    main()
