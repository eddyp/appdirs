import pytest
if __name__ != "__main__":
    import sys
    sys.path.append('.')

def patchapi(monkey, modname, apiname, retval):
    def mockreturn(a=None, b=None, c=None, d=None, e=None):
        return retval
    monkey.setattr(modname, apiname, mockreturn)

def forget_modules(modules, backup):
    for m in modules:
        try:
            backup[m] = sys.modules[m]
        except KeyError:
            backup[m] = None
        sys.modules[m] = None

def restore_modules(backup):
    for m in backup.keys():
        sys.modules[m] = backup[m]
        if backup[m] == None:
            del sys.modules[m]
        del backup[m]

@pytest.mark.parametrize(
            ("mod", "attr", "ret"),
            [ ("sys", "platform", "win32"),
              ("sys", "platform", "Linux2"),
              ("sys", "platform", "darwin")
            ]
        )
def test_config_dir(monkeypatch, mod, attr, ret):
    import sys
    modobj = sys.modules[mod]
    patchapi(monkeypatch, modobj, attr, ret)
    assert sys.platform() == ret



def test_user_data_dir_registry(monkeypatch):
    origmodlist = {}

    mp = monkeypatch
    import sys
    mp.setattr(sys, 'platform', 'win32')
    assert sys.platform == 'win32'
    forget_modules(['win32com', 'ctypes'], origmodlist)

    sys.path.insert(0, 'test2/mocks')
    import _winreg
    fakekey = 'fake\\_winreg\\key'
    fakedir = 'c:\\fake\\sh\\dir'
    patchapi(mp, _winreg, 'OpenKey', fakekey)
    patchapi(mp, _winreg, 'QueryValueEx', fakedir)

    import os
    patchapi(mp, os, 'pathsep', '\\')

    import appdirs
    assert appdirs.user_data_dir('MyApp', 'MyCompany') == \
                fakedir + "\\MyCompany\\MyApp"

    restore_modules(origmodlist)


if __name__=="__main__":
    pytest.main([ __file__ ])
    import appdirs
