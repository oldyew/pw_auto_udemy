from pytest import mark

ddt = {
    'argnames': 'name,description',
    'argvalues': [
        ('hello', 'world'),
        ('hello', ''),
        ('567567', 'world')],
    'ids': ['general test', 'without description', 'digits for name']
}


@mark.parametrize(**ddt)
def test_new_testcase(desktop_app_auth, name, description):
    desktop_app_auth.navigate_to("Create new test")
    desktop_app_auth.create_test(name, description)
    desktop_app_auth.navigate_to("Test Cases")
    assert desktop_app_auth.test_cases.check_test_exists(name)
    desktop_app_auth.test_cases.delete_test_by_name(name)


def test_testcase_does_not_exist(desktop_app_auth):
    desktop_app_auth.navigate_to("Test Cases")
    assert not desktop_app_auth.test_cases.check_test_exists('lsdhgldsjgfsdfljds')
