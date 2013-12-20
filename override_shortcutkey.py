#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sublime
import sublime_plugin
import threading

def achievement_dialog(message):
    message = "YOU GOT A NEW ACHIEVEMENT\n\n" + message
    sublime.message_dialog(message)

def count_achievement_function(setting_name, count, achieving_counts, message):
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


class OverrideCutCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command("cut")
        command_thread = OverrideCutCommandThread()
        thread = threading.Thread(target=command_thread)
        thread.setDaemon(True)
        thread.start()

class OverrideCutCommandThread(object):
    def __call__(self):
        setting = sublime.load_settings("achievement.sublime-settings")
        count = setting.get("cut_count", 0) + 1
        count_achievement_function("cut_count", count, (1,), "Scissors!")
        count_achievement_function("cut_count", count, (10, 100, 300, 500, 1000, 10000, 100000), "Cut {num} times!")
        count_achievement_function("cut_count", count, (99999999,), "Jack the Ripper")
        setting.set("cut_count", count)
        sublime.save_settings("achievement.sublime-settings")


class OverrideCopyCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command("copy")
        command_thread = OverrideCopyCommandThread()
        thread = threading.Thread(target=command_thread)
        thread.setDaemon(True)
        thread.start()

class OverrideCopyCommandThread(object):
    def __call__(self):
        setting = sublime.load_settings("achievement.sublime-settings")
        count = setting.get("copy_count", 0) + 1
        count_achievement_function("copy_count", count, (1,), "Copy Machine!")
        count_achievement_function("copy_count", count, (10, 100, 300, 500, 1000, 10000, 100000), "Copy {num} times!")
        count_achievement_function("copy_count", count, (99999999,), "Multiverse")
        setting.set("copy_count", count)
        sublime.save_settings("achievement.sublime-settings")


class OverridePasteCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command("paste")
        command_thread = OverridePasteCommandThread()
        thread = threading.Thread(target=command_thread)
        thread.setDaemon(True)
        thread.start()

class OverridePasteCommandThread(object):
    def __call__(self):
        setting = sublime.load_settings("achievement.sublime-settings")
        count = setting.get("paste_count", 0) + 1
        count_achievement_function("paste_count", count, (1,), "Paste")
        count_achievement_function("paste_count", count, (10, 100, 300, 500, 1000, 10000, 100000), "Paste {num} times!")
        count_achievement_function("paste_count", count, (99999999,), "Painter")
        setting.set("paste_count", count)
        sublime.save_settings("achievement.sublime-settings")
