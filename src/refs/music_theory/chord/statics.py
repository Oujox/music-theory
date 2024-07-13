
"""
Rules for generated quality
-----

1. omit chords
    [omit]      [on]
    [omit(3|5)] [/[0-12]]?

2. tension chords
    [3th]                     [67th]    [tension]            [denature]                  [on]
    [maj|m|sus2|sus4|dim|aug] [6|7|M7]? [(b|#)?9|#?11|b?13]? [(b|#)?5|(b|#)?9|(b|#)?11]? [/[0-12]]?

3. appended chords
    [3th]                     [67th]    [add]                [on]
    [maj|m|sus2|sus4|dim|aug] [6|7|M7]? [add(2|4|9|11|13)]? [/[0-12]]?

"""

import copy
import array


class QualityGenerator(dict[str, array.array[int]]):

    map_q3th: dict[str, tuple[int]] = {
        ""    : (0,  4,  7),
        "m"   : (0,  3,  7),
        "sus2": (0,  2,  7),
        "sus4": (0,  5,  7),
        "dim" : (0,  3,  6),
        "aug" : (0,  4,  8),
    }

    map_q67th: dict[str, int] = {
        "6" : 9,
        "7" : 10,
        "M7": 11,
    }

    map_qdim67th: dict[str, int] = {
        "6" : 8,
        "7" : 9,
        "M7": 10,
    }

    map_qtension: dict[int, tuple[int]] = {
        "9"  : (11, 14),
        "b9" : (11, 13),
        "#9" : (11, 15),
        "11" : (11, 14, 17),
        "#11": (11, 14, 18),
        "13" : (11, 14, 17, 21),
        "b13": (11, 14, 17, 20),
    }

    map_qdenature: dict[int, dict[str, tuple[int]]] = {
        3: {"b5":  (0,  0, -1),
            "#5":  (0,  0,  1),},
        5: {"b9":  (0,  0,  0,  0, -1),
            "#9":  (0,  0,  0,  0,  1),},
        6: {"#11": (0,  0,  0,  0,  0,  1),},
    }

    map_qadd: dict[str, int] = {
        "add2"  : 2,
        "add4"  : 5,
        "add9"  : 14,
        "add11" : 17,
        "add13" : 21,
    }

    map_qomit: dict[str, int] = {
        "omit3"  : (0, 7),
        "omit5"  : (0, 4),
    }

    def __init__(self) -> None:
        super().__init__()

    def generate(self, on_quality: bool = False) -> dict[str, array.array[int]]:
        self.generate_3th()
        qualities_omit = self.generate_omit(True)
        qualities_add = self.generate_add(self, True)

        self.generate_67th(self)
        self.generate_tension(self)
        self.generate_denature(self)

        if on_quality:
            self.generate_on(self)
            self.generate_on(qualities_omit)
            self.generate_on(qualities_add)

        return dict(self)

    def dump(self, qualities: dict[str, array.array[int]]):
        for k, v in qualities.items():
            self[k] = v

    def generate_3th(
            self,
            no_inplace: bool = False
            ) -> dict[str, array.array[int]]:

        _qualities = {}
        for k, v in self.map_q3th.items():
            _qualities[k] = array.array("i", v)

        if not no_inplace:
            self.dump(_qualities)
        return _qualities

    def generate_67th(
            self,
            qualities: dict[str, array.array[int]],
            no_inplace: bool = False
            ) -> dict[str, array.array[int]]:

        _qualities = {}
        for qname, quality in qualities.items():
            if qname.startswith("dim"):
                for suffix, interval in self.map_q67th.items():
                    _qname = qname + suffix
                    _quality = copy.copy(quality)
                    _quality.append(interval)
                    _qualities[_qname] = _quality
            else:
                for suffix, interval in self.map_qdim67th.items():
                    _qname = qname + suffix
                    _quality = copy.copy(quality)
                    _quality.append(interval)
                    _qualities[_qname] = _quality

        if not no_inplace:
            self.dump(_qualities)
        return _qualities

    def generate_tension(
            self,
            qualities: dict[str, array.array[int]],
            no_inplace: bool = False
            ) -> dict[str, array.array[int]]:

        _qualities = {}
        for qname, quality in qualities.items():
            for suffix, intervals in self.map_qtension.items():
                _qname = qname + suffix
                _quality = quality + array.array("i", intervals[len(quality)-3:])
                _qualities[_qname] = _quality

        if not no_inplace:
            self.dump(_qualities)
        return _qualities

    def generate_denature(
            self,
            qualities: dict[str, array.array[int]],
            no_inplace: bool = False
            ) -> dict[str, array.array[int]]:

        # TODO: 13b9b11 等のコードの変性形
        #       特にテンションコードの後に変性記号が二つ以上続く場合
        def _generate_denature(qname: str, quality: array.array[int]):
            for qsize in [ n for n in (3,5,6) if n <= len(quality) ]:
                for suffix, mask in self.map_qdenature[qsize].items():
                    # !! rule !!
                    if suffix == "b5" or suffix == "#5":
                        if qname.startswith(("sus2", "sus4", "dim", "aug")):
                            continue
                    _qname = qname + suffix
                    _quality = [ quality[i]+mask[i] for i in range(qsize) ]
                    _quality = array.array("i", _quality) + quality[qsize:]
                    yield _qname, _quality

        _qualities = {}
        for qname, quality in qualities.items():
            for qname, quality in _generate_denature(qname, quality):
                _qualities[qname] = quality

        if not no_inplace:
            self.dump(_qualities)
        return _qualities

    def generate_add(
            self,
            qualities: dict[str, array.array[int]],
            no_inplace: bool = False
            ) -> dict[str, array.array[int]]:

        _qualities = {}
        for qname, quality in qualities.items():
            for suffix, interval in self.map_qadd.items():
                if qname.startswith(("m", "sus2", "dim")) and suffix == "add2":
                    continue
                if qname.startswith(("sus4", "dim")) and suffix == "add4":
                    continue
                _qname = qname + suffix
                _quality = copy.copy(quality)
                _quality.append(interval)
                _qualities[_qname] = _quality

        if not no_inplace:
            self.dump(_qualities)
        return _qualities

    def generate_omit(
            self,
            no_inplace: bool = False
            ) -> dict[str, array.array[int]]:

        _qualities = {}
        for k, v in self.map_qomit.items():
            _qualities[k] = array.array("i", v)

        if not no_inplace:
            self.dump(_qualities)
        return _qualities

    def generate_on(
            self,
            qualities: dict[str, array.array[int]],
            no_inplace: bool = False
            ) -> dict[str, array.array[int]]:

        _qualities = {}
        for qname, quality in qualities.items():
            for i, n in enumerate(quality):
                q = quality[i:] + quality[:i]
                q = [ (j-q[0])%12 for j in q ]
                q = array.array("i", q)
                _qualities[qname+"/"+str(n)] = q

        if not no_inplace:
            self.dump(_qualities)
        return _qualities

NOON_QUALITIES = QualityGenerator().generate()
