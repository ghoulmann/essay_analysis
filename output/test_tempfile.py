import os
import tempfile

temp = tempfile.NamedTemporaryFile()
try:
    print 'temp:', temp
    print 'temp.name:', temp.name
    
finally:
    # Automatically cleans up the file
    temp.close()
print 'Exists after close:', os.path.exists(temp.name)
