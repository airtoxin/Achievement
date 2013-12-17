import sublime, sublime_plugin

class AutoRunner(sublime_plugin.EventListener):
    def on_post_save(self, view):
        setting = sublime.load_settings("achievement.sublime-settings")
        num_save = setting.get("num_save")
        sublime.message_dialog(str(num_save))
        num_save += 1
        setting.set("num_save", num_save)
        sublime.save_settings("achievement.sublime-settings")
