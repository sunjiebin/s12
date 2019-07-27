(function (jq) {
    var requesturl;

    function init() {
        //获取要显示的列
        //获取数据
        $.ajax({
            url: requesturl,
            type: 'GET',
            dataType: 'JSON',
            success: function (arg) {
                if (arg.status) {
                    //创建表格标题
                    console.log('数据类型',typeof arg.data.table_config);
                    console.log('table_config',arg.data.table_config);
                    createTablehead(arg.data.table_config);
                    createTablebody(arg.data.table_config, arg.data.data_list);
                } else {
                    alert(arg.message)
                }

            }
        })
    }

    function createTablehead(config) {
        console.log(config);
        var tr = document.createElement("tr");
        /*
        对config进行循环,config相当于一个字典，所以相当于对字典的循环，function(k,v) 其中k为config的第一个值，v为第二个值。
        config: 0 {q: "hostname", title: "主机名", display: 1}
         */

        $.each(config, function (k, v) {
            console.log(k, v);       // k:0 v:{title: "主机名", display: 1}   k:1 v:{title: "用户组", display: 0}
            if (v.display) {
                var th = document.createElement("th");    //创建th
                th.innerText = v.title;                   //给th标签里面添加文本,相当于<th>{{ v.title }}</th>
                tr.append(th);                          //将th标签添加到tr标签里面
                $('#tb').append(tr);                    //找到table标签，并添加tr标签
            }
        })
    }

    function createTablebody(tableconfig, datalist) {
        /*
           datalist=[{'hostname': 'zabbix', 'user_id': 2, 'port': 110}, {'hostname': 'nagios', 'user_id': 1, 'port': 22}]
           tableconfig=table_config=[
                {
                    'q':'hostname',
                    'title':'主机名',
                    'display':1,
                },
                {
                    'q':'user_id',
                    'title':'用户组',
                    'display':0,
                },
                ]
         */
        $.each(datalist, function (k, row) {
            console.log(k, row);
            var tr = document.createElement("tr");

            $.each(tableconfig, function (k2, configitem) {
                if (configitem.display == 1) {
                    var listname = configitem.q;
                    var td = document.createElement("td");
                    /*
                   注意：这里用row.listname是不行的，必须用row[listname]。因为变量listname得到的值是一个字符串。相当于row['hostname']
                   我们用row.hostnmae可以得到key值，但是row.listname是不行的，虽然listname="hostname",这相当于row."hostname"
                    */
                    console.log('listname类型',typeof listname);  //最后一个config.q得到的值为None，None为一个对象，所以最后一次循环返回的是object
                    td.innerText = row[listname];       //这里用row.listname是错误的
                    tr.append(td);
                }

            });
            $('#tb').append(tr);

        })
    }

    jq.extend({                 //注意：这里的jq要与上面的function(jq)对应
        /*
        从外部调用时，可以传递参数进来，参数url就是接受外面传递的参数。
        外部调用方法：$.Int('/server-json.html');
        此时 url='server-json.html'
        requesturl在自执行函数上面有定义。
         */
        'Int':function (url) {
            requesturl = url;
            init();
        }
    })
})(jQuery);     //注意：这里必须要写jQuery，如果不传进来，那么jq.extend方法就找不到。另外，这里要写jQuery，不是jquery，两个不是同一个东西。