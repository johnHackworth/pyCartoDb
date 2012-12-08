pyCartoDb
=========

pyCartoDb is a small ORM for CartoDb. It allows you to read your table and convert them to python objects, modify, delete and persist them

Examples of use:

[code]
  from cartodb import Cartodb

  # instantiate pyCartoDb with your cartodb's username
  pyCdb = Cartodb('user_name')

  # fetch all the content of a table
  full_table = pyCdb.at('table_name').open()

  # fetch the content of the same table, filtering by two columns
  table = pyCdb.at('table_name').field('name').has('javier').field('city').has('madrid').open()

  # change the names of all filtered records 
  for row in table:
    row.set('name', 'javi')
    row.save()

  # update the first record of the full table, to see if has changed
  name = full_table[0].get('name')
  full_table[0].fetch()

  # if the name has changed, delete the row
  if name != full_table[0].get('name'):
    full_table[0].delete()

  # if we want to create a new object, we need to import CartoDb_object
  from cartodb_object import CartoDb_object

  # also, we need to select a db where the new objects belogs
  pyCdb.db_name = 'table_name'
  # this value if setted authomatically if you have made any previous operation on that table

  # we create a new object passing an instantiated pyCdb as parameter
  new_object = CartoDb_object(pyCdb)
  
  # we set some info and persist the data to db
  new_object.set('name', 'perico')
  new_object.save()

 

[/code]