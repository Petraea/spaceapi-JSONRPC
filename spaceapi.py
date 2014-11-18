import json
import os

class SpaceapiMethods():
    '''API handling methods.'''
    tmpapifile ='/tmp/status.json.tmp'
    apifile = '/tmp/status.json'
    try:
        apidata = json.load(apifile)
    except:
        print ('Parse error! Defaulting...')
        apidata = {} #TBA
    def _update():
        '''Update the outward readable file.'''
        try:
            with open(tmpapifile,'w') as apifile:
                json.dump(api13, apifile,indent=1)
                self.apifile.flush()   # Build atomic operation to prevent zero-length file existing
                os.fsync(apifile.fileno())
            os.rename(tmpapifile, apifile)
        except:
            logging.error('write failed on status.json.')

    def get_state():
        '''Read the space open state'''
        return self.apidata['state']['open']

    def state_set(state=False):
        '''Write the space open state'''
        self.apidata['state']['open'] = state
        _update()
        return state
        
    def state_toggle():
        '''Toggle the space open state'''
        self.state_set(!self.get_state())        
        return self.get_state()
        
    def get_info(info):
        '''Try to match string structure into the api tree e.g. 'sensors.temperature.0.value' and return the resulting object.'''
        splitinfo = info.split('.')
        structure = self.apidata.copy()
        for n, word in enumerate(splitinfo):
            n = len(splitinfo) - n
            if n >1:
                if isinstance(structure,dict):
                    structure = structure[word]
                elif isinstance(structure,list) and word.isdigit():
                    structure = structure[int(word)]
                else:
                    raise ValueError
            else:
                if isinstance(structure,dict):
                    return structure[word]
                elif isinstance(structure,list):
                    return structure[int(word)]
        
    def update_info(info,value):
        '''Try to match string structure into the api tree e.g. 'sensors.temperature.0.value' and put the value object there.'''
        splitinfo = info.split('.')
        reverseinfo = splitinfo.reverse()
        structure = None
        for n, word in enumerate(reverseinfo):
            oldvalue = get_info('.'.join(splitinfo[:-n]))
            if n ==0:
                structure = value
            else:
                if isinstance(oldvalue,dict):
                    del oldvalue(word)
                    structure = oldvalue.update({word,structure})
                elif isinstance(oldvalue,list) and word.isdigit():
                    oldvalue[int(word)] = structure
                    structure = oldvalue
        self.apidata = structure

    def update_sensor(sensorid,data):
        pass
    def add_sensor(