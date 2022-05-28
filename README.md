# Sankaku Complex Tag Implications

This is a JSON dump of tag implications from Sankaku Channel.

See [implications.json](implications.json).

There's also a visualization is in [implications.svg](implications.svg) file. It's not perfect, but it's better than nothing.


## Making implications.json from Sankaku Complex's data

Configure authentication:

1. Go to https://beta.sankakucomplex.com/tag_implications
2. Open developer tools of your browser (F12)
3. Go to the "Network" tab and reload the page
4. Find the POST request to the GraphQL endpoint
5. Find the "authorization" request header and copy the value after "Bearer "
6. Copy `config.json.example` to `config.json`
7. Edit `config.json` and paste the auth token you've copied earlier there.

Set up the environment:

```bash
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

Get the implications:

```bash
python get_implications.py
```

The implications will be written to `implications.json` file.


## Updating the visualization

```bash
python generate_dot.py > implications.dot && dot -Tsvg implications.dot -o implications.svg
```
