import sys
import pandas as pd
import matplotlib.pyplot as plt

FILE = sys.argv[1] if len(sys.argv) > 1 else "population.csv"


def load_data(path):
    """Load CSV, skip invalid rows and duplicates. Returns a clean DataFrame."""
    try:
        raw = pd.read_csv(path, dtype=str)
    except FileNotFoundError:
        print("Error: file not found.")
        return None
    except Exception as e:
        print("Error reading file:", e)
        return None

    if not {"City", "Year", "Population"}.issubset(raw.columns):
        print("Error: CSV must have columns City, Year, Population.")
        return None

    good = []
    for i, row in raw.iterrows():
        n = i + 1                                   # data row number
        city = str(row["City"]).strip()
        if city == "" or city == "nan":
            print(f"Row {n} skipped: City is missing.")
            continue
        try:
            year = int(row["Year"])
        except (ValueError, TypeError):
            print(f"Row {n} skipped: invalid Year '{row['Year']}'.")
            continue
        try:
            pop = int(row["Population"])
        except (ValueError, TypeError):
            print(f"Row {n} skipped: invalid Population '{row['Population']}'.")
            continue
        if pop <= 0:
            print(f"Row {n} skipped: Population must be positive.")
            continue
        good.append({"City": city, "Year": year, "Population": pop})

    df = pd.DataFrame(good, columns=["City", "Year", "Population"])
    df = df.drop_duplicates(subset=["City", "Year"])
    print(f"Valid rows: {len(df)}")
    return df


def latest_population(df):
    """Latest record of each city (uses groupby)."""
    return df.sort_values("Year").groupby("City").last()


def growth_percent(df):
    """Growth % per city; cities with only one year are left out."""
    g = df.sort_values("Year").groupby("City")
    first, last = g.first(), g.last()
    growth = (last["Population"] - first["Population"]) / first["Population"] * 100
    growth = growth[first["Year"] != last["Year"]]
    city_order = df["City"].drop_duplicates()
    return growth.reindex([city for city in city_order if city in growth.index])


def show_summary(df):
    latest = latest_population(df)
    year = df["Year"].max()
    total = latest["Population"].sum()
    big = latest["Population"].idxmax()

    if len(df) == 1:
        print(f"Total population: {total} | Largest city: {big}")
    else:
        print(f"Total population ({year}): {total}")
        print(f"Largest city: {big} ({latest.loc[big, 'Population']})")

    growth = growth_percent(df)
    if growth.empty:
        print("Growth: not available (only one year of data)")
    else:
        fastest = growth.idxmax()
        print(f"Fastest growing: {fastest} ({growth[fastest]:+.2f}%)")


def show_growth_and_charts(df):
    growth = growth_percent(df)
    if growth.empty:
        print("Growth: not available (only one year of data)")
        return

    print(" | ".join(f"{c}: {v:+.2f}%" for c, v in growth.items()))

    # Bar chart
    plt.figure()
    plt.bar(growth.index, growth.values, color="steelblue")
    plt.title("Population Growth by City")
    plt.xlabel("City")
    plt.ylabel("Growth (%)")

    # Line chart
    trend = df.pivot(index="Year", columns="City", values="Population")
    plt.figure()
    for city in trend.columns:
        plt.plot(trend.index, trend[city], marker="o", label=city)
    plt.title("Population Trend")
    plt.xlabel("Year")
    plt.ylabel("Population")
    plt.xticks(trend.index)
    plt.legend()

    plt.show()


def main():
    df = load_data(FILE)
    if df is None or df.empty:
        print("No valid data to analyse.")
        return

    while True:
        print("\n1. Summary\n2. Growth and charts\n3. Exit")
        choice = input("Enter option: ").strip()
        if choice == "1":
            show_summary(df)
        elif choice == "2":
            show_growth_and_charts(df)
        elif choice == "3":
            break
        else:
            print("Invalid option. Choose 1, 2 or 3.")


if __name__ == "__main__":
    main()