# API

## 查询

接口：`/api/search`

方法：`POST`

参数：

```json
{
    color: 'ff00ff', // optional
    size: 'large', // optional, [large, small, medium]
    id: '313hn32g2u32g', // optional, img id
    page: 0, // optional, default is 0, the result on page 0
    num: 20, // optional, default is 20, return 20 imgs each time
}
```

结果：

```json
{
    code: 0, // status, 0 means normal, other means error
    msg: '', // message
    total: 119, // 119 imgs found
    page: 0, // the result on page 0
    num: 20, // the number of imgs
    imgs: [
        '.....1', // img id
        '.....2',
    ]
}
```

## 相关

接口：`/api/relate`

方法：`POST`

参数：

```json
{
    img: '.....1', // img id
    num: 20, // optional, default is 20, return first 20 imgs
}
```

结果：

```json
{
    code: 0, // status, 0 means normal, other means error
    msg: '', // message
    num: 20, // the number of imgs
    imgs: [
        '.....1', // img id
        '.....2',
    ]
}
```

## 上传图片

接口：`/api/upload`

方法：POST

参数：

```json
{
	img: (binary data) 
}
```

结果：

```json
{
    code: 0, // status, 0 means normal, other means error
    msg: '', // message
    id: '43h423dfuifds8f' // uploaded img id
}
```

## 获取并显示图片

接口：`/img/<imgID>` 和 `/upload/<imgID>`

参数：`?s=400y400` 表示求大小为 400x400 的缩略图

方法：GET
