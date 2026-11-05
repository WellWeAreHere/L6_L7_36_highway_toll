import pytest
from highway_toll import toll_for, toll_charge, pass_advice

# ---- toll_for: axle validation ----
def test_ambulance_is_exempt():
    assert toll_charge("ambulance", 2, False, False) == 0

def test_invalid_axle_count_raises():
    with pytest.raises(ValueError, match="invalid axle count"):
        toll_for(1, False, False)

def test_zero_and_negative_axles_raise():
    for a in (0, -3):
        with pytest.raises(ValueError):
            toll_for(a, False, False)

# ---- toll_for: base lookup (in table / not in table) ----
@pytest.mark.parametrize("axles,expected", [(2, 100), (3, 150), (4, 250)])
def test_base_toll_table(axles, expected):
    assert toll_for(axles, False, False) == expected

@pytest.mark.parametrize("axles", [5, 6, 10])
def test_axles_outside_table_use_default_400(axles):
    assert toll_for(axles, False, False) == 400

# ---- toll_for: peak True / False ----
def test_off_peak_no_surcharge():
    assert toll_for(2, False, False) == 100

def test_peak_surcharge():
    assert toll_for(2, True, False) == 125

# ---- toll_for: fastag False / True(2 axles) / True(other axles) ----
def test_no_fastag_no_discount():
    assert toll_for(3, False, False) == 150

def test_fastag_two_axles_10_percent():
    assert toll_for(2, False, True) == 90

def test_fastag_other_axles_5_percent():
    assert toll_for(3, False, True) == 142.5
    assert toll_for(5, False, True) == 380

def test_peak_and_fastag_combined():
    assert toll_for(2, True, True) == 112.5
    assert toll_for(4, True, True) == 296.88  # 250*1.25*0.95 = 296.875 -> rounded

# ---- toll_charge: exempt and non-exempt ----
@pytest.mark.parametrize("vehicle", ["ambulance", "fire_engine"])
def test_all_exempt_vehicles_free(vehicle):
    assert toll_charge(vehicle, 4, True, False) == 0

def test_exempt_vehicle_skips_axle_validation():
    assert toll_charge("ambulance", 0, False, False) == 0

def test_non_exempt_vehicle_charged():
    assert toll_charge("car", 2, False, False) == 100

def test_non_exempt_invalid_axles_raises():
    with pytest.raises(ValueError):
        toll_charge("truck", 1, False, False)

# ---- pass_advice: all three outcomes, loop 0/1/many iterations ----
def test_pass_advice_buy_pass():
    assert pass_advice([(False, False)] * 3, 2, 250) == "buy_pass"

def test_pass_advice_either_exact_equal():
    assert pass_advice([(False, False)] * 2, 2, 200) == "either"

def test_pass_advice_pay_per_trip():
    assert pass_advice([(False, False)], 2, 500) == "pay_per_trip"

def test_pass_advice_empty_trips_costs_zero():
    assert pass_advice([], 2, 100) == "pay_per_trip"
    assert pass_advice([], 2, 0) == "either"

def test_pass_advice_mixed_trips():
    trips = [(True, True), (False, False), (True, False)]
    # 112.5 + 100 + 125 = 337.5
    assert pass_advice(trips, 2, 337.5) == "either"
    assert pass_advice(trips, 2, 337) == "buy_pass"
    assert pass_advice(trips, 2, 338) == "pay_per_trip"

def test_pass_advice_invalid_axles_propagates():
    with pytest.raises(ValueError):
        pass_advice([(False, False)], 1, 100)
