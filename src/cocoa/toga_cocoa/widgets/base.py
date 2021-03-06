from toga_cocoa.constraints import Constraints


class Widget:
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self
        self._container = None
        self._viewport = None
        self.constraints = None
        self.native = None
        self.create()
        self.interface.style.reapply()
        self.set_enabled(self.interface.enabled)

    def create(self):
        raise NotImplementedError()

    def set_app(self, app):
        pass

    def set_window(self, window):
        pass

    @property
    def container(self):
        return self._container

    @container.setter
    def container(self, container):

        if container is None:
            self.constraints.container = None
            self._container = None
            self.native.removeFromSuperview()
        else:
            self._container = container
            self._container.native.addSubview(self.native)
            self.constraints.container = container

        for child in self.interface.children:
            child._impl.container = container

        self.rehint()

    def set_enabled(self, value):
        self.native.enabled = self.interface.enabled

    # APPLICATOR

    def set_bounds(self, x, y, width, height):
        # print("SET BOUNDS ON", self.interface, x, y, width, height)
        self.constraints.update(x, y, width, height)

    def set_alignment(self, alignment):
        pass

    def set_hidden(self, hidden):
        if self.native:
            self.native.setHidden(hidden)

    def set_font(self, font):
        pass

    def set_color(self, color):
        pass

    def set_background_color(self, color):
        pass

    # INTERFACE

    def add_child(self, child):
        child.container = self.container or self

    def insert_child(self, index, child):
        self.add_child(child)

    def remove_child(self, child):
        child.container = None

    def add_constraints(self):
        self.native.translatesAutoresizingMaskIntoConstraints = False
        self.constraints = Constraints(self)

    def rehint(self):
        pass
