import json

class CartoDb_object:

  def delete(self):
    if not self.is_new():
      sql = 'DELETE FROM ' + self.db_name + ' WHERE cartodb_id = '
      sql = sql + str(self.get('cartodb_id'))
      self.cartodb.sql(sql)
    return False

  def fetch(self):
    if not self.is_new():
      sql = 'SELECT * FROM ' + self.db_name
      sql = sql + ' WHERE cartodb_id = ' + str(self.get('cartodb_id'))
      response = json.loads(self.cartodb.sql(sql))
      for row in response['rows']:
        for key in row:
          self.set(key, row[key])
      self.is_dirty = False
    return False

  def save(self):
    sql = ''
    self.is_dirty = False
    if self.is_new():
      sql = 'INSERT INTO ' + self.db_name
      values = []
      keys = []
      for key in self.attributes:
        values.append(self.attr_to_save_text(key))
        keys.append(key)
      sql = sql + ' (' + ','.join(keys) + ') VALUES '
      sql = sql + ' (' + ','.join(values) + ')'
      return self.cartodb.sql(sql)
      # we need a way to retrieve the cartodb_id
    else:
      sql = 'UPDATE ' + self.db_name + ' SET '
      sets = []
      for key in self.attributes:
        sets.append(key + ' = ' + self.attr_to_save_text(key) + '')
      sql = sql + ','.join(sets)
      sql = sql + ' WHERE cartodb_id = ' + str(self.get('cartodb_id'))
      return self.cartodb.sql(sql)

  def is_new(self):
    return not "cartodb_id" in self.attributes

  def attr_to_save_text(self, key):
    if key == 'the_geom':
      json_attr = "ST_SetSRID(ST_GeomFromGeoJSON('" + self.attributes[key] +"'), 4326)"
      return json_attr #.replace('"', '\\"');
    else:
      json_attr = json.dumps(self.attributes[key])
      return json_attr.replace('"', "'")

  def __init__(self, cartodb, **kwargs):
    self.cartodb = cartodb
    self.domain_name = cartodb.domain_name
    self.db_name = cartodb.current_db
    self.attributes = {}
    self.is_dirty = False
    for key in kwargs:
      self.attributes[key] = kwargs[key]

  def get(self, attr):
    return self.attributes[attr]

  def set(self, attr, value):
    if attr == 'cartodb_id':
      return self
    self.attributes[attr] = value
    self.is_dirty = True
    return self


