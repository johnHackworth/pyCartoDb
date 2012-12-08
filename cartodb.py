import urllib2
import urllib
import json
from cartodb_object import CartoDb_object

try:
  from settings import *
except ImportError:
  print "Warning: custom_settings could not be loaded"
  pass

class Cartodb:
  api_key = pyCartodb_api_key
  domain_name = pyCartodb_domain_name

  def __init__(self, domain_name):
    self.domain_name = domain_name

  def urlRoot(self):
    return 'http://' + self.domain_name + '.cartodb.com/api/v2/sql?api_key='+ self.api_key+'&q='

  def parseSQL(self):
    self.params.reverse()
    db = self.params.pop()
    sql = ''
    if db['type'] == 'SELECT':
      sql = self.parseSELECT(db["value"])
    elif db['type'] == 'INSERT':
      sql = self.parseINSERT(db["value"])

    self.params = []
    return sql

  def parseINSERT(self, db_name):
    sql = 'INSERT INTO ' + db_name
    while len(self.params) > 0:
      fields = self.params.pop()
      col_names = []
      col_values = []
      for key in fields['column']:
        col_names.append(key)
        col_values.append(fields['column'][key])
      sql = sql + ' ("' + '","'.join(col_names) + '")'
      sql = sql + ' VALUES '
      sql = sql + ' (\'' + '\',\''.join(col_values) + '\')'
      sql = sql + ';'
    return sql

  def parseSELECT(self, db_name):

    sql = 'SELECT * FROM ' + db_name
    sql_params = []
    while len(self.params) > 0:
      sql_params.append(self.extractParam())
    if len(sql_params) > 0:
      sql = sql + ' WHERE ' + ' AND '.join(sql_params)
    return sql

  def extractParam(self):
    if len(self.params) > 0:
      param1 = self.params.pop()
      if param1["name"] == 'field':
        value = self.params.pop()
        if value["name"] != "comp":
          return ''
          # should throw and exception
        else:
          if value["type"] == 'is':
            return param1["value"] + " ilike '%" + value["value"] + "%'"
    return ''


  def at(self, db_name):
    self.current_db = db_name
    self.params = [{"name":"db_name", "type": "SELECT", "value": db_name}]
    return self

  def to(self, db_name):
    self.params = [{"name":"db_name", "type": "INSERT", "value": db_name}]
    return self

  def add(self, col):
    self.params.append({"name":"column", "column": col})
    return self

  def field(self, value):
    self.params.append({"name":"field", "value":value})
    return self

  def has(self, value):
    self.params.append({"name":"comp", "type": "is", "value": value})
    return self

  def bigger(self, value):
    self.params.append({"name":"comp", "type": "big", "value": value})
    return self

  def sql(self, sql):
    print self.urlRoot() + sql
    fetcher = urllib2.urlopen(self.urlRoot() + urllib.quote_plus(sql))
    result = fetcher.read()
    return result

  def open(self):
    response = self.sql(self.parseSQL())
    return self.objectify(response)

  def toObject(self, obj):
    return CartoDb_object(self, **obj)

  def objectify(self, jsonResponse):
    carto_objects = []
    responses = json.loads(jsonResponse)
    for obj in responses['rows']:
      carto_objects.append(self.toObject(obj))
    return carto_objects
