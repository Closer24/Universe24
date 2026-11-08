"""Make a hash-linked compact audit view; retain its complete original and gzip."""
import argparse,gzip,hashlib,json,shutil
from pathlib import Path

def file_sha(path):
 h=hashlib.sha256()
 with Path(path).open('rb') as f:
  for chunk in iter(lambda:f.read(1048576),b''):h.update(chunk)
 return h.hexdigest()

def compact(source):
 source=Path(source);zipped=source.with_suffix(source.suffix+'.gz');summary=source.with_name(source.stem+'_summary.json')
 assert not zipped.exists() and not summary.exists()
 with source.open('rb') as src,zipped.open('xb') as dst,gzip.GzipFile(fileobj=dst,mode='wb',mtime=0) as out:shutil.copyfileobj(src,out)
 data=json.loads(source.read_text());omitted=[]
 def visit(value,path):
  if isinstance(value,dict):
   for key in list(value):
    child=value[key]
    if key=='boundary_counter_hits' and isinstance(child,list):
     encoded=json.dumps(child,sort_keys=True,separators=(',',':')).encode();metadata=dict(count=len(child),canonical_sha256=hashlib.sha256(encoded).hexdigest());value.pop(key);value[key+'_summary']=metadata;omitted.append(dict(path=path+'/'+key,**metadata))
    else:visit(child,path+'/'+key)
  elif isinstance(value,list):
   for i,item in enumerate(value):visit(item,path+'/'+str(i))
 visit(data,'');data['complete_certificate']=dict(path=str(zipped),gzip_sha256=file_sha(zipped),decoded_sha256=file_sha(source),decoded_bytes=source.stat().st_size);data['summary_omissions']=omitted;data['summary_generator_sha256']=file_sha(__file__);data['summary_scope']='All checks and conclusions retained. Exhaustive boundary-address rows replaced only in this derivative view by counts and canonical hashes; complete original bytes remain available losslessly.'
 with summary.open('x') as f:json.dump(data,f,sort_keys=True,indent=2);f.write('\n')
 print(json.dumps(dict(summary=str(summary),gzip_bytes=zipped.stat().st_size,omitted_lists=len(omitted))))
if __name__=='__main__':
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('source');compact(ap.parse_args().source)
