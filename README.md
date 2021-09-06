# Markdown to Confluence Converter
Converts markdown language to confluens html/xhtml.

# Usage
First, you need python3. Then install `markdown` library with `pip install markdown`.

Then run the script. First parameter is file name where your markdown source is placed:

```
python3 markdown-to-confluence-converter.py your_markdown_file.md > confluence_xhtml_code.txt
```

Now you got confluence-formatted code in `confluence_xhtml_code.txt` file.

# Example
This README.md coverted with converter:

```
<h1>Markdown to Confluence Converter</h1>
<p>Converts markdown language to confluens html/xhtml.</p>
<h1>Usage</h1>
<p>First, you need python3. Then install <code>markdown</code> library with <code>pip install markdown</code>.</p>
<p>Then run the script. First parameter is file name where your markdown source is placed:</p>
<p><ac:structured-macro ac:name="code"><ac:plain-text-body><![CDATA[python3 markdown-to-confluence-converter.py your_markdown_file.md > confluence_xhtml_code.txt
]]></ac:plain-text-body></ac:structured-macro></p>
<p>Now you got confluence-formatted code in <code>confluence_xhtml_code.txt</code> file.</p>
```
