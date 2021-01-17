# ArticleReader2MD

Converts an ArticleReader app data export into a structured directory containing markdown files.

## Usage

```shell
pipenv shell
python convert.py INPUT-DIRECTORY OUTPUT-DIRECTORY
```

Where `INPUT-DIRECTORY` is the app data directory exported from ArticleReader and `OUTPUT-DIRECTORY` is the directory
to which converted files and category directories should be written.