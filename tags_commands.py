from .todoflow.todoflow import textutils
import sublime
import sublime_plugin


class ToggleDoneCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            self.run_on_line(edit, self.view.full_line(region))

    def run_on_line(self, edit, line_reqion):
        line = self.view.substr(line_reqion).rstrip()
        replacement = self.transform_line(line) + '\n'
        self.view.replace(edit, line_reqion, replacement)

    def transform_line(self, line):

        if textutils.has_tag(line, 'done'):
            return textutils.remove_tag(line, 'done')
        else:
            import datetime
            settings = sublime.load_settings('SublimeTodoflow.sublime-settings')
            tags_to_remove_one_done = settings.get('tags_to_remove_one_done')
            for tag in tags_to_remove_one_done:
                line = textutils.remove_tag(line, tag)
            line = textutils.add_tag(
                line, 'done', datetime.datetime.now().strftime('%F %R')
            )
            return line
