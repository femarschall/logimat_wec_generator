from utils.parser import parse_sto_location, extract_max_load_from_loadAidId

def test_stoLoc_parse():
    loc = "A1-2-015"
    lid, side, sup = parse_sto_location(loc)
    assert lid == "A1"
    assert side == 2
    assert sup == 15

def test_loadAidId():
    assert extract_max_load_from_loadAidId("310T3025x815") == 310
    assert extract_max_load_from_loadAidId("630T3500x800") == 630