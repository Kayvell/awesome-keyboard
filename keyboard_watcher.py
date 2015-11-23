from sys import platform as _platform

if _platform.startswith("linux"):
    try:
        from Xlib.display import Display
        from Xlib import X
        from Xlib.ext import record
        from Xlib.protocol import rq
    except ImportError, e:
        print 'KeyboardWatcher: Missing dependency:', e.message[16:]
        print 'KeyboardWatcher: Terminating application.'
        sys.exit(1)
elif _platform == "win32":
    import pyHook
    import pythoncom
else:
    print 'KeyboardWatcher: Unsupported operating system. Terminating application.'
    sys.exit(1)

from collections import defaultdict
import math

from multiprocessing import Process
import signal

class BaseWatcher(Process):

    def __init__(self,name,queue):
        super(BaseWatcher,self).__init__()
        self._queue = queue
        self._name = name

    def disable_keyboard_interrupt(self):
        s = signal.signal(signal.SIGINT, signal.SIG_IGN)

    def send_event(self,value):
        self._queue.put([self._name,value])

class KeyboardAndMouseWatcher(BaseWatcher):

    def __init__(self,name,queue):
        super(KeyboardAndMouseWatcher,self).__init__(name,queue)
        self._queue = queue
        self._mouse_last_x = None
        self._mouse_last_y = None
        if _platform.startswith("linux"):
            self._display = Display()

    def add_to_datapoint(self,x,y):
        if y[0] == 'keys_pressed':
            x[y[0]][y[1]]+=y[2]
        else:
            x[y[0]]+=y[1]
        return x

    def init_datapoint(self):
        return {'buttons_pressed': 0,'keys_pressed' :defaultdict(lambda :0),'mouse_moved':0}

    def handle_event(self,reply):
        """ This function is called when an xlib event is fired. """

        data = reply.data

        while len(data):
            event, data = rq.EventField(None).parse_binary_value(data, self._display.display, None, None)

            if event.type == X.MotionNotify:
                if self._mouse_last_x != None:
                    mouse_distance=math.sqrt((event.root_x-self._mouse_last_x)**2+(event.root_y-self._mouse_last_y)**2)
                    self.send_event(('mouse_moved',mouse_distance))
                self._mouse_last_x,self._mouse_last_y = event.root_x,event.root_y

            if event.type == X.ButtonPress:
                print event.sequence_number,event._data,event._fields
                self.send_event(('button_down',event._data['detail']))
            elif event.type == X.ButtonRelease:
                print event.sequence_number,event._data,event._fields
                self.send_event(('button_up',event._data['detail']))
            elif event.type == X.KeyPress and event.sequence_number == 0:
                key = event.detail
                self.send_event(('keys_pressed',key,1))

    def handle_win_event(self):
        """ This is the win32 pyHook equivalent of the Linux xlib event system. """

        def MouseMove(event):
            # TODO
            # Unsure why mouse motion was including in the Linux version in the first place... but this'll stay undone for now (simple send_event without mouse_distance included)...
            self.send_event(('mouse_moved'))
            return True

        # For the mouse ones, to be honest there's really nothing more to send other than the fact the button is up or down...

        def ButtonDown(event):
            self.send_event(('button_down'))
            return True

        def ButtonUp(event):
            self.send_event(('button_up'))
            return True

        # While according to the pyHook documentation this is not officially a "key press", officially just the key coming back up, this is pretty much a key press.

        def KeyPress(event):
            self.send_event(('keys_pressed', event.Key, 1))
            return True

        hm = pyHook.HookManager()
        # For performance purposes, this will remain commented out.
        # hm.MouseMove = MouseMove
        hm.MouseLeftDown = ButtonDown
        hm.MouseLeftUp = ButtonUp
        hm.HookMouse()
        hm.KeyUp = KeyPress
        hm.HookKeyboard()
        pythoncom.PumpMessages()
        hm.UnhookMouse()
        hm.UnhookKeyboard()

    def run(self):
        self.disable_keyboard_interrupt()
        if _platform.startswith("linux"):
            root = self._display.screen().root
            ctx = self._display.record_create_context(
                        0,
                        [record.AllClients],
                        [{
                                'core_requests': (0, 0),
                                'core_replies': (0, 0),
                                'ext_requests': (0, 0, 0, 0),
                                'ext_replies': (0, 0, 0, 0),
                                'delivered_events': (0, 0),
                                'device_events': (X.KeyReleaseMask, X.PointerMotionMask),
                                'errors': (0, 0),
                                'client_started': False,
                                'client_died': False,
                        }])

            self._display.record_enable_context(ctx, self.handle_event)
        elif _platform == "win32":
            self.handle_win_event()
