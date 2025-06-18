<p align="center">
    <img alt="Logo" src="resources/maruf_assets/maruf_icon.svg" width="128" />
    <h1 align="center">Ma'ruf</h1>
</p>

## Description
Ma'ruf is a fast, privacy-friendly and cross-platform desktop application for calculating daily Islamic prayer times locally on your device. Built with PyQt6/PySide6 and precise astronomical algorithms, no internet connection required.

## Screenshots
<p align="center">
  <img src="resources/screenshots/main_interface_v2.png" alt="Main Interface" width="600"><br>
  <em>Figure: Main Interface</em>
</p>
&nbsp;&nbsp;
<p align="center">
  <img src="resources/screenshots/settings_interface_v2.png" alt="Settings Interface" width="400"><br>
  <em>Figure: Settings Interface</em>
</p>

## TODOs
- [x] Add UTC Offset change option
- [x] Change UTC Offset when changing location based on coordinates
- [ ] Include fonts maybe or have better system font defaults for windows
- [ ] Implement changing time/date display format through `strftime()`
- [x] Query character limits/regex
- [x] Add timeout to ip and query threads when loading and exception handling if request doesn't work
- [x] Set character limits on region widget
- [x] Handling system color or set actual dark mode
- [ ] Custom Calculation Method for fajr and isha
- [x] Implement TOML persistent config
- [ ] Handle no rw or w access in directory
- [ ] Handle `None` being returned by `get_offset_name()` in `pray_data` or use Exceptions
- [ ] Handle error in loading config

## Credits
- Would not be possible without the information provided by [Radhi Fadlillah](https://radhifadlillah.com/) and [prayertimes.org](https://www.prayertimes.org/en/prayer-times-calculation-methodology/)
- [NOAA Solar Calculator](https://gml.noaa.gov/grad/solcalc/)
- [PrayTimes.org](https://praytimes.org/manual)
