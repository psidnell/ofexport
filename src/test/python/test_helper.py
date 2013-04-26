def catch_exception (fn):
    try:
        fn()
    except Exception as e:
        return e.message
    assert False, "Exception expected, none raised"
        