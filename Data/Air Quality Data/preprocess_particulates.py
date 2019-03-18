import csv
import os
import array as arr
import matplotlib.pyplot as plt


def main():
    co_data = []
    filtered_co_data = []
    filtered_no2_data = []
    filtered_ozone_data = []
    filtered_pm2_data = []
    filtered_pm10_data = []
    filtered_s02_data = []
    f4 = open("C:/Users/Wasif/gapsfound.txt", "w")

    year_start = 1988
    year_end = 2008

    co_data = read_particulate_directory("CO", year_start, year_end)
    filtered_co_data = filter_data(co_data, year_start, year_end, f4)
    write_filtered_data_to_file(filtered_co_data, year_start, year_end)

    no2_data = read_particulate_directory("NO2", year_start, year_end)
    filtered_no2_data = filter_data(no2_data, year_start, year_end, f4)
    write_filtered_data_to_file(filtered_no2_data, year_start, year_end)

    ozone_data = read_particulate_directory("OZONE", year_start, year_end)
    filtered_ozone_data = filter_data(ozone_data, year_start, year_end, f4)
    write_filtered_data_to_file(filtered_ozone_data, year_start, year_end)

    pm2_data = read_particulate_directory("PM2.5", year_start, year_end)
    filtered_pm2_data = filter_data(pm2_data, year_start, year_end, f4)
    write_filtered_data_to_file(filtered_pm2_data, year_start, year_end)

    pm10_data = read_particulate_directory("PM10", year_start, year_end)
    filtered_pm10_data = filter_data(pm10_data, year_start, year_end, f4)
    write_filtered_data_to_file(filtered_pm10_data, year_start, year_end)

    so2_data = read_particulate_directory("SO2", year_start, year_end)
    filtered_s02_data = filter_data(so2_data, year_start, year_end, f4)
    write_filtered_data_to_file(filtered_s02_data, year_start, year_end)

    # read_particulate_directory("NO2", 1980, 2016)
    # read_particulate_directory("OZONE", 1980, 2016)
    # read_particulate_directory("PM2.5", 1980, 2016)
    # read_particulate_directory("PM10", 1980, 2016)
    # read_particulate_directory("SO2", 1980, 2016)

    print(list(co_data[0][2])[0])

    f4.close()

    return


def write_filtered_data_to_file(data_point, year_start, year_end):
    f1 = open("C:/Users/Wasif/filtered_data_points_max_" + str(year_start) + "-" + str(year_end) + "_" + str(data_point[0][1]) + ".txt", "w")
    f2 = open("C:/Users/Wasif/filtered_data_points_min_" + str(year_start) + "-" + str(year_end) + "_" + str(data_point[0][1]) + ".txt", "w")
    f3 = open("C:/Users/Wasif/filtered_data_points_avg_" + str(year_start) + "-" + str(year_end) + "_" + str(data_point[0][1]) + ".txt", "w")

    for point in data_point:
        county_state = point[0]
        pollutant = point[1]
        years_dictionary = point[2]
        years_max_list = []
        years_min_list = []
        years_avg_list = []

        for key, value in years_dictionary.items():
            years_max_list.append(float(years_dictionary[key][0]))
            years_min_list.append(float(years_dictionary[key][1]))
            years_avg_list.append(float(years_dictionary[key][2]))

        max_data_point = (county_state, pollutant, years_max_list)
        min_data_point = (county_state, pollutant, years_min_list)
        avg_data_point = (county_state, pollutant, years_avg_list)

        f1.write(str(max_data_point) + "\n")
        f2.write(str(min_data_point) + "\n")
        f3.write(str(avg_data_point) + "\n")

    f1.close()
    f2.close()
    f3.close()

    return


def filter_data(data_points, year_start, year_end, file_out):
    filtered_data_points = []
    deleted_data_points = []
    number_of_years = year_end - year_start + 1
    for point in data_points:
        print(str(point))
        print(str(len(point[2])))

        beginning_year_present = False
        if str(year_start) in point[2]:
            beginning_year_present = True

        ending_year_present = False
        if str(year_end) in point[2]:
            ending_year_present = True

        first_year = list(point[2])[0]

        # if str(first_year) is not str(year_start):
        #     print(str(first_year) + " vs " + str(year_start))
        #     data_points.remove(point)
        #     print("REMOVED " + str(point[0]))
        #     deleted_data_points.append(point)
        # if len(point[2]) > number_of_years:
        #     data_points.remove(point)
        #     deleted_data_points.append(point)
        if len(point[2]) < number_of_years - 1:
            data_points.remove(point)
            deleted_data_points.append(point)
        elif not beginning_year_present or not ending_year_present:
            data_points.remove(point)
            deleted_data_points.append(point)
        else:
            filtered_data_points.append(point)


    print("HERE IS THE DICTIONARY: " + str(data_points))

    f = open("C:/Users/Wasif/filtered_data_points.txt", "w")
    f.write(str(len(data_points)) + "\n")
    for point in filtered_data_points:
        f.write(str(point) + "\n")
    f.close()

    gap_counter = 0
    for point in filtered_data_points:
        if len(point[2]) < number_of_years:
            print("GAP FOR " + str(point))
            gap_counter += 1


    file_out.write(("GAPS FOUND for " + str(data_points[0][1]) + " = " + str(gap_counter)) + "\n")

    return filtered_data_points


def read_particulate_directory(particulate_type, year_start, year_end):
    data_point_list = []
    earliest_county_year = {}
    latest_county_year = {}
    county_state_years = {}
    years = []
    year_frequencies = {}
    directory = os.path.join("C:/", "Users/Wasif/CS5140/DataMiningGroupProject/Data/Air Quality Data/Aggregated/"
                             + particulate_type + "/")

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".csv"):
                year_index = int(file.find(".csv")) - 4
                parsed_year = int(file[year_index: year_index+4])
                if year_start <= parsed_year <= year_end:
                    f = open(directory+file, 'r')
                    line_counter = 0
                    for line in f:
                        line_counter += 1
                        if line_counter > 2:
                            print(line)
                            data_row = line.split(',')
                            data_row[6] = data_row[6].rstrip()
                            county_state = data_row[0] + "-" + data_row[1]
                            data_point = search_data_point_by_county_state(data_point_list, county_state)
                            if not data_point:
                                data_point = create_data_point(data_row)
                                data_point_list.append(data_point)
                                earliest_county_year[county_state] = data_row[6]
                                latest_county_year[county_state] = data_row[6]
                                county_state_years[county_state] = [data_row[6]]
                            else:
                                append_year_data(data_point, data_row)

                                current_year = data_row[6]

                                earliest_year = earliest_county_year[county_state]
                                if current_year < earliest_year:
                                    earliest_county_year[county_state] = data_row[6]

                                latest_year = latest_county_year[county_state]
                                if current_year > latest_year:
                                    latest_county_year[county_state] = data_row[6]

                                county_years_list = county_state_years[county_state]
                                county_years_list.append(current_year)
                            if data_row[6] not in years:
                                years.append(data_row[6])
                            if(data_row[6] in year_frequencies):
                                year_frequencies[data_row[6]] = year_frequencies[data_row[6]] + 1
                            else:
                                year_frequencies[data_row[6]] = 1
                    f.close()

    earliest_years = []
    latest_years = []
    for county in earliest_county_year:
        print(county + " earliest year: " + earliest_county_year[county])
        earliest_years.append(earliest_county_year[county])

    for county in latest_county_year:
        print(county + " latest year: " + latest_county_year[county])
        latest_years.append(latest_county_year[county])

    earliest_years.sort(reverse=True)
    latest_years.sort()

    print("Earliest year: " + str(earliest_years))
    print("Latest year: " + str(latest_years))

    for key, value in sorted(earliest_county_year.items(), key=lambda x: x[1]):
        print(key + " " + value)

    for key, value in sorted(latest_county_year.items(), reverse=True, key=lambda x: x[1]):
        print(key + " " + value)

    # counter = 0
    # f = open("C:/Users/Wasif/small_county_data_" + particulate_type + ".txt", "w")
    # f.write(str(len(data_point_list)) + "\n")
    # for key, value in county_state_years.items():
    #     print(key + " " + str(value))
    #     print(str(len(value)))
    #     if len(value) >= 30:
    #         counter += 1
    #         print("YESSSSS")
    #         f.write(key + " " + str(len(value)) + "\n")
    # f.write(str(counter) + "\n")
    # f.close()

    print(years)
    print(year_frequencies)
    print("number of counties = " + str(len(data_point_list)))

    year_frequencies_array = []

    for key in year_frequencies:
        year_frequencies_array.append(year_frequencies[key])

    years_trimmed = []

    for year in years:
        years_trimmed.append(year[2:4])

    # plt.plot(years_trimmed, year_frequencies_array)
    # plt.show()

    return data_point_list


def append_year_data(data_point, data_row):
    year_dictionary = data_point[2]
    max_aqi = data_row[3]
    min_aqi = data_row[4]
    avg_aqi = data_row[5]
    year = data_row[6]
    year_dictionary[year] = [max_aqi, min_aqi, avg_aqi]

    return


def search_data_point_by_county_state(data_point_list, county_state):
    data_point = False

    for point in data_point_list:
        # print(str(point[0]) + " vs. " + county_state)
        if point[0] == county_state:
            # print("FOUND")
            data_point = point
            break

    return data_point


# The Data Point has the following structure:
# ('county-state', 'pollutant', {year: [max aqi, min aqi, avg aqi], ...})
def create_data_point(data_row):
    print("data row: " + str(data_row))

    year_dictionary = {}

    county_state = (data_row[0] + "-" + data_row[1])
    pollutant = data_row[2]
    max_aqi = data_row[3]
    min_aqi = data_row[4]
    avg_aqi = data_row[5]
    year = data_row[6]
    year_dictionary[year] = [max_aqi, min_aqi, avg_aqi]

    data_point = (county_state, pollutant, year_dictionary)

    return data_point


main()
