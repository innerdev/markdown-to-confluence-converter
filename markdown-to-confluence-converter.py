#/usr/bin/python
# -*- coding: utf-8 -*-

import re
import sys
import markdown
from markdown.extensions.codehilite import CodeHilite, CodeHiliteExtension, parse_hl_lines


CODE_WRAP = '<ac:structured-macro ac:name="code">%s<ac:plain-text-body><![CDATA[%s]]></ac:plain-text-body></ac:structured-macro>'
LANG_TAG = '<ac:parameter ac:name="language">%s</ac:parameter>'


class FencedCodeExtension(markdown.Extension):

    def __init__(self, *args, **kwargs):
        self.config = {'escape': ['True', 'Escape HTMP special chars'],
                       'code_wrap': ['<pre><code%s>%s</code></pre>', 'Code wrapper tag'],
                       'lang_tag': [' class="%s"', 'Code wrapper\'s tag']}
        super(FencedCodeExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        """ Add FencedBlockPreprocessor to the Markdown instance. """
        md.registerExtension(self)
        processor = FencedBlockPreprocessor(md)
        processor.config = self.getConfigs()
        md.preprocessors.add('fenced_code_block',
                             processor,
                             ">normalize_whitespace")


class FencedBlockPreprocessor(markdown.preprocessors.Preprocessor):
    FENCED_BLOCK_RE = re.compile(r'''
(?P<fence>^(?:~{3,}|`{3,}))[ ]*         # Opening ``` or ~~~
(\{?\.?(?P<lang>[a-zA-Z0-9_+-]*))?[ ]*  # Optional {, and lang
# Optional highlight lines, single- or double-quote-delimited
(hl_lines=(?P<quot>"|')(?P<hl_lines>.*?)(?P=quot))?[ ]*
}?[ ]*\n                                # Optional closing }
(?P<code>.*?)(?<=\n)
(?P=fence)[ ]*$''', re.MULTILINE | re.DOTALL | re.VERBOSE)

    def __init__(self, md):
        super(FencedBlockPreprocessor, self).__init__(md)

        self.checked_for_codehilite = False
        self.codehilite_conf = {}

    def run(self, lines):
        """ Match and store Fenced Code Blocks in the HtmlStash. """

        # Check for code hilite extension
        if not self.checked_for_codehilite:
            for ext in self.markdown.registeredExtensions:
                if isinstance(ext, CodeHiliteExtension):
                    self.codehilite_conf = ext.config
                    break

            self.checked_for_codehilite = True

        text = "\n".join(lines)
        while 1:
            m = self.FENCED_BLOCK_RE.search(text)
            if m:
                lang = ''
                if m.group('lang'):
                    lang = self.config['lang_tag'] % m.group('lang')

                # If config is not empty, then the codehighlite extension
                # is enabled, so we call it to highlight the code
                if self.codehilite_conf:
                    highliter = CodeHilite(
                        m.group('code'),
                        linenums=self.codehilite_conf['linenums'][0],
                        guess_lang=self.codehilite_conf['guess_lang'][0],
                        css_class=self.codehilite_conf['css_class'][0],
                        style=self.codehilite_conf['pygments_style'][0],
                        use_pygments=self.codehilite_conf['use_pygments'][0],
                        lang=(m.group('lang') or None),
                        noclasses=self.codehilite_conf['noclasses'][0],
                        hl_lines=parse_hl_lines(m.group('hl_lines'))
                    )

                    code = highliter.hilite()
                else:
                    if self.config['escape']:
                        code = self._escape(m.group('code'))
                    else:
                        code = m.group('code')
                    code = self.config['code_wrap'] % (lang, code)

                placeholder = self.markdown.htmlStash.store(code)
                text = '%s\n%s\n%s' % (text[:m.start()],
                                       placeholder,
                                       text[m.end():])
            else:
                break
        return text.split("\n")

    def _escape(self, txt):
        """ basic html escaping """
        txt = txt.replace('&', '&amp;')
        txt = txt.replace('<', '&lt;')
        txt = txt.replace('>', '&gt;')
        txt = txt.replace('"', '&quot;')
        return txt

if __name__ == "__main__":
    with open(sys.argv[1], "r+") as f:
        md = f.read()
    ext = FencedCodeExtension(escape=False,
                              code_wrap=CODE_WRAP,
                              lang_tag=LANG_TAG)
    html = markdown.markdown(md, extensions=[ext], safe_mode='replace')
    print (html)