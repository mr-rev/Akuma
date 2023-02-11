
import evdev


# Check that we have permissions to continue
def _check():
    # TODO: Implement!
    pass
_check()
del _check


class ListenerMixin(object):
    """A mixin for *uinput* event listeners.

    Subclasses should set a value for :attr:`_EVENTS` and implement
    :meth:`_handle`.
    """
    #: The events for which to listen
    _EVENTS = tuple()

    def __init__(self, *args, **kwargs):
        super(ListenerMixin, self).__init__(*args, **kwargs)
        self._dev = self._device(self._options.get(
            'device_paths',
            evdev.list_devices()))
        if self.suppress:
            self._dev.grab()

    def _run(self):
        for event in self._dev.read_loop():
            if event.type in self._EVENTS:
                self._handle(event)

    def _stop_platform(self):
        self._dev.close()

    def _device(self, paths):
        dev, count = None, 0
        for path in paths:
            # Open the device
            try:
                next_dev = evdev.InputDevice(path)
            except OSError:
                continue

            # Does this device provide more handled event codes?
            capabilities = next_dev.capabilities()
            next_count = sum(
                len(codes)
                for event, codes in capabilities.items()
                if event in self._EVENTS)
            if next_count > count:
                dev = next_dev
                count = next_count
            else:
                next_dev.close()

        if dev is None:
            raise OSError('no dlc7A device available')
        else:
            return dev

    def _handle(self, event):
        """Handles a single event.

        This method should call one of the registered event callbacks.

        :param event: The event.
        """
        raise NotImplementedError()
