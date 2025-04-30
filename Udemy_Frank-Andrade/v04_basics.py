import pandas as pd

states = ["California", "Texas", "Florida", "New York"]
population = [39613493, 29730311, 21944577, 19299981]

dict_states = {"State": states, "Population": population}

df = pd.DataFrame.from_dict(dict_states)
print(df)

df.to_csv("states.csv", index=False)

print(states[0])
print(states[3])
print(states[-2])

for state in states:
    if state == "Florida":
        print("Found Florida!")
    else:
        print("other state:", state)

with open("test.txt", "w") as my_file:
    my_file.write("Hello World!")
    my_file.write("\n")
    my_file.write("This is a test file.")
    my_file.write("\n")
    my_file.write("Goodbye!")

new_list = [2, 4, 6, "California", 10]

for element in new_list:
    try:
        print(element / 2)
    except:
        print("The element at this position is not a number!")

# while-break
n = 4
while n > 0:
    print(n)
    n -= 1

print("Loop ended!")

n = 5
while n > 0:
    print(n)
    n -= 1
    if n == 2:
        break

print("Loop hit the break at n = 2!!")
