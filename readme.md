<meta http-equiv="Content-Type" content="text/html; charset=utf-8">

# 项目结构说明
=========================

## magSearcher
 magSearcher 是一个搜索页面，负责查询关键字，展现Magnet连接

## 启动
uwsgi --ini uwsgiconf.ini --plugin python

## json data
allcuts.json
alltag.json
allcutsfilter.json
hottags_s100.json   根据alltag.json 生成的 热词，hashcode count > 100

## Todo List
1. 生成index (done)
2. 兼容多语言界面
3. 发布的反向代理功能
4. log 文件按照日期生成
5. 日志文件监视模块、网站状态监视
6. 更新 document index 的方法
7. sqlalchemy 结合 whoosh
8. 生成 最新的hash的sitemap.xml
8. scrap http://www.fhyishu.net/fhdq.htm 上的番号
9. 爬取电影信息
10. 对爬取的电影、番号信息，在数据库里搜索后，建立影片说明
