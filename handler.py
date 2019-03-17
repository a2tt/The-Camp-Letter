try:
    import unzip_requirements
except ImportError:
    pass

from tasks import crawler, the_camp


def send_letter(event, context):
    the_camp.send_letter()
    return


if __name__ == '__main__':
    send_letter(None, None)
