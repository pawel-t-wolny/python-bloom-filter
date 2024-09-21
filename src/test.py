from bloom_filter import BloomFilter


def main():
    bloom_filter = BloomFilter(0.001, 18232)
    print(bloom_filter)

    bloom_filter.add("test")
    print(bloom_filter.contains("test"))


if __name__ == "__main__":
    main()
