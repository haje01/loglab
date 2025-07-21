"""랩 파일 Document Object Model."""
import os
import copy
import json
from json.encoder import py_encode_basestring
from collections import defaultdict

from loglab.util import BUILTIN_TYPES, AttrDict, get_dt_desc


def _build_domain(data):
    """lab 파일에서 도메인 정보를 추출.
    
    Args:
        data (dict): lab 파일 데이터
        
    Returns:
        dict: 도메인 정보
        
    Raises:
        Exception: 도메인 정보가 없는 경우
    """
    if 'domain' not in data:
        raise Exception("Required domain information not found.")
    return data['domain']


def _build_types(data, _dnames=None, _types=None):
    """lab 파일에서 커스텀 타입 정보를 재귀적으로 수집.
    
    import된 파일들도 포함하여 모든 커스텀 타입을 수집하고
    도메인 경로와 함께 저장함.
    
    Args:
        data (dict): lab 파일 데이터
        _dnames (list, optional): 도메인 이름 경로
        _types (defaultdict, optional): 수집된 타입들
        
    Returns:
        defaultdict: 타입명을 키로 하고 [도메인경로, 타입정의] 리스트를 값으로 하는 딕셔너리
    """
    if _types is None:
        _types = defaultdict(list)

    if _dnames is None:
        _dnames = []

    if '_imported_' in data:
        for idata in data['_imported_']:
            dname = idata['domain']['name']
            _build_types(idata, _dnames + [dname], _types)

    if 'types' in data:
        for tname, tdata in data['types'].items():
            path = '.'.join(_dnames)
            _types[tname].append([path, tdata])

    return _types


def _resolve_type(tname, _types):
    """타입 이름을 사용하여 실제 타입 정의를 찾아 반환.
    
    도메인 경로를 고려하여 정확한 타입을 찾고, 직접 매치가 안되면
    부분 매치를 시도함.
    
    Args:
        tname (str): 'domain.types.typename' 형태의 타입 이름
        _types (defaultdict): 수집된 타입 정보
        
    Returns:
        dict: 타입 정의의 복사본
        
    Raises:
        AssertionError: 타입 이름이 타입 데이터에 없는 경우
        Exception: 해당 도메인에서 타입을 찾을 수 없는 경우
    """
    elms = tname.split('.')
    domain = '.'.join(elms[:-2])
    name = elms[-1]
    assert name in _types, f"Can not find '{name}' in type data."

    # direct match
    for item in _types[name]:
        idomain, idata = item
        if idomain == domain:
            return copy.deepcopy(idata)

    # indirect match
    for item in _types[name]:
        idomain, idata = item
        if idomain.startswith(domain):
            return copy.deepcopy(idata)

    raise Exception(f"Can not find '{tname}' in type data")


def _flat_fields(data, _types, _dnames, lang, for_event=False, use_ctype=False):
    """베이스 또는 이벤트의 필드를 평탄화하고 타입을 해결.
    
    필드 정의를 표준화된 형태로 변환하고, 커스텀 타입을 실제 타입 정의로 치환.
    이벤트인 경우 DateTime 필드를 자동으로 추가함.
    
    Args:
        data (dict): 베이스 또는 이벤트 데이터
        _types (defaultdict): 커스텀 타입 정보
        _dnames (list): 도메인 이름 경로
        lang (str): 언어 코드
        for_event (bool): 이벤트용인지 여부. 기본 False
        use_ctype (bool): 커스텀 타입을 그대로 유지할지 여부. 기본 False
        
    Returns:
        dict: 평탄화된 필드 정보를 포함한 데이터
    """
    if 'fields' not in data:
        data['fields'] = {}
    else:
        data = copy.deepcopy(data)

    def _is_flat(fdata):
        """필드 데이터가 이미 평탄화되었는지 확인.
        
        Args:
            fdata: 필드 데이터
            
        Returns:
            bool: 평탄화된 상태인지 여부
        """
        if type(fdata) is not defaultdict:
            return False
        if len(fdata) == 0:
            return True
        return type(list(fdata.values())[0]) is list

    if _is_flat(data['fields']):
        return data

    fields = defaultdict(list)
    if for_event:
        tdata = dict(type='datetime', desc=get_dt_desc(lang))
        fields['DateTime'].append(['', tdata])

    for f in data['fields']:
        path = '.'.join(_dnames)
        rst = {}
        if type(f) is dict:
            rst = copy.deepcopy(f)
            del rst['name']
            del rst['type']
            del rst['desc']
            f = [f['name'], f['type'], f['desc']]
            if 'option' in f:
                f.append(f['option'])
                del rst['option']

        tname = f[1]
        if tname not in BUILTIN_TYPES:
            # if 'types.' not in tname:
            #     raise Exception("Illegal custom type (Are you forgetting 'types.' for custom type?).")
            tname = f'{path}.{tname}' if len(path) > 0 else tname

        if 'types' in tname and not use_ctype:
            tdata = _resolve_type(tname, _types)
            tdata['desc'] = f[2]
        else:
            tdata = dict(type=tname, desc=f[2])
        if len(f) > 3:
            tdata['option'] = f[3]

        if len(rst) > 0:
            for k, v in rst.items():
                tdata[k] = v
        fields[f[0]].append([path, tdata])
    data['fields'] = fields

    return data


def _resolve_mixins(name, lang, _dnames, _bases, _events=None, for_event=False):
    """믹스인을 해결하여 최종 필드 구성을 생성.
    
    지정된 믹스인들을 순서대로 처리하여 필드를 병합하고,
    설명(desc)이 없는 경우 믹스인에서 가져옴.
    
    Args:
        name (str): 처리할 베이스/이벤트 이름
        lang (str): 언어 코드
        _dnames (list): 도메인 이름 경로
        _bases (defaultdict): 베이스 정보
        _events (defaultdict, optional): 이벤트 정보
        for_event (bool): 이벤트용인지 여부. 기본 False
        
    Raises:
        Exception: 믹스인을 찾을 수 없거나 부적절한 믹스인 사용시
    """
    pbase = name in _bases
    pevent = name in _events if _events is not None else False
    if not pbase and not pevent:
        raise Exception("Can not find mixin {name} in both bases and events.")
    if _events is None and pevent:
        raise Exception("You can not mixin an event for a base.")

    _refer = _bases if _events is None else _events
    data = _refer[name][-1][1]
    if 'mixins' not in data:
        return data

    fields = defaultdict(list)
    if for_event:
        tdata = dict(type='datetime', desc=get_dt_desc(lang))
        fields['DateTime'].append(['', tdata])

    mdesc = None
    # mixin fields first
    for mpath in data['mixins']:
        mpath = '.'.join(_dnames + [mpath])
        if not for_event and 'events' in mpath:
            raise Exception(f"You can not mixin '{mpath}' for a base.")
        mname, mdata = _find_mixin(mpath, _bases, _events)
        if mdesc is None and 'desc' in mdata[1]:
            mdesc = mdata[1]['desc']
        if 'fields' not in mdata[1]:
            continue
        for mf, mds in mdata[1]['fields'].items():
            if mf != 'DateTime' or mf not in fields:
                fields[mf].append(mds[-1])

    # resolve desc
    if 'desc' not in data:
        if mdesc is None:
            raise Exception(f"'Can not resolve description for '{name}'.")

        data['desc'] = mdesc

    # then own fields
    if 'fields' in data:
        for k, v in data['fields'].items():
            if k != 'DateTime' or k not in fields:
                fields[k].append(v[-1])

    data['fields'] = fields
    del data['mixins']


def _find_mixin(path, _bases, _events):
    """믹스인 경로를 파싱하여 해당 믹스인을 찾아 반환.
    
    Args:
        path (str): 'domain.bases.name' 또는 'domain.events.name' 형태의 믹스인 경로
        _bases (defaultdict): 베이스 정보
        _events (defaultdict): 이벤트 정보
        
    Returns:
        tuple: (믹스인 이름, [도메인경로, 믹스인데이터])
        
    Raises:
        Exception: 잘못된 믹스인 경로이거나 믹스인을 찾을 수 없는 경우
    """
    if '.' not in path:
        raise Exception(f"Illegal mixin path '{path}'")
    elms = path.split('.')
    atype = elms[-2]
    if atype not in ('bases', 'events'):
        raise Exception(f"Illegal mixin type '{atype}'")
    name = elms[-1]
    _path = '.'.join(elms[:-2])
    _refer = _bases if atype == 'bases' else _events

    if name not in _refer:
        raise Exception(f"Can not find mixin '{name}' in {atype}")
    for e in _refer[name]:
        if e[0] == _path:
            return name, e
    raise Exception(f"Can not find mixin path '{path}'")


def _build_bases(data, lang, _dnames=None, _types=None, _bases=None, use_ctype=False):
    """베이스 요소들을 빌드하고 믹스인을 해결.
    
    재귀적으로 import된 파일들의 베이스도 처리하고,
    각 베이스의 필드를 평탄화한 후 믹스인을 해결함.
    
    Args:
        data (dict): lab 파일 데이터
        lang (str): 언어 코드
        _dnames (list, optional): 도메인 이름 경로
        _types (defaultdict, optional): 커스텀 타입 정보
        _bases (defaultdict, optional): 수집된 베이스 정보
        use_ctype (bool): 커스텀 타입을 그대로 유지할지 여부. 기본 False
        
    Returns:
        defaultdict: 베이스명을 키로 하고 [도메인경로, 베이스정의] 리스트를 값으로 하는 딕셔너리
    """
    if _types is None:
        _types = defaultdict(list)
    if _bases is None:
        _bases = defaultdict(list)
    if _dnames is None:
        _dnames = []

    data = copy.deepcopy(data)

    if '_imported_' in data:
        for idata in data['_imported_']:
            dname = idata['domain']['name']
            _build_bases(idata, lang, _dnames + [dname], _types, _bases, use_ctype)

    if 'types' in data:
        _build_types(data, _dnames, _types)

    if 'bases' not in data:
        return _bases

    # flatten fields
    nbdata = {}
    for bname, bdata in data['bases'].items():
        path = '.'.join(_dnames)
        ndata = _flat_fields(bdata, _types, _dnames, lang, use_ctype=use_ctype)
        nbdata[bname] = ndata
        _bases[bname].append([path, ndata])

    for bname, bdata in nbdata.items():
        _resolve_mixins(bname, lang, _dnames, _bases)

    return _bases


def _build_events(data, lang=None, _dnames=None, _types=None, _bases=None, _events=None,
                  use_ctype=False):
    """이벤트들을 빌드하고 관련 베이스/타입들도 함께 처리.
    
    재귀적으로 import된 파일들도 처리하고, 베이스를 먼저 빌드한 후
    이벤트들의 필드를 평탄화하고 믹스인을 해결함.
    
    Args:
        data (dict): lab 파일 데이터
        lang (str, optional): 언어 코드
        _dnames (list, optional): 도메인 이름 경로
        _types (defaultdict, optional): 커스텀 타입 정보
        _bases (defaultdict, optional): 베이스 정보
        _events (defaultdict, optional): 수집된 이벤트 정보
        use_ctype (bool): 커스텀 타입을 그대로 유지할지 여부. 기본 False
        
    Returns:
        defaultdict: 이벤트명을 키로 하고 [도메인경로, 이벤트정의] 리스트를 값으로 하는 딕셔너리
    """
    if _types is None:
        _types = defaultdict(list)
    if _bases is None:
        _bases = defaultdict(list)
    if _events is None:
        _events = defaultdict(list)
    if _dnames is None:
        _dnames = []
    data = copy.deepcopy(data)

    if '_imported_' in data:
        # 수입된 것이 있으면 그것도 빌드
        for idata in data['_imported_']:
            dname = idata['domain']['name']
            _build_events(idata, lang, _dnames + [dname], _types, _bases,
                          _events, use_ctype=use_ctype)
    if 'types' in data:
        _build_types(data, _dnames, _types)

    if 'bases' in data:
        _build_bases(data, lang, _dnames, _types, _bases, use_ctype)

    if 'events' not in data:
        return _events

    # flatten fields
    nedata = {}
    for ename, edata in data['events'].items():
        path = '.'.join(_dnames)
        ndata = _flat_fields(edata, _types, _dnames, lang, True, use_ctype=use_ctype)
        nedata[ename] = ndata
        _events[ename].append([path, ndata])

    for ename, edata in nedata.items():
        _resolve_mixins(ename, lang, _dnames, _bases, _events, True)

    return _events


def build_model(data, lang=None, use_ctype=False):
    """lab 파일 데이터로부터 완전한 모델을 구성.
    
    도메인, 타입, 베이스, 이벤트 정보를 모두 수집하고 해결하여
    사용 가능한 형태의 모델 객체를 생성함.

    Args:
        data (dict): lab 파일 데이터
        lang (str, optional): 언어 코드 (국제화용)
        use_ctype (bool): 커스텀 타입을 원본 형태로 유지할지 여부. 기본 False
        
    Returns:
        AttrDict: domain, types, bases, events 속성을 가진 모델 객체
    """
    domain = _build_domain(data)

    types = defaultdict(list)
    bases = defaultdict(list)
    events = defaultdict(list)
    _build_events(data, lang, None, types, bases, events, use_ctype)
    return AttrDict(dict(domain=domain, types=types, bases=bases,
                    events=events))


def handle_import(labfile, labjs):
    """랩 파일이 참조하는 외부 랩 파일들을 재귀적으로 로드.
    
    import 필드에 지정된 파일들을 찾아 로드하고,
    해당 파일들이 또 다른 import를 가지고 있으면 재귀적으로 처리.
    로드된 데이터는 '_imported_' 키에 저장됨.

    Args:
        labfile (str): 기준이 되는 랩파일 경로
        labjs (dict): 랩 데이터 (수정됨)
        
    Raises:
        FileNotFoundError: import할 파일을 찾을 수 없는 경우
    """
    if 'import' not in labjs:
        return labjs

    if '_imported_' not in labjs:
        labjs['_imported_'] = []

    adir = os.path.dirname(labfile)

    for imp in labjs['import']:
        path = os.path.join(adir, f'{imp}.lab.json')
        if not os.path.isfile(path):
            raise FileNotFoundError(path)

        with open(path, 'rt', encoding='utf8') as f:
            body = f.read()
            data = json.loads(body)
            if 'import' in data:
                handle_import(labfile, data)
            labjs['_imported_'].append(AttrDict(data))


def _handle_import(labjs):
    """랩 파일의 import 데이터를 처리 (테스트용).
    
    실제 파일 시스템이 아닌 메모리상의 데이터로부터
    import를 처리하는 테스트용 함수.

    Args:
        labjs (dict): 랩 데이터 (수정됨)
    """
    if 'import' not in labjs:
        return labjs

    if '_imported_' not in labjs:
        labjs['_imported_'] = []

    for idata in labjs['import']:
        if 'import' in idata:
            _handle_import(idata)
        labjs['_imported_'].append(AttrDict(idata))