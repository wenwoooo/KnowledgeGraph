import main
import re

if __name__ == '__main__':
    main.process_all_keys()
    temp = '味辛、性温'
    print(type(temp))
    slice_ = temp.split('性')
    print(slice_[0][1:], slice_[1][0:])
