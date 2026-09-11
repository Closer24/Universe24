from multiprocessing import freeze_support

from .runner import main

if __name__ == "__main__":
    freeze_support()
    main()
