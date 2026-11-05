import pytest
from highway_toll import toll_for, toll_charge, pass_advice

# Example tests (from starter)
def test_ambulance_is_exempt():
    assert toll_charge("ambulance", 2, False, False) == 0

def test_two_axle_base_toll():
    assert toll_for(2, False, False) == 100

# Additional tests aimed at line (statement) coverage
def test_invalid_axle_count_raises():
    with pytest.raises(ValueError):
        toll_for(1, False, False)

def test_more_than_four_axles_uses_default_base():
    assert toll_for(5, False, False) == 400

def test_peak_surcharge():
    assert toll_for(2, True, False) == 125

def test_fastag_discount_two_axles():
    assert toll_for(2, False, True) == 90

def test_fastag_discount_heavy_vehicle():
    assert toll_for(3, False, True) == 142.5

def test_regular_vehicle_is_charged():
    assert toll_charge("car", 2, False, False) == 100

def test_pass_advice_buy_pass():
    assert pass_advice([(False, False)] * 3, 2, 250) == "buy_pass"

def test_pass_advice_either():
    assert pass_advice([(False, False)] * 2, 2, 200) == "either"

def test_pass_advice_pay_per_trip():
    assert pass_advice([(False, False)], 2, 500) == "pay_per_trip"
