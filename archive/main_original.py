

def main():
    bkg = "White"
    frg = "black"
    default_block = [(0, 0), ("background", False)]
    a1 = []
    a2 = []
    a3 = []
    a4 = []
    a5 = []
    a6 = []
    a7 = []
    a8 = []
    env = []
    # set up datastructure to hold the environment.
    for ablock in range(0, 8):
        a1.append(default_block)
        a2.append(default_block)
        a3.append(default_block)
        a4.append(default_block)
        a5.append(default_block)
        a6.append(default_block)
        a7.append(default_block)
        a8.append(default_block)

    env.append(a1)
    env.append(a2)
    env.append(a3)
    env.append(a4)
    env.append(a5)
    env.append(a6)
    env.append(a7)
    env.append(a8)

    for mf in range(0, 8):
        for ms in range(0, 8):
            env[mf][ms]=[(mf, ms), ("background", False)]
            print("{} {}".format(mf, ms))
            print(env[mf][ms])

    for block in env:
        print(block)

if __name__=="__main__":
    main()
