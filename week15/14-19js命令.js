// 本内容可以赚chrome的console控制台执行
a='alex'
a.concat(' is a teacher')
a
a.indexOf('ex')

// 17节 直接查找标签内容
// document可以通过id,标签名词,name属性,class属性来查找对应的内容
// 根据id名词获取整个标签
document.getElementById('i1');
a=document.getElementById('i1');
// 获取标签里面的内容
a.innerText;
// 修改标签里面的内容
a.innerText='测试';
// 获取所有的a标签,获取的标签会以列表的形式展现出来
b=document.getElementsByTagName('a');
b;
// 获取第二个a标签
b[1];
// 对第二个a标签的值进行修改
b[1].innerText='2222'
// 用for循环来修改所有的a标签
for(var i=0;i<b.length;i++){b[i].innerText='全被替换'};
// 可以根据类的名称查找
c=document.getElementsByClassName('test2');
c[0].innerText='替换class';

// 18节 间接查找标签内容,以18为操作页面
// 获取i1的标签
tag=document.getElementById('i1');
// 获取i1标签的父级标签
tag.parentElement;
// 获取第一个子级标签
tag.parentElement.firstElementChild;
// 获取最后一个子标签
tag.parentElement.lastElementChild;
// 获取父级目录下所有子标签,包括其他类型的标签,并以数组(python中叫列表)的形式展示
tag.parentElement.children;
// 获取下一个兄弟标签
tag.parentElement.nextElementSibling;
// 获取上一个兄弟标签
tag.previousElementSibling;

// 对标签的修改操作
//className直接对class整体替换新增等操作.classList对class追加删除等操作
//对tag添加一个class属性,值为c1.此时div标签中会多了class='c1'的属性
tag.className='c1';
// 将c1修改为c2
tag.className='c2';
// 以列表的形式显示tag下的所有class
tag.classList;
// 追加class c4
tag.classList.add('c4');
// 移除class c4
tag.classList.remove('c4');