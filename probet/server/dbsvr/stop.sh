for iPid in `ps aux | grep python3.6 |  grep db_svr.py | awk '{print $2}'`; do kill -9 ${iPid}; done
