string = "[0, 10000, 19000, 29000, 41500, 49000, 59000, 71000, 80000, 90000, 98000, 106500,  1:57, 2:08, 2:18, 2:27, 2:37, 2:47, 2:57, 3:06, 3:15, 3:24, 3:34, 3:44, 3:54, 4:07, 4:15, 4:25, 4:33, 4:47, 4:57, 5:05, 5:16, 5:26, 5:35, 5:45, 5:56, 6:04, 6:14]"
final_str = string[1:string.find(":")]
final_str = final_str[:-4]
string = string[len(final_str)+4:-1]

for time in string.split(","):
    time = time.strip()
    ms = 60000 * int(time[0]) + 1000 * int(time[2:])
    final_str += ", " + str(ms)

print(final_str)
print(string)
