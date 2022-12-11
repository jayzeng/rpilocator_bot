from src.api import Rpilocator, RpilocatorMock

def main():
    # rpilocator = Rpilocator('us')
    # print(rpilocator.send())

    rpilocator = RpilocatorMock('us')
    data = rpilocator.send()
    print(data)

if __name__ == "__main__":
    main()