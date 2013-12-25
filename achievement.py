#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sublime
import sublime_plugin
import sys
sys.path.append("/".join(__file__.split("/")[:-1]))
from override_shortcutkey import *
from achievement_functions import achievement_dialog, achievement_function, count_achievement_function


class EventAchievementChecker(sublime_plugin.EventListener):
    def on_post_save_async(self, view):
        setting = sublime.load_settings("achievement.sublime-settings")

        # save_count achievement
        setting_name = "save_count"
        count = setting.get(setting_name, 0) + 1
        self.count_achievement_function(setting_name, count, (1,), "Hello Save World!")
        self.count_achievement_function(setting_name, count, (10, 100, 300, 500, 1000, 10000, 100000), "Save {num} times!")
        self.count_achievement_function(setting_name, count, (99999999,), "Oversave!!! (Save 99999999 times!!!)")
        setting.set(setting_name, count)

        # filename achievement
        setting_name = "filename"
        filename = view.file_name().split("/")[-1].lower()
        if "hoge" in filename:
            message = "new file contains 'hoge' in filename"
            achievement_function(setting_name, message)
        if "fuga" in filename:
            message = "new file contains 'fuga' in filename"
            achievement_function(setting_name, message)
        if "piyo" in filename:
            message = "new file contains 'piyo' in filename"
            achievement_function(setting_name, message)
        if "foo" in filename:
            message = "new file contains 'foo' in filename"
            achievement_function(setting_name, message)
        if "baa" in filename:
            message = "new file contains 'bar' in filename"
            achievement_function(setting_name, message)
        if "baz" in filename:
            message = "new file contains 'baz' in filename"
            achievement_function(setting_name, message)
        if "xyzzy" in filename:
            message = "new file contains 'xyzzy' in filename"
            achievement_function(setting_name, message)
        if "the answer to the ultimate question of life, the universe, and everything" == filename:
            setting_name = "easter_egg"
            message = "42"
            achievement_function(setting_name, message)

        # file_type achievement
        setting = self._file_type_achievement(view, setting)

        # easter_egg
        if view.settings().get("font_size", 0) >= 50:
            setting_name = "easter_egg"
            message = "Eyes are bad? (Font size greater than 50)"
            achievement_function(setting_name, message)

        sublime.save_settings("achievement.sublime-settings")

    def on_load_async(self, view):
        setting = sublime.load_settings("achievement.sublime-settings")

        # load_count achievement
        count = setting.get("load_count", 0) + 1
        self.count_achievement_function("load_count", count, (1,), "Helload World!")
        self.count_achievement_function("load_count", count, (10, 100, 300, 500, 1000, 10000, 100000), "Load {num} times!")
        self.count_achievement_function("load_count", count, (99999999,), "Overload!!!")
        setting.set("load_count", count)

        # file_type achievement
        setting = self._file_type_achievement(view, setting)

        sublime.save_settings("achievement.sublime-settings")

    def on_new_async(self, view):
        setting = sublime.load_settings("achievement.sublime-settings")

        # new_file_count achievement
        count = setting.get("new_file_count", 0) + 1
        self.count_achievement_function("new_file_count", count, (1,), "Hello World!")
        self.count_achievement_function("new_file_count", count, (10, 100, 300, 500, 1000, 10000, 100000), "Create new file {num} times!")
        self.count_achievement_function("new_file_count", count, (99999999,), "THE MAKER")
        setting.set("new_file_count", count)

        sublime.save_settings("achievement.sublime-settings")

    def on_clone_async(self, view):
        setting = sublime.load_settings("achievement.sublime-settings")

        # clone_file_count achievement
        count = setting.get("clone_file_count", 0) + 1
        self.count_achievement_function("clone_file_count", count, (1,), "Duplicate Window!")
        self.count_achievement_function("clone_file_count", count, (10, 100, 300, 500, 1000, 10000, 100000), "Duplicate file {num} times!")
        self.count_achievement_function("clone_file_count", count, (99999999,), "Cloned Human")
        setting.set("clone_file_count", count)

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

    def on_selection_modified_async(self, view):
        count_achievement_function("selector_count", len(view.sel()), (2,), "multi selector!")
        count_achievement_function("selector_count", len(view.sel()), (15, 30, 50, 100), "select {num} place one time")
        count_achievement_function("selector_count", len(view.sel()), (200,), "THE SELECTOR")

    def on_text_command(self, view, command_name, args):
        # print("TEXT")
        # print(view, command_name, args)
        thread = threading.Thread(target=self._on_text_command_achievement_thread, args=(view, command_name, args))
        thread.setDaemon(True)
        thread.start()

    def _on_text_command_achievement_thread(self, view, command_name, args):

        if command_name == "drag_select":
            # easter egg achievement
            if args["event"]["x"] < 10 and args["event"]["y"] < 10:
                setting_name = "easter_egg"
                message = "click corner x < 10, y < 10"
                achievement_function(setting_name, message)
        elif command_name == "view_achievement":
            # view_achievement_count achievement
            setting = sublime.load_settings("achievement.sublime-settings")
            count = setting.get("view_achievement_count", 0) + 1
            count_achievement_function("view_achievement_count", count, (1,), "Checking!")
            count_achievement_function("view_achievement_count", count, (10, 100, 300, 500, 1000, 10000, 100000), "View achievements {num} times!")
            count_achievement_function("view_achievement_count", count, (99999999,), "Loiterer")
            setting.set("view_achievement_count", count)
            sublime.save_settings("achievement.sublime-settings")

    def on_window_command(self, window, command_name, args):
        pass
        # print("WINDOW")
        # print(window, command_name, args)
    def on_query_context(view, key, operator, operand, match_all):
        pass
        # print("QUERY_CONTEXT")
        # print(key, operator, operand, match_all)

    def _file_type_achievement(self, view, setting):
        # file_type achievement
        setting_name = "file_type"
        current_syntax = view.settings().get("syntax")
        syntaxes = setting.get(setting_name, [])
        if current_syntax not in syntaxes:
            syntaxes.append(current_syntax)
            setting.set(setting_name, syntaxes)
            if len(syntaxes) == 10:
                message = "Multilingual (Use 10 kinds of language syntax)"
                achievement_function(setting_name, message)
            elif len(syntaxes) == 20:
                message = "Multibilingual (Use 20 kinds of language syntax)"
                achievement_function(setting_name, message)
            elif len(syntaxes) == 30:
                message = "Multitrilingual (Use 30 kinds of language syntax)"
                achievement_function(setting_name, message)
            elif len(syntaxes) == 40:
                message = "Multiquadrilingual (Use 40 kinds of language syntax)"
                achievement_function(setting_name, message)
            elif len(syntaxes) >= 50:
                message = "THE TRANSLATOR (Over 50 language syntaxes used)"
                achievement_function(setting_name, message)
        return setting


class ViewAchievementCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        size = 50
        w = self.view.window()
        achievement_window = w.new_file()
        # write unlocked achievement
        unlocked_settings = sublime.load_settings("unlocked.sublime-settings")
        unlocked_titles = unlocked_settings.get("unlocked_titles", [])
        for unlocked_title in sorted(unlocked_titles):
            for unlock in reversed(unlocked_settings.get(unlocked_title, [])):
                line = "{unlock}".format(unlock=unlock).center(size) + "\n"
                achievement_window.insert(edit, 0, line)

            line = "\n" + "+=+=+=+=+=+=+=+ {unlocked_title} +=+=+=+=+=+=+=+".format(unlocked_title=unlocked_title).center(size) + "\n"
            achievement_window.insert(edit, 0, line)

        message = "*=*=*=*=*=*=*=* UNLOCKED ACHIEVEMENTS *=*=*=*=*=*=*=*".center(size) + "\n"
        achievement_window.insert(edit, 0, message)
