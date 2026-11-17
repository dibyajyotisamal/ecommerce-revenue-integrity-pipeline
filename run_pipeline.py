from src import (
    load_raw_data,
    standardize_strings,
    deduplicate_orders,
    clean_customer_age,
    clean_order_amount,
    clean_order_dates,
    clean_categories_and_boolean,
    export_csv,
)

def main() -> None:
    
    df = load_raw_data()

    df = (
        df.pipe(standardize_strings)\
            .pipe(deduplicate_orders)\
            .pipe(clean_customer_age)\
            .pipe(clean_order_amount)\
            .pipe(clean_order_dates)\
            .pipe(clean_categories_and_boolean)
    )

    export_csv(df)

if __name__ == "__main__":
        main()