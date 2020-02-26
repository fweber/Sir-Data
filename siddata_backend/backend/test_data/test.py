import csv


with open('datasets_x5gon_user_data.psv') as tsvfile:
  reader = csv.reader(tsvfile, delimiter='|')
  for row in reader:
      id = row[1]
      if id != 'url':
          if type(id) != str:
              print(type(id))
          id = int(id)

      # for i in id:
      #     if i not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
      #         print(id)
