import asyncio
import json
import logging
from error.errorCode import exceptionLogic, errorLogic
from datawrapper.sqlBaseMgr import classSqlBaseMgr
from gmweb.utils.tools import token_required, permission_required
from lib.jsonhelp import classJsonDump
from lib.timehelp.timeHelp import getNow


class cData():
    def __init__(self):
        self.pc = []
        self.app = []


class cResp():
    def __init__(self):
        self.ret = 0
        self.retDes = ""
        self.data = []


@token_required
@permission_required('推广域名管理')
@asyncio.coroutine
def handleHttp(request: dict):
    """删除域名"""
    objRep = cResp()

    domainId = request.get('domainId', '')

    if not domainId:
        logging.debug(errorLogic.client_param_invalid)
        raise exceptionLogic(errorLogic.client_param_invalid)
    try:
        sql = "delete from dj_domain where domainId='{}' ".format(domainId)
        yield from classSqlBaseMgr.getInstance()._exeCuteCommit(sql)
        sql = "select * from dj_domain"
        result = yield from classSqlBaseMgr.getInstance()._exeCute(sql)
        if result.rowcount <= 0:
            return classJsonDump.dumps(objRep)
        else:
            pcDomainName = []
            appDomainName = []
            for var_row in result:
                if var_row.domainType == 'pc':
                    domainDict = {}
                    domainDict['domainId'] = var_row.domainId
                    domainDict['domainName'] = var_row.domainName
                    pcDomainName.append(domainDict)
                elif var_row.domainType == 'app':
                    domainDict = {}
                    domainDict['domainId'] = var_row.domainId
                    domainDict['domainName'] = var_row.domainName
                    appDomainName.append(domainDict)
            objRep.data = cData()
            objRep.data.pc = pcDomainName
            objRep.data.app = appDomainName
            fileName = __name__
            nameList = fileName.split('.')
            methodName = nameList.pop()
            # 日志
            dictActionBill = {
                'billType': 'adminActionBill',
                'accountId': request.get('accountId', ''),
                'action': "删除推广域名",
                'actionTime': getNow(),
                'actionMethod': methodName,
                'actionDetail': "删除推广域名Id：{}".format(domainId),
                'actionIp': request.get('srcIp', ''),
            }
            logging.getLogger('bill').info(json.dumps(dictActionBill))
            return classJsonDump.dumps(objRep)
    except Exception as e:
        logging.exception(e)
        raise e

