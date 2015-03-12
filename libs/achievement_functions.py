#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sublime
import sublime_plugin

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
