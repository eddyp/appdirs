import pytest
if __name__ != "__main__":
    import sys
    sys.path.append('.')

def helper_patchpair(monkey, modname, apiname, retval):
    def mockreturn(a=None, b=None, c=None, d=None, e=None):
        return retval
    monkey.setattr(modname, apiname, mockreturn)

#@pytest.mark.parametrize(
        #("platform", "patchpairs", "mockpairs", "roaming", "envvar"), 
            #(   "win32",
                #{ '_winreg':
                    #{ 'OpenKey': 'fake\\_winreg\\key',
                      #'QueryValueEx': 'c:\\fake\\shell\\folder'
                    #},
                  #'win32com':None, 
                  #'ctypes':None
                #}, 
                #False,
                #{}
            #)
        #)
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
