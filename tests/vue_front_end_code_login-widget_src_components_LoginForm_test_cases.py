import pytest
from scr.LoginForm import LoginForm

def test_login_form_button_style_happy_path():
    form = LoginForm()
    assert form.button_style == 'background-color: #42b983; color: white; border: none; border-radius: 6px;'

def test_login_form_button_style_invalid_input():
    with pytest.raises(AttributeError):
        form = LoginForm()
        form.button_style = 'invalid style'

def test_login_form_button_style_boundary():
    form = LoginForm()
    assert form.button_style == 'background-color: #42b983; color: white; border: none; border-radius: 6px;'