import requests
import re
import execjs
def get_521_content():
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'
    }
    req=requests.get('http://www.gsxt.gov.cn/corp-query-entprise-info-hot-search-list.html?province=100000',headers=headers)
    cookies=req.cookies
 
    cookies='; '.join(['='.join(item) for item in cookies.items()])
    txt_521=req.text
    txt_521=''.join(re.findall('<script>(.*?)</script>',txt_521))
    return (txt_521,cookies)

def fixed_fun(function):
    func_return=function.replace('eval','return')
    content=execjs.compile(func_return)
    evaled_func=content.call('f')
    #return evaled_func
    mode_func=evaled_func.replace('''setTimeout('location.href=location.pathname+location.search.replace(/[\?|&]captcha-challenge/,\'\')',1500);''','').\
        replace('document.cookie=','return').replace(';if((function(){try{return !!window.addEventListener;}','').\
        replace('''catch(e){return false;}})()){document.addEventListener('DOMContentLoaded',_j,false)}''','').\
        replace('''else{document.attachEvent('onreadystatechange',_j)}''','')
    content = execjs.compile(mode_func)
    #cookies=content.call('_H')
    #__jsl_clearance=cookies.split(';')[0]
    return content

if __name__ == '__main__':
    func=get_521_content()
    content=func[0]
    cookie_id=func[1]
    print(cookie_id)
    cookie_js=fixed_fun(func[0])
    print(cookie_js)
