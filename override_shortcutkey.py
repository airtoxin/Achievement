#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sublime
import sublime_plugin
import threading

def achievement_dialog(message):
    message = "YOU GOT A NEW ACHIEVEMENT\n\n" + message
    sublime.message_dialog(message)

def achievement_function(setting_name, message):
    u"""
    setting_name(str): 'hogehoge'
    message(str): '!!CONGRATULATION!!'
    """
    if len(message) == 0:
        return
    unlocked_settings = sublime.load_settings("unlocked.sublime-settings")
    unlocked_titles = unlocked_settings.get("unlocked_titles", [])
    if setting_name in unlocked_titles:
        c_setting = unlocked_settings.get(setting_name, [])
        if message in c_setting:
            return
        else:
            c_setting.append(message)
            unlocked_settings.set(setting_name, c_setting)
    else:
        unlocked_titles.append(setting_name)
        unlocked_settings.set("unlocked_titles", unlocked_titles)
        unlocked_settings.set(setting_name, [message])
    sublime.save_settings("unlocked.sublime-settings")
    achievement_dialog(message)

def count_achievement_function(setting_name, count, achieving_counts, message):
    u"""
    setting_name(str): 'load_count'
    achieving_counts(int list): (1, 10, 100, 5000, 1000)
    message(str): 'save {num} times!'
        message can contain integer number{num}
    """
    if count in achieving_counts:
        message = message.format(num=count)
        achievement_function(setting_name, message)


class OverrideCutCommand(sublime_plugin.TextCommand):
    u""" ⌘+x """
    def run(self, edit):
        self.view.run_command("cut")
        thread = threading.Thread(target=self._command_thread)
        thread.setDaemon(True)
        thread.start()

    def _command_thread(self):
        setting = sublime.load_settings("achievement.sublime-settings")
        count = setting.get("cut_count", 0) + 1
        count_achievement_function("cut_count", count, (1,), "Scissors!")
        count_achievement_function("cut_count", count, (10, 100, 300, 500, 1000, 10000, 100000), "Cut {num} times!")
        count_achievement_function("cut_count", count, (99999999,), "Jack the Ripper")
        setting.set("cut_count", count)
        sublime.save_settings("achievement.sublime-settings")


class OverrideCopyCommand(sublime_plugin.TextCommand):
    u""" ⌘+c """
    def run(self, edit):
        self.view.run_command("copy")
        thread = threading.Thread(target=self._command_thread)
        thread.setDaemon(True)
        thread.start()

    def _command_thread(self):
        setting = sublime.load_settings("achievement.sublime-settings")
        count = setting.get("copy_count", 0) + 1
        count_achievement_function("copy_count", count, (1,), "Copy Machine!")
        count_achievement_function("copy_count", count, (10, 100, 300, 500, 1000, 10000, 100000), "Copy {num} times!")
        count_achievement_function("copy_count", count, (99999999,), "Multiverse")
        setting.set("copy_count", count)
        sublime.save_settings("achievement.sublime-settings")


class OverridePasteCommand(sublime_plugin.TextCommand):
    u""" ⌘+v """
    def run(self, edit):
        self.view.run_command("paste")
        paste_command_thread = threading.Thread(target=self._override_paste_command_thread)
        paste_command_thread.setDaemon(True)
        paste_command_thread.start()

        count_paste_size_thread = threading.Thread(target=self._count_paste_size_thread)
        count_paste_size_thread.setDaemon(True)
        count_paste_size_thread.start()

    def _override_paste_command_thread(self):
        setting = sublime.load_settings("achievement.sublime-settings")
        count = setting.get("paste_count", 0) + 1
        count_achievement_function("paste_count", count, (1,), "Paste")
        count_achievement_function("paste_count", count, (10, 100, 300, 500, 1000, 10000, 100000), "Paste {num} times!")
        count_achievement_function("paste_count", count, (99999999,), "Painter")
        setting.set("paste_count", count)
        sublime.save_settings("achievement.sublime-settings")

    def _count_paste_size_thread(self):
        setting_name = "pasting"
        message = ""
        paste_size = len(sublime.get_clipboard(1073741824)) # if character size over 1073741824(1GB), return 0
        print(paste_size)
        if paste_size == 1:
            message = "ant"
        elif paste_size == 0:
            message = "TOO BIG TO PASTE"
        elif paste_size == 1000000000:
            message = "JUST A BILLION CHARACTERS PASTE ONE TIME"
        elif paste_size == 1000000:
            message = "JUST A MILLION CHARACTERS PASTE ONE TIME"
        elif paste_size == 1024:
            message = "JUST A 1024 CHARACTERS PASTE ONE TIME"
        elif paste_size == 65536:
            message = "JUST A 2^(2^(2^2)) CHARACTERS PASTE ONE TIME"
        achievement_function(setting_name, message)
