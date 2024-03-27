import pytest
from unittest.mock import patch
from io import StringIO
from project import current_forecast, polution, convert_time

# decorator to check with other valueset
@pytest.mark.parametrize("lat, lon, loc, api_key", [(42.3770, -71.1167, "Harvard University", "c93986d568f30cefc45c66d9d26ba3cb")])
def test_current_forecast(lat, lon, loc, api_key):
    #using patch for test based on API
    with patch("builtins.input", return_value="1"):
        with patch("requests.get") as mock_get:
            #giving mock values to each param
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = {
                "main": {"temp": 300, "humidity": 50},
                "weather": [{"main": "Clear"}],
                "sys": {"sunrise": 1642061175, "sunset": 1642100912},
            }
            with patch("sys.exit"):
                # StringIO prevent creation of file to make it more faster
                with patch("sys.stdout", new_callable=StringIO) as mock_out:
                    current_forecast(lat, lon, loc, api_key)
                    assert mock_out.getvalue().strip() == "Current temperature at Harvard University: 26.85°C\nHumidity at Harvard University: 50.00%"


def test_convert_time():
    assert convert_time(1642061175) == "13:36"
    assert convert_time(1642748946) != "16:32"

@pytest.mark.parametrize("lat, lon, loc, api_key", [(42.3770, -71.1167, "Harvard University", "c93986d568f30cefc45c66d9d26ba3cb")])
def test_polution(lat, lon, loc, api_key):
    with patch("builtins.input", return_value="5"):
        with patch("requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = {
                "list": [
                    {
                        "components": {
                            "co": 1.5,
                            "no": 10,
                            "no2": 20,
                            "so2": 5,
                            "o3": 50,
                            "nh3": 2,
                        }
                    }
                ]
            }
            with patch("sys.exit"):
                polution(lat, lon, loc, api_key)

                assert mock_get.return_value.json.return_value["list"][0]["components"]["co"] == 1.5