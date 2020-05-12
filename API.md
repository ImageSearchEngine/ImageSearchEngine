# API

## 查询

接口：`/api/search/`

方法：`POST`

参数：

```json
{
    color: 'FF00FF', //null表示不约束这一维
    size: 'large', //large small medium null表示不约束
    keyword: '关键词', //null表示不约束
    page: 0, //以上关键词查询下第k页的结果
    pagesize: 20, //每页显示20张图片
}
```

结果：

```json
{
    total: 119, //总共找到119条结果
    page: 0, //这是第0页的结果列表
    pagesize: 20, //每页返回20个
    imgURLs:[
        '.....1.png',
        '.....2.png',
    ]
}
```



## 相关


接口：`/api/relate/`

方法：`POST`

参数：

```json
{
    imgURL:'....1.png',//查询的图片的url
    maxsize:20,//返回前20个相关图片   
}
```

结果：

```json
{
    maxsize: 20, //前20个相关图片
    imgURLs:[
        '.....1.png',
        '.....2.png',
    ]
}
```
