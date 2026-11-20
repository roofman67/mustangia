from statistics import mean


def main():
    values = [4, 7, 9, 10, 12]
    print(f"Sample count: {len(values)}")
    print(f"Mean: {mean(values):.1f}")


if __name__ == "__main__":
    main()
