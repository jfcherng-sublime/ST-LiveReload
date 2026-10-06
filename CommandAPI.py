#!/usr/bin/python

import os
import webbrowser

import sublime
import sublime_plugin

from .server.PluginAPI import PluginInterface as Plugin


class LiveReloadTest(sublime_plugin.ApplicationCommand):

    def run(self):
        path = os.path.join(sublime.packages_path(), 'LiveReload', 'web')
        file_name = os.path.join(path, 'test.html')
        webbrowser.open_new_tab("file://" + file_name)


class LiveReloadHelp(sublime_plugin.ApplicationCommand):

    def run(self):
        webbrowser.open_new_tab('https://github.com/alepez/LiveReload-sublimetext3#using'
                                )


class LiveReloadEnablePluginCommand(sublime_plugin.ApplicationCommand):

    def on_done(self, index):
        if index != -1:
            Plugin.togglePlugin(index)

    def run(self):
        sublime.active_window().show_quick_panel(Plugin.listPlugins(),
                self.on_done)
