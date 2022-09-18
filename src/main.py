import subprocess
import sys
import json
import os
from datetime import timedelta
sys.path.append('/app')
from timer import *
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, GLib, Adw, Gio

def strfdelta(tdelta, fmt):
    d = {"days": tdelta.days}
    d["hours"], rem = divmod(tdelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    return fmt.format(**d)

class Dialog_settings(Gtk.Dialog):
    def __init__(self, parent, **kwargs):
        super().__init__(use_header_bar=True)
        #self.parent = parent

        self.set_title(title=preferences)
        self.use_header_bar = True
        self.set_modal(modal=True)
        self.connect('response', self.dialog_response)

        # Buttons
        self.add_buttons(
            close, Gtk.ResponseType.CANCEL,
        )

        # Close button response ID
        btn_cancel = self.get_widget_for_response(
            response_id=Gtk.ResponseType.CANCEL,
        )
        btn_cancel.get_style_context().add_class(class_name='destructive-action')
        
        content_area = self.get_content_area()
        content_area.set_orientation(orientation=Gtk.Orientation.VERTICAL)
        content_area.set_spacing(spacing=12)
        content_area.set_margin_top(margin=12)
        content_area.set_margin_end(margin=12)
        content_area.set_margin_bottom(margin=12)
        content_area.set_margin_start(margin=12)
        
        # Spinner size desc
        label = Gtk.Label(xalign=0, yalign=0)
        label.set_markup(spinner + "\n" + spinner_size_desc)
        content_area.append(child=label)
        
        # ComboBox  
        sizes = [
            '5', '10', '15', '20', '25', '30', '35', '40 (%s)' % default, '45', '50', '55', '60', '65', '70', '75', '80'
        ]
        combobox_text = Gtk.ComboBoxText.new()
        for text in sizes:
            combobox_text.append_text(text=text)
        if os.path.exists(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.timer/data/spinner.json'):
            with open(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.timer/data/spinner.json') as p:
                jsonSpinner = json.load(p)
            combobox_s = jsonSpinner["spinner-size"]
            if combobox_s == "5":
                combobox_text.set_active(index_=0)
            elif combobox_s == "10":
                combobox_text.set_active(index_=1)
            elif combobox_s == "15":
                combobox_text.set_active(index_=2)
            elif combobox_s == "20":
                combobox_text.set_active(index_=3)
            elif combobox_s == "25":
                combobox_text.set_active(index_=4)
            elif combobox_s == "30":
                combobox_text.set_active(index_=5)
            elif combobox_s == "35":
                combobox_text.set_active(index_=6)
            elif combobox_s == "40 (%s)" % default:
                combobox_text.set_active(index_=7)
            elif combobox_s == "45":
                combobox_text.set_active(index_=8)
            elif combobox_s == "50":
                combobox_text.set_active(index_=9)
            elif combobox_s == "55":
                combobox_text.set_active(index_=10)
            elif combobox_s == "60":
                combobox_text.set_active(index_=11)
            elif combobox_s == "65":
                combobox_text.set_active(index_=12)
            elif combobox_s == "70":
                combobox_text.set_active(index_=13)
            elif combobox_s == "75":
                combobox_text.set_active(index_=14)
            elif combobox_s == "80":
                combobox_text.set_active(index_=15)
        else:
            combobox_text.set_active(index_=7)
        combobox_text.connect('changed', self.on_combo_box_text_changed)
        content_area.append(child=combobox_text)
        
        # Label about resizable of Window
        label2 = Gtk.Label(xalign=0, yalign=0)
        label2.set_markup("<b>" + resizable_of_window + "</b>")
        content_area.append(child=label2)
        
        # Check button about resizable of Window     
        check_button = Gtk.CheckButton.new_with_label(label=resizable_of_window)
        if os.path.exists(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.timer/data/window.json'):
            with open(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.timer/data/window.json') as r:
                jR = json.load(r)
            resizable = jR["resizable"]
            if resizable == "true":
                check_button.set_active(True)
        check_button.connect('toggled', self.on_check_button_toggled)
        content_area.append(child=check_button)
        
        # Label about theme
        label3 = Gtk.Label(yalign=0, xalign=0)
        label3.set_markup("<b>%s</b>\n%s" % (theme, theme_desc))
        content_area.append(child=label3)
        
        # Dark/light switcher
        switcher = Gtk.CheckButton.new_with_label(label=dark_theme)
        if os.path.exists(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.timer/data/theme.json'):
            with open(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.timer/data/theme.json') as r:
                jR = json.load(r)
            dark = jR["theme"]
            if dark == "dark":
                switcher.set_active(True)
        switcher.connect('toggled', self.on_switcher_toggled)
        content_area.append(child=switcher)
        
        # Label about restart
        label4 = Gtk.Label()
        label4.set_markup(restart_timer_desc)
        content_area.append(child=label4)
        self.show()
    
    # Save app theme configuration
    def on_switcher_toggled(self, switcher):
        if switcher.get_active():
            with open(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.timer/data/theme.json', 'w') as t:
                t.write('{\n "theme": "dark"\n}')
        else:
            with open(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.timer/data/theme.json', 'w') as t:
                t.write('{\n "theme": "system"\n}')
    
    # Save resizable window configuration
    def on_check_button_toggled(self, checkbutton):
        if checkbutton.get_active():
            with open(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.timer/data/window.json', 'w') as w:
                w.write('{\n "resizable": "true"\n}')
        else:
            os.remove(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.timer/data/window.json')
    
    # Save Combobox configuration
    def on_combo_box_text_changed(self, comboboxtext):
        with open(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.timer/data/spinner.json', 'w') as s:
            s.write('{\n "spinner-size": "%s"\n}' % comboboxtext.get_active_text())
    # Close button clicked action
    def dialog_response(self, dialog, response):
        if response == Gtk.ResponseType.CANCEL:
            dialog.close()
            print(preferences_saved)

print(timer_running)
class TimerWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resizable()
        self.application = kwargs.get('application')
        self.style_manager = self.application.get_style_manager()
        self.theme()
        self.set_title(title=timer_title)
        headerbar = Gtk.HeaderBar.new()
        self.set_titlebar(titlebar=headerbar)
        
        # Gtk.Box() layout
        self.mainBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        self.mainBox.set_margin_start(10)
        self.mainBox.set_margin_end(10)
        self.set_child(self.mainBox)
        
        # App menu
        menu_button_model = Gio.Menu()
        menu_button_model.append(preferences, 'app.settings')
        menu_button_model.append(about_app, 'app.about')
        menu_button = Gtk.MenuButton.new()
        menu_button.set_icon_name(icon_name='open-menu-symbolic')
        menu_button.set_menu_model(menu_model=menu_button_model)
        headerbar.pack_end(child=menu_button)
        
        # Spinner
        self.spinner = Gtk.Spinner()
        self.spinner_size()
        self.mainBox.append(self.spinner)
        
        self.label = Gtk.Label()
        self.mainBox.append(self.label)
        
        # Entry
        self.make_timer_box()
        
        # Start timer button
        self.buttonStart = Gtk.Button(label=run_timer)
        self.buttonStart.connect("clicked", self.on_buttonStart_clicked)
        self.button1_style_context = self.buttonStart.get_style_context()
        self.button1_style_context.add_class('suggested-action')
        self.mainBox.append(self.buttonStart)
        
        # Stop timer button
        self.buttonStop = Gtk.Button(label=stop_timer)
        self.buttonStop.set_sensitive(False)
        self.button2_style_context = self.buttonStop.get_style_context()
        self.buttonStop.connect("clicked", self.on_buttonStop_clicked)
        self.mainBox.append(self.buttonStop)

        self.timeout_id = None
        self.connect("destroy", self.on_SpinnerWindow_destroy)
    

    def make_timer_box(self):
        # Load counter.json (config file with time counter values)
        if os.path.exists(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.timer/data/counter.json'):
            with open(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.timer/data/counter.json') as jc:
                jC = json.load(jc)
            hour_e = jC["hour"]
            min_e = jC["minutes"]
            sec_e = jC["seconds"]
        else:
            hour_e = "0"
            min_e = "1"
            sec_e = "0"
        # Layout
        self.timerBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=3)
        self.timerBox.set_margin_start(50)
        self.timerBox.set_margin_end(50)
        # Hour entry and label
        self.hour_entry = Gtk.Entry()
        self.hour_entry.set_text(hour_e)
        self.hour_entry.set_alignment(xalign=1)
        self.timerBox.append(self.hour_entry)

        label = Gtk.Label(label = "h")
        label.set_hexpand(False)
        self.timerBox.append(label)
        # Minute entry and label
        self.minute_entry = Gtk.Entry()
        self.minute_entry.set_text(min_e)
        self.minute_entry.set_alignment(xalign=1)
        self.timerBox.append(self.minute_entry)
        
        label = Gtk.Label(label = "m")        
        label.set_hexpand(False)
        self.timerBox.append(label)
        # Second entry and label
        self.secs_entry = Gtk.Entry()
        self.secs_entry.set_text(sec_e)
        self.secs_entry.set_alignment(xalign=1)
        self.timerBox.append(self.secs_entry)
        
        label = Gtk.Label(label = "s")        
        label.set_hexpand(False)
        self.timerBox.append(label)
        
        self.mainBox.append(self.timerBox)

    # Theme setup
    def theme(self):
        if os.path.exists(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.timer/data/theme.json'):
            with open(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.timer/data/theme.json') as jt:
                t = json.load(jt)
            theme = t["theme"]
            if theme == "dark":
                self.style_manager.set_color_scheme(
                    color_scheme=Adw.ColorScheme.PREFER_DARK
                )
                
    # Resizable of Window
    def resizable(self):
        if os.path.exists(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.timer/data/window.json'):
            with open(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.timer/data/window.json') as jr:
                rezisable = json.load(jr)
            if rezisable == "true":
                self.set_resizable(True)
        else:
            self.set_resizable(False)
    
    # Spinner size
    def spinner_size(self):
        if os.path.exists(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.timer/data/spinner.json'):
            with open(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.timer/data/spinner.json') as j:
                jsonObject = json.load(j)
            spinner = jsonObject["spinner-size"]
            if spinner == "5":
                self.spinner.set_size_request(5,5)
                self.set_default_size(300, 300)
                self.set_size_request(300, 300)
            if spinner == "10":
                self.spinner.set_size_request(10,10)
                self.set_default_size(300, 300)
                self.set_size_request(300, 300)
            if spinner == "15":
                self.spinner.set_size_request(15,15)
                self.set_default_size(300, 300)
                self.set_size_request(300, 300)
            if spinner == "20":
                self.spinner.set_size_request(20,20)
                self.set_default_size(320, 320)
                self.set_size_request(320, 320)
            if spinner == "25":
                self.spinner.set_size_request(25,25)
                self.set_default_size(320, 320)
                self.set_size_request(320, 320)
            if spinner == "30":
                self.spinner.set_size_request(30,30)
                self.set_default_size(340, 340)
                self.set_size_request(340, 340)
            if spinner == "35":
                self.spinner.set_size_request(35,35)
                self.set_default_size(340, 340)
                self.set_size_request(340, 340)
            if spinner == "40 (%s)" % default:
                self.spinner.set_size_request(40,40)
                self.set_default_size(340, 340)
                self.set_size_request(340, 340)
            if spinner == "45":
                self.spinner.set_size_request(45,45)
                self.set_default_size(340, 340)
                self.set_size_request(340, 340)
            if spinner == "50":
                self.spinner.set_size_request(50,50)
                self.set_default_size(350, 350)
                self.set_size_request(350, 350)
            if spinner == "55":
                self.spinner.set_size_request(55,55)
                self.set_default_size(350, 350)
                self.set_size_request(350, 350)
            if spinner == "60":
                self.spinner.set_size_request(60,60)
                self.set_default_size(360, 360)
                self.set_size_request(360, 360)
            if spinner == "65":
                self.spinner.set_size_request(65,65)
                self.set_default_size(360, 360)
                self.set_size_request(360, 360)
            if spinner == "70":
                self.spinner.set_size_request(70,70)
                self.set_default_size(370, 370)
                self.set_size_request(370, 370)
            if spinner == "75":
                self.spinner.set_size_request(75,75)
                self.set_default_size(370, 370)
                self.set_size_request(370, 370)
            if spinner == "80":
                self.spinner.set_size_request(80,80)
                self.set_default_size(400, 400)
                self.set_size_request(400, 400)
        else:
            # default spinner size
            self.spinner.set_size_request(40,40)
            # default size of Window
            self.set_default_size(340, 340)
            self.set_size_request(340, 340)
    
    def on_buttonStart_clicked(self, widget, *args):
        """ button "clicked" in event buttonStart. """
        self.start_timer()

    def on_buttonStop_clicked(self, widget, *args):
        """ button "clicked" in event buttonStop. """
        self.stop_timer(timing_ended)

    def on_SpinnerWindow_destroy(self, widget, *args):
        """ procesing closing window """
        if self.timeout_id:
            GLib.source_remove(self.timeout_id)
            self.timeout_id = None
        Gtk.main_quit()

    tick_counter = timedelta(milliseconds = 250) # static object so we don't recreate the object every time
    zero_counter = timedelta()
    def on_timeout(self, *args, **kwargs):
        self.counter -= self.tick_counter
        if self.counter <= self.zero_counter:
            self.stop_timer(timing_finished)
            self.label.set_markup("<b>" + timing_finished + "</b>")
            subprocess.call(['notify-send',timer_title,timing_finished,'-i','com.github.vikdevelop.timer'])
            print(timing_finished)
            return False
        self.label.set_markup("{}\n<big><b>{}</b></big>".format(
            time_text,
            strfdelta(self.counter, "{hours} h {minutes} m {seconds} s")
        ))
        return True

    def start_timer(self):
        """ Run Timer. """
        self.buttonStart.set_sensitive(False)
        self.buttonStop.set_sensitive(True)
        self.button2_style_context.add_class('suggested-action')
        self.button1_style_context.remove_class('suggested-action')
        self.counter = timedelta(hours = int(self.hour_entry.get_text()), minutes = int(self.minute_entry.get_text()), seconds = int(self.secs_entry.get_text()))
        # Save time counter values
        hour = self.hour_entry.get_text()
        minute = self.minute_entry.get_text()
        sec = self.secs_entry.get_text()
        with open(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.timer/data/counter.json', 'w') as c:
            c.write('{\n "hour": "%s",\n "minutes": "%s",\n "seconds": "%s"\n}' % (hour, minute, sec))
        print('\a')
        self.label.set_markup("{}\n<big><b>{}</b></big>".format(
            time_text,
            strfdelta(self.counter, "{hours} h {minutes} m {seconds} s")
        ))
        self.spinner.start()
        self.timeout_id = GLib.timeout_add(250, self.on_timeout, None)
        
    def stop_timer(self, alabeltext):
        """ Stop Timer """
        if self.timeout_id:
            GLib.source_remove(self.timeout_id)
            self.timeout_id = None
        self.spinner.stop()
        self.buttonStart.set_sensitive(True)
        self.buttonStop.set_sensitive(False)
        self.button2_style_context.remove_class('suggested-action')
        self.button1_style_context.add_class('suggested-action')
        self.label.set_label(alabeltext)
        print('\a')
        print(timing_ended)

class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.connect('activate', self.on_activate)
        self.create_action('about', self.on_about_action)
        self.create_action('settings', self.on_settings_action)

    def on_about_action(self, action, param):
        dialog = Gtk.AboutDialog()
        dialog.set_title(about)
        dialog.set_name(timer_title)
        dialog.set_version("2.2")
        dialog.set_license_type(Gtk.License(Gtk.License.GPL_3_0))
        dialog.set_comments(simple_timer)
        dialog.set_website("https://github.com/vikdevelop/timer")
        dialog.set_website_label(source_code)
        dialog.set_authors(["vikdevelop https://github.com/vikdevelop"])
        dialog.set_translator_credits(translator_credits)
        dialog.set_copyright("© 2022 vikdevelop")
        dialog.set_logo_icon_name("com.github.vikdevelop.timer")
        dialog.show()
        
    def on_settings_action(self, action, param):
        self.dialog = Dialog_settings(self)

    def create_action(self, name, callback, shortcuts=None):
        action = Gio.SimpleAction.new(name, None)
        action.connect('activate', callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f'app.{name}', shortcuts)
    
    def on_activate(self, app):
        self.win = TimerWindow(application=app)
        self.win.present()
app = MyApp(application_id="com.github.vikdevelop.timer")
app.run(sys.argv)
print(timer_quit)
