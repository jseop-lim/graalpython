# Copyright (c) 2026, Oracle and/or its affiliates. All rights reserved.
# DO NOT ALTER OR REMOVE COPYRIGHT NOTICES OR THIS FILE HEADER.
#
# The Universal Permissive License (UPL), Version 1.0
#
# Subject to the condition set forth below, permission is hereby granted to any
# person obtaining a copy of this software, associated documentation and/or
# data (collectively the "Software"), free of charge and under any and all
# copyright rights in the Software, and any and all patent rights owned or
# freely licensable by each licensor hereunder covering either (i) the
# unmodified Software as contributed to or provided by such licensor, or (ii)
# the Larger Works (as defined below), to deal in both
#
# (a) the Software, and
#
# (b) any piece of software and/or hardware listed in the lrgrwrks.txt file if
# one is included with the Software each a "Larger Work" to which the Software
# is contributed by such licensors),
#
# without restriction, including without limitation the rights to copy, create
# derivative works of, display, perform, and distribute the Software and make,
# use, sell, offer for sale, import, export, have made, and have sold the
# Software and the Larger Work(s), and to sublicense the foregoing rights on
# either these or other terms.
#
# This license is subject to the following condition:
#
# The above copyright notice and either this complete permission notice or at a
# minimum a reference to the UPL must be included in all copies or substantial
# portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import collections
import heapq


def assert_raises(err, fn, *args, **kwargs):
    raised = False
    try:
        fn(*args, **kwargs)
    except err:
        raised = True
    assert raised


def test_heap_must_be_list():
    assert_raises(TypeError, heapq.heappush, None, 1)
    assert_raises(TypeError, heapq.heappush, collections.deque([2]), 1)
    assert_raises(TypeError, heapq.heappop, None)
    assert_raises(TypeError, heapq.heappop, collections.deque([2]))
    assert_raises(TypeError, heapq.heapreplace, (), 1)
    assert_raises(TypeError, heapq.heapreplace, {0: 5}, 1)
    assert_raises(TypeError, heapq.heappushpop, None, 1)
    assert_raises(TypeError, heapq.heappushpop, (), 1)
    assert_raises(TypeError, heapq.heapify, ())
    assert_raises(TypeError, heapq.heapify, {})


def test_max_heap_must_be_list():
    assert_raises(TypeError, heapq._heappop_max, collections.deque([2]))
    assert_raises(TypeError, heapq._heapreplace_max, {0: 5}, 1)
    assert_raises(TypeError, heapq._heapify_max, ())


def test_heap_class_attribute_is_not_trusted():
    class Fake:
        __class__ = list

        def __len__(self):
            return 0

    assert_raises(TypeError, heapq.heappushpop, Fake(), 1)


def test_list_subclass_heap():
    class L(list):
        pass

    heap = L([3, 1, 2])
    heapq.heapify(heap)
    heapq.heappush(heap, 0)
    assert heapq.heappop(heap) == 0
    assert heapq.heapreplace(heap, 5) == 1
    assert heapq.heappushpop(heap, 4) == 2
    assert heap == [3, 4, 5]
