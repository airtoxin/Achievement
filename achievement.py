import sublime
import sublime_plugin
import json

def achievement_dialog(message):
    message = "YOU GOT A NEW ACHIEVEMENT\n\n" + message
    sublime.message_dialog(message)

class AutoRunner(sublime_plugin.EventListener):
    def on_post_save_async(self, view):
        setting = sublime.load_settings("achievement.sublime-settings")
        count = setting.get("save_count") + 1
        self.count_achievement_function("save_count", count, (1,), "Hello save world!")
        self.count_achievement_function("save_count", count, (10, 100, 300, 500, 1000, 10000, 100000), "Save {num} times!")
        self.count_achievement_function("save_count", count, (99999999,), "Oversave!!!")
        setting.set("save_count", count)
        sublime.save_settings("achievement.sublime-settings")

    def on_load_async(self, view):
        setting = sublime.load_settings("achievement.sublime-settings")
        count = setting.get("load_count") + 1
        self.count_achievement_function("load_count", count, (1,), "Hello load world!")
        self.count_achievement_function("load_count", count, (10, 100, 300, 500, 1000, 10000, 100000), "Soad {num} times!")
        self.count_achievement_function("load_count", count, (99999999,), "Overload!!!")
        setting.set("load_count", count)
        sublime.save_settings("achievement.sublime-settings")

    def count_achievement_function(self, setting_name, count, achieving_counts, message):
        u"""
        setting_name(str): 'load_count'
        achieving_counts(int list): (1, 10, 100, 5000, 1000)
        message(str): 'save {num} times!'
            message can contain integer number{num}
        """
        if count in achieving_counts:
            message = message.format(num=count)
            achievement_dialog(message)
            unlocked_settings = sublime.load_settings("unlocked.sublime-settings")
            unlocked_titles = unlocked_settings.get("unlocked_titles", [])
            if setting_name in unlocked_titles:
                c_setting = unlocked_settings.get(setting_name, [])
                c_setting.append(message)
                unlocked_settings.set(setting_name, c_setting)
            else:
                unlocked_titles.append(setting_name)
                unlocked_settings.set("unlocked_titles", unlocked_titles)
                unlocked_settings.set(setting_name, [message])
            sublime.save_settings("unlocked.sublime-settings")


class ViewAchievementCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        w = self.view.window()
        achievement_window = w.new_file()
        # write unlocked achievement
        unlocked_settings = sublime.load_settings("unlocked.sublime-settings")
        unlocked_titles = unlocked_settings.get("unlocked_titles", [])
        for unlocked_title in sorted(unlocked_titles):
            for unlock in reversed(sorted(unlocked_settings.get(unlocked_title, []))):
                line = "*\t{unlock}\n".format(unlock=unlock)
                achievement_window.insert(edit, 0, line)

            line = "\n+=+=+=+=+=+=+=+ {unlocked_title} +=+=+=+=+=+=+=+\n".format(unlocked_title=unlocked_title)
            achievement_window.insert(edit, 0, line)

        message = "*=*=*=*=*=*=*=* UNLOCKED ACHIEVEMENTS *=*=*=*=*=*=*=*\n"
        achievement_window.insert(edit, 0, message)
