from fpinglib.fping import Fping,SingleFping


if __name__ == "__main__":
    filename="checklist"

    print ">>>>Fping with count=3"
    o1=Fping(filename)
    for host in o1.checkStatus():
        print host.address, host.lossrate+"%"

    print ">>>>SingleFping"
    o2=SingleFping(filename)
    for host in o2.checkAlive():
        print host, 'alive'
    for host in o2.checkDead():
        print host, 'dead'