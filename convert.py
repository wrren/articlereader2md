import os
import sys
import sqlite3
from lxml.html import parse
from markdownify import markdownify
from pathvalidate import sanitize_filename

def usage():
  print("Usage:")
  print("convert.py INPUT-DIRECTORY OUTPUT-DIRECTORY")
  exit(1)

def read_database(filename):
  articles = []
  conn = sqlite3.connect(filename)
  c = conn.cursor()
  for row in c.execute("SELECT title, date, folders FROM articles"):
    articles.append(row)

  return articles

def read_html_file(path, articles):
  file = open(path, encoding="utf8")
  page = parse(file)
  title = page.find("//title").text
  file.close()
  category = None
  if title is not None:
    for article in articles:
      if article[0] is not None and article[0].strip() == title.strip():
        category = article[2]
  
  file = open(path, encoding="utf8")
  return (title, category, file.read())

def write_markdown(title, category, html, output_directory):
  markdown = markdownify(html)
  output_path = os.path.join(output_directory, sanitize_filename(title + ".md").strip())
  if category is not None:
    if not os.path.isdir(os.path.join(output_directory, category)):
      os.makedirs(os.path.join(output_directory, category), exist_ok=True)
    output_path = os.path.join(output_directory, category, sanitize_filename(title + ".md").strip())
  
  file = open(output_path, "w", encoding="utf8")
  file.write(markdown)
  file.close()

if __name__ == '__main__':
  if len(sys.argv) < 3:
    usage()

  input_directory   = sys.argv[1]
  output_directory  = sys.argv[2]
  db_path           = os.path.join(input_directory, "databases", "ArticleReader.db")
  files_path        = os.path.join(input_directory, "files")
  markdown_files    = []
  articles          = []

  if os.path.isfile(db_path):
    articles = read_database(db_path)
    print("Read {0} article entries from database {1}".format(len(articles), db_path))
  else:
    print("Failed to find database file ", db_path)
    usage()
  
  if os.path.isdir(files_path):
    for subdir, dirs, files in os.walk(files_path):
      for filename in files:
        if filename == "html":
          filepath = os.path.join(subdir, filename)
          (title, category, html) = read_html_file(filepath, articles)
          print("Read article {0} with category {1}, converting to markdown...".format(title, category))
          write_markdown(title, category, html, output_directory)

  else:
    print("Failed to find HTML files directory ", files_path)
    usage()
          
