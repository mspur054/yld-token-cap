from yldtokenmonitor.get_exchange_data import flatten

def test_flatten_dictionary():

    intial_dict:dict = {'outer': {'inner':'value', 'also_inner':'teams'}}
    
    expected_flattened:dict = {'outer_inner': 'value', 'outer_also_inner': 'teams'}

    assert flatten(intial_dict) == expected_flattened

