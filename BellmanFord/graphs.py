import matplotlib.pyplot as plt
import numpy

years = [1900, 1930, 1960, 1990, 2020]
population = [2.1, 2.9, 4.5, 6.7, 8.2]

plt.scatter(years, population, s = population)
plt.xlabel("Years")
plt.ylabel("Population (Billions)")
plt.title("Population Growth")
plt.grid(True)
plt.show()

