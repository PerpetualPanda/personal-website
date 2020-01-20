from bs4 import BeautifulSoup
from shutil import copyfile
from typing import List
from typing import Tuple
import csv
import datetime
import markdown2
import os
import re

# Default directory paths
BACKUP_DIR = './backup'
BLOGS_DIR = '../blogs'
BLOGS_LINK = '/blogs'
MARKDOWN_DIR = '../blogs/markdown'
MEDIA_DIR = '../blogs/media'
TEMP_DIR = './tmp'

# Default file names
ARTICLE_TEMPLATE_FN = 'article-template.html'
LINK_FILE_FN = 'article-list.html'
LINK_TEMPLATE_FN = 'link-template.html'
LOG_FN = 'log.csv'

# Default file paths
ARTICLE_TEMPLATE = './templates/' + ARTICLE_TEMPLATE_FN
LINK_FILE = '../assets/includes/' + LINK_FILE_FN
LINK_TEMPLATE = './templates/' + LINK_TEMPLATE_FN
LOG = './' + LOG_FN


class Article:
	def __init__(self, author: str, title: str, blurb: str, markdown: str, media: List[str]):
		self.author = author.strip()
		self.title = title.strip()
		self.blurb = blurb.strip()
		self.markdown = markdown.strip()
		self.media = media

		self.date = datetime.datetime.now()
		self.html = self.markdown_to_html(markdown)
		self.html = self.html_beautify(self.html)
		self.length, self.read_time = self.calc_length(markdown)

		self.post_id = self.gen_id(LOG)
		self.filename = self.gen_filename(title)
		self.link = BLOGS_LINK.rstrip('/') + '/' + self.filename
		self.push_files = []

	def calc_length(self, markdown_content: str) -> Tuple[int]:
		"""Returns word count and time in minutes to read content"""

		word_count = len(markdown_content.split(' '))
		read_time = round(word_count/200)

		if read_time == 0:
			read_time = 1

		return word_count, read_time

	def clear_temp(self) -> None:
		"""Clears temporary directory"""

		files = os.listdir(TEMP_DIR)
		for f in files:
			os.remove(TEMP_DIR.rstrip('/') + '/' + f)

	def html_beautify(self, html: str) -> str:
		"""Takes in HTML and returns beautified HTML"""
		
		orig_prettify = BeautifulSoup.prettify
		r = re.compile(r'^(\s*)', re.MULTILINE)

		def prettify(self, encoding=None, formatter='minimal', indent_width=2):
			return r.sub(r'\1' * indent_width, orig_prettify(self, encoding, formatter))

		BeautifulSoup.prettify = prettify
		
		return BeautifulSoup(html, 'html.parser').prettify()

	def gen_filename(self, title: str) -> str:
		"""Takes title and creates a valid filename"""

		ignore = '-'
		title = title.strip().lower().replace(' ', '-')
		title = re.sub(r'[^\w'+ignore+']', '',title)

		return title + '-id' + str(self.post_id)

	def gen_id(self, log_path: str) -> int:
		"""Finds ID number of last post in log and increments by one"""

		with open(log_path, mode='r') as csv_log:
			reader = list(csv.reader(csv_log))

		if len(reader) > 1:
			return int(reader[1][0]) + 1
		return 1

	def markdown_to_html(self, markdown_content: str) -> str:
		"""Converts markdown content to HTML"""
		return markdown2.markdown(markdown_content)
	
	def push_content(self) -> None:
		"""Moves blog data into proper folders, backs up old files"""

		post_media_dir = MEDIA_DIR.rstrip('/') + '/' + str(self.post_id)
		if not os.path.isdir(post_media_dir) and len(self.media) > 0:
			os.mkdir(post_media_dir)

		for push in self.push_files:
			name = os.path.basename(push[1])

			if os.path.isfile(push[1]):
				os.rename(push[1], BACKUP_DIR.rstrip('/') + '/' + str(self.post_id) + ' BACKUP ' + name)

			os.rename(push[0], push[1])
				

	def write_article(self) -> None:
		"""Creates new HTML file for article and writes to temp directory"""

		filename = self.filename + '.html'
		tab_title = self.author + ' - ' + self.title
		title = self.title
		post_date = self.date.strftime('%B %-dth, %Y')
		subtitle = self.author + '&nbsp; | &nbsp;' + post_date + '&nbsp; | &nbsp;' + str(self.read_time) + ' Minute Read&nbsp; | &nbsp;'
		post_content = self.html

		with open(ARTICLE_TEMPLATE, mode='r') as template:
			content = template.read()
			content = content.replace('ARTICLE_TAB_TITLE', tab_title, 1)
			content = content.replace('ARTICLE_TITLE', title, 1)
			content = content.replace('ARTICLE_SUBTITLE', subtitle, 1)
			content = content.replace('ARTICLE_CONTENT', post_content, 1)
			content = self.html_beautify(content)

		output_path = TEMP_DIR.rstrip('/') + '/' + filename
		with open(output_path, mode='w') as article:
			article.write(content)

		paths = (output_path, BLOGS_DIR.rstrip('/') + '/' + filename)
		self.push_files.append(paths)

	def write_log(self) -> None:
		"""Writes article metadata to CSV at file_path"""

		meta = [str(self.post_id),
				str(self.date),
				self.title,
				str(self.length),
				self.link]

		with open(LOG, mode='r') as csv_log:
			reader = list(csv.reader(csv_log))
			reader.insert(1, meta)
			output_path = TEMP_DIR.rstrip('/') + '/' + LOG_FN

			with open (output_path, mode='w') as output:
				writer = csv.writer(output)
				for line in reader:
					writer.writerow(line)

			paths = (output_path, LOG)
			self.push_files.append(paths)

	def write_link(self) -> None:
		"""Writes new article link/blurb entry to temp directory"""

		filename = 'article-list.html'
		id_num = self.post_id
		title = self.title
		blurb = self.blurb
		post_date = self.date.strftime('%d %b %Y')

		with open(LINK_TEMPLATE, mode='r') as template:
			content = template.read()
			content = content.replace('ID_NUMBER', str(id_num), 1)
			content = content.replace('POST_LINK', self.link, 1)
			content = content.replace('POST_TITLE', title, 1)
			content = content.replace('POST_DATE', post_date, 1)
			content = content.replace('POST_BLURB', blurb, 1)

		with open(LINK_FILE, mode='r') as link_file:
			old_content = link_file.read()
			index = old_content.find('<article')

			if index == -1:
				index = len(old_content)

			new_content = old_content[:index] + content + '\n\n' + old_content[index:]

			output_path = TEMP_DIR.rstrip('/') + '/' + filename
			with open(output_path, mode='w') as new_link_file:
				new_link_file.write(new_content)

		paths = (output_path, LINK_FILE.rstrip('/'))
		self.push_files.append(paths)
	
	def write_markdown(self) -> None:
		"""Writes article's markdown content to temp directory"""
		
		filename = self.filename + '.md'
		output_path = TEMP_DIR.rstrip('/') + '/' + filename

		with open(output_path, mode='w') as md:
			md.write(self.markdown)
			paths = (output_path, MARKDOWN_DIR.rstrip('/') + '/' + filename)
			self.push_files.append(paths)

	def write_media(self) -> None:
		"""Writes all media to temp folder"""

		output_path = TEMP_DIR.rstrip('/')
		for m in self.media:
			name = os.path.basename(m)
			copyfile(m, output_path + '/' + name)

			paths = (output_path + '/' + name, MEDIA_DIR.rstrip('/') + '/' + str(self.post_id) + '/' + name)
			self.push_files.append(paths)


def yes_no(message='') -> bool:
	"""Returns True if choice is 'y' or 'yes', False otherwise"""

	choice = input(message)

	if choice.strip().lower() in ('y', 'yes'):
		return True
	return False


def confirmed_input(message='') -> str:
	"""Prompts user to confirm text is their desired input"""

	text = input(message)
	confirm = yes_no('Are you sure? (y/n): ')

	if confirm:
		return text
	return confirmed_input(message)


def markdown_input(message: str) -> str:
    """Instructs user to enter markdown"""

    print('\nIMPORTANT: Type <ENDFILE> on its own line to specify when your input is finished\n')
    print(message)

    lines = []
    while True:
        line = input()
        if line.strip() != '<ENDFILE>':
            lines.append(line)
        else:
            break

    text = '\n'.join(lines).strip()
    print('\n' + text + '\n')
    confirm = yes_no('Confirm input (y/n): ')

    if not confirm:
        return markdown_input(message)
    return text


def media_input() -> List[str]:
	"""Input file paths to media to be copied"""

	media_paths = []
	if yes_no('Any media (images/video) to upload? (y/n): '):
		more = True
		while more:
			path = confirmed_input('Enter path to media: ').strip()
			name = os.path.basename(path)

			if name in media_paths:
				print('Error, file with same name already exists: ' + name)
			elif os.path.isfile(path):
				media_paths.append(path)
			else:
				print('Error, not a file: ' + path)

			more = yes_no('Upload more? (y/n): ')

	return media_paths

def main():
	"""Updates blog with new post content"""

	if yes_no('\nCreate a new blog post? (y/n): '):
		name = confirmed_input('Enter your name: ').strip()
		title = confirmed_input('Enter title: ').strip()
		blurb = confirmed_input('Enter blurb: ').strip()
		content = markdown_input('Enter markdown content below:').strip()
		media = media_input()

		post = Article(name, title, blurb, content, media)
		post.write_markdown()
		post.write_article()
		post.write_media()
		post.write_link()
		post.write_log()
		
		print('\nConfirmation:\n')
		print('Title:', post.title)
		print('Author:', post.author)
		print('Date:', post.date)
		print('Blurb:', post.blurb)
		print('Media:', post.media)
		print('Length:', str(post.length) + ' words')
		print('Link:', post.link)

		if yes_no('\nDo you wish to push this content? (y/n): '):
			post.push_content()

		post.push_files = []
		post.clear_temp()

	print('\nDone\n')

if __name__ == "__main__":
    main()