from streamlit.testing.v1 import AppTest
import pytest 

def pytest_namespace():
    return {'ss': 0}

def test_run():
    at = AppTest.from_file("run.py").run()
    print(at.session_state)
    assert not at.exception
    at.text_input('pid').input("abcd").run()
    at.checkbox("cnst").check().run()
    at.button("btn1").click().run()
    # pytest.ss = at.session_state
    # print(at.session_state)
    # at = AppTest.switch_page(at, page_path="pages/chat1.py")
    # print(at)
    # at.button("strtcht").click().run()

    # # assert at.warning[0].value == "Try again."

# def test_chat1():
#     at = AppTest.from_file("pages/chat1.py").run()

#     # at.session_state = pytest.ss
#     assert not at.exception
#     at.button("strtcht").click().run()
#     print(at.session_state)
#     at.button("adf").click().run()