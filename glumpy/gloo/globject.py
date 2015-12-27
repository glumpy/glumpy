# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------

class GLObject(object):
    """ Generic GL object that may live both on CPU and GPU """

    # Internal id counter to keep track of GPU objects
    _idcount = 0

    def __init__(self):
        """ Initialize the object in the default state """

        self._handle = -1
        self._target = None
        self._need_setup = True
        self._need_create = True
        self._need_update = True
        self._need_delete = False

        GLObject._idcount += 1
        self._id = GLObject._idcount


    # def __del__(self):
    #     """ Fake deletion """
    #     # You never know when this is goint to happen. The window might
    #     # already be closed and no OpenGL context might be available.
    #     # Worse, there might be multiple contexts and calling delete()
    #     # at the wrong moment might remove other gl objects, leading to
    #     # very strange and hard to debug behavior.
    #     #
    #     # So we don't do anything.
    #     if hasattr(self, "_handle"):
    #         if self._handle > -1:
    #             self._delete()
    #     else:
    #         print "Deleting something"


    @property
    def need_create(self):
        """ Whether object needs to be created """
        return self._need_create


    @property
    def need_update(self):
        """ Whether object needs to be updated """
        return self._need_update


    @property
    def need_setup(self):
        """ Whether object needs to be setup """
        return self._need_setup


    @property
    def need_delete(self):
        """ Whether object needs to be deleted """
        return self._need_delete


    def delete(self):
        """ Delete the object from GPU memory """

        #if self.need_delete:
        self._delete()
        self._handle = -1
        self._need_setup = True
        self._need_create = True
        self._need_update = True
        self._need_delete = False


    def activate(self):
        """ Activate the object on GPU """

        if hasattr(self, "base") and isinstance(self.base,GLObject):
            self.base.activate()
            return

        if self.need_create:
            self._create()
            self._need_create = False

        self._activate()

        if self.need_setup:
            self._setup()
            self._need_setup = False

        if self.need_update:
            self._update()
            self._need_update = False


    def deactivate(self):
        """ Deactivate the object on GPU """

        if hasattr(self,"base") and isinstance(self.base,GLObject):
            self.base.deactivate()
        else:
            self._deactivate()


    @property
    def handle(self):
        """ Name of this object on the GPU """

        if hasattr(self, "base") and isinstance(self.base,GLObject):
            if hasattr(self.base, "_handle"):
                return self.base._handle
        return self._handle
        #return self._handle


    @property
    def target(self):
        """ OpenGL type of object. """

        if hasattr(self, "base") and isinstance(self.base,GLObject):
            return self.base._target
        return self._target
        #return self._handle


    def _create(self):
        """ Dummy create method """

        pass


    def _delete(self):
        """ Dummy delete method """

        pass


    def _activate(self):
        """ Dummy activate method """

        pass


    def _deactivate(self):
        """ Dummy deactivate method """

        pass


    def _setup(self):
        """ Dummy setup method """

        pass


    def _update(self):
        """ Dummy update method """

        pass
