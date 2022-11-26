import hug

counter = 0


@hug.get("/increment")
def increment():
    counter += 1
    return counter
