import hashlib

def hash(msg):
  encoder = hashlib.sha256()
  encoder.update(msg.encode())
  return encoder.hexdigest()