def first_attempt():
    start = time.time()
    voters = pd.read_csv(active_voters_csv)
    addy = gpd.read_file(address_gpkg)
    print("read files done in ", time.time() - start, " seconds")
    voters['processed_address'] = voters['res_street_address'].apply(preprocess_address_data)
    print("first preprocess done in ", time.time() - start, " seconds")
    addy['processed_address'] = addy['FullAddres'].apply(preprocess_address_data)
    print("second preprocess done in ", time.time() - start, " seconds")
    matched_address = addy.merge(voters, how='inner', on='processed_address')
    print("merge done in ", time.time() - start, " seconds")
    total = len(matched_address)
    matched_address.to_file(matched_address_gpkg, driver="GPKG")
    matched_address.plot()
    plt.title(str(total))
    plt.show()
    print(time.time() - start, " seconds")