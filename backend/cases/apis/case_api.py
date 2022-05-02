from typing import List

from django.forms import model_to_dict
from django.shortcuts import get_object_or_404
from ninja import Router, Query
from ninja.pagination import paginate

import requests

from backend.common import Error, response, children_node, node_tree
from backend.pagination import CustomPagination

from cases.apis.api_schema import CaseIn, CaseDebugIn, CaseAssertIn, CaseOut
from cases.models import Module, TestCase

router = Router()


@router.post("/", auth=None)
def create_case(request, data: CaseIn):
    """
    创建用例
    auth=None，该接口不需要认证
    """

    case = Module.objects.filter(id=data.module_id)
    if len(case) == 0:
        return response(error=Error.MODULE_NOT_EXIST)

    case = TestCase.objects.create(**data.dict())
    return response(item=model_to_dict(case))


@router.post('/debug/', auth=None)
def debug_case(request, data: CaseDebugIn):
    """
    测试用例调试
    auth=None，该接口不需要认证
    """

    method = data.method.value
    param_type = data.params_type.value

    if method == "GET" and param_type == "Params":
        resp = requests.request(method=method, url=data.url, headers=data.header, params=data.params_body).text
    elif method in ["POST", "PUT", "DELETE"] and param_type == "Form":
        resp = requests.request(method=method, url=data.url, headers=data.header, data=data.params_body).text
    elif method in {"POST", "PUT", "DELETE"} and param_type == "Json":
        resp = requests.request(method=method, url=data.url, headers=data.header, json=data.params_body).text
    else:
        return response(error=Error.CASE_REQEUST_ERROR)
    return response(item={"response": resp})


@router.post("/assert/", auth=None)
def assert_cast(request, data: CaseAssertIn):
    """
    断言判断
    auth=None，该接口不需要认证
    """

    resp = data.response
    assert_type = data.assert_type.value
    assert_text = data.assert_text

    if assert_type == "include":
        if assert_text in resp:
            return response()
        else:
            return response(success=False)
    elif assert_type == "equal":
        if assert_text == resp:
            return response()
        else:
            return response(success=False)
    return response()


@router.put("/update/{case_id}", auth=None)
def update_case(request, case_id: int, data: CaseIn):
    """
    用例更新
    auth=None，该接口不需要认证
    """

    case = get_object_or_404(TestCase, id=case_id)
    for attr, value in data.dict().items():
        setattr(case, attr, value)
    case.save()
    return response()


@router.delete("/delete/{case_id}", auth=None)
def delete_case(request, case_id):
    """
    删除测试用例
    auth=None，该接口不需要认证
    """

    case = get_object_or_404(TestCase, id=case_id)
    case.is_delete = True
    case.save()
    return response()


@router.get('/list/', auth=None, response=List[CaseOut])
@paginate(CustomPagination, page_size=6)  # type: ignore
def list_case(request, **kwargs):
    """
    查询用例列表
    auth=None，该接口不需要认证
    """

    return TestCase.objects.filter(is_delete=False).all()


@router.get('/{case_id}/', auth=None)
def detail_case(request, case_id):
    """
    获取项目详情
    auth=None，该接口不需要认证
    """

    case = get_object_or_404(TestCase, id=case_id)  # django 的获取对象方法，没有返回 404 和 msg，节省捕捉异常逻辑
    if case.is_delete is True:
        return response(error=Error.CASE_IS_DEELEE)

    data = {
        "id": case.id,
        "name": case.name,
        "url": case.url,
        "method": case.method,
        "create_time": case.create_time,
        "update_time": case.update_time
    }
    return response(item=data)