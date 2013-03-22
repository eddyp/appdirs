import pytest
if __name__ != "__main__":
    import sys
    sys.path.append('.')
    import appdirs

def test_metadata():
    assert hasattr(appdirs, "__version__")
    assert hasattr(appdirs, "__version_info__")

def helper_type_test(t):
    assert type(t.site_data_dir('MyApp', 'MyCompany')) == type('')
    assert type(t.site_config_dir('MyApp', 'MyCompany')) == type('')

    assert type(t.user_data_dir('MyApp', 'MyCompany')) == type('')
    assert type(t.user_config_dir('MyApp', 'MyCompany')) == type('')
    assert type(t.user_cache_dir('MyApp', 'MyCompany')) == type('')
    assert type(t.user_log_dir('MyApp', 'MyCompany')) == type('')

def test_helpers():
    helper_type_test(appdirs)

def test_dirs():
    dirs = appdirs.AppDirs('MyApp', 'MyCompany', version='1.0')
    helper_type_test(dirs)

if __name__=="__main__":
    pytest.main([ __file__ ])
    import appdirs
