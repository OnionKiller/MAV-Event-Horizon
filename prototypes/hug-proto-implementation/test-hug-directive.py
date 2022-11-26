import hug


@hug.directive()
def basic(default="test", **kwargs):
    return str(default) + " there!"


@hug.get("/test")
def test(hug_basic):
    return hug_basic
