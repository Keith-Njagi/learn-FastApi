from pydantic import BaseModel

class Car(BaseModel):
    brand: str
    model: str
    year: int
def update():
    car = {
    "brand": "Ford",
    "model": "Mustang",
    "year": 1964
    }

    x = car.copy()

    print(f'Car 1(x): {x}')

    car2 = {
    "brand": "Volkswagen",
    "model": "Golf",
    # "year": 2017
    }

    print(f'Car 2: {car2}')

    my_car = Car(**car)
    print(f'My Car: {my_car}')
    y = my_car.copy(update=car2)
    print(f'Y: {y}')

    print(f'Car 3: {y}')
    return None

if __name__ == '__main__':
    update()