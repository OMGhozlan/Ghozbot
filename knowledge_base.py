import os

JOKES_FILE = "jokes.txt"
QUOTES_FILE = "quotes_file.txt"
STORIES_FILE = "stories.txt"
UPPER_FILE = "upper_words.txt"

class GhozKB:
    def __init__(self):
		"""
		Knowledge base class

		Args:
			None.

		Returns:
			None.

		Raises:
			None.
		"""	
        self.upper_words = {}
        self.stories = {}
        self.jokes = []
		self.quotes = []

    def load_knbase(self, knbase_dir):
		"""
		Loads knowledge base for the bot

		Args:
			knbase_dir: Folder containing the knowledge base files.

		Returns:
			None.

		Raises:
			None.
		"""
        upper_file_name = os.path.join(knbase_dir, UPPER_FILE)
        stories_file_name = os.path.join(knbase_dir, STORIES_FILE)
        jokes_file_name = os.path.join(knbase_dir, JOKES_FILE)
		quotes_file_name = os.path.join(knbase_dir, QUOTES_FILE)

        with open(upper_file_name, 'r') as upper_f:
            for line in upper_f:
                ln = line.strip()
                if not ln or ln.startswith('#'):
                    continue
                cap_words = ln.split(',')
                for cpw in cap_words:
                    tmp = cpw.strip()
                    self.upper_words[tmp.lower()] = tmp

        with open(stories_file_name, 'r') as stories_f:
            s_name, s_content = '', ''
            for line in stories_f:
                ln = line.strip()
                if not ln or ln.startswith('#'):
                    continue
                if ln.startswith('_NAME:'):
                    if s_name != '' and s_content != '':
                        self.stories[s_name] = s_content
                        s_name, s_content = '', ''
                    s_name = ln[6:].strip().lower()
                elif ln.startswith('_CONTENT:'):
                    s_content = ln[9:].strip()
                else:
                    s_content += ' ' + ln.strip()

            if s_name != '' and s_content != '':  # The last one
                self.stories[s_name] = s_content

        with open(jokes_file_name, 'r') as jokes_f:
            for line in jokes_f:
                ln = line.strip()
                if not ln or ln.startswith('#'):
                    continue
                self.jokes.append(ln)
				
        with open(quotes_file_name, 'r') as quotes_f:
            for line in quotes_f:
                ln = line.strip()
                if not ln or ln.startswith('#'):
                    continue
                self.quotes.append(ln)				