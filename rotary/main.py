from controller import Controller
from player import Player
from phoneeventsource import PhoneEventSource


def main():
    player = Player('sounds')
    controller = Controller(player)
    PhoneEventSource(controller.trigger)

    print('Press CTRL+C to quit.')
    try:
        controller.run()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
