import requests

print("Start....")

class PokeAPI:
    def __init__(self):
        self.base_url = "https://pokeapi.co/api/v2/pokemon/"
        self.pokemon_list = []

    class Pokemon:
        def __init__(self, pokemon_id, name, types, weight):
            self.id = pokemon_id
            self.name = name
            self.types = types
            self.weight = weight

    def get_pokemon_data(self, pokemon_id):
        response = requests.get(f"{self.base_url}{pokemon_id}")
        data = response.json()
        types = [t['type']['name'] for t in data['types']] if data['types'] else []
        act_pokemon = self.Pokemon(pokemon_id, data['name'], types, data['weight'])
        self.pokemon_list.append(act_pokemon)
        return act_pokemon

    def init_pokemon_list(self, max_id):
        self.pokemon_list = [self.get_pokemon_data(i) for i in range(1, max_id)]

    def get_pokemon_by_id(self, pokemon_id):
        for p in self.pokemon_list:
            if p.id == pokemon_id:
                return p
        return None

    def get_pokemon_sorted(self, sort_by=("id",), reverse=False):
        sort_keys = {
            "id": lambda x: x.id,
            "weight": lambda x: x.weight
        }
        return sorted(self.pokemon_list, key=lambda x: tuple(sort_keys[key](x) for key in sort_by), reverse=reverse)

    def get_pokemon_weights(self, min_weight=None, max_weight=None):
        filtered_list = []
        for p in self.pokemon_list:
            if min_weight is not None and p.weight < min_weight:
                continue
            if max_weight is not None and p.weight > max_weight:
                continue
            filtered_list.append(p)
        return sorted(filtered_list, key=lambda x: x.weight, reverse=True)


# 初始化 PokeAPI
size = 10
poke_api = PokeAPI()
poke_api.init_pokemon_list(size)

pokemon_6 = poke_api.get_pokemon_by_id(6)
print(f"1. 列出 id 為 6 的寶可夢名稱（name）: {pokemon_6.name}")

print("2. 列出 id < 20, id > 0 的寶可夢名稱（name）以及其寶可夢的屬性（types），依照 id 由小至大排序:")
for pokemon in poke_api.get_pokemon_sorted(sort_by=("id",)):
    if pokemon.id < 20:
        print(f"ID: {pokemon.id}, Name: {pokemon.name}, Types: {pokemon.types}")

print("3. 列出 id < 100, id > 0 的寶可夢中，體重（weight） < 50 的寶可夢名稱（name）及寶可夢體重（weight），並且依照體重由大至小排序:")
for pokemon in poke_api.get_pokemon_weights(max_weight=50):
    print(f"ID: {pokemon.id}, Name: {pokemon.name}, Weight: {pokemon.weight}")
