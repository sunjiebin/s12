

# Create your views here.
from django.shortcuts import render
from stark import settings
from django.http import FileResponse
from django.utils.encoding import smart_str
def file_download(request):
    '''访问url时将下载文件，而不是显示文件，就跟ftp一样
    django里面有HttpResponse,StreamingHttpResponse,FileResponse
    '''
    file_path=request.GET.get('file_path')
    if file_path:
        file_center_dir=settings.SALT_CONFIG_FILES_DIR
        file_path=f'{file_center_dir}{file_path}'
        print('file_path',file_path)
        file_name=file_path.split('/')[-1]
        response=FileResponse(open(file_path,'rb'))    #用django的FileResponse来打开file_path文件
        # 将Content-Disposition的请求头设置为attachment格式，也就是附件的形式。filename为附件文件名
        response['Content-Disposition']='attachment;filename=%s'%file_name
        # 格式化
        response['X-Sendfile']=smart_str(file_path)
        return response
    else:
        raise  KeyError