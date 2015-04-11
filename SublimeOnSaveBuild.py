import sublime
import sublime_plugin
import re


class SublimeOnSaveBuild(sublime_plugin.EventListener):
    def on_post_save(self, view):
        global_settings = sublime.load_settings(self.__class__.__name__+'.sublime-settings')
        view_settings = view.settings()
        cur_window = view.window()

        # See if we should build. A project level build_on_save setting
        # takes precedence. To be backward compatible, we assume the global
        # build_on_save to be true if not defined.
        build_on_save = view_settings.get('build_on_save', global_settings.get('build_on_save', True))
        filename_filter = view_settings.get('filename_filter', global_settings.get('filename_filter', '.*'))
        verbose = view_settings.get('verbose', global_settings.get('verbose', False))

        # check if it is a project and supports building...
        if build_on_save and cur_window.project_data() and re.search(filename_filter, view.file_name()):
            if verbose:
                print('Save detected, running build.')
            cur_window.run_command('build')