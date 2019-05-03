obj=document.getElementById('i1');
obj.innerText;
obj.innerHTML;
obj.innerText='sun13';
obj.innerHTML='sun';
// 将内容修改
// innertext会将内容都识别为字符
obj.innerText="<a href=http://www.sina.com>xinlang</a>";
// innerHTML会识别语法
obj.innerHTML="<a href=http://www.sian.com>xinlang</a>";


