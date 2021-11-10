from mixer.backend.marshmallow import TypeMixer, Mixer
import functools
import subprocess
import pytest


def catch_exception(func):
    """
    Returns:
        object:
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        worker = kwargs['error_catcher']
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print('stdout:', worker.stdout.read().decode("utf-8"))
            print('stderr:', worker.stderr.read().decode("utf-8"))
            raise

    return wrapper


@pytest.fixture(scope='module')
def error_catcher(request) -> subprocess.Popen:
    """py.test fixture to create app scaffold."""
    cmdline = ["echo", "ERROR!!"]

    worker = subprocess.Popen(cmdline, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    worker.wait(timeout=5.0)

    return worker


class TestTypeMixer(TypeMixer):
    def __init__(self, cls, **params):
        super(TestTypeMixer, self).__init__(cls, **params)

    def is_required(self, field):
        # Avoid dict generations errors
        #
        return field.scheme.__class__.__name__ != 'Dict'


class TestMixer(Mixer):
    def __init__(self, **params):
        self.type_mixer_cls = TestTypeMixer
        params.setdefault('required', False)
        super(TestMixer, self).__init__(**params)


mixer = TestMixer()
