from dsp import RandWalk

STEPS: int = 15

def main():
    rw = RandWalk(time_steps=STEPS)
    rw.plt()

if __name__ == '__main__':
    main()