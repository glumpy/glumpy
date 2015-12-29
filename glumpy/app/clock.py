# ----------------------------------------------------------------------------
# pyglet
# Copyright (c) 2006-2008 Alex Holkner
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of pyglet nor the names of its
#    contributors may be used to endorse or promote products
#    derived from this software without specific prior written
#    permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------------

'''Precise framerate calculation, scheduling and framerate limiting.

Measuring time
==============

The `tick` and `get_fps` functions can be used in conjunction to fulfil most
games' basic requirements::

    from glumpy.app import clock
    while True:
        dt = clock.tick()
        # ... update and render ...
        print 'FPS is %f' % clock.get_fps()

The ``dt`` value returned gives the number of seconds (as a float) since the
last "tick".

The `get_fps` function averages the framerate over a sliding window of
approximately 1 second.  (You can calculate the instantaneous framerate by
taking the reciprocal of ``dt``).

Always remember to `tick` the clock!

Limiting frame-rate
===================

The framerate can be limited::

    clock.set_fps_limit(60)

This causes `clock` to sleep during each `tick` in an attempt to keep the
number of ticks (frames) per second below 60.

The implementation uses platform-dependent high-resolution sleep functions to
achieve better accuracy with busy-waiting than would not be possible using just
the `time` module.

Scheduling
==========

You can schedule a function to be called every time the clock is ticked::

    def callback(dt):
        print '%f seconds since last callback' % dt

    clock.schedule(callback)

The `schedule_interval` method causes a function to be called every "n"
seconds::

    clock.schedule_interval(callback, .5)   # called twice a second

The `schedule_once` method causes a function to be called once "n" seconds
in the future::

    clock.schedule_once(callback, 5)        # called in 5 seconds

All of the `schedule` methods will pass on any additional args or keyword args
you specify to the callback function::

    def animate(dt, velocity, sprite):
       sprite.position += dt * velocity

    clock.schedule(animate, velocity=5.0, sprite=alien)

You can cancel a function scheduled with any of these methods using
`unschedule`::

    clock.unschedule(animate)

Displaying FPS
==============

The ClockDisplay class provides a simple FPS counter.  You should create
an instance of ClockDisplay once during the application's start up::

    fps_display = clock.ClockDisplay()

Call draw on the ClockDisplay object for each frame::

    fps_display.draw()

There are several options to change the font, color and text displayed
within the __init__ method.

Using multiple clocks
=====================

The clock functions are all relayed to an instance of `Clock` which is
initialised with the module.  You can get this instance to use directly::

    clk = clock.get_default()

You can also replace the default clock with your own:

    myclk = clock.Clock()
    clock.set_default(myclk)

Each clock maintains its own set of scheduled functions and FPS
limiting/measurement.  Each clock must be "ticked" separately.

Multiple and derived clocks potentially allow you to separate "game-time" and
"wall-time", or to synchronise your clock to an audio or video stream instead
of the system clock.

'''

__docformat__ = 'restructuredtext'
__version__ = '$Id$'

import time
import sys
import ctypes, ctypes.util

if sys.platform in ('win32', 'cygwin'):
    # Win32 Sleep function is only 10-millisecond resolution, so instead
    # use a waitable timer object, which has up to 100-nanosecond resolution
    # (hardware and implementation dependent, of course).
    _kernel32 = ctypes.windll.kernel32
    class _ClockBase(object):
        def __init__(self):
            self._timer = _kernel32.CreateWaitableTimerA(None, True, None)

        def sleep(self, microseconds):
            delay = ctypes.c_longlong(int(-microseconds * 10))
            _kernel32.SetWaitableTimer(self._timer, ctypes.byref(delay),
                0, ctypes.c_void_p(), ctypes.c_void_p(), False)
            _kernel32.WaitForSingleObject(self._timer, 0xffffffff)

    _default_time_function = time.clock

else:
    _c_file = ctypes.util.find_library('c')
    _c = ctypes.CDLL(_c_file)
    _c.usleep.argtypes = [ctypes.c_ulong]
    class _ClockBase(object):
        def sleep(self, microseconds):
            _c.usleep(int(microseconds))

    _default_time_function = time.time

class _ScheduledItem(object):
    __slots__ = ['func', 'args', 'kwargs']
    def __init__(self, func, args, kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

class _ScheduledIntervalItem(object):
    __slots__ = ['func', 'interval', 'last_ts', 'next_ts',
                 'args', 'kwargs']
    def __init__(self, func, interval, last_ts, next_ts, args, kwargs):
        self.func = func
        self.interval = interval
        self.last_ts = last_ts
        self.next_ts = next_ts
        self.args = args
        self.kwargs = kwargs

def _dummy_schedule_func(*args, **kwargs):
    '''Dummy function that does nothing, placed onto zombie scheduled items
    to ensure they have no side effect if already queued inside tick() method.
    '''
    pass

class Clock(_ClockBase):
    '''Class for calculating and limiting framerate, and for calling scheduled
    functions.
    '''

    #: The minimum amount of time in seconds this clock will attempt to sleep
    #: for when framerate limiting.  Higher values will increase the
    #: accuracy of the limiting but also increase CPU usage while
    #: busy-waiting.  Lower values mean the process sleeps more often, but is
    #: prone to over-sleep and run at a potentially lower or uneven framerate
    #: than desired.
    MIN_SLEEP = 0.005

    #: The amount of time in seconds this clock subtracts from sleep values
    #: to compensate for lazy operating systems.
    SLEEP_UNDERSHOOT = MIN_SLEEP - 0.001

    # List of functions to call every tick.
    _schedule_items = None

    # List of schedule interval items kept in sort order.
    _schedule_interval_items = None

    # If True, a sleep(0) is inserted on every tick.
    _force_sleep = False

    def __init__(self, fps_limit=None, time_function=_default_time_function):
        '''Initialise a Clock, with optional framerate limit and custom
        time function.

        :Parameters:
            `fps_limit` : float
                If not None, the maximum allowable framerate.  Defaults
                to None. 
            `time_function` : function
                Function to return the elapsed time of the application,
                in seconds.  Defaults to time.time, but can be replaced
                to allow for easy time dilation effects or game pausing.

        '''

        super(Clock, self).__init__()
        self.time = time_function
        self.next_ts = self.time()
        self.last_ts = None
        self.times = []

        self.set_fps_limit(fps_limit)
        self.cumulative_time = 0

        self._schedule_items = []
        self._schedule_interval_items = []

    def update_time(self):
        '''Get the elapsed time since the last call to `update_time`.

        This updates the clock's internal measure of time and returns
        the difference since the last update (or since the clock was created).

        :rtype: float
        :return: The number of seconds since the last `update_time`, or 0
            if this was the first time it was called.
        '''
        ts = self.time()
        if self.last_ts is None:
            delta_t = 0
        else:
            delta_t = ts - self.last_ts
            self.times.insert(0, delta_t)
            if len(self.times) > self.window_size:
                self.cumulative_time -= self.times.pop()
        self.cumulative_time += delta_t
        self.last_ts = ts

        return delta_t

    def call_scheduled_functions(self, dt):
        '''Call scheduled functions that elapsed on the last `update_time`.

        :Parameters:
            dt : float
                The elapsed time since the last update to pass to each
                scheduled function.  This is *not* used to calculate which
                functions have elapsed.

        :rtype: bool
        :return: True if any functions were called, otherwise False.
        '''
        ts = self.last_ts
        result = False

        # Call functions scheduled for every frame
        # Dupe list just in case one of the items unchedules itself
        for item in list(self._schedule_items):
            result = True
            item.func(dt, *item.args, **item.kwargs)

        # Call all scheduled interval functions and reschedule for future.
        need_resort = False
        # Dupe list just in case one of the items unchedules itself
        for item in list(self._schedule_interval_items):
            if item.next_ts > ts:
                break
            result = True
            item.func(ts - item.last_ts, *item.args, **item.kwargs)
            if item.interval:
                # Try to keep timing regular, even if overslept this time;
                # but don't schedule in the past (which could lead to
                # infinitely-worsing error).
                item.next_ts = item.last_ts + item.interval
                item.last_ts = ts
                if item.next_ts <= ts:
                    if ts - item.next_ts < 0.05:
                        # Only missed by a little bit, keep the same schedule
                        item.next_ts = ts + item.interval
                    else:
                        # Missed by heaps, do a soft reschedule to avoid
                        # lumping everything together.
                        item.next_ts = self._get_soft_next_ts(ts, item.interval)
                        # Fake last_ts to avoid repeatedly over-scheduling in
                        # future.  Unfortunately means the next reported dt is
                        # incorrect (looks like interval but actually isn't).
                        item.last_ts = item.next_ts - item.interval
                need_resort = True
            else:
                item.next_ts = None

        # Remove finished one-shots.
        self._schedule_interval_items = \
            [item for item in self._schedule_interval_items \
             if item.next_ts is not None]

        if need_resort:
            # TODO bubble up changed items might be faster
            self._schedule_interval_items.sort(key=lambda a: a.next_ts)

        return result

    def tick(self, poll=False):
        '''Signify that one frame has passed.

        This will call any scheduled functions that have elapsed.

        :Parameters:
            `poll` : bool
                If True, the function will call any scheduled functions
                but will not sleep or busy-wait for any reason.  Recommended
                for advanced applications managing their own sleep timers
                only.

        :rtype: float
        :return: The number of seconds since the last "tick", or 0 if this was
            the first frame.
        '''
        if poll:
            if self.period_limit:
                self.next_ts = self.next_ts + self.period_limit
        else:
            if self.period_limit:
                self._limit()

            if self._force_sleep:
                self.sleep(0)

        delta_t = self.update_time()
        self.call_scheduled_functions(delta_t)
        return delta_t

    def _limit(self):
        '''Sleep until the next frame is due.  Called automatically by
        `tick` if a framerate limit has been set.

        This method uses several heuristics to determine whether to
        sleep or busy-wait (or both).
        '''
        ts = self.time()
        # Sleep to just before the desired time
        sleeptime = self.get_sleep_time(False)
        while sleeptime - self.SLEEP_UNDERSHOOT > self.MIN_SLEEP:
            self.sleep(1000000 * (sleeptime - self.SLEEP_UNDERSHOOT))
            sleeptime = self.get_sleep_time(False)

        # Busy-loop CPU to get closest to the mark
        sleeptime = self.next_ts - self.time()
        while sleeptime > 0:
            sleeptime = self.next_ts - self.time()

        if sleeptime < -2 * self.period_limit:
            # Missed the time by a long shot, let's reset the clock
            # print >> sys.stderr, 'Step %f' % -sleeptime
            self.next_ts = ts + 2 * self.period_limit
        else:
            # Otherwise keep the clock steady
            self.next_ts = self.next_ts + self.period_limit

    def get_sleep_time(self, sleep_idle):
        '''Get the time until the next item is scheduled.

        This method considers all scheduled items and the current
        ``fps_limit``, if any.

        Applications can choose to continue receiving updates at the
        maximum framerate during idle time (when no functions are scheduled),
        or they can sleep through their idle time and allow the CPU to
        switch to other processes or run in low-power mode.

        If `sleep_idle` is ``True`` the latter behaviour is selected, and
        ``None`` will be returned if there are no scheduled items.

        Otherwise, if `sleep_idle` is ``False``, a sleep time allowing
        the maximum possible framerate (considering ``fps_limit``) will
        be returned; or an earlier time if a scheduled function is ready.

        :Parameters:
            `sleep_idle` : bool
                If True, the application intends to sleep through its idle
                time; otherwise it will continue ticking at the maximum
                frame rate allowed.

        :rtype: float
        :return: Time until the next scheduled event in seconds, or ``None``
            if there is no event scheduled.

        '''
        if self._schedule_items or not sleep_idle:
            if not self.period_limit:
                return 0.
            else:
                wake_time = self.next_ts
                if self._schedule_interval_items:
                    wake_time = min(wake_time,
                                    self._schedule_interval_items[0].next_ts)
                return max(wake_time - self.time(), 0.)

        if self._schedule_interval_items:
            return max(self._schedule_interval_items[0].next_ts - self.time(),
                       0)

        return None

    def set_fps_limit(self, fps_limit):
        '''Set the framerate limit.

        The framerate limit applies only when a function is scheduled
        for every frame.  That is, the framerate limit can be exceeded by
        scheduling a function for a very small period of time.

        :Parameters:
            `fps_limit` : float
                Maximum frames per second allowed, or None to disable
                limiting.
        '''
        if not fps_limit:
            self.period_limit = None
        else:
            self.period_limit = 1. / fps_limit
        self.window_size = fps_limit or 60

    def get_fps_limit(self):
        '''Get the framerate limit.

        :rtype: float
        :return: The framerate limit previously set in the constructor or
            `set_fps_limit`, or None if no limit was set.
        '''
        if self.period_limit:
            return 1. / self.period_limit
        else:
            return 0

    def get_fps(self):
        '''Get the average FPS of recent history.

        The result is the average of a sliding window of the last "n" frames,
        where "n" is some number designed to cover approximately 1 second.

        :rtype: float
        :return: The measured frames per second.
        '''
        if not self.cumulative_time:
            return 0
        return len(self.times) / self.cumulative_time

    def schedule(self, func, *args, **kwargs):
        '''Schedule a function to be called every frame.

        The function should have a prototype that includes ``dt`` as the
        first argument, which gives the elapsed time, in seconds, since the
        last clock tick.  Any additional arguments given to this function
        are passed on to the callback::

            def callback(dt, *args, **kwargs):
                pass

        :Parameters:
            `func` : function
                The function to call each frame.
        '''
        item = _ScheduledItem(func, args, kwargs)
        self._schedule_items.append(item)

    def _schedule_item(self, func, last_ts, next_ts, interval, *args, **kwargs):
        item = _ScheduledIntervalItem(
            func, interval, last_ts, next_ts, args, kwargs)

        # Insert in sort order
        for i, other in enumerate(self._schedule_interval_items):
            if other.next_ts is not None and other.next_ts > next_ts:
                self._schedule_interval_items.insert(i, item)
                break
        else:
            self._schedule_interval_items.append(item)

    def schedule_interval(self, func, interval, *args, **kwargs):
        '''Schedule a function to be called every `interval` seconds.

        Specifying an interval of 0 prevents the function from being
        called again (see `schedule` to call a function as often as possible).

        The callback function prototype is the same as for `schedule`.

        :Parameters:
            `func` : function
                The function to call when the timer lapses.
            `interval` : float
                The number of seconds to wait between each call.

        '''
        last_ts = self.last_ts or self.next_ts

        # Schedule from now, unless now is sufficiently close to last_ts, in
        # which case use last_ts.  This clusters together scheduled items that
        # probably want to be scheduled together.  The old (pre 1.1.1)
        # behaviour was to always use self.last_ts, and not look at ts.  The
        # new behaviour is needed because clock ticks can now be quite
        # irregular, and span several seconds.
        ts = self.time()
        if ts - last_ts > 0.2:
            last_ts = ts

        next_ts = last_ts + interval
        self._schedule_item(func, last_ts, next_ts, interval, *args, **kwargs)

    def schedule_interval_soft(self, func, interval, *args, **kwargs):
        '''
        Schedule a function to be called every `interval` seconds,
        beginning at a time that does not coincide with other scheduled
        events.

        This method is similar to `schedule_interval`, except that the
        clock will move the interval out of phase with other scheduled
        functions so as to distribute CPU more load evenly over time.

        This is useful for functions that need to be called regularly, but not
        relative to the initial start time.  Using the soft interval
        scheduling, the load is more evenly distributed.

        Soft interval scheduling can also be used as an easy way to schedule
        graphics animations out of phase; for example, multiple flags
        waving in the wind.

        :Parameters:
            `func` : function
                The function to call when the timer lapses.
            `interval` : float
                The number of seconds to wait between each call.
        '''
        last_ts = self.last_ts or self.next_ts

        # See schedule_interval
        ts = self.time()
        if ts - last_ts > 0.2:
            last_ts = ts

        next_ts = self._get_soft_next_ts(last_ts, interval)
        last_ts = next_ts - interval
        self._schedule_item(func, last_ts, next_ts, interval, *args, **kwargs)

    def _get_soft_next_ts(self, last_ts, interval):
        def taken(ts, e):
            '''Return True if the given time has already got an item
            scheduled nearby.
            '''
            for item in self._schedule_interval_items:
                if item.next_ts is None:
                    pass
                elif abs(item.next_ts - ts) <= e:
                    return True
                elif item.next_ts > ts + e:
                    return False
            return False

        # Binary division over interval:
        #
        # 0                          interval
        # |--------------------------|
        #   5  3   6   2   7  4  8   1          Order of search
        #
        # i.e., first scheduled at interval,
        #       then at            interval/2
        #       then at            interval/4
        #       then at            interval*3/4
        #       then at            ...
        #
        # Schedule is hopefully then evenly distributed for any interval,
        # and any number of scheduled functions.

        next_ts = last_ts + interval
        if not taken(next_ts, interval / 4):
            return next_ts

        dt = interval
        divs = 1
        while True:
            next_ts = last_ts
            for i in range(divs - 1):
                next_ts += dt
                if not taken(next_ts, dt / 4):
                    return next_ts
            dt /= 2
            divs *= 2

            # Avoid infinite loop in pathological case
            if divs > 16:
                return next_ts

    def schedule_once(self, func, delay, *args, **kwargs):
        '''Schedule a function to be called once after `delay` seconds.

        The callback function prototype is the same as for `schedule`.

        :Parameters:
            `func` : function
                The function to call when the timer lapses.
            `delay` : float
                The number of seconds to wait before the timer lapses.
        '''
        last_ts = self.last_ts or self.next_ts

        # See schedule_interval
        ts = self.time()
        if ts - last_ts > 0.2:
            last_ts = ts

        next_ts = last_ts + delay
        self._schedule_item(func, last_ts, next_ts, 0, *args, **kwargs)

    def unschedule(self, func):
        '''Remove a function from the schedule.

        If the function appears in the schedule more than once, all occurrences
        are removed.  If the function was not scheduled, no error is raised.

        :Parameters:
            `func` : function
                The function to remove from the schedule.

        '''
        # First replace zombie items' func with a dummy func that does
        # nothing, in case the list has already been cloned inside tick().
        # (Fixes issue 326).
        for item in self._schedule_items:
            if item.func == func:
                item.func = _dummy_schedule_func

        for item in self._schedule_interval_items:
            if item.func == func:
                item.func = _dummy_schedule_func

        # Now remove matching items from both schedule lists.
        self._schedule_items = \
            [item for item in self._schedule_items \
                  if item.func is not _dummy_schedule_func]

        self._schedule_interval_items = \
            [item for item in self._schedule_interval_items \
                  if item.func is not _dummy_schedule_func]

# Default clock.
_default = Clock()

def set_default(default):
    '''Set the default clock to use for all module-level functions.

    By default an instance of `Clock` is used.

    :Parameters:
        `default` : `Clock`
            The default clock to use.
    '''
    global _default
    _default = default

def get_default():
    '''Return the `Clock` instance that is used by all module-level
    clock functions.

    :rtype: `Clock`
    :return: The default clock.
    '''
    return _default

def tick(poll=False):
    '''Signify that one frame has passed on the default clock.

    This will call any scheduled functions that have elapsed.

    :Parameters:
        `poll` : bool
            If True, the function will call any scheduled functions
            but will not sleep or busy-wait for any reason.  Recommended
            for advanced applications managing their own sleep timers
            only.

    :rtype: float
    :return: The number of seconds since the last "tick", or 0 if this was the
        first frame.
    '''

    return _default.tick(poll)

def get_sleep_time(sleep_idle):
    '''Get the time until the next item is scheduled on the default clock.

    See `Clock.get_sleep_time` for details.

    :Parameters:
        `sleep_idle` : bool
            If True, the application intends to sleep through its idle
            time; otherwise it will continue ticking at the maximum
            frame rate allowed.

    :rtype: float
    :return: Time until the next scheduled event in seconds, or ``None``
        if there is no event scheduled.
    '''
    return _default.get_sleep_time(sleep_idle)

def get_fps():
    '''Return the current measured FPS of the default clock.

    :rtype: float
    '''
    return _default.get_fps()

def set_fps_limit(fps_limit):
    '''Set the framerate limit for the default clock.

    :Parameters:
        `fps_limit` : float
            Maximum frames per second allowed, or None to disable
            limiting.
    '''
    _default.set_fps_limit(fps_limit)

def get_fps_limit():
    '''Get the framerate limit for the default clock.

    :return: The framerate limit previously set by `set_fps_limit`, or None if
        no limit was set.

    '''
    return _default.get_fps_limit()

def schedule(func, *args, **kwargs):
    '''Schedule 'func' to be called every frame on the default clock.

    The arguments passed to func are ``dt``, followed by any ``*args`` and
    ``**kwargs`` given here.

    :Parameters:
        `func` : function
            The function to call each frame.
    '''
    _default.schedule(func, *args, **kwargs)

def schedule_interval(func, interval, *args, **kwargs):
    '''Schedule 'func' to be called every 'interval' seconds on the default
    clock.

    The arguments passed to 'func' are 'dt' (time since last function call),
    followed by any ``*args`` and ``**kwargs`` given here.

    :Parameters:
        `func` : function
            The function to call when the timer lapses.
        `interval` : float
            The number of seconds to wait between each call.

    '''
    _default.schedule_interval(func, interval, *args, **kwargs)

def schedule_interval_soft(func, interval, *args, **kwargs):
    '''Schedule 'func' to be called every 'interval' seconds on the default
    clock, beginning at a time that does not coincide with other scheduled
    events.

    The arguments passed to 'func' are 'dt' (time since last function call),
    followed by any ``*args`` and ``**kwargs`` given here.

    :see: `Clock.schedule_interval_soft`

    :Parameters:
        `func` : function
            The function to call when the timer lapses.
        `interval` : float
            The number of seconds to wait between each call.

    '''
    _default.schedule_interval_soft(func, interval, *args, **kwargs)

def schedule_once(func, delay, *args, **kwargs):
    '''Schedule 'func' to be called once after 'delay' seconds (can be
    a float) on the default clock.  The arguments passed to 'func' are
    'dt' (time since last function call), followed by any ``*args`` and
    ``**kwargs`` given here.

    If no default clock is set, the func is queued and will be scheduled
    on the default clock as soon as it is created.

    :Parameters:
        `func` : function
            The function to call when the timer lapses.
        `delay` : float
            The number of seconds to wait before the timer lapses.

    '''
    _default.schedule_once(func, delay, *args, **kwargs)

def unschedule(func):
    '''Remove 'func' from the default clock's schedule.  No error
    is raised if the func was never scheduled.

    :Parameters:
        `func` : function
            The function to remove from the schedule.

    '''
    _default.unschedule(func)

