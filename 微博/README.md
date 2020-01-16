针对于微博登陆加密破解  

登陆流程：  
1.get请求https://login.sina.com.cn/sso/prelogin.php?entry=weibo获取pcid，nonce,publickey,rsakv,servertime(后面post提交请求登陆和RSA加密会用到)  

2.验证码识别，这里投机取巧了下，用的是Zok大佬用易语言集成的接口直接识别；里面也集成了不止微博一种验证码的识别，且会不断增加不同类型验证码的模型。  
有兴趣的同学可以加群：497377504  
当然，你也可以自己用tensorflow搭建模型进行识别。  

3.模拟登陆中的变化参数主要有：  
pcid: # 第一次请求中会得到  
door:  # 识别出来的验证码  
su: # 用户名加密参数  
servertime:  # 时间戳，第一次请求中会得到  
sp: # 时间戳 + nonce + 密码的加密  
所以最主要的JS加密就是su和sp
