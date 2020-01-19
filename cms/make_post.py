import csv
import datetime
import os

# Default directory paths
BLOGS_DIR = '../blogs'
MARKDOWN_DIR = '../blogs/markdown'

# Default file paths
ARTICLE_TEMPLATE = 'article-template.html'
LINK_FILE = '../assets/includes/article-list.html'
LINK_TEMPLATE = 'link-template.html'
LOG = 'log.csv'


class Article:
	def __init__(self, title: str, blurb: str, markdown: str):
		self.title = title.strip()
		self.blurb = blurb.strip()
		self.markdown = markdown.strip()

		self.date = datetime.datetime.now()
		self.html = self.html_to_markdown(markdown)
		self.html = self.html_beautify(self.html)
		self.length, self.read_time = self.calc_length(markdown)

		self.post_id = self.gen_id(LOG)
		self.filename = self.gen_filename(title)

	def calc_length(self, markdown_content: str) -> int, int:
		"""
		Returns word count and time in minutes to read content
		"""
		word_count = len(markdown_content.split(' '))
		read_time = round(word_count/200)

		if read_time == 0:
			read_time = 1

		return word_count, read_time

	def html_beautify(self, html: str) -> str:
		"""
		Takes in HTML and returns beautified HTML
		"""
		pass
	
	def gen_filename(self, title: str) -> str:
		"""
		Takes title and creates a valid filename
		"""
		title = title.lower().replace(' ', '-')

	def gen_id(self, log_path: str) -> int:
		"""
		Finds ID number of last post in log and increments by one
		"""
		pass

	def markdown_to_html(self, markdown: str) -> str:
		"""
		Converts markdown content to HTML
		"""
		pass

	def write_markdown(self, dir_path: str) -> None:
		"""
		Writes article's markdown content to markdown directory
		"""
		pass

	def write_article(self, template_path: str, dir_path: str) -> None:
		"""
		Creates new HTML file for article and writes to blogs directory
		"""
		pass

	def write_log(self, file_path: str) -> None:
		"""
		Writes article metadata to CSV log file
		"""
		pass

	def write_link(self, template_path: str, file_path: str) -> None:
		"""
		Writes new article link/blurb entry to HTML article list file
		"""
		pass


def yes_no(message='') -> bool:
	"""
	Returns True if choice is 'y' or 'yes', False otherwise
	"""
	choice = input(message)

	if choice.strip().lower() in ('y', 'yes'):
		return True
	return False


def confirmed_input(message='') -> str:
	"""
	Prompts user to confirm text is their desired input
	"""
	text = input(message)
	confirm = input('Are you sure? (y/n): ')

	if not confirm:
		return confirm_input(message)
	return text


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

    text = '\n'.join(lines)
    print(text.strip() + '\n')
    confirm = yes_no('Confirm input (y/n): ')

    if not confirm:
        return markdown_input(message)
    return text


def main():
	"""	
	Updates blog with new post content
	"""
	if yes_no('Create a new blog post? (y/n): '):
		title = confirmed_input('Enter title: ')
		blurb = confirmed_input('Enter blurb: ')
		content = markdown_input('Enter markdown content below:')
		
		post = Article(title, blurb, content)
		post.write_markdown(MARKDOWN_DIR)
		post.write_article(BLOGS_DIR)
		post.write_link(LINK_FILE)
		post.write_log(LOG)

	print('Done')


if __name__ == "__main__":
    main()
