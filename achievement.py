import sublime
import sublime_plugin
import json

class AutoRunner(sublime_plugin.EventListener):
    def on_post_save(self, view):
        self._count_save()

    def _count_save(self):
        setting = sublime.load_settings("achievement.sublime-settings")
        save_count = setting.get("save_count")
        save_count += 1
        self._check_save_achievement(save_count)
        setting.set("save_count", save_count)
        sublime.save_settings("achievement.sublime-settings")

    def _check_save_achievement(self, save_count):
        print(save_count)
        if save_count in range(1000): #(1, 10, 100, 300, 500, 1000):
            message = "save " + str(save_count) + " times!"
            sublime.message_dialog(message)
            unlocked_achievement = sublime.load_settings("unlocked.sublime-settings")
            unlocked = unlocked_achievement.get("unlocked")
            unlocked.append(message)
            unlocked_achievement.set("unlocked", unlocked)
            sublime.save_settings("unlocked.sublime-settings")


class ViewAchievementCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        w = self.view.window()
        achievement_window = w.new_file()
        # write unlocked achievement
        unlocked = sublime.load_settings("unlocked.sublime-settings").get("unlocked")
        for lock in reversed(unlocked):
            line = "*\t" + lock + "\n"
            achievement_window.insert(edit, 0, line)

        message = "*=*=*=*=*=*=*=* UNLOCKED ACHIEVEMENTS *=*=*=*=*=*=*=*\n"
        achievement_window.insert(edit, 0, message)