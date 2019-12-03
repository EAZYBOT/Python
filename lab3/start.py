from DialogHandler import  DialogHandler
import test_append


if __name__ == '__main__':
    dh = DialogHandler()
    test_append.test_append(dh.pets_manager)
    dh.run()
