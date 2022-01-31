#!/usr/bin/python3
# Copyright 2021 Canonical Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import cgi
import datetime
import email.parser
import io
import json
import unittest
import unittest.mock
import unittest.util
import sys

import ops.pebble as pebble
import test.fake_pebble as fake_pebble
from ops._private import yaml


# Ensure unittest diffs don't get truncated like "[17 chars]"
unittest.util._MAX_LENGTH = 1000


def datetime_utc(y, m, d, hour, min, sec, micro=0):
    tz = datetime.timezone.utc
    return datetime.datetime(y, m, d, hour, min, sec, micro, tzinfo=tz)


def datetime_nzdt(y, m, d, hour, min, sec, micro=0):
    tz = datetime.timezone(datetime.timedelta(hours=13))
    return datetime.datetime(y, m, d, hour, min, sec, micro, tzinfo=tz)


class TestHelpers(unittest.TestCase):
    def test_parse_timestamp(self):
        self.assertEqual(pebble._parse_timestamp('2020-12-25T13:45:50+13:00'),
                         datetime_nzdt(2020, 12, 25, 13, 45, 50, 0))

        self.assertEqual(pebble._parse_timestamp('2020-12-25T13:45:50.123456789+13:00'),
                         datetime_nzdt(2020, 12, 25, 13, 45, 50, 123457))

        self.assertEqual(pebble._parse_timestamp('2021-02-10T04:36:22Z'),
                         datetime_utc(2021, 2, 10, 4, 36, 22, 0))

        self.assertEqual(pebble._parse_timestamp('2021-02-10t04:36:22z'),
                         datetime_utc(2021, 2, 10, 4, 36, 22, 0))

        self.assertEqual(pebble._parse_timestamp('2021-02-10T04:36:22.118970777Z'),
                         datetime_utc(2021, 2, 10, 4, 36, 22, 118971))

        self.assertEqual(pebble._parse_timestamp('2020-12-25T13:45:50.123456789+00:00'),
                         datetime_utc(2020, 12, 25, 13, 45, 50, 123457))

        tzinfo = datetime.timezone(datetime.timedelta(hours=-11, minutes=-30))
        self.assertEqual(pebble._parse_timestamp('2020-12-25T13:45:50.123456789-11:30'),
                         datetime.datetime(2020, 12, 25, 13, 45, 50, 123457, tzinfo=tzinfo))

        tzinfo = datetime.timezone(datetime.timedelta(hours=4))
        self.assertEqual(pebble._parse_timestamp('2000-01-02T03:04:05.006000+04:00'),
                         datetime.datetime(2000, 1, 2, 3, 4, 5, 6000, tzinfo=tzinfo))

        with self.assertRaises(ValueError):
            pebble._parse_timestamp('')

        with self.assertRaises(ValueError):
            pebble._parse_timestamp('foobar')

        with self.assertRaises(ValueError):
            pebble._parse_timestamp('2021-99-99T04:36:22Z')

        with self.assertRaises(ValueError):
            pebble._parse_timestamp(pebble._parse_timestamp('2021-02-10T04:36:22.118970777x'))

        with self.assertRaises(ValueError):
            pebble._parse_timestamp(pebble._parse_timestamp('2021-02-10T04:36:22.118970777-99:99'))


class TestTypes(unittest.TestCase):
    maxDiff = None

    def test_error(self):
        error = pebble.Error('error')
        self.assertIsInstance(error, Exception)

    def test_timeout_error(self):
        error = pebble.TimeoutError('timeout!')
        self.assertIsInstance(error, pebble.Error)
        self.assertIsInstance(error, TimeoutError)
        self.assertEqual(str(error), 'timeout!')

    def test_connection_error(self):
        error = pebble.ConnectionError('connerr!')
        self.assertIsInstance(error, pebble.Error)
        self.assertEqual(str(error), 'connerr!')

    def test_protocol_error(self):
        error = pebble.ProtocolError('protoerr!')
        self.assertIsInstance(error, pebble.Error)
        self.assertEqual(str(error), 'protoerr!')

    def test_path_error(self):
        error = pebble.PathError('not-found', 'thing not found')
        self.assertIsInstance(error, pebble.Error)
        self.assertEqual(error.kind, 'not-found')
        self.assertEqual(error.message, 'thing not found')
        self.assertEqual(str(error), 'not-found - thing not found')

    def test_api_error(self):
        body = {
            "result": {
                "message": "no services to start provided"
            },
            "status": "Bad Request",
            "status-code": 400,
            "type": "error"
        }
        error = pebble.APIError(body, 400, "Bad Request", "no services")
        self.assertIsInstance(error, pebble.Error)
        self.assertEqual(error.body, body)
        self.assertEqual(error.code, 400)
        self.assertEqual(error.status, 'Bad Request')
        self.assertEqual(error.message, 'no services')
        self.assertEqual(str(error), 'no services')

    def test_change_error(self):
        change = pebble.Change(
            id=pebble.ChangeID('1234'),
            kind='start',
            summary='Start service "foo"',
            status='Done',
            tasks=[],
            ready=True,
            err=None,
            spawn_time=datetime.datetime.now(),
            ready_time=datetime.datetime.now(),
        )
        error = pebble.ChangeError('Some error', change)
        self.assertIsInstance(error, pebble.Error)
        self.assertEqual(error.err, 'Some error')
        self.assertEqual(error.change, change)
        self.assertEqual(str(error), 'Some error')

    def test_warning_state(self):
        self.assertEqual(list(pebble.WarningState), [
            pebble.WarningState.ALL,
            pebble.WarningState.PENDING,
        ])
        self.assertEqual(pebble.WarningState.ALL.value, 'all')
        self.assertEqual(pebble.WarningState.PENDING.value, 'pending')

    def test_change_state(self):
        self.assertEqual(list(pebble.ChangeState), [
            pebble.ChangeState.ALL,
            pebble.ChangeState.IN_PROGRESS,
            pebble.ChangeState.READY,
        ])
        self.assertEqual(pebble.ChangeState.ALL.value, 'all')
        self.assertEqual(pebble.ChangeState.IN_PROGRESS.value, 'in-progress')
        self.assertEqual(pebble.ChangeState.READY.value, 'ready')

    def test_system_info_init(self):
        info = pebble.SystemInfo(version='1.2.3')
        self.assertEqual(info.version, '1.2.3')

    def test_system_info_from_dict(self):
        info = pebble.SystemInfo.from_dict({'version': '3.2.1'})
        self.assertEqual(info.version, '3.2.1')

    def test_warning_init(self):
        warning = pebble.Warning(
            message='Beware!',
            first_added=datetime_utc(2021, 1, 1, 1, 1, 1),
            last_added=datetime_utc(2021, 1, 26, 2, 3, 4),
            last_shown=None,
            expire_after='1s',
            repeat_after='2s',
        )
        self.assertEqual(warning.message, 'Beware!')
        self.assertEqual(warning.first_added, datetime_utc(2021, 1, 1, 1, 1, 1))
        self.assertEqual(warning.last_added, datetime_utc(2021, 1, 26, 2, 3, 4))
        self.assertEqual(warning.last_shown, None)
        self.assertEqual(warning.expire_after, '1s')
        self.assertEqual(warning.repeat_after, '2s')

    def test_warning_from_dict(self):
        d = {
            'message': 'Look out...',
            'first-added': '2020-12-25T17:18:54.016273778+13:00',
            'last-added': '2021-01-26T17:01:02.12345+13:00',
            'expire-after': '1s',
            'repeat-after': '2s',
        }
        warning = pebble.Warning.from_dict(d)
        self.assertEqual(warning.message, 'Look out...')
        self.assertEqual(warning.first_added, datetime_nzdt(2020, 12, 25, 17, 18, 54, 16274))
        self.assertEqual(warning.last_added, datetime_nzdt(2021, 1, 26, 17, 1, 2, 123450))
        self.assertEqual(warning.last_shown, None)
        self.assertEqual(warning.expire_after, '1s')
        self.assertEqual(warning.repeat_after, '2s')

        d['last-shown'] = None
        warning = pebble.Warning.from_dict(d)
        self.assertEqual(warning.last_shown, None)

        d['last-shown'] = '2021-08-04T03:02:01.000000000+13:00'
        warning = pebble.Warning.from_dict(d)
        self.assertEqual(warning.last_shown, datetime_nzdt(2021, 8, 4, 3, 2, 1))

        d['first-added'] = '2020-02-03T02:00:40.000000+00:00'
        d['last-added'] = '2021-03-04T03:01:41.100000+00:00'
        d['last-shown'] = '2022-04-05T06:02:42.200000+00:00'
        warning = pebble.Warning.from_dict(d)
        self.assertEqual(warning.first_added, datetime_utc(2020, 2, 3, 2, 0, 40, 0))
        self.assertEqual(warning.last_added, datetime_utc(2021, 3, 4, 3, 1, 41, 100000))
        self.assertEqual(warning.last_shown, datetime_utc(2022, 4, 5, 6, 2, 42, 200000))

    def test_task_progress_init(self):
        tp = pebble.TaskProgress(label='foo', done=3, total=7)
        self.assertEqual(tp.label, 'foo')
        self.assertEqual(tp.done, 3)
        self.assertEqual(tp.total, 7)

    def test_task_progress_from_dict(self):
        tp = pebble.TaskProgress.from_dict({
            'label': 'foo',
            'done': 3,
            'total': 7,
        })
        self.assertEqual(tp.label, 'foo')
        self.assertEqual(tp.done, 3)
        self.assertEqual(tp.total, 7)

    def test_task_id(self):
        task_id = pebble.TaskID('1234')
        self.assertEqual(task_id, '1234')

    def test_task_init(self):
        task = pebble.Task(
            id=pebble.TaskID('42'),
            kind='start',
            summary='Start service "svc"',
            status='Done',
            log=[],
            progress=pebble.TaskProgress(label='foo', done=3, total=7),
            spawn_time=datetime_nzdt(2021, 1, 28, 14, 37, 3, 270218),
            ready_time=datetime_nzdt(2021, 1, 28, 14, 37, 2, 247158),
        )
        self.assertEqual(task.id, '42')
        self.assertEqual(task.kind, 'start')
        self.assertEqual(task.summary, 'Start service "svc"')
        self.assertEqual(task.status, 'Done')
        self.assertEqual(task.log, [])
        self.assertEqual(task.progress.label, 'foo')
        self.assertEqual(task.progress.done, 3)
        self.assertEqual(task.progress.total, 7)
        self.assertEqual(task.spawn_time, datetime_nzdt(2021, 1, 28, 14, 37, 3, 270218))
        self.assertEqual(task.ready_time, datetime_nzdt(2021, 1, 28, 14, 37, 2, 247158))

    def test_task_from_dict(self):
        d = {
            "id": "78",
            "kind": "start",
            "progress": {
                "done": 1,
                "label": "",
                "total": 1,
            },
            "ready-time": "2021-01-28T14:37:03.270218778+13:00",
            "spawn-time": "2021-01-28T14:37:02.247158162+13:00",
            "status": "Done",
            "summary": 'Start service "svc"',
        }
        task = pebble.Task.from_dict(d)
        self.assertEqual(task.id, '78')
        self.assertEqual(task.kind, 'start')
        self.assertEqual(task.summary, 'Start service "svc"')
        self.assertEqual(task.status, 'Done')
        self.assertEqual(task.log, [])
        self.assertEqual(task.progress.label, '')
        self.assertEqual(task.progress.done, 1)
        self.assertEqual(task.progress.total, 1)
        self.assertEqual(task.ready_time, datetime_nzdt(2021, 1, 28, 14, 37, 3, 270219))
        self.assertEqual(task.spawn_time, datetime_nzdt(2021, 1, 28, 14, 37, 2, 247158))

        d['ready-time'] = '2021-01-28T14:37:03.270218778+00:00'
        d['spawn-time'] = '2021-01-28T14:37:02.247158162+00:00'
        task = pebble.Task.from_dict(d)
        self.assertEqual(task.ready_time, datetime_utc(2021, 1, 28, 14, 37, 3, 270219))
        self.assertEqual(task.spawn_time, datetime_utc(2021, 1, 28, 14, 37, 2, 247158))

    def test_change_id(self):
        change_id = pebble.ChangeID('1234')
        self.assertEqual(change_id, '1234')

    def test_change_init(self):
        change = pebble.Change(
            id=pebble.ChangeID('70'),
            kind='autostart',
            err='SILLY',
            ready=True,
            ready_time=datetime_nzdt(2021, 1, 28, 14, 37, 4, 291517),
            spawn_time=datetime_nzdt(2021, 1, 28, 14, 37, 2, 247202),
            status='Done',
            summary='Autostart service "svc"',
            tasks=[],
        )
        self.assertEqual(change.id, '70')
        self.assertEqual(change.kind, 'autostart')
        self.assertEqual(change.err, 'SILLY')
        self.assertEqual(change.ready, True)
        self.assertEqual(change.ready_time, datetime_nzdt(2021, 1, 28, 14, 37, 4, 291517))
        self.assertEqual(change.spawn_time, datetime_nzdt(2021, 1, 28, 14, 37, 2, 247202))
        self.assertEqual(change.status, 'Done')
        self.assertEqual(change.summary, 'Autostart service "svc"')
        self.assertEqual(change.tasks, [])

    def test_change_from_dict(self):
        d = {
            "id": "70",
            "kind": "autostart",
            "err": "SILLY",
            "ready": True,
            "ready-time": "2021-01-28T14:37:04.291517768+13:00",
            "spawn-time": "2021-01-28T14:37:02.247202105+13:00",
            "status": "Done",
            "summary": 'Autostart service "svc"',
            "tasks": [],
        }
        change = pebble.Change.from_dict(d)
        self.assertEqual(change.id, '70')
        self.assertEqual(change.kind, 'autostart')
        self.assertEqual(change.err, 'SILLY')
        self.assertEqual(change.ready, True)
        self.assertEqual(change.ready_time, datetime_nzdt(2021, 1, 28, 14, 37, 4, 291518))
        self.assertEqual(change.spawn_time, datetime_nzdt(2021, 1, 28, 14, 37, 2, 247202))
        self.assertEqual(change.status, 'Done')
        self.assertEqual(change.summary, 'Autostart service "svc"')
        self.assertEqual(change.tasks, [])

        d['ready-time'] = '2021-01-28T14:37:04.291517768+00:00'
        d['spawn-time'] = '2021-01-28T14:37:02.247202105+00:00'
        change = pebble.Change.from_dict(d)
        self.assertEqual(change.ready_time, datetime_utc(2021, 1, 28, 14, 37, 4, 291518))
        self.assertEqual(change.spawn_time, datetime_utc(2021, 1, 28, 14, 37, 2, 247202))

    def test_file_type(self):
        self.assertEqual(list(pebble.FileType), [
            pebble.FileType.FILE,
            pebble.FileType.DIRECTORY,
            pebble.FileType.SYMLINK,
            pebble.FileType.SOCKET,
            pebble.FileType.NAMED_PIPE,
            pebble.FileType.DEVICE,
            pebble.FileType.UNKNOWN,
        ])
        self.assertEqual(pebble.FileType.FILE.value, 'file')
        self.assertEqual(pebble.FileType.DIRECTORY.value, 'directory')
        self.assertEqual(pebble.FileType.SYMLINK.value, 'symlink')
        self.assertEqual(pebble.FileType.SOCKET.value, 'socket')
        self.assertEqual(pebble.FileType.NAMED_PIPE.value, 'named-pipe')
        self.assertEqual(pebble.FileType.DEVICE.value, 'device')
        self.assertEqual(pebble.FileType.UNKNOWN.value, 'unknown')

    def test_file_info_init(self):
        info = pebble.FileInfo('/etc/hosts', 'hosts', pebble.FileType.FILE, 123, 0o644,
                               datetime_nzdt(2021, 1, 28, 14, 37, 4, 291518),
                               12, 'bob', 34, 'staff')
        self.assertEqual(info.path, '/etc/hosts')
        self.assertEqual(info.name, 'hosts')
        self.assertEqual(info.type, pebble.FileType.FILE)
        self.assertEqual(info.size, 123)
        self.assertEqual(info.permissions, 0o644)
        self.assertEqual(info.last_modified, datetime_nzdt(2021, 1, 28, 14, 37, 4, 291518))
        self.assertEqual(info.user_id, 12)
        self.assertEqual(info.user, 'bob')
        self.assertEqual(info.group_id, 34)
        self.assertEqual(info.group, 'staff')

    def test_file_info_from_dict(self):
        d = {
            'path': '/etc',
            'name': 'etc',
            'type': 'directory',
            'permissions': '644',
            'last-modified': '2021-01-28T14:37:04.291517768+13:00',
        }
        info = pebble.FileInfo.from_dict(d)
        self.assertEqual(info.path, '/etc')
        self.assertEqual(info.name, 'etc')
        self.assertEqual(info.type, pebble.FileType.DIRECTORY)
        self.assertEqual(info.permissions, 0o644)
        self.assertEqual(info.last_modified, datetime_nzdt(2021, 1, 28, 14, 37, 4, 291518))
        self.assertIs(info.user_id, None)
        self.assertIs(info.user, None)
        self.assertIs(info.group_id, None)
        self.assertIs(info.group, None)

        d['type'] = 'foobar'
        d['size'] = 123
        d['user-id'] = 12
        d['user'] = 'bob'
        d['group-id'] = 34
        d['group'] = 'staff'
        info = pebble.FileInfo.from_dict(d)
        self.assertEqual(info.type, 'foobar')
        self.assertEqual(info.size, 123)
        self.assertEqual(info.user_id, 12)
        self.assertEqual(info.user, 'bob')
        self.assertEqual(info.group_id, 34)
        self.assertEqual(info.group, 'staff')


class TestPlan(unittest.TestCase):
    def test_no_args(self):
        with self.assertRaises(TypeError):
            pebble.Plan()

    def test_services(self):
        plan = pebble.Plan('')
        self.assertEqual(plan.services, {})

        plan = pebble.Plan('services:\n foo:\n  override: replace\n  command: echo foo')

        self.assertEqual(len(plan.services), 1)
        self.assertEqual(plan.services['foo'].name, 'foo')
        self.assertEqual(plan.services['foo'].override, 'replace')
        self.assertEqual(plan.services['foo'].command, 'echo foo')

        # Should be read-only ("can't set attribute")
        with self.assertRaises(AttributeError):
            plan.services = {}

    def test_yaml(self):
        # Starting with nothing, we get the empty result
        plan = pebble.Plan('')
        self.assertEqual(plan.to_yaml(), '{}\n')
        self.assertEqual(str(plan), '{}\n')

        # With a service, we return validated yaml content.
        raw = '''\
services:
 foo:
  override: replace
  command: echo foo
'''
        plan = pebble.Plan(raw)
        reformed = yaml.safe_dump(yaml.safe_load(raw))
        self.assertEqual(plan.to_yaml(), reformed)
        self.assertEqual(str(plan), reformed)


class TestLayer(unittest.TestCase):
    def _assert_empty(self, layer):
        self.assertEqual(layer.summary, '')
        self.assertEqual(layer.description, '')
        self.assertEqual(layer.services, {})
        self.assertEqual(layer.to_dict(), {})

    def test_no_args(self):
        s = pebble.Layer()
        self._assert_empty(s)

    def test_dict(self):
        s = pebble.Layer({})
        self._assert_empty(s)

        d = {
            'summary': 'Sum Mary',
            'description': 'The quick brown fox!',
            'services': {
                'foo': {
                    'summary': 'Foo',
                    'command': 'echo foo',
                },
                'bar': {
                    'summary': 'Bar',
                    'command': 'echo bar',
                },
            }
        }
        s = pebble.Layer(d)
        self.assertEqual(s.summary, 'Sum Mary')
        self.assertEqual(s.description, 'The quick brown fox!')
        self.assertEqual(s.services['foo'].name, 'foo')
        self.assertEqual(s.services['foo'].summary, 'Foo')
        self.assertEqual(s.services['foo'].command, 'echo foo')
        self.assertEqual(s.services['bar'].name, 'bar')
        self.assertEqual(s.services['bar'].summary, 'Bar')
        self.assertEqual(s.services['bar'].command, 'echo bar')

        self.assertEqual(s.to_dict(), d)

    def test_yaml(self):
        s = pebble.Layer('')
        self._assert_empty(s)

        yaml = """description: The quick brown fox!
services:
  bar:
    command: echo bar
    environment:
      ENV1: value1
      ENV2: value2
    summary: Bar
  foo:
    command: echo foo
    summary: Foo
summary: Sum Mary
"""
        s = pebble.Layer(yaml)
        self.assertEqual(s.summary, 'Sum Mary')
        self.assertEqual(s.description, 'The quick brown fox!')
        self.assertEqual(s.services['foo'].name, 'foo')
        self.assertEqual(s.services['foo'].summary, 'Foo')
        self.assertEqual(s.services['foo'].command, 'echo foo')
        self.assertEqual(s.services['bar'].name, 'bar')
        self.assertEqual(s.services['bar'].summary, 'Bar')
        self.assertEqual(s.services['bar'].command, 'echo bar')
        self.assertEqual(s.services['bar'].environment,
                         {'ENV1': 'value1', 'ENV2': 'value2'})

        self.assertEqual(s.to_yaml(), yaml)
        self.assertEqual(str(s), yaml)


class TestService(unittest.TestCase):
    def _assert_empty(self, service, name):
        self.assertEqual(service.name, name)
        self.assertEqual(service.summary, '')
        self.assertEqual(service.description, '')
        self.assertEqual(service.startup, '')
        self.assertEqual(service.override, '')
        self.assertEqual(service.command, '')
        self.assertEqual(service.after, [])
        self.assertEqual(service.before, [])
        self.assertEqual(service.requires, [])
        self.assertEqual(service.environment, {})
        self.assertEqual(service.to_dict(), {})

    def test_name_only(self):
        s = pebble.Service('Name 0')
        self._assert_empty(s, 'Name 0')

    def test_dict(self):
        s = pebble.Service('Name 1', {})
        self._assert_empty(s, 'Name 1')

        d = {
            'summary': 'Sum Mary',
            'description': 'The lazy quick brown',
            'startup': 'Start Up',
            'override': 'override',
            'command': 'echo sum mary',
            'after': ['a1', 'a2'],
            'before': ['b1', 'b2'],
            'requires': ['r1', 'r2'],
            'environment': {'k1': 'v1', 'k2': 'v2'},
        }
        s = pebble.Service('Name 2', d)
        self.assertEqual(s.name, 'Name 2')
        self.assertEqual(s.description, 'The lazy quick brown')
        self.assertEqual(s.startup, 'Start Up')
        self.assertEqual(s.override, 'override')
        self.assertEqual(s.command, 'echo sum mary')
        self.assertEqual(s.after, ['a1', 'a2'])
        self.assertEqual(s.before, ['b1', 'b2'])
        self.assertEqual(s.requires, ['r1', 'r2'])
        self.assertEqual(s.environment, {'k1': 'v1', 'k2': 'v2'})

        self.assertEqual(s.to_dict(), d)

        # Ensure pebble.Service has made copies of mutable objects
        s.after.append('a3')
        s.before.append('b3')
        s.requires.append('r3')
        s.environment['k3'] = 'v3'
        self.assertEqual(s.after, ['a1', 'a2', 'a3'])
        self.assertEqual(s.before, ['b1', 'b2', 'b3'])
        self.assertEqual(s.requires, ['r1', 'r2', 'r3'])
        self.assertEqual(s.environment, {'k1': 'v1', 'k2': 'v2', 'k3': 'v3'})
        self.assertEqual(d['after'], ['a1', 'a2'])
        self.assertEqual(d['before'], ['b1', 'b2'])
        self.assertEqual(d['requires'], ['r1', 'r2'])
        self.assertEqual(d['environment'], {'k1': 'v1', 'k2': 'v2'})


class TestServiceInfo(unittest.TestCase):
    def test_service_startup(self):
        self.assertEqual(list(pebble.ServiceStartup), [
            pebble.ServiceStartup.ENABLED,
            pebble.ServiceStartup.DISABLED,
        ])
        self.assertEqual(pebble.ServiceStartup.ENABLED.value, 'enabled')
        self.assertEqual(pebble.ServiceStartup.DISABLED.value, 'disabled')

    def test_service_status(self):
        self.assertEqual(list(pebble.ServiceStatus), [
            pebble.ServiceStatus.ACTIVE,
            pebble.ServiceStatus.INACTIVE,
            pebble.ServiceStatus.ERROR,
        ])
        self.assertEqual(pebble.ServiceStatus.ACTIVE.value, 'active')
        self.assertEqual(pebble.ServiceStatus.INACTIVE.value, 'inactive')
        self.assertEqual(pebble.ServiceStatus.ERROR.value, 'error')

    def test_service_info(self):
        s = pebble.ServiceInfo('svc1', pebble.ServiceStartup.ENABLED, pebble.ServiceStatus.ACTIVE)
        self.assertEqual(s.name, 'svc1')
        self.assertEqual(s.startup, pebble.ServiceStartup.ENABLED)
        self.assertEqual(s.current, pebble.ServiceStatus.ACTIVE)

        s = pebble.ServiceInfo.from_dict({
            'name': 'svc2',
            'startup': 'disabled',
            'current': 'inactive',
        })
        self.assertEqual(s.name, 'svc2')
        self.assertEqual(s.startup, pebble.ServiceStartup.DISABLED)
        self.assertEqual(s.current, pebble.ServiceStatus.INACTIVE)

        s = pebble.ServiceInfo.from_dict({
            'name': 'svc2',
            'startup': 'thingy',
            'current': 'bob',
        })
        self.assertEqual(s.name, 'svc2')
        self.assertEqual(s.startup, 'thingy')
        self.assertEqual(s.current, 'bob')

    def test_is_running(self):
        s = pebble.ServiceInfo('s', pebble.ServiceStartup.ENABLED, pebble.ServiceStatus.ACTIVE)
        self.assertTrue(s.is_running())
        for current in [pebble.ServiceStatus.INACTIVE, pebble.ServiceStatus.ERROR, 'other']:
            s = pebble.ServiceInfo('s', pebble.ServiceStartup.ENABLED, current)
            self.assertFalse(s.is_running())


class MockClient(pebble.Client):
    """Mock Pebble client that simply records reqeusts and returns stored responses."""

    def __init__(self):
        self.requests = []
        self.responses = []

    def _request(self, method, path, query=None, body=None):
        self.requests.append((method, path, query, body))
        return self.responses.pop(0)

    def _request_raw(self, method, path, query=None, headers=None, data=None):
        self.requests.append((method, path, query, headers, data))
        headers, body = self.responses.pop(0)
        return MockHTTPResponse(headers, body)


class MockHTTPResponse:
    def __init__(self, headers, body):
        self.headers = headers
        reader = io.BytesIO(body)
        self.read = reader.read


class MockTime:
    """Mocked versions of time.time() and time.sleep().

    MockTime.sleep() advances the clock and MockTime.time() returns the current time.
    """

    def __init__(self):
        self._time = 0

    def time(self):
        return self._time

    def sleep(self, delay):
        self._time += delay


class TestClient(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.client = MockClient()

    def test_client_init(self):
        pebble.Client(socket_path='foo')  # test that constructor runs
        with self.assertRaises(ValueError):
            pebble.Client()  # socket_path arg required

    def test_get_system_info(self):
        self.client.responses.append({
            "result": {
                "version": "1.2.3",
                "extra-field": "foo",
            },
            "status": "OK",
            "status-code": 200,
            "type": "sync"
        })
        info = self.client.get_system_info()
        self.assertEqual(info.version, '1.2.3')
        self.assertEqual(self.client.requests, [
            ('GET', '/v1/system-info', None, None),
        ])

    def test_get_warnings(self):
        empty = {
            "result": [],
            "status": "OK",
            "status-code": 200,
            "type": "sync"
        }
        self.client.responses.append(empty)
        warnings = self.client.get_warnings()
        self.assertEqual(warnings, [])

        self.client.responses.append(empty)
        warnings = self.client.get_warnings(select=pebble.WarningState.ALL)
        self.assertEqual(warnings, [])

        self.assertEqual(self.client.requests, [
            ('GET', '/v1/warnings', {'select': 'pending'}, None),
            ('GET', '/v1/warnings', {'select': 'all'}, None),
        ])

    def test_ack_warnings(self):
        self.client.responses.append({
            "result": 0,
            "status": "OK",
            "status-code": 200,
            "type": "sync"
        })
        num = self.client.ack_warnings(datetime_nzdt(2021, 1, 28, 15, 11, 0))
        self.assertEqual(num, 0)
        self.assertEqual(self.client.requests, [
            ('POST', '/v1/warnings', None, {
                'action': 'okay',
                'timestamp': '2021-01-28T15:11:00+13:00',
            }),
        ])

    def build_mock_change_dict(self):
        return {
            "id": "70",
            "kind": "autostart",
            "ready": True,
            "ready-time": "2021-01-28T14:37:04.291517768+13:00",
            "spawn-time": "2021-01-28T14:37:02.247202105+13:00",
            "status": "Done",
            "summary": 'Autostart service "svc"',
            "tasks": [
                {
                    "id": "78",
                    "kind": "start",
                    "progress": {
                        "done": 1,
                        "label": "",
                        "total": 1,
                        "extra-field": "foo",
                    },
                    "ready-time": "2021-01-28T14:37:03.270218778+13:00",
                    "spawn-time": "2021-01-28T14:37:02.247158162+13:00",
                    "status": "Done",
                    "summary": 'Start service "svc"',
                    "extra-field": "foo",
                },
            ],
            "extra-field": "foo",
        }

    def assert_mock_change(self, change):
        self.assertEqual(change.id, '70')
        self.assertEqual(change.kind, 'autostart')
        self.assertEqual(change.summary, 'Autostart service "svc"')
        self.assertEqual(change.status, 'Done')
        self.assertEqual(len(change.tasks), 1)
        self.assertEqual(change.tasks[0].id, '78')
        self.assertEqual(change.tasks[0].kind, 'start')
        self.assertEqual(change.tasks[0].summary, 'Start service "svc"')
        self.assertEqual(change.tasks[0].status, 'Done')
        self.assertEqual(change.tasks[0].log, [])
        self.assertEqual(change.tasks[0].progress.done, 1)
        self.assertEqual(change.tasks[0].progress.label, '')
        self.assertEqual(change.tasks[0].progress.total, 1)
        self.assertEqual(change.tasks[0].ready_time,
                         datetime_nzdt(2021, 1, 28, 14, 37, 3, 270219))
        self.assertEqual(change.tasks[0].spawn_time,
                         datetime_nzdt(2021, 1, 28, 14, 37, 2, 247158))
        self.assertEqual(change.ready, True)
        self.assertEqual(change.err, None)
        self.assertEqual(change.ready_time, datetime_nzdt(2021, 1, 28, 14, 37, 4, 291518))
        self.assertEqual(change.spawn_time, datetime_nzdt(2021, 1, 28, 14, 37, 2, 247202))

    def test_get_changes(self):
        empty = {
            "result": [],
            "status": "OK",
            "status-code": 200,
            "type": "sync"
        }
        self.client.responses.append(empty)
        changes = self.client.get_changes()
        self.assertEqual(changes, [])

        self.client.responses.append(empty)
        changes = self.client.get_changes(select=pebble.ChangeState.ALL)
        self.assertEqual(changes, [])

        self.client.responses.append(empty)
        changes = self.client.get_changes(select=pebble.ChangeState.ALL, service='foo')
        self.assertEqual(changes, [])

        self.client.responses.append({
            "result": [
                self.build_mock_change_dict(),
            ],
            "status": "OK",
            "status-code": 200,
            "type": "sync"
        })
        changes = self.client.get_changes()
        self.assertEqual(len(changes), 1)
        self.assert_mock_change(changes[0])

        self.assertEqual(self.client.requests, [
            ('GET', '/v1/changes', {'select': 'in-progress'}, None),
            ('GET', '/v1/changes', {'select': 'all'}, None),
            ('GET', '/v1/changes', {'select': 'all', 'for': 'foo'}, None),
            ('GET', '/v1/changes', {'select': 'in-progress'}, None),
        ])

    def test_get_change(self):
        self.client.responses.append({
            "result": self.build_mock_change_dict(),
            "status": "OK",
            "status-code": 200,
            "type": "sync"
        })
        change = self.client.get_change('70')
        self.assert_mock_change(change)
        self.assertEqual(self.client.requests, [
            ('GET', '/v1/changes/70', None, None),
        ])

    def test_abort_change(self):
        self.client.responses.append({
            "result": self.build_mock_change_dict(),
            "status": "OK",
            "status-code": 200,
            "type": "sync"
        })
        change = self.client.abort_change('70')
        self.assert_mock_change(change)
        self.assertEqual(self.client.requests, [
            ('POST', '/v1/changes/70', None, {'action': 'abort'}),
        ])

    def _services_action_helper(self, action, api_func, services):
        self.client.responses.append({
            "change": "70",
            "result": None,
            "status": "Accepted",
            "status-code": 202,
            "type": "async"
        })
        change = self.build_mock_change_dict()
        change['ready'] = False
        self.client.responses.append({
            "result": change,
            "status": "OK",
            "status-code": 200,
            "type": "sync"
        })
        change = self.build_mock_change_dict()
        change['ready'] = True
        self.client.responses.append({
            "result": change,
            "status": "OK",
            "status-code": 200,
            "type": "sync"
        })
        change_id = api_func()
        self.assertEqual(change_id, '70')
        self.assertEqual(self.client.requests, [
            ('POST', '/v1/services', None, {'action': action, 'services': services}),
            ('GET', '/v1/changes/70', None, None),
            ('GET', '/v1/changes/70', None, None),
        ])

    def _services_action_async_helper(self, action, api_func, services):
        self.client.responses.append({
            "change": "70",
            "result": None,
            "status": "Accepted",
            "status-code": 202,
            "type": "async"
        })
        change_id = api_func(timeout=0)
        self.assertEqual(change_id, '70')
        self.assertEqual(self.client.requests, [
            ('POST', '/v1/services', None, {'action': action, 'services': services}),
        ])

    def test_autostart_services(self):
        self._services_action_helper('autostart', self.client.autostart_services, [])

    def test_autostart_services_async(self):
        self._services_action_async_helper('autostart', self.client.autostart_services, [])

    def test_start_services(self):
        def api_func():
            return self.client.start_services(['svc'])
        self._services_action_helper('start', api_func, ['svc'])

        with self.assertRaises(TypeError):
            self.client.start_services(1)

        with self.assertRaises(TypeError):
            self.client.start_services([1])

        with self.assertRaises(TypeError):
            self.client.start_services([['foo']])

    def test_start_services_async(self):
        def api_func(timeout=30):
            return self.client.start_services(['svc'], timeout=timeout)
        self._services_action_async_helper('start', api_func, ['svc'])

    def test_stop_services(self):
        def api_func():
            return self.client.stop_services(['svc'])
        self._services_action_helper('stop', api_func, ['svc'])

        with self.assertRaises(TypeError):
            self.client.stop_services(1)

        with self.assertRaises(TypeError):
            self.client.stop_services([1])

        with self.assertRaises(TypeError):
            self.client.stop_services([['foo']])

    def test_stop_services_async(self):
        def api_func(timeout=30):
            return self.client.stop_services(['svc'], timeout=timeout)
        self._services_action_async_helper('stop', api_func, ['svc'])

    def test_change_error(self):
        self.client.responses.append({
            "change": "70",
            "result": None,
            "status": "Accepted",
            "status-code": 202,
            "type": "async"
        })
        change = self.build_mock_change_dict()
        change['err'] = 'Some kind of service error'
        self.client.responses.append({
            "result": change,
            "status": "OK",
            "status-code": 200,
            "type": "sync"
        })
        with self.assertRaises(pebble.ChangeError) as cm:
            self.client.autostart_services()
        self.assertIsInstance(cm.exception, pebble.Error)
        self.assertEqual(cm.exception.err, 'Some kind of service error')
        self.assertIsInstance(cm.exception.change, pebble.Change)
        self.assertEqual(cm.exception.change.id, '70')

        self.assertEqual(self.client.requests, [
            ('POST', '/v1/services', None, {'action': 'autostart', 'services': []}),
            ('GET', '/v1/changes/70', None, None),
        ])

    def test_wait_change_timeout(self):
        with unittest.mock.patch('ops.pebble.time', MockTime()):
            change = self.build_mock_change_dict()
            change['ready'] = False
            for _ in range(3):
                self.client.responses.append({
                    "result": change,
                    "status": "OK",
                    "status-code": 200,
                    "type": "sync"
                })

            with self.assertRaises(pebble.TimeoutError) as cm:
                self.client.wait_change('70', timeout=3, delay=1)
            self.assertIsInstance(cm.exception, pebble.Error)
            self.assertIsInstance(cm.exception, TimeoutError)

            self.assertEqual(self.client.requests, [
                ('GET', '/v1/changes/70', None, None),
                ('GET', '/v1/changes/70', None, None),
                ('GET', '/v1/changes/70', None, None),
            ])

    def test_wait_change_error(self):
        change = self.build_mock_change_dict()
        change['err'] = 'Some kind of service error'
        self.client.responses.append({
            "result": change,
            "status": "OK",
            "status-code": 200,
            "type": "sync"
        })
        # wait_change() itself shouldn't raise an error
        response = self.client.wait_change('70')
        self.assertEqual(response.id, '70')
        self.assertEqual(response.err, 'Some kind of service error')

        self.assertEqual(self.client.requests, [
            ('GET', '/v1/changes/70', None, None),
        ])

    def test_add_layer(self):
        okay_response = {
            "result": True,
            "status": "OK",
            "status-code": 200,
            "type": "sync"
        }
        self.client.responses.append(okay_response)
        self.client.responses.append(okay_response)
        self.client.responses.append(okay_response)
        self.client.responses.append(okay_response)

        layer_yaml = """
services:
  foo:
    command: echo bar
    override: replace
"""[1:]
        layer = pebble.Layer(layer_yaml)

        self.client.add_layer('a', layer)
        self.client.add_layer('b', layer.to_yaml())
        self.client.add_layer('c', layer.to_dict())
        self.client.add_layer('d', layer, combine=True)

        def build_expected(label, combine):
            return {
                'action': 'add',
                'combine': combine,
                'label': label,
                'format': 'yaml',
                'layer': layer_yaml,
            }

        self.assertEqual(self.client.requests, [
            ('POST', '/v1/layers', None, build_expected('a', False)),
            ('POST', '/v1/layers', None, build_expected('b', False)),
            ('POST', '/v1/layers', None, build_expected('c', False)),
            ('POST', '/v1/layers', None, build_expected('d', True)),
        ])

    def test_add_layer_invalid_type(self):
        with self.assertRaises(TypeError):
            self.client.add_layer('foo', 42)
        with self.assertRaises(TypeError):
            self.client.add_layer(42, 'foo')

        # combine is a keyword-only arg (should be combine=True)
        with self.assertRaises(TypeError):
            self.client.add_layer('foo', {}, True)

    def test_get_plan(self):
        plan_yaml = """
services:
  foo:
    command: echo bar
    override: replace
"""[1:]
        self.client.responses.append({
            "result": plan_yaml,
            "status": "OK",
            "status-code": 200,
            "type": "sync"
        })
        plan = self.client.get_plan()
        self.assertEqual(plan.to_yaml(), plan_yaml)
        self.assertEqual(len(plan.services), 1)
        self.assertEqual(plan.services['foo'].command, 'echo bar')
        self.assertEqual(plan.services['foo'].override, 'replace')

        self.assertEqual(self.client.requests, [
            ('GET', '/v1/plan', {'format': 'yaml'}, None),
        ])

    def test_get_services_all(self):
        self.client.responses.append({
            "result": [
                {
                    "current": "inactive",
                    "name": "svc1",
                    "startup": "disabled"
                },
                {
                    "current": "active",
                    "name": "svc2",
                    "startup": "enabled"
                }
            ],
            "status": "OK",
            "status-code": 200,
            "type": "sync"
        })
        services = self.client.get_services()
        self.assertEqual(len(services), 2)
        self.assertEqual(services[0].name, 'svc1')
        self.assertEqual(services[0].startup, pebble.ServiceStartup.DISABLED)
        self.assertEqual(services[0].current, pebble.ServiceStatus.INACTIVE)
        self.assertEqual(services[1].name, 'svc2')
        self.assertEqual(services[1].startup, pebble.ServiceStartup.ENABLED)
        self.assertEqual(services[1].current, pebble.ServiceStatus.ACTIVE)

        self.assertEqual(self.client.requests, [
            ('GET', '/v1/services', None, None),
        ])

    def test_get_services_names(self):
        self.client.responses.append({
            "result": [
                {
                    "current": "inactive",
                    "name": "svc1",
                    "startup": "disabled"
                },
                {
                    "current": "active",
                    "name": "svc2",
                    "startup": "enabled"
                }
            ],
            "status": "OK",
            "status-code": 200,
            "type": "sync"
        })
        services = self.client.get_services(['svc1', 'svc2'])
        self.assertEqual(len(services), 2)
        self.assertEqual(services[0].name, 'svc1')
        self.assertEqual(services[0].startup, pebble.ServiceStartup.DISABLED)
        self.assertEqual(services[0].current, pebble.ServiceStatus.INACTIVE)
        self.assertEqual(services[1].name, 'svc2')
        self.assertEqual(services[1].startup, pebble.ServiceStartup.ENABLED)
        self.assertEqual(services[1].current, pebble.ServiceStatus.ACTIVE)

        self.client.responses.append({
            "result": [
                {
                    "current": "active",
                    "name": "svc2",
                    "startup": "enabled"
                }
            ],
            "status": "OK",
            "status-code": 200,
            "type": "sync"
        })
        services = self.client.get_services(['svc2'])
        self.assertEqual(len(services), 1)
        self.assertEqual(services[0].name, 'svc2')
        self.assertEqual(services[0].startup, pebble.ServiceStartup.ENABLED)
        self.assertEqual(services[0].current, pebble.ServiceStatus.ACTIVE)

        self.assertEqual(self.client.requests, [
            ('GET', '/v1/services', {'names': 'svc1,svc2'}, None),
            ('GET', '/v1/services', {'names': 'svc2'}, None),
        ])

    def test_pull_text(self):
        self.client.responses.append((
            {'Content-Type': 'multipart/form-data; boundary=01234567890123456789012345678901'},
            b"""
--01234567890123456789012345678901
Content-Disposition: form-data; name="files"; filename="/etc/hosts"

127.0.0.1 localhost  # """ + b'\xf0\x9f\x98\x80' + b"""
--01234567890123456789012345678901
Content-Disposition: form-data; name="response"

{
    "result": [{"path": "/etc/hosts"}],
    "status": "OK",
    "status-code": 200,
    "type": "sync"
}
--01234567890123456789012345678901--
""",
        ))

        content = self.client.pull('/etc/hosts').read()
        self.assertEqual(content, '127.0.0.1 localhost  # 😀')

        self.assertEqual(self.client.requests, [
            ('GET', '/v1/files', {'action': 'read', 'path': '/etc/hosts'},
                {'Accept': 'multipart/form-data'}, None),
        ])

    def test_pull_binary(self):
        self.client.responses.append((
            {'Content-Type': 'multipart/form-data; boundary=01234567890123456789012345678901'},
            b"""
--01234567890123456789012345678901
Content-Disposition: form-data; name="files"; filename="/etc/hosts"

127.0.0.1 localhost  # """ + b'\xf0\x9f\x98\x80' + b"""
--01234567890123456789012345678901
Content-Disposition: form-data; name="response"

{
    "result": [{"path": "/etc/hosts"}],
    "status": "OK",
    "status-code": 200,
    "type": "sync"
}
--01234567890123456789012345678901--
""",
        ))

        content = self.client.pull('/etc/hosts', encoding=None).read()
        self.assertEqual(content, b'127.0.0.1 localhost  # \xf0\x9f\x98\x80')

        self.assertEqual(self.client.requests, [
            ('GET', '/v1/files', {'action': 'read', 'path': '/etc/hosts'},
                {'Accept': 'multipart/form-data'}, None),
        ])

    def test_pull_path_error(self):
        self.client.responses.append((
            {'Content-Type': 'multipart/form-data; boundary=01234567890123456789012345678901'},
            b"""
--01234567890123456789012345678901
Content-Disposition: form-data; name="response"

{
    "result": [
        {"path": "/etc/hosts", "error": {"kind": "not-found", "message": "not found"}}
    ],
    "status": "OK",
    "status-code": 200,
    "type": "sync"
}
--01234567890123456789012345678901--
""",
        ))

        with self.assertRaises(pebble.PathError) as cm:
            self.client.pull('/etc/hosts')
        self.assertIsInstance(cm.exception, pebble.Error)
        self.assertEqual(cm.exception.kind, 'not-found')
        self.assertEqual(cm.exception.message, 'not found')

        self.assertEqual(self.client.requests, [
            ('GET', '/v1/files', {'action': 'read', 'path': '/etc/hosts'},
                {'Accept': 'multipart/form-data'}, None),
        ])

    def test_pull_protocol_errors(self):
        self.client.responses.append(({'Content-Type': 'ct'}, b''))
        with self.assertRaises(pebble.ProtocolError) as cm:
            self.client.pull('/etc/hosts')
        self.assertIsInstance(cm.exception, pebble.Error)
        self.assertEqual(str(cm.exception),
                         "expected Content-Type 'multipart/form-data', got 'ct'")

        self.client.responses.append(({'Content-Type': 'multipart/form-data'}, b''))
        with self.assertRaises(pebble.ProtocolError) as cm:
            self.client.pull('/etc/hosts')
        self.assertEqual(str(cm.exception), "invalid boundary ''")

        self.client.responses.append((
            {'Content-Type': 'multipart/form-data; boundary=01234567890123456789012345678901'},
            b"""
--01234567890123456789012345678901
Content-Disposition: form-data; name="files"; filename="/bad"

bad path
--01234567890123456789012345678901--
""",
        ))
        with self.assertRaises(pebble.ProtocolError) as cm:
            self.client.pull('/etc/hosts')
        self.assertEqual(str(cm.exception), "path not expected: /bad")

        self.client.responses.append((
            {'Content-Type': 'multipart/form-data; boundary=01234567890123456789012345678901'},
            b"""
--01234567890123456789012345678901
Content-Disposition: form-data; name="files"; filename="/etc/hosts"

bad path
--01234567890123456789012345678901--
""",
        ))
        with self.assertRaises(pebble.ProtocolError) as cm:
            self.client.pull('/etc/hosts')
        self.assertEqual(str(cm.exception), 'no "response" field in multipart body')

    def test_push_str(self):
        self._test_push_str('content 😀')

    def test_push_text(self):
        self._test_push_str(io.StringIO('content 😀'))

    def _test_push_str(self, source):
        self.client.responses.append((
            {'Content-Type': 'application/json'},
            b"""
{
    "result": [
        {"path": "/foo/bar"}
    ],
    "status": "OK",
    "status-code": 200,
    "type": "sync"
}
""",
        ))

        self.client.push('/foo/bar', source)

        self.assertEqual(len(self.client.requests), 1)
        request = self.client.requests[0]
        self.assertEqual(request[:3], ('POST', '/v1/files', None))

        headers, body = request[3:]
        content_type = headers['Content-Type']
        req, filename, content = self._parse_write_multipart(content_type, body)
        self.assertEqual(filename, '/foo/bar')
        self.assertEqual(content, b'content \xf0\x9f\x98\x80')
        self.assertEqual(req, {
            'action': 'write',
            'files': [{'path': '/foo/bar'}],
        })

    def test_push_bytes(self):
        self._test_push_bytes(b'content \xf0\x9f\x98\x80')

    def test_push_binary(self):
        self._test_push_bytes(io.BytesIO(b'content \xf0\x9f\x98\x80'))

    def _test_push_bytes(self, source):
        self.client.responses.append((
            {'Content-Type': 'application/json'},
            b"""
{
    "result": [
        {"path": "/foo/bar"}
    ],
    "status": "OK",
    "status-code": 200,
    "type": "sync"
}
""",
        ))

        self.client.push('/foo/bar', source)

        self.assertEqual(len(self.client.requests), 1)
        request = self.client.requests[0]
        self.assertEqual(request[:3], ('POST', '/v1/files', None))

        headers, body = request[3:]
        content_type = headers['Content-Type']
        req, filename, content = self._parse_write_multipart(content_type, body)
        self.assertEqual(filename, '/foo/bar')
        self.assertEqual(content, b'content \xf0\x9f\x98\x80')
        self.assertEqual(req, {
            'action': 'write',
            'files': [{'path': '/foo/bar'}],
        })

    def test_push_all_options(self):
        self.client.responses.append((
            {'Content-Type': 'application/json'},
            b"""
{
    "result": [
        {"path": "/foo/bar"}
    ],
    "status": "OK",
    "status-code": 200,
    "type": "sync"
}
""",
        ))

        self.client.push('/foo/bar', 'content', make_dirs=True, permissions=0o600,
                         user_id=12, user='bob', group_id=34, group='staff')

        self.assertEqual(len(self.client.requests), 1)
        request = self.client.requests[0]
        self.assertEqual(request[:3], ('POST', '/v1/files', None))

        headers, body = request[3:]
        content_type = headers['Content-Type']
        req, filename, content = self._parse_write_multipart(content_type, body)
        self.assertEqual(filename, '/foo/bar')
        self.assertEqual(content, b'content')
        self.assertEqual(req, {
            'action': 'write',
            'files': [{
                'path': '/foo/bar',
                'make-dirs': True,
                'permissions': '600',
                'user-id': 12,
                'user': 'bob',
                'group-id': 34,
                'group': 'staff',
            }],
        })

    def test_push_uid_gid(self):
        self.client.responses.append((
            {'Content-Type': 'application/json'},
            b"""
{
    "result": [
        {"path": "/foo/bar"}
    ],
    "status": "OK",
    "status-code": 200,
    "type": "sync"
}
""",
        ))

        self.client.push('/foo/bar', 'content', user_id=12, group_id=34)

        self.assertEqual(len(self.client.requests), 1)
        request = self.client.requests[0]
        self.assertEqual(request[:3], ('POST', '/v1/files', None))

        headers, body = request[3:]
        content_type = headers['Content-Type']
        req, filename, content = self._parse_write_multipart(content_type, body)
        self.assertEqual(filename, '/foo/bar')
        self.assertEqual(content, b'content')
        self.assertEqual(req, {
            'action': 'write',
            'files': [{
                'path': '/foo/bar',
                'user-id': 12,
                'group-id': 34,
            }],
        })

    def test_push_path_error(self):
        self.client.responses.append((
            {'Content-Type': 'application/json'},
            b"""
{
    "result": [
        {"path": "/foo/bar", "error": {"kind": "not-found", "message": "not found"}}
    ],
    "status": "OK",
    "status-code": 200,
    "type": "sync"
}
""",
        ))

        with self.assertRaises(pebble.PathError) as cm:
            self.client.push('/foo/bar', 'content')
        self.assertEqual(cm.exception.kind, 'not-found')
        self.assertEqual(cm.exception.message, 'not found')

        self.assertEqual(len(self.client.requests), 1)
        request = self.client.requests[0]
        self.assertEqual(request[:3], ('POST', '/v1/files', None))

        headers, body = request[3:]
        content_type = headers['Content-Type']
        req, filename, content = self._parse_write_multipart(content_type, body)
        self.assertEqual(filename, '/foo/bar')
        self.assertEqual(content, b'content')
        self.assertEqual(req, {
            'action': 'write',
            'files': [{'path': '/foo/bar'}],
        })

    def _parse_write_multipart(self, content_type, body):
        ctype, options = cgi.parse_header(content_type)
        self.assertEqual(ctype, 'multipart/form-data')
        boundary = options['boundary']

        # We have to manually write the Content-Type with boundary, because
        # email.parser expects the entire multipart message with headers.
        parser = email.parser.BytesFeedParser()
        parser.feed(b'Content-Type: multipart/form-data; boundary=' +
                    boundary.encode('utf-8') + b'\r\n\r\n')
        parser.feed(body)
        message = parser.close()

        req = None
        filename = None
        content = None
        for part in message.walk():
            name = part.get_param('name', header='Content-Disposition')
            if name == 'request':
                req = json.loads(part.get_payload())
            elif name == 'files':
                # decode=True, ironically, avoids decoding bytes to str
                content = part.get_payload(decode=True)
                filename = part.get_filename()
        return (req, filename, content)

    def test_list_files_path(self):
        self.client.responses.append({
            "result": [
                {
                    'path': '/etc/hosts',
                    'name': 'hosts',
                    'type': 'file',
                    'size': 123,
                    'permissions': '644',
                    'last-modified': '2021-01-28T14:37:04.291517768+13:00',
                    'user-id': 12,
                    'user': 'bob',
                    'group-id': 34,
                    'group': 'staff',
                },
                {
                    'path': '/etc/nginx',
                    'name': 'nginx',
                    'type': 'directory',
                    'permissions': '755',
                    'last-modified': '2020-01-01T01:01:01.000000+13:00',
                },
            ],
            'status': 'OK',
            'status-code': 200,
            'type': 'sync',
        })
        infos = self.client.list_files('/etc')

        self.assertEqual(len(infos), 2)
        self.assertEqual(infos[0].path, '/etc/hosts')
        self.assertEqual(infos[0].name, 'hosts')
        self.assertEqual(infos[0].type, pebble.FileType.FILE)
        self.assertEqual(infos[0].size, 123)
        self.assertEqual(infos[0].permissions, 0o644)
        self.assertEqual(infos[0].last_modified, datetime_nzdt(2021, 1, 28, 14, 37, 4, 291518))
        self.assertEqual(infos[0].user_id, 12)
        self.assertEqual(infos[0].user, 'bob')
        self.assertEqual(infos[0].group_id, 34)
        self.assertEqual(infos[0].group, 'staff')
        self.assertEqual(infos[1].path, '/etc/nginx')
        self.assertEqual(infos[1].name, 'nginx')
        self.assertEqual(infos[1].type, pebble.FileType.DIRECTORY)
        self.assertEqual(infos[1].size, None)
        self.assertEqual(infos[1].permissions, 0o755)
        self.assertEqual(infos[1].last_modified, datetime_nzdt(2020, 1, 1, 1, 1, 1, 0))
        self.assertIs(infos[1].user_id, None)
        self.assertIs(infos[1].user, None)
        self.assertIs(infos[1].group_id, None)
        self.assertIs(infos[1].group, None)

        self.assertEqual(self.client.requests, [
            ('GET', '/v1/files', {'action': 'list', 'path': '/etc'}, None),
        ])

    def test_list_files_pattern(self):
        self.client.responses.append({
            "result": [],
            'status': 'OK',
            'status-code': 200,
            'type': 'sync',
        })

        infos = self.client.list_files('/etc', pattern='*.conf')

        self.assertEqual(len(infos), 0)
        self.assertEqual(self.client.requests, [
            ('GET', '/v1/files', {'action': 'list', 'path': '/etc', 'pattern': '*.conf'}, None),
        ])

    def test_list_files_itself(self):
        self.client.responses.append({
            "result": [],
            'status': 'OK',
            'status-code': 200,
            'type': 'sync',
        })

        infos = self.client.list_files('/etc', itself=True)

        self.assertEqual(len(infos), 0)
        self.assertEqual(self.client.requests, [
            ('GET', '/v1/files', {'action': 'list', 'path': '/etc', 'itself': 'true'}, None),
        ])

    def test_make_dir_basic(self):
        self.client.responses.append({
            "result": [{'path': '/foo/bar'}],
            'status': 'OK',
            'status-code': 200,
            'type': 'sync',
        })
        self.client.make_dir('/foo/bar')
        req = {'action': 'make-dirs', 'dirs': [{
            'path': '/foo/bar',
        }]}
        self.assertEqual(self.client.requests, [
            ('POST', '/v1/files', None, req),
        ])

    def test_make_dir_all_options(self):
        self.client.responses.append({
            "result": [{'path': '/foo/bar'}],
            'status': 'OK',
            'status-code': 200,
            'type': 'sync',
        })
        self.client.make_dir('/foo/bar', make_parents=True, permissions=0o600,
                             user_id=12, user='bob', group_id=34, group='staff')

        req = {'action': 'make-dirs', 'dirs': [{
            'path': '/foo/bar',
            'make-parents': True,
            'permissions': '600',
            'user-id': 12,
            'user': 'bob',
            'group-id': 34,
            'group': 'staff',
        }]}
        self.assertEqual(self.client.requests, [
            ('POST', '/v1/files', None, req),
        ])

    def test_make_dir_error(self):
        self.client.responses.append({
            "result": [{
                'path': '/foo/bar',
                'error': {
                    'kind': 'permission-denied',
                    'message': 'permission denied',
                },
            }],
            'status': 'OK',
            'status-code': 200,
            'type': 'sync',
        })
        with self.assertRaises(pebble.PathError) as cm:
            self.client.make_dir('/foo/bar')
        self.assertIsInstance(cm.exception, pebble.Error)
        self.assertEqual(cm.exception.kind, 'permission-denied')
        self.assertEqual(cm.exception.message, 'permission denied')

    def test_remove_path_basic(self):
        self.client.responses.append({
            "result": [{'path': '/boo/far'}],
            'status': 'OK',
            'status-code': 200,
            'type': 'sync',
        })
        self.client.remove_path('/boo/far')
        req = {'action': 'remove', 'paths': [{
            'path': '/boo/far',
        }]}
        self.assertEqual(self.client.requests, [
            ('POST', '/v1/files', None, req),
        ])

    def test_remove_path_recursive(self):
        self.client.responses.append({
            "result": [{'path': '/boo/far'}],
            'status': 'OK',
            'status-code': 200,
            'type': 'sync',
        })
        self.client.remove_path('/boo/far', recursive=True)

        req = {'action': 'remove', 'paths': [{
            'path': '/boo/far',
            'recursive': True,
        }]}
        self.assertEqual(self.client.requests, [
            ('POST', '/v1/files', None, req),
        ])

    def test_remove_path_error(self):
        self.client.responses.append({
            "result": [{
                'path': '/boo/far',
                'error': {
                    'kind': 'generic-file-error',
                    'message': 'some other error',
                },
            }],
            'status': 'OK',
            'status-code': 200,
            'type': 'sync',
        })
        with self.assertRaises(pebble.PathError) as cm:
            self.client.remove_path('/boo/far')
        self.assertIsInstance(cm.exception, pebble.Error)
        self.assertEqual(cm.exception.kind, 'generic-file-error')
        self.assertEqual(cm.exception.message, 'some other error')


class TestSocketClient(unittest.TestCase):
    @unittest.skipIf(sys.platform == 'win32', "Unix sockets don't work on Windows")
    def test_socket_not_found(self):
        client = pebble.Client(socket_path='does_not_exist')
        with self.assertRaises(pebble.ConnectionError) as cm:
            client.get_system_info()
        self.assertIsInstance(cm.exception, pebble.Error)

    @unittest.skipIf(sys.platform == 'win32', "Unix sockets don't work on Windows")
    def test_real_client(self):
        shutdown, socket_path = fake_pebble.start_server()

        try:
            client = pebble.Client(socket_path=socket_path)
            info = client.get_system_info()
            self.assertEqual(info.version, '3.14.159')

            change_id = client.start_services(['foo'], timeout=0)
            self.assertEqual(change_id, '1234')

            with self.assertRaises(pebble.APIError) as cm:
                client.start_services(['bar'], timeout=0)
            self.assertIsInstance(cm.exception, pebble.Error)
            self.assertEqual(cm.exception.code, 400)
            self.assertEqual(cm.exception.status, 'Bad Request')
            self.assertEqual(cm.exception.message, 'service "bar" does not exist')

        finally:
            shutdown()
