import hug


@hug.context_factory()
def context_maker(*args, **kwargs):
    return dict(t=10)


@hug.cli()
def test(**kwargs):
    print("kwargs", kwargs)
    context = kwargs["context"]
    print(context)
    context = {"t": 0}
    if "t" not in context:
        context["t"] = 1
    else:
        context["t"] += 1

    return context


if __name__ == "__main__":
    test.interface.cli()
