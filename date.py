import time  # return current date & time


# defines all months names and sets a numeric value
month_dict = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12,
}

## returns what time a post was made
def calculate_post_time(post_date): #Ex. Fri Dec  2 21:00:54 2022 -> 9:00pm takes the current time and date then returns the time in 12 hour format
    post_date = time.ctime()

    split_date = post_date.split(" ")
    if "" in split_date:  # this is for single digit days like 5,6,7 are different than 10,12,13
        split_date.remove("")
    split_hours = split_date[3].split(":")
    current_hour = int(split_hours[0])
    # current_hour-=4 #this is because heroku servers arent located on the west coast so the if not this then servers return their time zone
    # print(current_hour)
    if current_hour > 12:
        finished_post_time = current_hour - 12
        # print(current_hour)
        # print(split_hours)
        if finished_post_time > 0:
            if current_hour > 12:
                # print(str(finished_post_time) + ":" + str(split_hours[1]) + " pm")
                return str(finished_post_time) + ":" + str(split_hours[1]) + " pm"
            else:
                # print(str(finished_post_time) + ":" + str(split_hours[1]) + " am")
                return str(finished_post_time) + ":" + str(split_hours[1]) + " am"

    elif current_hour == 12:
        current_hour = 12
        return str(current_hour) + ":" + str(split_hours[1]) + " pm"

    elif current_hour == 0:
        current_hour = 12
        return str(current_hour) + ":" + str(split_hours[1]) + " am"

    elif current_hour < 12:
        # print(str(current_hour) + ":" + str(split_hours[1]) + " am")
        return str(current_hour) + ":" + str(split_hours[1]) + " am"


# takes the time object and returns the original post day because the time object return day and time Ex. Sun Aug 15 20:28:12 2021
def split_compare_date(full_date): #Ex. Fri Dec  2 21:00:54 2022 -> Dec 2 2022
    # print(full_date)
    full_date = full_date.split(" ")

    if (
        "" in full_date
    ):  # this is for single digit days like 5,6,7 are different than 10,12,13
        full_date.remove("")

    month = full_date[1]
    day = full_date[2]
    year = full_date[4]
    # print(full_date)
    split_date = [month, day, year]
    date = " "
    compare_date = date.join(split_date)
    # print(compare_date)
    return compare_date


# returns current day and splits it into a list
def split_current_date(current_post_date):
    current_post_date = current_post_date.split(" ")
    if "" in current_post_date:
        current_post_date.remove("")
    # print(post_date)
    month = current_post_date[1]
    day = current_post_date[2]
    year = current_post_date[4]
    split_date = [month, day, year]
    date = " "
    current_post_date = date.join(split_date)
    # print(current_post_date)
    return current_post_date.split(" ")


# compares the original date and the current post dates and returns how long ago it was posted Ex. 2 months ago
def get_time_ago(date1): #Ex. takes a python time object of today then converts to date of month day year and converts that date to today to return the amount of time passed Tue Jul 1 12:11:51 2021 vs Fri Dec  2 21:00:54 2022 -> 1 year ago
    # print(date1)
    full_date = "Tue Jul 1 12:11:51 2021"
    current_post_date = time.ctime()

    compare_date = split_current_date(date1) #retuens 
    current_post_date = split_current_date(current_post_date)
    # print(current_post_date)
    print(compare_date)
    print(current_post_date)

    if compare_date[2] == current_post_date[2]:
        # print("Same year")
        pass

        if compare_date[0] == current_post_date[0]:
            # print("same month")
            pass

            if compare_date[1] == current_post_date[1]:
                # print("same day")
                return "today"

            elif compare_date[1] != current_post_date[1]:
                # print(f"{get_post_date_or_time()[1]} days ago")
                day_difference = int(current_post_date[1]) - int(compare_date[1])
                # print(f"{day_difference} days ago")
                return f"{day_difference} days ago"

        elif compare_date[0] != current_post_date[0]:
            # print(f"{get_post_date_or_time()[0]} months ago")
            month_difference = (
                month_dict[current_post_date[0]] - month_dict[compare_date[0]]
            )
            # print(f"{month_difference} months ago")
            return f"{month_difference} months ago"

    elif compare_date[2] != current_post_date[2]:
        # print(f"{get_post_date_or_time()[2]} years ago")
        year_difference = int(current_post_date[2]) - int(compare_date[2])
        # print(f"{year_difference} years ago")
        return f"{year_difference} years ago"


current_time = time.ctime()
# print(time.ctime())
# 
# print(calculate_post_time(time.ctime())) 

# print(split_compare_date(current_time))
# print(split_current_date(current_time))

print(get_time_ago("Fri Nov  1 21:00:54 2020"))