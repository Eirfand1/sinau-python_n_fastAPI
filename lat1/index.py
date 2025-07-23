from typing import Optional

def get_full_name(first_name: str, last_name: str):
    full_name = first_name.title() + " " + last_name.title()
    return full_name

print(get_full_name("Ego", "Irfandi"))

def get_name_with_age(name: str, age: int):
    name_with_age = name.title() + "is this old" + " " + str(age)
    return name_with_age

print(get_name_with_age("Ego", 8))

print('Coba tipe data list')
def process_items(items: list[str]):
    for item in items:
        print(item)


process_items(['a','b','c','d'])

def process_items_tuple(items_t:tuple[int, int, str], items_s: set[bytes]):
    return items_t, items_s

test_tuple_t, test_tuple_s = process_items_tuple([1,2,'3'], ['tes', 'tes', 3])

print('====================\nCoba tipe data tuple[int,int,str]')
for tt in test_tuple_t:
    print(tt)

print('====================\n coba tipe data set dengan type bytes')
for ts in test_tuple_s:
    print(ts)


""" Sama aja kaya object di js atau array assoc di php """
print('Mencoba tipe data dict')
def process_items_dict(prices: dict[str, float]):
    for item_name, item_price in prices.items():
        print(item_name)
        print(item_price)

process_items_dict({"item_name": "bakso", "item_price": 120000})


print('Mencoba tipe Union(OR)')
def process_items_union(item: int | str):
    print(item)

""" Memperbolehkan untuk tipe data str dan int """
process_items_union("cek str")
process_items_union(1234)



def say_hi(name: Optional[str] = None):
    if name is not None:
        print(f"halo {name}!")
    else:
        print("Hello World")

print("================\n Mencoba parameter optional")
say_hi()
say_hi("joko")

print("================'\n pake union")
def say_hi_union(name: str | None = None):
    if name is not None:
        print(f"halo {name}! pake union")
    else:
        print("Hello World pake union")

say_hi_union()
say_hi_union("Sastro")

def say_hi_simpel(name: str | None):
    if name is not None:
        print(f"Halo {name}")

""" say_hi_simpel() """
say_hi_simpel("Darso")





