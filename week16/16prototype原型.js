function foo2(n) {
    this.name=n;
    this.sayname=function () {
        console.log(this.name);
    }
}
// 通过上面的定义,下面创建了两个对象,sayname函数被重复定义,不利于内存的优化
var obj3=new foo2('hei');
obj3.name
obj3.sayname();
var obj4=new foo2('an');
obj4.sayname();

// 引入原型,通过原型,解决重复定义问题
function foo(n) {
    this.name=n;
};
// foo的原型
foo.prototype={
    'sayname':function () {
        console.log(this.name);
    }
};
// 通过上面的定义,在创建对象时,就只加载了this.name.
obj1=new foo('we');
obj2=new foo('魏');
obj1.sayname();