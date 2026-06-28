class Program:
    def __init__(self) -> None:
        pass

    def run(self) -> None:
        ...


if __name__ == "__main__":
    try:
        program: Program = Program()
        program.run()

    except Exception as e:
        print(f"Caught exception: {e}")

    except KeyboardInterrupt:
        print("=== Program Stopped ===")
