import sys
from browser import window


class Err:
    def write(self, err):
        window.alert(err)

sys.stderr = Err()



class TermoApp:

    def call(self, attr, *args, **kwargs):

        termo_repr_args = []

        if not args and not kwargs:
            data = None
        
        else:
            data = window.FormData.new()
            
            for index, i in enumerate(args):
                kwargs[f'termo-arg-{index}'] = i

            for i in kwargs:

                value = kwargs[i]
                classname = value.__class__.__name__

                if classname not in ('str', 'JSObj'):
                    termo_repr_args.append(i)
                    value = repr(value)

                data.append(i, value)


        xhr = window.XMLHttpRequest.new()

        xhr.overrideMimeType('text/plain; charset=x-user-defined')
        xhr.open('POST', '/'+attr, False)
        #xhr.responseType = 'arraybuffer'
        xhr.setRequestHeader('termo-repr-args', ';'.join(termo_repr_args))
        xhr.send(data)

        rtype = xhr.getResponseHeader('termo-response-type')

        if rtype == 'str':
            r = xhr.response

        elif rtype == 'bytes':
            r = window._termojs.str2buff(xhr.response)

        else:
            r = eval(xhr.response)

        return r


    def __getattr__(self, attr):
        return lambda *args, **kwargs: self.call(attr, *args, **kwargs)





app = TermoApp()

utils = window.Object.new()
utils.blob = lambda data: window.Blob.new([data])
utils.url = lambda blob: window.URL.createObjectURL(blob)