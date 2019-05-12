
//创建自执行函数()(). 就是在创建函数时,函数就已经执行了.这样可以避免引用多个js文件时,不同的文件中的
//全局变量命相同而照成的冲突问题
//arg是形式参数,实参是jquery
(function (arg) {
    var status=1;
    arg.extend({
        jie:function () {
            return 'jie';
        }
    })
// 传入的jquery为实际参数,这里可以用$替代
})(jQuery);

(function () {
    var status=2;
    $.extend({
        bin:function () {
            return status;
        }
    })
})();



$.extend({
    sun:function () {
        return 'aa';
    }
});