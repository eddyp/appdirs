import pytest
if __name__ != "__main__":
    import sys
    sys.path.append('.')

def helper_patchpair(monkey, modname, apiname, retval):
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
    helper_patchpair(monkeypatch, modobj, attr, ret)
    assert sys.platform() == ret



if __name__=="__main__":
    pytest.main([ __file__ ])
    import appdirs
