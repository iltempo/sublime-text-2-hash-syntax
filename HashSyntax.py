import sublime, sublime_plugin, re

# http://www.sublimetext.com/docs/2/api_reference.html#sublime_plugin.TextCommand
# http://net.tutsplus.com/tutorials/python-tutorials/how-to-create-a-sublime-text-2-plugin/

def new_style_hash(matchobj):
    spaces = len(matchobj.group(3) + matchobj.group(4)) - 1
    if spaces < 1:
        spaces = 1

    return "%s%s:%s" % (matchobj.group(1), matchobj.group(2), spaces * ' ')

class HashSyntaxCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if sum(len(region) for region in self.view.sel()) == 0:
            region = sublime.Region(0, self.view.size())
            self.replace_hashes(edit, region)

        for region in self.view.sel():
            if not region.empty():
                self.replace_hashes(edit, region)

    def replace_hashes(self, edit, region):
        # Get the selected text
        s = self.view.substr(region)
        # Transform Ruby 1.8 hash syntax to 1.9
        s = re.sub(r'([^\:])\:([a-zA-Z_0-9]*)(\s*)=\>(\s*)', new_style_hash, s)
        # Replace the selection with transformed text
        self.view.replace(edit, region, s)
