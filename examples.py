import cartodb
from cartodb_object import CartoDb_object
cartoPy = cartodb.Cartodb('xabel')
all_table = cartoPy.at('mercadona').open()
new_object = CartoDb_object(cartoPy)
new_object.set('pc','55533')
new_object.save()

filtered_table = cartoPy.at('mercadona').field('pc').has('55533').open()
filtered_table[0].set('pc', '54321')
filtered_table[0].fetch() # restores the values
filtered_table[0].delete()
