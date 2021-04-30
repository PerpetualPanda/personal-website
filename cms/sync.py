from bs4 import BeautifulSoup
import markdown
import os
import re


# CMS default locations
MARKDOWN_DIR = './markdown'
MEDIA_DIR = './media'
ARTICLE_TEMPLATE = './templates/article-template.html'
LINK_TEMPLATE = './templates/link-template.html'

# Main site default locations
POSTS_DIR = '../posts'
LINKS_FILE = '../posts/article-list.id{PID}.html'
BLOG_FILE = '../blog.html'


def prettify():
    """Modify the BeautifulSoup prettify function to indent by 4"""

    orig_prettify = BeautifulSoup.prettify
    r = re.compile(r'^(\s*)', re.MULTILINE)

    # Modify BeautifulSoup.prettify function to 4 space indents
    def helper(self, encoding=None, formatter='minimal', indent_width=4):
        return r.sub(r'\1' * indent_width, orig_prettify(self, encoding, formatter))

    return helper


def generate_article_html(article, template):
    """Takes in article dictionary and html template string, returns html page"""

    subtitle = article['author'] + ' | ' + \
               article['date'] + ' | ' + \
               str(round(article['wordcount'] / 200)) + \
               ' Minute Read | '

    page = template.format(
        ARTICLE_TAB_TITLE = article['title'] + ' - ' + article['author'],
        ARTICLE_TITLE = article['title'],
        ARTICLE_SUBTITLE = subtitle,
        ARTICLE_CONTENT = markdown.markdown(article['content'], extensions=['pymdownx.superfences']),
        FEATURED_IMAGE_SRC = article['image']
    )

    return page


def generate_link_html(article, template, id_num):
    """Takes in article dictionary, html template string and id number; returns html link entry"""

    return template.format(
        ID_NUMBER = id_num,
        POST_LINK = os.path.join(POSTS_DIR, article['permalink'] + '-id' + str(id_num)),
        POST_TITLE = article['title'],
        POST_DATE = article['date'],
        POST_BLURB = article['blurb']
    )


def read_markdown(markdown_file):
    """Read a markdown file into a dictionary"""

    with open(markdown_file) as md:
        raw = md.read().strip()

    pattern = r'title:(.+)\nauthor:(.+)\ndate:(.+)\nimage:(.+?)\nblurb:(.+)\npermalink:(.+)\n((\s|.)+)'
    matches = re.match(pattern, raw)

    assert matches, 'A post is improperly formatted: ' + markdown_file

    content = matches.group(7).strip()
    wordcount = len(content.split())

    return {
        'title': matches.group(1).strip(),
        'author': matches.group(2).strip(),
        'date': matches.group(3).strip(),
        'image': matches.group(4).strip(),
        'blurb': matches.group(5).strip(),
        'permalink': matches.group(6).strip(),
        'content': content,
        'wordcount': wordcount
    }


def convert_date(article):
    """Convert date in the form Day Month, Year to sortable Year Month Day"""

    mappings = {
        'january': 1,
        'febuary': 2,
        'march': 3,
        'april': 4,
        'may': 5,
        'june': 6,
        'july': 7,
        'august': 8,
        'september': 9, 
        'october': 10,
        'november': 11,
        'december': 12
    }

    date = article['date']

    m = re.match(r'([A-Za-z]+)\s*(\d)+,\s*(\d)+', date)
    assert m, 'Article has malformed date: ' + str(article)

    return int(m.group(3)), mappings[m.group(1).lower()], int(m.group(2))


def clear_posts():
    """Deletes existing html files in posts directory"""

    for f in os.listdir(POSTS_DIR):
        if f.endswith(".html"):
            os.remove(os.path.join(POSTS_DIR, f))


def write_article(text, filename):
    """Writes articles as html files"""

    with open(filename, mode='w') as f:
        f.write(text)


def write_links(text, id_num):
    """Writes links to article list"""

    filename = LINKS_FILE.format(PID=id_num)
    with open(filename, mode='w') as f:
        f.write(text)


def update_blogpage(id_num):
    """Updates BLOG_FILE to point to new article list"""

    with open(BLOG_FILE, mode='r') as f:
        parsed_html = BeautifulSoup(f.read(), features='html.parser')

    article_list_div = parsed_html.find(id='article-list')
    stop = article_list_div['include-html'].find('.id')
    article_list_div['include-html'] = article_list_div['include-html'][:stop] + '.id{0}.html'.format(id_num)

    with open(BLOG_FILE, mode='w') as bp:
        bp.write(parsed_html.prettify())


def sync_posts():
    """Sync the current article list with the markdown files"""

    with open(ARTICLE_TEMPLATE) as f:
        article_template = f.read()

    with open(LINK_TEMPLATE) as f:
        link_template = f.read()

    print('\nIndexing markdown files...')
    article_names = [os.path.join(MARKDOWN_DIR, f) for f in os.listdir(MARKDOWN_DIR) if f.endswith('.md')]

    print('Reading file contents...')
    articles = [read_markdown(file) for file in article_names]

    print('Assigning IDs by date...')
    ordered_by_date = sorted(articles, key=lambda a: convert_date(a))

    print('\nSyncing...')

    articlelist = []
    clear_posts()
    i = 0

    for i, a in enumerate(ordered_by_date):
        print('  Generating Article (ID #{0}): {1}...'.format(i, a['title']))
        article_html = generate_article_html(a, article_template)
        link_html = generate_link_html(a, link_template, i)

        write_article(article_html, os.path.join(POSTS_DIR, '{0}-id{1}.html'.format(a['permalink'], i)))
        articlelist.insert(0, link_html)

    print('\nUpdating article listing...')
    write_links('\n\n'.join(articlelist), i)
    update_blogpage(i)

    print('Done.')


if __name__ == '__main__':
    BeautifulSoup.prettify = prettify()
    sync_posts()
