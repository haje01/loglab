"""랩파일 Document Object Model."""
import copy
from collections import defaultdict
from json.encoder import py_encode_basestring

import pandas as pd


def _build_types(data, _dnames=None, _types=None):
    if _types is None:
        _types = defaultdict(list)

    if _dnames is None:
        _dnames = []

    if 'import' in data:
        for idata in data['import']:
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


def _norm_fields(data, _types, _dnames):
    if 'fields' not in data:
        return data

    data = copy.deepcopy(data)

    def _is_norm(fdata):
        if type(fdata) is not defaultdict:
            return False
        if len(fdata) == 0:
            return True
        return type(list(fdata.values())[0]) is list

    if not _is_norm(data['fields']):
        fields = defaultdict(list)
        for f in data['fields']:
            path = '.'.join(_dnames)
            tname = f'{path}.{f[1]}' if len(path) > 0 else f[1]
            if 'types' in tname:
                tdata = _resolve_type(tname, _types)
                tdata['desc'] = f[2]
            else:
                tdata = dict(type=tname, desc=f[2])
            fields[f[0]].append([path, tdata])
        data['fields'] = fields

    return data


def _resolve_mixins(name, _dnames, _types, _bases, _events=None):
    pbase = name in _bases
    pevent = name in _events if _events is not None else False
    if not pbase and not pevent:
        raise Exception("Can not find mixin {name} in both bases and events.")
    if pbase and pevent:
        raise Exception(f"Since the name '{name} is duplicated in the bases "
                        "& events, It is ambiguous to select.")
    if _events is None and pevent:
        raise Exception("You can not mixin an event for a base.")

    _refer = _bases if pbase else _events
    data = _refer[name][-1][1]
    if 'mixins' not in data:
        return data

    fields = defaultdict(list)
    for mpath in data['mixins']:
        mpath = '.'.join(_dnames + [mpath])
        mname, mdata = _find_mixin(mpath, _bases, _events)
        if 'fields' not in mdata[1]:
            continue
        # mixins first
        for mf, mds in mdata[1]['fields'].items():
            fields[mf].append(mds[-1])
        if 'fields' in data:
            for k, v in data['fields'].items():
                fields[k].append(v[-1])

    data['fields'] = fields

    del data['mixins']
    return data


def _find_mixin(path, _bases, _events):
    elms = path.split('.')
    atype = elms[-2]
    name = elms[-1]
    path = '.'.join(elms[:-2])
    _refer = _bases if atype == 'bases' else _events
    if name not in _refer:
        raise Exception(f"Can not find mixin '{path}' in {atype}")
    for e in _refer[name]:
        if e[0] == path:
            return name, e
    raise Exception(f"Can not find minxin path {path}")


def _build_bases(data, _dnames=None, _types=None, _bases=None):
    if _types is None:
        _types = defaultdict(list)
    if _bases is None:
        _bases = defaultdict(list)
    if _dnames is None:
        _dnames = []

    data = copy.deepcopy(data)

    if 'import' in data:
        for idata in data['import']:
            dname = idata['domain']['name']
            _build_bases(idata, _dnames + [dname], _types, _bases)

    if 'types' in data:
        _build_types(data, _dnames, _types)

    if 'bases' not in data:
        return _bases

    # normalize fields
    nbdata = {}
    for bname, bdata in data['bases'].items():
        path = '.'.join(_dnames)
        ndata = _norm_fields(bdata, _types, _dnames)
        nbdata[bname] = ndata
        _bases[bname].append([path, ndata])

    for bname, bdata in nbdata.items():
        _resolve_mixins(bname, _dnames, _types, _bases)

    return _bases


def _build_events(data, _dnames=None, _types=None, _bases=None, _events=None):
    if _types is None:
        _types = defaultdict(list)
    if _bases is None:
        _bases = defaultdict(list)
    if _events is None:
        _events = defaultdict(list)
    if _dnames is None:
        _dnames = []

    data = copy.deepcopy(data)

    if 'import' in data:
        for idata in data['import']:
            dname = idata['domain']['name']
            _build_events(idata, _dnames + [dname], _types, _bases, _events)

    if 'types' in data:
        _build_types(data, _dnames, _types)

    if 'bases' in data:
        _build_bases(data, _dnames, _types, _bases)

    if 'events' not in data:
        return _events

    # normalize fields
    nedata = {}
    for ename, edata in data['events'].items():
        path = '.'.join(_dnames)
        ndata = _norm_fields(edata, _types, _dnames)
        nedata[ename] = ndata
        _events[ename].append([path, ndata])

    for ename, edata in nedata.items():
        _resolve_mixins(ename, _dnames, _types, _bases, _events)

    return _events
