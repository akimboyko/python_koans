#!/usr/bin/env python
# -*- coding: utf-8 -*-

from runner.koan import *
from functools import wraps

class AboutDecorators(Koan):
    def once(self, func):
        """Evaluates a function only once.

        Any value returned on the first call is returned on all
        subsequent calls.
        """
        # Write your decorator here.
        was_called = False
        result = None

        @wraps(func)
        def inner():
            nonlocal was_called, result

            if not was_called:
                was_called = True
                result = func()

            return result

        return inner

    def test_once_is_a_proper_decorator(self):
        @self.once
        def do_something():
            """I do something."""

        self.assertEquals("do_something", do_something.__name__)
        self.assertEquals("I do something.", do_something.__doc__)

    def test_once_evaluates_the_function_once(self):
        counter = 0

        @self.once
        def do_something():
            nonlocal counter
            counter += 1

        do_something()
        self.assertEquals(1, counter)
        do_something()
        self.assertEquals(1, counter)

    def test_once_propagates_return_value(self):
        @self.once
        def do_something():
            return []

        self.assertEquals([], do_something())
        self.assertEquals([], do_something())

    # ------------------------------------------------------------------

    def post(self, cond):
        """Asserts a condition against the function result.

        Raises AssertionError (via assert statement) if the condition
        is False.
        """
        def decorator(func):
            # Write your decorator here.
            @wraps(func)
            def inner(*args, **kwds):
                result = func(*args, **kwds)
                assert cond(result)
                return result

            return inner

        return decorator

    def test_post_is_a_proper_decorator(self):
        @self.post(lambda *args, **kwargs: True)
        def do_something():
            """I do something."""

        self.assertEquals("do_something", do_something.__name__)
        self.assertEquals("I do something.", do_something.__doc__)

    def test_post_fails_when_needed(self):
        @self.post(lambda r: r > 10)
        def do_something(x):
            return x + 1

        with self.assertRaises(AssertionError):
            do_something(0)

    def test_post_is_correct(self):
        @self.post(lambda r: r > 10)
        def do_something(x):
            return x + 1

        self.assertEquals(43, do_something(42))

    # ------------------------------------------------------------------

    def retry(self, n_times, on_exc_cls=Exception):
        """Retries the decorated function n times on exception.

        The retry only happens if the function raises an exception of the
        specified type (on_exc_cls). Any other exception is propagated.

        Raises RuntimeException if all of the n retry attempts failed.
        """
        def decorator(func):
            # Write your decorator here.
            @wraps(func)
            def inner(*args, **kwds):
                for _ in range(0, n_times + 1):
                    try:
                        return func(*args, **kwds)
                    except Exception as ex:
                        if not isinstance(ex, on_exc_cls):
                            raise
                else:
                    raise RuntimeError()

            return inner

        return decorator

    def test_retry_is_a_proper_decorator(self):
        @self.retry(4)
        def do_something():
            """I do something."""

        self.assertEquals("do_something", do_something.__name__)
        self.assertEquals("I do something.", do_something.__doc__)

    def fail_n_times(self, n):
        def inner():
            nonlocal n
            if n:
                n -= 1
                raise ValueError
            return 42
        return inner

    def test_retry_fails_after_n_failures(self):
        fail_retry = self.retry(2)(self.fail_n_times(4))
        with self.assertRaises(RuntimeError):
            fail_retry()

    def test_retry_bypasses_other_exceptions(self):
        # Bypasses exceptions other than on_exc_class.
        fail_retry = self.retry(2, on_exc_cls=TypeError)(self.fail_n_times(4))
        with self.assertRaises(ValueError):
            fail_retry()

    def test_retry_returns_a_value(self):
        fail_retry = self.retry(4, on_exc_cls=ValueError)(self.fail_n_times(2))
        self.assertEquals(42, fail_retry())