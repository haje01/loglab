"""가짜 로그 생성."""

from datetime import datetime
from dateutil.parser import parse

from loglab.dom import build_dom


def generate_dummy_sync(lab, flow):
    """랩 파일에 기반해 가짜 로그 생성 (동기).

    Args:
        lab (dict): 랩 파일 데이터 
        flow (dict): 플로우 파일 데이터

    """
    # flow = {
    #     "labfile": "foo.lab.json",
    #     "file_by": ["ServerNo", [1, 2]],
    #     "file_ptrn": "foo_{ServerNo:03d}_%Y%m%d.txt",
    #     "datetime": {
    #         "start": "2021-10-20 13",
    #         "speed": 2
    #     },
    #     "flow": {
    #         "spawn_by": ["AcntId", ["aaa", "bbb", "ccc"]],
    #         "spawn_cnt": 2,
    #         "steps": [
    #             "Login",
    #             "Logout"
    #         ]
    #     }
    # }
    dname = lab['domain']['name']
    fptrn = f'{dname}.txt'
    fnames = []

    if 'file_by' in flow:
        if 'file_ptrn' not in flow:
            raise Exception("file_ptrn is required.")
        fby = flow['file_by']
        fld = fby[0]
        fvals = fby[1]

    if 'file_ptrn' in flow:
        fptrn = flow['file_ptrn']

    dt_start = datetime.today()
    dt_speed = 1
    if 'datetime' in flow:
        fdt = flow['datetime']
        if 'start' in fdt:
            dt_start = parse(fdt['start'])
        if 'speed' in fdt:
            dt_speed = fdt['speed']

    d = {}
    if 'file_by' in flow:
        for fv in fvals:
            d[fld] = fv
            fname = dt_start.strftime(fptrn).format(**d)
            fnames.append(fname)
    else:
        fnames = [dt_start.strftime(fptrn).format(**d)]

    if 'flow' in flow:
        import pdb; pdb.set_trace();
        for evt in flow['flow']:
        flines = [
            [
                {"DateTime": "2021-10-20T13:00:00+09:00", "Event": "Login"},
                {"DateTime": "2021-10-20T13:00:01+09:00", "Event": "Logout"}
            ]
        ]
    else:
        flines = [[] for f in fnames]

    return dict(zip(fnames, flines))

    # for path in iter_path(flow):
    #     fp = request_fp(path)
    #     for line in iter_line(path):
    #         fp.write(line)

    # if 'file_by' in flow:
    #     file_field = flow['file_by'][0]
    #     for 
    #     files = for f in flow['file_by']
    # files = dict(for f in flow['file_by'])
    # file_cnt = flow['file_cnt'] if 'file_cnt' in flow else 1
    # file_names = []
    # lab = build_dom(lab)
    # import pdb; pdb.set_trace();

    # f1lines = [
    #     {
    #         "DateTime": "2021-10-20T13:00:00+09:00",
    #         "Event": "Login",
    #         "ServerNo": 1,
    #         "Account": 1
    #     },
    #     {
    #         "DateTime": "2021-10-20T13:00:00+09:00",
    #         "Event": "Login",
    #         "ServerNo": 1,
    #         "Account": 2
    #     },
    #     {
    #         "DateTime": "2021-10-20T13:00:02+09:00",
    #         "Event": "Logout",
    #         "ServerNo": 1,
    #         "Account": 1
    #     },
    #     {
    #         "DateTime": "2021-10-20T13:00:02+09:00",
    #         "Event": "Logout",
    #         "ServerNo": 1,
    #         "Account": 2
    #     }
    # ]
    # f2lines = [
    #     {
    #         "DateTime": "2021-10-20T13:00:00+09:00",
    #         "Event": "Login",
    #         "ServerNo": 2,
    #         "Account": 1
    #     },
    #     {
    #         "DateTime": "2021-10-20T13:00:00+09:00",
    #         "Event": "Login",
    #         "ServerNo": 2,
    #         "Account": 2
    #     },
    #     {
    #         "DateTime": "2021-10-20T13:00:02+09:00",
    #         "Event": "Logout",
    #         "ServerNo": 2,
    #         "Account": 1
    #     },
    #     {
    #         "DateTime": "2021-10-20T13:00:02+09:00",
    #         "Event": "Logout",
    #         "ServerNo": 2,
    #         "Account": 2
    #     }
    # ]
    # files = {
    #     "foo_001_20211020.txt": f1lines,
    #     "foo_002_20211020.txt": f2lines
    # }
    # return files