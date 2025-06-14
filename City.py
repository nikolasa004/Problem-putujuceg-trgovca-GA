import random
import os
project_folder=folder=os.path.dirname(os.path.abspath(__file__))

#klasa za grad
class City:
    def __init__ (self,id,x,y):
        self.id = id
        self.name = make_city_name()
        self.x = x
        self.y = y

#funkcija koja pravi ime grada
def make_city_name():
    with open(project_folder+"/Data/firstWordCity.txt") as file:
        first_words=file.read().split("\n")
    with open(project_folder+"/Data/secondWordCity.txt") as file:
        second_words=file.read().split("\n")

    first_word=random.choice(first_words)
    second_word=random.choice(second_words)

    return first_word + " " + second_word

#funkcija koja cita gradove iz fajla i pravi listu objekata tipa City
def read_cities():
    cities=[]
    with open(project_folder+"/Data/data_tsp.txt") as file:
        lines=file.readlines()
        for line in lines:
            city_data=line.split(" ")
            new_city=City(int(city_data[0]),float(city_data[1]),float(city_data[2]))
            cities.append(new_city)

    return cities