import os
import sys
import gtk
import gobject

try:
    import pynotify
except ImportError:
    pynotify = None
    sys.stderr.write('\n\n*** Could not import pynotify. '
        'Make sure it is installed so you can see the notifications ***\n\n\n')


IMAGE_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'images/')
PASS_ICON = os.path.join(IMAGE_DIR, 'green_belt.png')
FAIL_ICON = os.path.join(IMAGE_DIR, 'red_belt.png')

__all__ = ['UserInterface']

class UserInterface(object):

    def __init__(self, timer):
        self.timer = timer
        self.current_status = 0

        self.status_icon = gtk.StatusIcon()
        self.status_icon.set_from_file(PASS_ICON)
        self._create_menu()
        self.status_icon.set_visible(True)

        self.start_timer()

        gobject.timeout_add(1000, self.update_timer)

    def _create_menu(self):
        self.menu = gtk.Menu()

        self.pause_item = gtk.ImageMenuItem(gtk.STOCK_MEDIA_PAUSE)
        self.pause_item.connect('activate', self.pause_timer)

        self.play_item = gtk.ImageMenuItem(gtk.STOCK_MEDIA_PLAY)
        self.play_item.connect('activate', self.start_timer)

        self.quit_item = gtk.ImageMenuItem(gtk.STOCK_QUIT)
        self.quit_item.connect('activate', gtk.main_quit, gtk)

        self.separator = gtk.MenuItem()

        self.menu.append(self.pause_item)
        self.menu.append(self.play_item)
        self.menu.append(self.separator)
        self.menu.append(self.quit_item)

        self.status_icon.connect('popup-menu', self.show_menu, self.menu)

    def show_menu(self, widget, button, time, data):
        data.show_all()
        data.popup(None, None, None, button, time)

    def _warn_time_is_up(self):
        """Shows a dialog warning the pilot that his time is up"""
        dialog = gtk.Dialog('Dojotools', buttons=(gtk.STOCK_OK, 0))
        dialog.set_default_size(180, 120)
        dialog.set_keep_above(True)
        dialog.vbox.pack_start(gtk.Label('Your time is up!'))
        dialog.show_all()
        dialog.run()
        dialog.destroy()

    def _show_command_results(self, status, output):
        """
        Shows the output to the users.

        For now, it will write the output to stdout,
        change the icon depending on the status (green
        if the tests are passing, red otherwise) and,
        if pynotify is installed, show a notification.

        If you use this in Ubuntu, I'm sorry for you.
        Canonical just decided to break libnotify in so
        many ways that it is *impossible* to use it sanely.

        """

        sys.stdout.write(output)

        self.current_status = status

        if self.timer.running:
            self.status_icon.set_from_file(
                PASS_ICON if status == 0 else FAIL_ICON
            )

        if pynotify is not None:
            pynotify.init('dojotools')
            message = pynotify.Notification('Dojotools', output)
            message.attach_to_status_icon(self.status_icon)
            message.set_urgency(
                pynotify.URGENCY_NORMAL if status == 0
                else pynotify.URGENCY_CRITICAL
            )
            message.show()

    def update_timer(self):
        if self.timer.time_left:
            time_str = '%02d:%02d' % (
                (self.timer.time_left / 60),
                (self.timer.time_left % 60)
            )
            self.status_icon.set_tooltip(time_str)
        else:
            self.pause_timer()
            self._warn_time_is_up()
            self.start_timer()

        return True

    def pause_timer(self, widget=None):
        self.status_icon.set_from_stock(gtk.STOCK_MEDIA_PAUSE)
        self.timer.pause()

    def start_timer(self, widget=None):
        self.status_icon.set_from_file(
            PASS_ICON if self.current_status == 0 else FAIL_ICON
        )
        self.timer.start()