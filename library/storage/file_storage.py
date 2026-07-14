from library.storage.base import Storage

class FileStorage(Storage):
 def __init__(self, path: str) -> None:
   self.path = path

 def load(self) -> list[dict]:
   ... # TODO: reuse your fundamentals file handling; split on "|"
   records=[]
   try:
    with open(self.path,'r') as file:
      for line in file:
        line=line.strip()
        if not line:
          continue
        fields=line.split('|')
        keys=fields[0::2]
        values=fields[1::2]
        records.append(dict(zip(keys,values)))
   except FileNotFoundError as e:
    print(e)
   return records
             

 def save(self, records: list[dict]) -> None:
   ... # TODO: serialize each record and write the file
   with open(self.path,'w') as file:
     for record in records:
       line="|".join(f"{k}|{v}" for k, v in record.items())
       file.write(line+"\n")
