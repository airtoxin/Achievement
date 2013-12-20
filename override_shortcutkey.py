#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sublime
import sublime_plugin
import threading
import sys
sys.path.append("/".join(__file__.split("/")[:-1]))
from achievement_functions import achievement_dialog, achievement_function, count_achievement_function


class OverrideCutCommand(sublime_plugin.TextCommand):
    u""" ⌘+x """
    def run(self, edit):
        self.view.run_command("cut")
        thread = threading.Thread(target=self._command_thread)
        thread.setDaemon(True)
        thread.start()

    def _command_thread(self):
        setting = sublime.load_settings("achievement.sublime-settings")

        # cut_count achievement
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

        # copy_count achievement
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
        # paste_count achievement
        count = setting.get("paste_count", 0) + 1
        count_achievement_function("paste_count", count, (1,), "Paste")
        count_achievement_function("paste_count", count, (10, 100, 300, 500, 1000, 10000, 100000), "Paste {num} times!")
        count_achievement_function("paste_count", count, (99999999,), "Painter")
        setting.set("paste_count", count)

        sublime.save_settings("achievement.sublime-settings")

    def _count_paste_size_thread(self):
        # pasting achievement
        setting_name = "pasting"
        message = ""
        paste_size = len(sublime.get_clipboard(1073741824)) # if character size over 1073741824(1GB), return 0
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


class OverrideSelectAllCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        selection = self.view.sel()
        selection.add(sublime.Region(0, self.view.size()))
        thread = threading.Thread(target=self._override_select_all_command_thread)
        thread.setDaemon(True)
        thread.start()

    def _override_select_all_command_thread(self):
        setting = sublime.load_settings("achievement.sublime-settings")

        # select_all_count achievement
        setting_name = "select_all_count"
        count = setting.get(setting_name, 0) + 1
        count_achievement_function(setting_name, count, (1,), "Whole selection")
        count_achievement_function(setting_name, count, (10, 100, 300, 500, 1000, 10000, 100000), "Select all {num} times!")
        count_achievement_function(setting_name, count, (99999999,), "ALL")
        setting.set(setting_name, count)

        # selectiong_characters_size achievement
        setting_name = "selectiong_characters_size"
        message = ""
        size = self.view.size()
        if size == 1:
            message = "Minimal file"
            achievement_function(setting_name, message)
        if size == 666:
            message = "EVILMAN"
            achievement_function(setting_name, message)
        if size >= 104857600:
            message = "Over 100MB selection"
            achievement_function(setting_name, message)
        if size >= 314572800:
            message = "Over 300MB selection"
            achievement_function(setting_name, message)
        if size >= 524288000:
            message = "Over 500MB selection"
            achievement_function(setting_name, message)
        if size >= 1073741824:
            message = "Over 1GB selection"
            achievement_function(setting_name, message)
        if size >= 10737418240:
            message = "OMG!! Over 10GB selection!!"
            achievement_function(setting_name, message)
        if size >= 1099511627776:
            message = "!!!!!!UNBELIEVABLE!!!Over!1TB!selection!!!!!!!!!"
            achievement_function(setting_name, message)

        sublime.save_settings("achievement.sublime-settings")