import asyncio
import json
from error.errorCode import exceptionLogic, errorLogic
from gmweb.utils.tools import token_required, permission_required
from lib.jsonhelp import classJsonDump
from lib.timehelp import timeHelp
from datawrapper.sqlBaseMgr import classSqlBaseMgr
import logging


class cResp():
    def __init__(self):
        self.ret = 0
        self.retDes = ""
        self.data = []


@token_required
@permission_required('推广素材管理')
@asyncio.coroutine
def handleHttp(request: dict):
    """获取推广素材"""

    objRep = cResp()

    try:
        sql = "select * from dj_material order by update_time desc"
        result = yield from classSqlBaseMgr.getInstance()._exeCute(sql)
        if result.rowcount <= 0:
            return classJsonDump.dumps(objRep)
        else:
            for var in result:
                materialData = {}
                materialData['imageId'] = var.imageId
                materialData['image_url'] = var.image_url
                materialData['imageSize'] = var.imageSize
                objRep.data.append(materialData)
        fileName = __name__
        nameList = fileName.split('.')
        methodName = nameList.pop()
        # 日志
        dictActionBill = {
            'billType': 'adminActionBill',
            'accountId': request.get('accountId', ''),
            'action': "获取推广素材",
            'actionTime': timeHelp.getNow(),
            'actionMethod': methodName,
            'actionDetail': "获取推广素材",
            'actionIp': request.get('srcIp', ''),
        }
        logging.getLogger('bill').info(json.dumps(dictActionBill))
        return classJsonDump.dumps(objRep)
    except Exception as e:
        logging.exception(e)
        raise exceptionLogic(errorLogic.db_error)

