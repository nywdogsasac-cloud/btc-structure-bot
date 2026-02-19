import threading
from bot_runner import run_bot
from trade_monitor import run_monitor


def start_bot():
    run_bot()


def start_monitor():
    run_monitor()


if __name__ == "__main__":
    t1 = threading.Thread(target=start_bot)
    t2 = threading.Thread(target=start_monitor)

    t1.start()
    t2.start()

    t1.join()
    t2.join()
