'use strict';

window._termojs = {

    str2buff(str) {
        const buf = new ArrayBuffer(str.length);
        const buf_view = new Uint8Array(buf);

        let i = 0;
        while (i < str.length) {
            buf_view[i] = str[i].charCodeAt(0);
            i++;
        }
        
        return buf;
    }

}