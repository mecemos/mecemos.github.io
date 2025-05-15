import os
from datetime import datetime

POSTS_DIR = 'poemario_txt'
OUTPUT_DIR = 'poemario'
TEMPLATE_PATH = 'plantillas/poema_plantilla.html'

def parse_post(file_path):
    with open(file_path, encoding='utf-8') as f:
        lines = f.readlines()

    metadata = {'title': '', 'date': '', 'comment': '', 'author':'', 'first_line':''}
    content_lines = []
    for line in lines:
        if line.startswith('title:'):
            metadata['title'] = line[len('title:'):].strip()
        elif line.startswith('date:'):
            metadata['date'] = line[len('date:'):].strip()
        elif line.startswith('author:'):
            metadata['author'] = line[len('author:'):].strip()
        elif line.startswith('comment:'):
            metadata['comment'] = ', '+line[len('comment:'):].strip()
        elif line.strip() == '' and metadata['first_line']=='':
            continue
        else:
            content_lines.append(line)
            #if this is the first line, add the first line info
            if metadata['first_line']=='':
                metadata['first_line']=line

    content = ''.join(content_lines).strip()
    return metadata, content

def render_template(template_str, metadata, content):
    if metadata['title']=='':
        title_page=metadata['first_line']
    else:
        title_page=metadata['title']
    return (
        template_str
        .replace('{{title_page}}', title_page)
        .replace('{{title}}', metadata['title'])
        .replace('{{author}}', metadata['author'])
        .replace('{{date}}', metadata['date'])
        .replace('{{comment}}', metadata['comment'])
        .replace('{{content}}', content)
    )

def generate():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(TEMPLATE_PATH, encoding='utf-8') as f:
        template = f.read()

    post_links = []

    for filename in sorted(os.listdir(POSTS_DIR)):
        if filename.endswith('.txt'):
            filepath = os.path.join(POSTS_DIR, filename)
            post_id = os.path.splitext(filename)[0]
            metadata, content = parse_post(filepath)

            html = render_template(template, metadata, content)
            out_path = os.path.join(OUTPUT_DIR, f'{post_id}.html')

            with open(out_path, 'w', encoding='utf-8') as out_file:
                out_file.write(html)

            post_links.append((metadata['title'], metadata['date'], metadata['first_line'], f'{post_id}.html'))

    # Generate index.html
    with open(os.path.join(OUTPUT_DIR, 'poemario.html'), 'w', encoding='utf-8') as index_file:
        index_file.write('<!DOCTYPE html><html><head><meta charset="UTF-8"><title>My Blog</title>\n')
        index_file.write('<style>body{background:black;color:white;font-family:monospace;padding:20px;}a{color:#00ffff}</style>\n')
        index_file.write('</head><body><h1>Poemario</h1><ul>\n')

        for title, date, first_line, link in post_links:
            #use first line as title if no title
            if title=='':
                title='<i>'+first_line+'</i>'
            index_file.write(f'<li><a href="{link}">{title}</a> <em>({date})</em></li>\n')

        index_file.write('</ul></body></html>')

if __name__ == '__main__':
    generate()
