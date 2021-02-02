# Bug南航- i南航 自动打卡系统
## 使用方法
1. fork本项目到自己的仓库
2. 在settings-secrets里面设置以下secret,详见[参数配置](#canshu)
3. 提交一次，你可以删除本文档中任何一个字符然后提交一次

<h2 id="canshu">参数配置</h2>
student_id 学号  

password 密码  

sckey 在 [Server酱-发送消息](http://sc.ftqq.com/?c=code) 绑定微信找到SCKEY填入  

address XX省XX市（区）(XX县)XXX  

## 注意：
1. config.ini中所有的参数都是提交时提交上去的，默认全否。
2. 如果您要修改打卡时间，请修改nuaa.yaml中的` - cron: '30 16 * * *'`,30代表分钟，16代表小时。请注时间是GMT时间，也就是比北京时间慢8个小时。

### 免责声明
本程序仅供学习参考，请在下载或fork后24小时内删除，否则后果自负！

