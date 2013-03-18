# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from settings import PROJECT_DIR
import os
import datetime
from models import Records
import sys, traceback

def edit_file(request):
    return  render_to_response('edit.html',context_instance = RequestContext( request ) )

def file_content(request):
    if request.POST.has_key('_path') and request.POST.has_key('_content'):
        _path = request.POST['_path']
        _full_path = (PROJECT_DIR+'/'+_path).replace( '\\', '/' )
        _token = 'DT-CONTENT'+request.POST['_token']
        try:
            if os.path.exists(_full_path):
                _actual_content = actual_content(_path)
                _file = open(_full_path,'w')
                _content = request.POST['_content'].split('\n')
                for _line in _content:
                    _file.write(_line)
                    _file.write('\n')
                _file.close()
                _file = open(_full_path,'r')
                _content = _file.read()
                _file.close()
                _diff_content = dif(_actual_content,_content)
                modify_record(_token,_diff_content)
                return HttpResponse(_content)
            else:
                return HttpResponse('Path error')
        except Exception:
            traceback.print_exc(file=sys.stdout)
            return HttpResponse('False')

    else:
        _path = request.POST['_path']
        _full_path = (PROJECT_DIR+'/'+_path).replace( '\\', '/' )

        if os.path.exists(_full_path):
            _file = open(_full_path,'r')
            _content = _file.read()
            _file.close()
            _token = ref_number()
            add_record(_token,_full_path,request.user)
            _content += str(_token)
            return HttpResponse(_content)
        else:
            return HttpResponse('False')

def add_record(value,filename,user):
    _obj = Records()
    _obj.check_sum =value
    _obj.file_name =filename
    _obj.modified_by = user
    _obj.save()

def modify_record(value,data_dict):
    try:
        _obj = Records.objects.get(check_sum = value)
        _obj.modified_dt = datetime.datetime.now()
        _obj.content_diff = str(data_dict)
        _obj.save()
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        pass


def actual_content(_path):
    _full_path = (PROJECT_DIR+'/'+_path).replace( '\\', '/' )
    if os.path.exists(_full_path):
        _file = open(_full_path,'r')
        _content = _file.read()
        _file.close()
        return _content


def dif(_actual, _modified):
    _diff_content = {}
    _actual = _actual.split('\n')
    _modified = _modified.split('\n')
    if len(_modified)-len(_actual) > 0:
        _diff_positions =  [i for i in range(len(_actual)) if _actual[i] != _modified[i]]
    else:
        _diff_positions =  [i for i in range(len(_modified)) if _actual[i] != _modified[i]]
    for _each_pos in _diff_positions:
        _diff_content[_each_pos] = [_actual[_each_pos],_modified[_each_pos]]
    if len(_modified)-len(_actual) > 0:
       _diff_content[len(_actual)+1] = _modified[len(_actual):]
    else:
        _diff_content[len(_modified)+1] = _actual[len(_modified):]
    return _diff_content


def ref_number():
    litrl = ['-',' ',':','.']
    str_date = str(datetime.datetime.now())
    for each_ltrl in litrl:
        str_date=str_date.replace(each_ltrl,'')
    return 'DT-CONTENT'+str_date
