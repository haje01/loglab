"""랩 파일 Document Object Model."""
import copy
from json.encoder import py_encode_basestring

from loglab.util import BUILTIN_TYPES, AttrDict, DefaultOrderedDict


def _build_domain(data):
    if 'domain' not in data:
        raise Exception("Required domain information not found.")
    return data['domain']


def _build_types(data, _dnames=None, _types=None):
    if _types is None:
        _types = DefaultOrderedDict(list)

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


def _flat_fields(data, _types, _dnames, for_event=False, use_ctype=False):
    """베이스 또는 이벤트가 참조하는 필드를 평탄화."""
    if 'fields' not in data:
        data['fields'] = {}
    else:
        data = copy.deepcopy(data)

    def _is_flat(fdata):
        if type(fdata) is not DefaultOrderedDict:
            return False
        if len(fdata) == 0:
            return True
        return type(list(fdata.values())[0]) is list

    if _is_flat(data['fields']):
        return data

    fields = DefaultOrderedDict(list)
    if for_event:
        tdata = dict(type='datetime', desc='이벤트 일시')
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


def _resolve_mixins(name, _dnames, _bases, _events=None, for_event=False):
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

    fields = DefaultOrderedDict(list)
    if for_event:
        tdata = dict(type='datetime', desc='이벤트 일시')
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
            raise Exception(f"Can not resolve description for '{name}'.")
        data['desc'] = mdesc

    # then own fields
    if 'fields' in data:
        for k, v in data['fields'].items():
            if k != 'DateTime' or k not in fields:
                fields[k].append(v[-1])

    data['fields'] = fields
    del data['mixins']


def _find_mixin(path, _bases, _events):
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
    import pdb; pdb.set_trace()
    raise Exception(f"Can not find minxin path {path}")


# def _resolve_import(data):
#     if len(data) == 0 or type(data[0]) is dict:
#         return
#     if type(data[0]) is dict:


def _build_bases(data, _dnames=None, _types=None, _bases=None, use_ctype=False):
    """베이스 요소 빌드."""
    if _types is None:
        _types = DefaultOrderedDict(list)
    if _bases is None:
        _bases = DefaultOrderedDict(list)
    if _dnames is None:
        _dnames = []

    data = copy.deepcopy(data)

    if '_imported_' in data:
        for idata in data['_imported_']:
            dname = idata['domain']['name']
            _build_bases(idata, _dnames + [dname], _types, _bases, use_ctype)

    if 'types' in data:
        _build_types(data, _dnames, _types)

    if 'bases' not in data:
        return _bases

    # normalize fields
    nbdata = {}
    for bname, bdata in data['bases'].items():
        path = '.'.join(_dnames)
        ndata = _flat_fields(bdata, _types, _dnames, use_ctype=use_ctype)
        nbdata[bname] = ndata
        _bases[bname].append([path, ndata])

    for bname, bdata in nbdata.items():
        _resolve_mixins(bname, _dnames, _bases)

    return _bases


def _build_events(data, _dnames=None, _types=None, _bases=None, _events=None,
                  use_ctype=False):
    """이벤트 및 관련 요소들 빌드."""
    if _types is None:
        _types = DefaultOrderedDict(list)
    if _bases is None:
        _bases = DefaultOrderedDict(list)
    if _events is None:
        _events = DefaultOrderedDict(list)
    if _dnames is None:
        _dnames = []
    data = copy.deepcopy(data)

    if '_imported_' in data:
        # 수입된 것이 있으면 그것도 빌드
        for idata in data['_imported_']:
            dname = idata['domain']['name']
            _build_events(idata, _dnames + [dname], _types, _bases, _events,
                          use_ctype=use_ctype)

    if 'types' in data:
        _build_types(data, _dnames, _types)

    if 'bases' in data:
        _build_bases(data, _dnames, _types, _bases, use_ctype)

    if 'events' not in data:
        return _events

    # flatten fields
    nedata = {}
    for ename, edata in data['events'].items():
        path = '.'.join(_dnames)
        ndata = _flat_fields(edata, _types, _dnames, True, use_ctype=use_ctype)
        nedata[ename] = ndata
        _events[ename].append([path, ndata])

    for ename, edata in nedata.items():
        _resolve_mixins(ename, _dnames, _bases, _events, True)

    return _events


def build_dom(data, use_ctype=False):
    """DOM 을 만듦.

    Args:
        data (dict): lab 파일 데이터
        use_ctype (bool): 커스텀 타입 유지 여부. 기본 False

    """
    domain = _build_domain(data)

    types = DefaultOrderedDict(list)
    bases = DefaultOrderedDict(list)
    events = DefaultOrderedDict(list)
    _build_events(data, None, types, bases, events, use_ctype)
    return AttrDict(dict(domain=domain, types=types, bases=bases,
                    events=events))